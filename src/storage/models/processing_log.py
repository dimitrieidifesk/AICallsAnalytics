import uuid
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, JSON, ForeignKey

from src.storage.models import IdUUIDPkMixin, CreatedMixin
from src.storage.models.base import Base
from src.storage.models.enums import RequestTypeOpenAi

if TYPE_CHECKING:
    from src.storage import CallSession


class ProcessingLog(Base, IdUUIDPkMixin, CreatedMixin):
    request: Mapped[dict] = mapped_column(JSON)
    response: Mapped[dict] = mapped_column(JSON)
    request_type: Mapped[RequestTypeOpenAi] = mapped_column(
        Enum(RequestTypeOpenAi, values_callable=lambda x: [e.value for e in RequestTypeOpenAi]),
        name="request_type",
        default=RequestTypeOpenAi.TRANSCRIPTION,
    )
    # Foreign keys
    call_session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("call_sessions.id", ondelete="CASCADE")
    )
    # Relationships
    call_session: Mapped["CallSession"] = relationship(
        foreign_keys=[call_session_id], back_populates="processing_logs"
    )
