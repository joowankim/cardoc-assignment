import pytest

from src.authenticates.application.services import AuthenticationService
from src.users.application.services import UserRegistry
from src.users.application.unit_of_work import AbstractUserUnitOfWork
from src.users.domain import models
from src.users.domain.models import User
from src.users.exceptions import UserNotFoundException, UserIdDuplicatedException
from src.users.infra.repository import AbstractUserRepository


class FakeUserRepository(AbstractUserRepository):
    def __init__(self, users):
        self._users = users

    def add(self, new_user: User):
        exists = self._users.get(new_user.id, None)
        if exists:
            raise UserIdDuplicatedException(f"user {new_user.id} is duplicated")
        self._users[new_user.id] = new_user

    def get(self, id: str) -> models.User:
        try:
            return self._users[id]
        except KeyError:
            raise UserNotFoundException(f"user {id} is not found")


class FakeUserUnitOfWork(AbstractUserUnitOfWork):
    def __init__(self):
        self.users = FakeUserRepository(dict())
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


@pytest.fixture
def user_registry():
    return UserRegistry(FakeUserUnitOfWork())


@pytest.fixture
def authentication_service(user_registry):
    return AuthenticationService(user_registry)
