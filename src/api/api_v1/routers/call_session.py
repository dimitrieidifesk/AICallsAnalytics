from http import HTTPStatus

from fastapi import APIRouter

from src.api.api_v1.schemas.call_session import (
    CallSessionCreateSchema,
    CallSessionAnalysisResponseSchema,
    TranscriptionCallSessionResponseSchema
)
from src.api.dependencies.getter import CallSessionServiceDep
from src.api.dependencies.verify_user import VerifyUser

router = APIRouter()


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_call_session(
    _: VerifyUser,
    data: CallSessionCreateSchema,
    service: CallSessionServiceDep,
) -> None:

    return await service.create_new_call_session(data)


@router.get("/analysis/{session_id}")
async def get_call_session_analysis(
    _: VerifyUser,
    session_id: str,
    service: CallSessionServiceDep,
) -> CallSessionAnalysisResponseSchema:

    return await service.get_call_session_analysis(session_id)


@router.get("/transcription/{session_id}")
async def get_call_session_transcription(
    _: VerifyUser,
    session_id: str,
    service: CallSessionServiceDep,
) -> TranscriptionCallSessionResponseSchema:

    return await service.get_call_session_transcription(session_id)
