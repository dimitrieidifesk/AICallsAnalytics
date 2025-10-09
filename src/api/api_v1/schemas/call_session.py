import uuid
from datetime import datetime

from loguru import logger
from pydantic import HttpUrl
from pydantic import field_validator

from src.api.api_v1.schemas.base import BaseSchema
from src.core.config import settings
from src.storage.models.enums import LeadQuality


class CallCreateSchema(BaseSchema):
    session_id: str
    recording_url: HttpUrl
    is_sales_line: bool
    is_first_call: bool


class ObjectionRequestSchema(BaseSchema):
    title: str
    text: str


class ObjectionResponseSchema(BaseSchema):
    title: str
    compliance_percentage: int
    client_raised: bool
    
    @field_validator("compliance_percentage", mode="before")
    def validate_compliance_percentage(cls, value):
        if isinstance(value, float):
            return int(value)
        return value


class StageRequestSchema(BaseSchema):
    id: int
    title: str
    text: str
    objections: list[ObjectionRequestSchema]
    


class StageResponseSchema(BaseSchema):
    stage_id: int
    title: str
    compliance_percentage: int
    objections: list[ObjectionResponseSchema]
    
    @field_validator("compliance_percentage", mode="before")
    def validate_compliance_percentage(cls, value):
        if isinstance(value, float):
            return int(value)
        return value


class ScriptSchema(BaseSchema):
    title: str
    stages: list[StageRequestSchema]


class CallSessionCreateSchema(BaseSchema):
    call: CallCreateSchema
    script: ScriptSchema


class CallSessionCreateResponseSchema(BaseSchema):
    call_session_id: uuid.UUID


class ScriptComplianceSchema(BaseSchema):
    overall_percentage: int
    stages: list[StageResponseSchema]
    
    @field_validator("overall_percentage", mode="before")
    def validate_overall_percentage(cls, value):
        if isinstance(value, float):
            return int(value)
        return value


class ClientUncertaintySchema(BaseSchema):
    detected: bool
    resolved_by_operator: bool
    comment: str
    
    @field_validator("resolved_by_operator", mode="before")
    def validate_resolved_by_operator(cls, value):
        if not isinstance(value, bool) and value is not None:
            logger.error(f"Invalid value for resolved_by_operator: {value}")
            return False
        return value if value is not None else False


class LeadQualitySchema(BaseSchema):
    status: LeadQuality
    
    @field_validator("status", mode="before")
    def validate_status(cls, value):
        if isinstance(value, str):
            if value == 'NOT_QUALIFIED' or value == 'NOT QUALIFIED':
                return LeadQuality.UNQUALIFIED
            if value not in ("QUALIFIED", "UNQUALIFIED", "UNDETERMINED"):
                return "UNDETERMINED"
            return str(value)
        return value


class CityAskedSchema(BaseSchema):
    was_asked_or_mentioned: bool
    client_city: str | None


class UnscriptedObjectionSchema(BaseSchema):
    text: str
    stage_context: str


class AnalysisResponseSchema(BaseSchema):
    script_compliance: ScriptComplianceSchema
    client_uncertainty: ClientUncertaintySchema
    lead_quality: LeadQualitySchema
    city_asked: CityAskedSchema
    unscripted_objections: list[UnscriptedObjectionSchema]


class MetadataSchema(BaseSchema):
    processed_at: datetime
    gpt_model_used: str = settings.open_ai.chat_model
    transcription_model_used: str = settings.open_ai.whisper_model
    analysis_version: str = "0.0.1"


class TranscriptionCallSessionResponseSchema(BaseSchema):
    transcription: list[dict[str, str]]


class CallSessionAnalysisResponseSchema(BaseSchema):
    session_id: str
    analysis: AnalysisResponseSchema
    metadata: MetadataSchema

