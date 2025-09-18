from typing import TypeVar, Generic, Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model
