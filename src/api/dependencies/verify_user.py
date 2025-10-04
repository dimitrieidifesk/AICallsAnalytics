from typing import Annotated

from aiocache import cached
from aiocache.serializers import PickleSerializer

from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.core.config import settings

security = HTTPBasic()


@cached(ttl=200, serializer=PickleSerializer())
async def verify_user(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    correct_username = credentials.username == settings.user_credential.username
    correct_password = credentials.password == settings.user_credential.password
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )


VerifyUser = Annotated[None, Depends(verify_user)]
