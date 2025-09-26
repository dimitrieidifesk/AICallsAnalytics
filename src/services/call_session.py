import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.api_v1.schemas.call_session import (
    CallSessionCreateSchema,
    CallSessionAnalysisResponseSchema,
    TranscriptionCallSessionResponseSchema,
    CallSessionCreateResponseSchema
)
from src.core.exceptions import ExceptionCallSessionNotFound, ExceptionCallSessionStatusWhenGetting
from src.integrations.broker.rabbit_broker import broker
from src.integrations.broker.schemas import CallSessionProcessingSchema
from src.storage.models.enums import CallSessionStatus
from src.storage.repositories.call_session import CallSessionRepository


class CallSessionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._repository = CallSessionRepository(self.session)

    async def create_new_call_session(self, data: CallSessionCreateSchema) -> CallSessionCreateResponseSchema:
        data_dict: dict[str, Any] = data.call.model_dump()
        data_dict["script"] = data.script.model_dump()
        data_dict["recording_url"] = str(data.call.recording_url)
        call_session = await self._repository.create(data_dict)
        await broker.publish(
            CallSessionProcessingSchema(call_session_id=call_session.id)
        )

        return CallSessionCreateResponseSchema(call_session_id=call_session.id)

    async def get_call_session_analysis(self, call_session_id: uuid.UUID) -> CallSessionAnalysisResponseSchema:
        call_session = await self._repository.get_call_session_by_id(call_session_id)
        if not call_session:
            raise ExceptionCallSessionNotFound

        if call_session.status != CallSessionStatus.PROCESSING_COMPLETED:
            raise ExceptionCallSessionStatusWhenGetting(call_session.status)

        return 

    async def get_call_session_transcription(self, call_session_id: uuid.UUID) -> TranscriptionCallSessionResponseSchema:
        call_session = await self._repository.get_call_session_by_id(call_session_id)
        if not call_session:
            raise ExceptionCallSessionNotFound

        if call_session.status != CallSessionStatus.PROCESSING_COMPLETED:
            raise ExceptionCallSessionStatusWhenGetting(call_session.status)

        return TranscriptionCallSessionResponseSchema(transcription=call_session.transcription.get("data"))
