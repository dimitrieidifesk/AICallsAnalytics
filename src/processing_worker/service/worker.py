import asyncio
import json
import time
import uuid

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import ExceptionProcessingCallSession
from src.processing_worker.service.open_ai import OpenAIService
from src.storage import CallSession
from src.storage.models.enums import CallSessionStatus
from src.storage.repositories.call_session import CallSessionRepository


class CallSessionProcessingWorker:

    def __init__(self, session: AsyncSession, call_session_id: uuid.UUID):
        self.call_session_id = call_session_id
        self.session = session
        self._call_session_repo = CallSessionRepository(self.session)
        self._open_ai_service = None

    async def get_text_from_audio(self, call_session: CallSession) -> str:
        try:
            text_from_audio = await self._open_ai_service.text_transcription_from_url()
            await asyncio.sleep(1)
        except Exception as e:
            error_text = f"Text transcription from url {call_session.recording_url} failed! Error: {e}"
            await self._call_session_repo.update(
                self.call_session_id, {"status": CallSessionStatus.ERROR_RECEIVING_TRANSCRIPTION}
            )
            raise ExceptionProcessingCallSession(error_text)
        else:
            await self._call_session_repo.update(
                self.call_session_id, {
                    "text_from_audio": text_from_audio,
                    "status": CallSessionStatus.RECEIVING_TRANSCRIPTION
                }
            )
            return text_from_audio

    async def structure_text_to_dict(self, text: str) -> dict[str, str] | None:
        try:
            data = await self._open_ai_service.structure_text_with_chatgpt(text)
            await asyncio.sleep(1)
            structure_text = json.loads(data["choices"][0]["message"]["content"])
            if isinstance(structure_text, dict) and structure_text.get("status") == "invalid":
                logger.info(structure_text)
                structure_text = None

        except Exception as e:
            error_text = f"Structure text from url failed! Error: {e}"
            await self._call_session_repo.update(
                self.call_session_id, {"status": CallSessionStatus.ERROR_RECEIVING_TRANSCRIPTION}
            )
            raise ExceptionProcessingCallSession(error_text)
        else:
            if structure_text:
                await self._call_session_repo.update(
                    self.call_session_id, {"transcription": {"data": structure_text}}
                )
            return structure_text

    async def get_analytical_for_structure_text(
            self, structure_text: dict[str, str], analysis_benchmark: dict[str, str]
    ) -> None:
        try:
            data = await self._open_ai_service.analyze_structured_text(structure_text, analysis_benchmark)
            await asyncio.sleep(1)
            result = json.loads(data["choices"][0]["message"]["content"])
        except Exception as e:
            await self._call_session_repo.update(
                self.call_session_id, {"status": CallSessionStatus.ERROR_RECEIVING_ANALYTICS}
            )
            error_text = f"Analytical structure text from url failed! Error: {e}"
            raise ExceptionProcessingCallSession(error_text)
        else:
            await self._call_session_repo.update(
                self.call_session_id, {"analysis": {"data": result}}
            )

    async def processing(self):
        call_session = await self._call_session_repo.get_call_session_by_id(self.call_session_id)
        if not call_session:
            error_text =f"Call session id {self.call_session_id} not found!"
            raise ExceptionProcessingCallSession(error_text)

        self._open_ai_service = OpenAIService(call_session.recording_url, self.session, call_session.id)
        await self._call_session_repo.update(
            self.call_session_id, {"status": CallSessionStatus.IN_PROCESSING}
        )
        try:
            start_time = time.time()
            text_from_audio = await self.get_text_from_audio(call_session)
            structure_text = await self.structure_text_to_dict(text_from_audio)
            if structure_text:
                await self.get_analytical_for_structure_text(structure_text, call_session.script)
                status = CallSessionStatus.PROCESSING_COMPLETED
            else:
                status = CallSessionStatus.FAKE_DIALOGUE
            end_time = time.time()
            logger.info(f"Processing time: {round(end_time - start_time, 2)} seconds")
        except Exception as e:
            raise ExceptionProcessingCallSession(str(e))
        else:
            await self._call_session_repo.update(
                self.call_session_id, {"status": status}
            )

    async def finish_processing(self):
        call_session = await self._call_session_repo.get_call_session_by_id(self.call_session_id)
        if not call_session:
            error_text = f"Call session id {self.call_session_id} not found!"
            raise ExceptionProcessingCallSession(error_text)

        self._open_ai_service = OpenAIService(call_session.recording_url, self.session, call_session.id)
        await self._call_session_repo.update(
            self.call_session_id, {"status": CallSessionStatus.IN_PROCESSING}
        )
        try:
            if not call_session.analysis:
                if call_session.transcription:
                    await self.get_analytical_for_structure_text(call_session.transcription, call_session.script)
                else:
                    if call_session.text_from_audio:
                        structure_text = await self.structure_text_to_dict(call_session.text_from_audio)
                    else:
                        text_from_audio = await self.get_text_from_audio(call_session)
                        structure_text = await self.structure_text_to_dict(text_from_audio)

                    await self.get_analytical_for_structure_text(structure_text, call_session.script)

        except Exception as e:
            raise ExceptionProcessingCallSession(str(e))
        else:
            await self._call_session_repo.update(
                self.call_session_id, {"status": CallSessionStatus.PROCESSING_COMPLETED}
            )