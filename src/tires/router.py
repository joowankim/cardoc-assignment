from fastapi import APIRouter, Depends
from starlette import status

from src.authenticates.router import authorize
from src.dependencies import get_session_factory
from src.users.domain import models

tires_router = APIRouter(prefix="/tires")


@tires_router.post("", status_code=status.HTTP_200_OK)
def create_tire(
        user: models.User = Depends(authorize),
        session_factory=Depends(get_session_factory)
):
    pass


@tires_router.get("", status_code=status.HTTP_200_OK)
def list_tires(
        user: models.User = Depends(authorize),
        session_factory=Depends(get_session_factory)
):
    pass
