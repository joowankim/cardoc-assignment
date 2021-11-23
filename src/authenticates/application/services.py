from jose import jwt, JWTError

from src.authenticates.dto import LoginInfo, Authorized
from src.authenticates.exceptions import InvalidPasswordException, InvalidAccessTokenException, \
    EmptyAccessTokenException
from src.configs import authenticate
from src.users.application.services import UserRegistry
from src.users.domain import models


class AuthenticationService:
    def __init__(self, user_registry: UserRegistry):
        self.registry = user_registry
        self.secret = authenticate.SECRET
        self.algorithm = authenticate.ALGORITHM
        self.access_token_type = authenticate.TOKEN_TYPE

    def __get_access_token(self, user: models.User):
        claims = {
            "user_id": user.id
        }
        return self.access_token_type + " " + jwt.encode(claims, key=self.secret, algorithm=self.algorithm)

    def __get_claims_of(self, access_token: str):
        if self.access_token_type not in access_token:
            InvalidAccessTokenException("access token in invalid")
        type_removed = access_token[len(self.access_token_type)+1:]
        try:
            return jwt.decode(token=type_removed, key=self.secret, algorithms=self.algorithm)
        except JWTError:
            raise InvalidAccessTokenException("access token in invalid")

    def access_token(self, info: LoginInfo) -> Authorized:
        user = self.registry.user(info.id)
        if user.password != info.password:
            raise InvalidPasswordException("incorrect password")
        token = self.__get_access_token(user)
        return Authorized(access_token=token)

    def authorized_user(self, access_token: str) -> models.User:
        if not access_token:
            raise EmptyAccessTokenException("access token is required")
        user_id = self.__get_claims_of(access_token)["user_id"]
        return self.registry.user(user_id)

