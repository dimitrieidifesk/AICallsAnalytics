import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from loguru import logger

from src.core.exceptions import ExceptionWhenCreatingProcessingLogRecord
from src.storage import ProcessingLog
from src.storage.models.enums import RequestTypeOpenAi
from src.storage.repositories.base import BaseRepository


class ProcessingLogRepository(BaseRepository[ProcessingLog]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ProcessingLog)

    async def create(
            self, request: str, response: str, call_session_id: uuid.UUID, request_type: RequestTypeOpenAi
    ) -> None:
        call_session = self.model(
            call_session_id=call_session_id,
            request=request,
            response=response,
            request_type=request_type
        )
        self.session.add(call_session)
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            raise ExceptionWhenCreatingProcessingLogRecord
