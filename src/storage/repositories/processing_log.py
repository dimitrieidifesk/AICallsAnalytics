import uuid
from typing import Any

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from loguru import logger

from src.core.exceptions import ExceptionWhenCreatingProcessingLogRecord, ExceptionWhenUpdatingProcessingLogRecord
from src.storage import ProcessingLog
from src.storage.models.enums import RequestTypeOpenAi
from src.storage.repositories.base import BaseRepository


class ProcessingLogRepository(BaseRepository[ProcessingLog]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ProcessingLog)

    async def create(self, data: dict[str, Any]) -> ProcessingLog:
        processing_log = self.model(**data)
        processing_log.id = uuid.uuid4()
        self.session.add(processing_log)
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            raise ExceptionWhenCreatingProcessingLogRecord

        return processing_log

    async def update(self, processing_log_id: uuid.UUID, data: dict[str, Any]) -> None:
        query = (
            update(self.model)
            .where(self.model.id == processing_log_id)
            .values(**data)
        )
        try:
            await self.session.execute(query)
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            raise ExceptionWhenUpdatingProcessingLogRecord
