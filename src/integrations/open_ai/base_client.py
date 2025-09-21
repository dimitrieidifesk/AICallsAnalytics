import aiohttp
import io
from typing import BinaryIO
from urllib.parse import urlparse
import time

from loguru import logger
from pydantic import HttpUrl

from src.core.config import settings
from src.core.exceptions import (
    ExceptionWhenDownloadAudio,
    ExceptionTranscriptionAPI,
    ExceptionTranscriptionFailed
)


class OpenAITranscriptionService:
    def __init__(self, audio_url: HttpUrl):
        self.buffer = io.BytesIO()
        self.audio_url = audio_url
        self._url = settings.open_ai.audio_transcription_url
        self.filename = self._get_filename_from_url(audio_url)
        self.language_code = settings.open_ai.language_code
        self.api_key = settings.open_ai.api_key
        self.proxy_url = settings.open_ai.proxy_url
        self.whisper_model = settings.open_ai.whisper_model
        self._prompt = """
        TRANSCRIPTION FORMAT REQUIREMENTS:
        Return STRICT JSON format only, no other text.
        
        REQUIRED JSON STRUCTURE:
        {
          "data": [
            {"role": "client", "text": "client speech text"},
            {"role": "manager", "text": "manager speech text"},
            {"role": "client", "text": "client speech text"},
            ...
          ]
        }

        RULES:
        1. Identify speaker role: "client" for customer, "manager" for operator
        2. Split by speaker changes
        3. Maintain dialogue sequence
        4. No additional comments, only pure JSON
        5. Preserve original text without modifications
        6. Mark unclear speech as "[неразборчиво]"
        7. For customer use role: "client", for operator - "manager"
        
        CONTEXT:
        - Call center conversation about disinfection, disinsection, deratization
        - Operator offers services, asks questions
        - Customer responds, expresses needs or objections
        - Typical Russian names: Ivan, Maria, Alexander, Sergei
        """
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def download_audio_from_s3_to_buffer(self) -> io.BytesIO:
        logger.info(f"Downloading audio from: {self.audio_url}")
        start_time = time.time()
        try:
            timeout = aiohttp.ClientTimeout(total=300)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(self.audio_url) as response:
                    if response.status != 200:
                        logger.error(f"Failed to download audio: HTTP {response.status}")
                        raise ExceptionWhenDownloadAudio(f"{response.status}")

                    async for chunk in response.content.iter_chunked(8192):
                        self.buffer.write(chunk)

                    self.buffer.seek(0)
                    download_time = time.time() - start_time
                    file_size = self.buffer.getbuffer().nbytes
                    logger.info(f"Audio downloaded to buffer: {file_size} bytes, time: {download_time:.2f}s")

                    return self.buffer

        except aiohttp.ClientError as e:
            logger.error(f"Network error during audio download: {str(e)}")
            raise ExceptionWhenDownloadAudio(str(e))

    async def transcribe_from_buffer(self, audio_buffer: BinaryIO) -> str:
        logger.info(f"Starting transcription from buffer, size: {audio_buffer.getbuffer().nbytes} bytes")
        start_time = time.time()

        data = aiohttp.FormData()
        data.add_field('file', audio_buffer, filename=self.filename, content_type="audio/mpeg")
        data.add_field('model', self.whisper_model)
        data.add_field('language', self.language_code)
        data.add_field('prompt', self._prompt)

        try:
            timeout = aiohttp.ClientTimeout(total=180)
            async with aiohttp.ClientSession(timeout=timeout, headers=self._headers) as session:
                async with session.post(self._url, data=data, proxy=self.proxy_url) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Transcription API error: {response.status}, {error_text}")
                        raise ExceptionTranscriptionAPI(f"{response.status}, {error_text}")

                    result = await response.json()
                    transcribed_text = result.get('text', '').strip()
                    transcription_time = time.time() - start_time
                    logger.info(f"Transcription completed: {len(transcribed_text)} chr, {transcription_time:.2f}s")
                    return transcribed_text

        except aiohttp.ClientError as e:
            logger.error(f"Network error during transcription: {str(e)}")
            raise ExceptionTranscriptionFailed(str(e))

    async def transcribe_from_url(self) -> str | None:
        audio_buffer = await self.download_audio_from_s3_to_buffer()
        try:
            transcription =  await self.transcribe_from_buffer(audio_buffer=audio_buffer)
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            return
        else:
            return transcription
        finally:
            audio_buffer.close()

    @staticmethod
    def _get_filename_from_url(audio_url: HttpUrl) -> str:
        default_filename = "audio.mp3"
        try:
            path = urlparse(audio_url).path
            if path:
                return path.split('/')[-1]

            return default_filename
        except Exception as e:
            logger.error(f"Failed to get filename from URL: {str(e)}")
            return default_filename
