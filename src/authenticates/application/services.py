from jose import jwt

from src.authenticates.dto import LoginInfo, Authorized
from src.authenticates.exceptions import InvalidPasswordException
from src.configs import authenticate
from src.users.application.services import UserRegistry
from src.users.domain import models


class AuthenticationService:
    def __init__(self, user_registry: UserRegistry):
        self.registry = user_registry
        self.secret = authenticate.SECRET
        self.algorithm = authenticate.ALGORITHM

    def __get_access_token(self, user: models.User):
        return "Bearer " + jwt.encode({"user_id": user.id}, key=self.secret, algorithm=self.algorithm)

    def access_token(self, info: LoginInfo) -> Authorized:
        user = self.registry.user(info.id)
        if user.password != info.password:
            raise InvalidPasswordException("incorrect password")
        token = self.__get_access_token(user)
        return Authorized(access_token=token)

    def authorized_user(self, authorized: Authorized) -> models.User:
        pass
