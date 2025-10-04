from fastapi import APIRouter

from src.core.config import settings
from src.api.api_v1.routers.common import router as common_router
from src.api.api_v1.routers.call_session import router as call_session_router
from src.core.constants import CALL_SESSION_TAG

router = APIRouter(prefix=settings.api.v1.prefix)

router.include_router(common_router, prefix=settings.api.v1.common)
router.include_router(call_session_router, prefix=settings.api.v1.call_session, tags=[CALL_SESSION_TAG])
