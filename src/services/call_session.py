from sqlalchemy.ext.asyncio import AsyncSession

from src.api.api_v1.schemas.call_session import CallSessionCreateSchema, CallSessionAnalysisResponseSchema
from src.core.exceptions import ExceptionCallSessionNotFound
from src.storage.repositories.call_session import CallSessionRepository


class CallSessionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._repository = CallSessionRepository(self.session)

    async def create_new_call_session(self, data: CallSessionCreateSchema) -> None:
        call_session = await self._repository.create(data)
        # TODO: Здесь необходимо отправлять сообщение в очередь для запуска задачи по обработке.
        return

    async def get_call_session_analysis(self, session_id: str) -> CallSessionAnalysisResponseSchema:
        call_session = await self._repository.get_call_session_from_db(session_id)
        if not call_session:
            raise ExceptionCallSessionNotFound

        # TODO: Здесь необходимо реализовать обработку статуса.
        return ...

    async def get_call_session_transcription(self, session_id: str) -> None:
        call_session = await self._repository.get_call_session_transcription(session_id)
        if not call_session:
            raise ExceptionCallSessionNotFound

        # TODO: Здесь необходимо реализовать обработку статуса.
        return
