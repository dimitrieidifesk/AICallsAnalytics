from src.core.config import BaseSchema, settings
from src.storage.models.enums import PromtMessageRole


class PromtMessageSchema(BaseSchema):
    role: PromtMessageRole
    content: str

class StructureTextRequestSchema(BaseSchema):
    model: str = settings.open_ai.chat_model
    messages: list[PromtMessageSchema]