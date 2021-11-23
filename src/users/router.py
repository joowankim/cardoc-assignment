from fastapi import APIRouter, Depends
from starlette import status

from src.dependencies import get_session_factory
from src.users.application.services import UserRegistry
from src.users.application.unit_of_work import SqlUserUnitOfWork
from src.users.domain.models import User

users_router = APIRouter(prefix="/users")


@users_router.post("", status_code=status.HTTP_200_OK)
def signup(user: User, session_factory=Depends(get_session_factory)):
    user_registry = UserRegistry(uow=SqlUserUnitOfWork(session_factory))
    user_registry.register(user)
