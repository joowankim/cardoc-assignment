import re
from typing import List

import pytest

from src.authenticates.application.services import AuthenticationService
from src.tires.application.services import TireCheckroom
from src.tires.application.unit_of_work import AbstractTireUnitOfWork
from src.tires.domain.models import Tire, TireInfo, TirePosition
from src.tires.infra.data_source import AbstractCarDataSource
from src.tires.infra.repository import AbstractTireRepository
from src.users.application.services import UserRegistry
from src.users.application.unit_of_work import AbstractUserUnitOfWork
from src.users.domain.models import User
from src.users.exceptions import UserNotFoundException, UserIdDuplicatedException
from src.users.infra.repository import AbstractUserRepository
from tests.unit.fixtures.car_data import data


class FakeUserRepository(AbstractUserRepository):
    def __init__(self, users):
        self._users = users

    def add(self, new_user: User):
        exists = self._users.get(new_user.id, None)
        if exists:
            raise UserIdDuplicatedException(f"user {new_user.id} is duplicated")
        self._users[new_user.id] = new_user

    def get(self, id: str) -> User:
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


class FakeTireRepository(AbstractTireRepository):
    def __init__(self, tires):
        self._tires = tires

    def put(self, new_tires: List[Tire]) -> None:
        self._tires += new_tires

    def list_of(self, owner_id: str) -> List[Tire]:
        return list(filter(lambda tire: tire.owner_id == owner_id, self._tires))


class FakeTireUnitOfWork(AbstractTireUnitOfWork):
    def __init__(self):
        self.tires = FakeTireRepository(list())
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


class FakeCarDataSource(AbstractCarDataSource):
    def __init__(self):
        self._source = data

    def get_tires_of(self, trim_id: int) -> List[TireInfo]:
        front_tire = self._source[trim_id]["spec"]["driving"]["frontTire"]["value"]
        rear_tire = self._source[trim_id]["spec"]["driving"]["rearTire"]["value"]

        tires = []
        width, flat, wheel = re.split('[/R]', front_tire)
        tires.append(
            TireInfo(
                trim_id=trim_id, position=TirePosition.FRONT, width=width, flatness_ratio=flat, wheel_size=wheel
            )
        )
        width, flat, wheel = re.split('[/R]', rear_tire)
        tires.append(
            TireInfo(
                trim_id=trim_id, position=TirePosition.REAR, width=width, flatness_ratio=flat, wheel_size=wheel
            )
        )
        return tires


@pytest.fixture
def tire_checkroom():
    return TireCheckroom(FakeTireUnitOfWork(), FakeCarDataSource())
