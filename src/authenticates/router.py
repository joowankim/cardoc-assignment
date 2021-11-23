from fastapi import APIRouter, Depends
from starlette import status

from src.authenticates.application.services import AuthenticationService
from src.authenticates.dto import LoginInfo, Authorized
from src.dependencies import get_session_factory
from src.users.application.services import UserRegistry
from src.users.application.unit_of_work import SqlUserUnitOfWork

auth_router = APIRouter(prefix="/auth")


@auth_router.post("", status_code=status.HTTP_200_OK, response_model=Authorized)
def sign_in(info: LoginInfo, session_factory=Depends(get_session_factory)):
    user_registry = UserRegistry(uow=SqlUserUnitOfWork(session_factory))
    authentication_service = AuthenticationService(user_registry)
    return authentication_service.access_token(info)
