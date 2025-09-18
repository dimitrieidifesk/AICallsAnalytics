from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.core.config import settings


class CreatedMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.timezone(settings.default_timezone, func.now()))


class UpdatedMixin:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.timezone(settings.default_timezone, func.now()),
        onupdate=func.timezone(settings.default_timezone, func.now()),
    )
