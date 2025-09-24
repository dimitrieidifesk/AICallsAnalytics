from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.api_v1.schemas.call_session import CallSessionCreateSchema, CallSessionAnalysisResponseSchema
from src.core.exceptions import ExceptionCallSessionNotFound
from src.storage.repositories.call_session import CallSessionRepository


class CallSessionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._repository = CallSessionRepository(self.session)

    async def create_new_call_session(self, data: CallSessionCreateSchema) -> None:
        data_dict: dict[str, Any] = data.call.model_dump()
        data_dict["script"] = data.script.model_dump()
        data_dict["recording_url"] = str(data.call.recording_url)
        call_session = await self._repository.create(data_dict)

        return

    async def get_call_session_analysis(self, session_id: str) -> CallSessionAnalysisResponseSchema:
        call_session = await self._repository.get_call_session_by_session_id(session_id)
        if not call_session:
            raise ExceptionCallSessionNotFound

        # TODO: Здесь необходимо реализовать обработку статуса.
        return ...

    async def get_call_session_transcription(self, session_id: str) -> None:
        call_session = await self._repository.get_call_session_by_session_id(session_id)
        if not call_session:
            raise ExceptionCallSessionNotFound

        # TODO: Здесь необходимо реализовать обработку статуса.
        return
