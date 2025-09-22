import aiohttp
import io
from urllib.parse import urlparse

from loguru import logger
from pydantic import HttpUrl

from src.core.exceptions import ExceptionWhenDownloadAudio


class AudioService:
    def __init__(self, audio_url: HttpUrl):
        self.buffer = io.BytesIO()
        self.audio_url = str(audio_url)
        self.filename = self._get_filename_from_url(audio_url)

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

    async def download_audio_from_s3_to_buffer(self) -> io.BytesIO:
        logger.info(f"Downloading audio from: {self.audio_url}")
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
                    if self.buffer.getbuffer().nbytes == 0:
                        raise ExceptionWhenDownloadAudio("Downloaded audio is empty")

                    return self.buffer

        except aiohttp.ClientError as e:
            logger.error(f"Network error during audio download: {str(e)}")
            raise ExceptionWhenDownloadAudio(str(e))
