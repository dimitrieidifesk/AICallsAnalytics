import uuid
from http import HTTPStatus

from fastapi import APIRouter

from src.api.api_v1.schemas.call_session import (
    CallSessionCreateSchema,
    CallSessionCreateResponseSchema,
    TranscriptionCallSessionResponseSchema, CallSessionAnalysisResponseSchema,
)
from src.api.dependencies.getter import CallSessionServiceDep
from src.api.dependencies.verify_user import VerifyUser

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_call_session(
    _: VerifyUser,
    data: CallSessionCreateSchema,
    service: CallSessionServiceDep,
) -> CallSessionCreateResponseSchema:

    return await service.create_new_call_session(data)


@router.get("/analysis/by_session_id/{session_id}")
async def get_call_session_analysis(
    _: VerifyUser,
    session_id: str,
    service: CallSessionServiceDep,
) -> CallSessionAnalysisResponseSchema:

    return await service.get_call_session_analysis_by_session_id(session_id)


@router.get("/analysis/{call_session_id}")
async def get_call_session_analysis(
    _: VerifyUser,
    call_session_id: uuid.UUID,
    service: CallSessionServiceDep,
) -> CallSessionAnalysisResponseSchema:

    return await service.get_call_session_analysis(call_session_id)


@router.get("/transcription/{call_session_id}")
async def get_call_session_transcription(
    _: VerifyUser,
    call_session_id: uuid.UUID,
    service: CallSessionServiceDep,
) -> TranscriptionCallSessionResponseSchema:

    return await service.get_call_session_transcription(call_session_id)


@router.get("/finish_processing/{call_session_id}")
async def finish_processing_call_session(
    _: VerifyUser,
    call_session_id: uuid.UUID,
    service: CallSessionServiceDep,
) -> None:

    return await service.finish_processing_call_session_by_status(call_session_id)
