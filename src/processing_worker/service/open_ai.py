from typing import BinaryIO, Any

import aiohttp

from loguru import logger
from pydantic import HttpUrl

from src.processing_worker.schema.open_ai import StructureTextRequestSchema, PromtMessageSchema
from src.core.config import settings
from src.core.exceptions import ExceptionTranscriptionAPI, ExceptionOpenAiFailed
from src.core.prompts import (
    MAKING_STRUCTURE_SYSTEM_PROMPT,
    MAKING_STRUCTURE_USER_PROMPT,
    MAKING_ANALYZES_SYSTEM_PROMPT,
    MAKING_ANALYZES_USER_PROMPT, REQUIRED_JSON_OUTPUT_FORMAT
)
from src.services.audio import AudioService
from src.storage.models.enums import PromtMessageRole


class OpenAIService:
    def __init__(self, audio_url: HttpUrl):
        self.proxy_url = str(settings.open_ai.proxy_url)
        self._audio_service = AudioService(str(audio_url))
        self._headers = {"Authorization": f"Bearer {settings.open_ai.api_key}"}

    async def get_raw_transcription_from_buffer(self, audio_buffer: BinaryIO, filename: str) -> str:
        data = aiohttp.FormData()
        data.add_field('file', audio_buffer, filename=filename, content_type='audio/mpeg')
        data.add_field('model', settings.open_ai.whisper_model)
        data.add_field('language', settings.open_ai.language_code)

        async with aiohttp.ClientSession(headers=self._headers) as session:
            async with session.post(
                settings.open_ai.audio_transcription_url,
                data=data,
                proxy=self.proxy_url,
                ssl=False
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get('text', '')
                else:
                    error_text = f"Whisper failed: {response.status}"
                    logger.error(error_text)
                    raise ExceptionOpenAiFailed(error_text)

    async def structure_text_with_chatgpt(self, text: str) -> dict:
        data = StructureTextRequestSchema(
            messages=[
                PromtMessageSchema(role=PromtMessageRole.SYSTEM, content=MAKING_STRUCTURE_SYSTEM_PROMPT),
                PromtMessageSchema(role=PromtMessageRole.USER, content=MAKING_STRUCTURE_USER_PROMPT.format(text=text))
            ]
        )
        try:
            timeout = aiohttp.ClientTimeout(total=300)
            async with aiohttp.ClientSession(timeout=timeout, headers=self._headers) as session:
                async with session.post(
                    settings.open_ai.chat_gpt_url,
                    json=data.model_dump(),
                    proxy=self.proxy_url,
                    ssl=False
                ) as response:
                    result = await response.json()
                    if response.status != 200:
                        error_text = f"Transcription API error: {response.status}, {result}"
                        logger.error(error_text)
                        raise ExceptionOpenAiFailed(error_text)

                    return result

        except aiohttp.ClientError as e:
            error_text = f"Network error during transcription: {str(e)}"
            logger.error(error_text)
            raise ExceptionOpenAiFailed(error_text)

    async def text_transcription_from_url(self):
        audio_buffer = await self._audio_service.download_audio_from_s3_to_buffer()
        try:
            text_transcription = await self.get_raw_transcription_from_buffer(
                audio_buffer, self._audio_service.filename
            )
            return text_transcription
        except Exception as e:
            error_text = f"Transcription failed: {str(e)}"
            logger.error(error_text)
            raise ExceptionOpenAiFailed(error_text)

        finally:
            audio_buffer.close()

    async def analyze_structured_text(
        self, structure_text: dict[str, str], analysis_benchmark: dict[str, str]
    ) -> dict[Any, Any]:
        data = StructureTextRequestSchema(
            messages=[
                PromtMessageSchema(role=PromtMessageRole.SYSTEM, content=MAKING_ANALYZES_SYSTEM_PROMPT),
                PromtMessageSchema(
                    role=PromtMessageRole.USER,
                    content=MAKING_ANALYZES_USER_PROMPT.format(
                        structure_text=structure_text,
                        analysis_benchmark=analysis_benchmark,
                        REQUIRED_JSON_OUTPUT_FORMAT=REQUIRED_JSON_OUTPUT_FORMAT
                    )
                )
            ]
        )
        try:
            timeout = aiohttp.ClientTimeout(total=300)
            async with aiohttp.ClientSession(timeout=timeout, headers=self._headers) as session:
                async with session.post(
                        settings.open_ai.chat_gpt_url,
                        json=data.model_dump(),
                        proxy=self.proxy_url,
                        ssl=False
                ) as response:
                    result = await response.json()
                    if response.status != 200:
                        logger.error(f"Analyze API error: {response.status}, {result}")
                        raise ExceptionTranscriptionAPI(f"{response.status}, {result}")

                    return result

        except aiohttp.ClientError as e:
            error_text = f"Network error during analyze: {str(e)}"
            logger.error(error_text)
            raise ExceptionOpenAiFailed(error_text)