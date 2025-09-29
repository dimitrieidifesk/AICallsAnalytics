import uuid

from pydantic import BaseModel

from src.storage.models.enums import QueueAction


class CallSessionProcessingSchema(BaseModel):
    call_session_id: uuid.UUID
    action: QueueAction
