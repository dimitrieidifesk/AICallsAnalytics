from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.call_session import CallSessionService
from src.storage.models.db_helper import db_connector

GetSession = Annotated[AsyncSession, Depends(db_connector.session_getter)]


def get_call_session_service(session: GetSession) -> CallSessionService:
    return CallSessionService(session)


CallSessionServiceDep = Annotated[CallSessionService, Depends(get_call_session_service)]
