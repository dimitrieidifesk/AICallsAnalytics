import uuid
from typing import Any

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from loguru import logger

from src.core.exceptions import (
    ExceptionWhenCreatingCallSessionRecord,
    ExceptionWhenUpdatingCallSessionRecord
)
from src.storage.models.call_session import CallSession
from src.storage.repositories.base import BaseRepository


class CallSessionRepository(BaseRepository[CallSession]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, CallSession)

    async def create(self, data: dict[str, Any]) -> CallSession:
        call_session = self.model(**data)
        call_session.id = uuid.uuid4()
        self.session.add(call_session)
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            raise ExceptionWhenCreatingCallSessionRecord

        return call_session

    async def get_call_session_by_id(self, call_session_id: uuid.UUID) -> CallSession:
        query = (
            select(self.model)
            .where(self.model.id == call_session_id)
        )
        res = await self.session.execute(query)

        return res.scalar()

    async def update_call_session(
        self, call_session_id: uuid.UUID, data: dict[str, Any]
    ):
        query = (
            update(self.model)
            .where(self.model.id == call_session_id)
            .values(**data)
        )
        try:
            await self.session.execute(query)
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            raise ExceptionWhenUpdatingCallSessionRecord
