import uuid

from pydantic import BaseModel


class CallSessionProcessingSchema(BaseModel):
    call_session_id: uuid.UUID
