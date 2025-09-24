import json

from loguru import logger

from src.processing_worker.service.open_ai import OpenAIService
from src.storage.models.db_helper import db_connector
from src.storage.models.enums import CallSessionStatus
from src.storage.repositories.call_session import CallSessionRepository


async def process_audio_recording(data: ...):
    async for session in db_connector.session_getter():
        call_session_repo = CallSessionRepository(session)
        call_session = await call_session_repo.get_call_session_by_id(data.call_session_id)
        if not call_session:
            logger.error(f"Call session id {data.call_session_id} not found!")
            return

        await call_session_repo.update_call_session(data.id, {"status": CallSessionStatus.IN_PROCESSING})
        open_ai_service = OpenAIService(call_session.recording_url)
        text_from_audio = await open_ai_service.text_transcription_from_url()
        if not text_from_audio:
            logger.error(f"Text transcription from url {call_session.recording_url} failed!")
            await call_session_repo.update_call_session(
                data.id, {"status": CallSessionStatus.ERROR_RECEIVING_TRANSCRIPTION}
            )
            return

        await call_session_repo.update_call_session(data.id, {"text_from_audio": text_from_audio})
        structure_text = await open_ai_service.structure_text_with_chatgpt(text_from_audio)
        try:
            dict_structure_text = json.loads(structure_text)
        except Exception as e:
            logger.error(f"Structure text failed! Error: {e}")
            await call_session_repo.update_call_session(
                data.id, {"status": CallSessionStatus.ERROR_RECEIVING_TRANSCRIPTION}
            )
            return

        await call_session_repo.update_call_session(data.id, {"transcription": dict_structure_text})
