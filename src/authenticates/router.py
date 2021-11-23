from fastapi import APIRouter, Depends
from starlette import status

from src.authenticates.dto import LoginInfo
from src.dependencies import get_session_factory

auth_router = APIRouter(prefix="/auth")


@auth_router.post("", status_code=status.HTTP_200_OK)
def signin(info: LoginInfo, session_factory=Depends(get_session_factory)):
    pass
