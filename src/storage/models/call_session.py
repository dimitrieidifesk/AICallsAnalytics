from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, Boolean, JSON

from src.storage.models import IdUUIDPkMixin, CreatedMixin, UpdatedMixin
from src.storage.models.base import Base
from src.storage.models.enums import CallSessionStatus

if TYPE_CHECKING:
    from src.storage import ProcessingLog


class CallSession(Base, IdUUIDPkMixin, CreatedMixin, UpdatedMixin):
    session_id: Mapped[str] = mapped_column(String(256))
    recording_url: Mapped[str] = mapped_column(String(256))
    is_sales_line: Mapped[bool] = mapped_column(Boolean)
    is_first_call: Mapped[bool] = mapped_column(Boolean)
    script: Mapped[dict] = mapped_column(JSON)
    transcription: Mapped[dict] = mapped_column(JSON)
    analysis: Mapped[dict] = mapped_column(JSON)
    status: Mapped[CallSessionStatus] = mapped_column(
        Enum(CallSessionStatus, values_callable=lambda x: [e.value for e in CallSessionStatus]),
        name="type_campaign",
        default=CallSessionStatus.RECEIVED,
    )
    processing_logs: Mapped[list["ProcessingLog"]] = relationship(
        "ProcessingLog", back_populates="call_session"
    )
