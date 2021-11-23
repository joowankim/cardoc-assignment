from typing import List

import pytest
from assertpy import assert_that
from pydantic import parse_obj_as

from src.tires.application.unit_of_work import SqlTireUnitOfWork
from src.tires.domain import models
from src.tires.domain.models import TirePosition


def add_users(session):
    session.execute(
        "INSERT INTO users (id, password) VALUES "
        "('cherry', '123qwe'),"
        "('banana', 'qwe123')"
    )


def get_all_tires(session):
    tires = session.execute("SELECT * FROM tires").all()
    return parse_obj_as(List[models.Tire], tires)


@pytest.fixture
def tires():
    return [
        models.Tire(
            owner_id="cherry", trim_id=5000, position=TirePosition.REAR, width=255, flatness_ratio=60, wheel_size=16
        ),
        models.Tire(
            owner_id="cherry", trim_id=5000, position=TirePosition.FRONT, width=255, flatness_ratio=60, wheel_size=16
        ),
        models.Tire(
            owner_id="cherry", trim_id=8000, position=TirePosition.FRONT, width=255, flatness_ratio=80, wheel_size=25
        ),
        models.Tire(
            owner_id="cherry", trim_id=8000, position=TirePosition.REAR, width=255, flatness_ratio=80, wheel_size=25
        ),
        models.Tire(
            owner_id="banana", trim_id=5000, position=TirePosition.FRONT, width=255, flatness_ratio=40, wheel_size=16
        ),
        models.Tire(
            owner_id="banana", trim_id=5000, position=TirePosition.REAR, width=255, flatness_ratio=40, wheel_size=16
        ),
    ]


def test_put_with_valid_tire(session_factory, tires):
    session = session_factory()
    add_users(session)
    session.commit()

    uow = SqlTireUnitOfWork(session_factory)
    with uow:
        uow.tires.put(tires)
        uow.commit()

    tires = get_all_tires(session)
    assert_that(len(tires)).is_equal_to(6)
    assert_that(tires[0]).is_instance_of(models.Tire)


def insert_tires(session):
    session.execute(
        "INSERT INTO tires (owner_id, trim_id, position, width, flatness_ratio, wheel_size) VALUES "
        "('cherry', '5000', 'FRONT', '255', '60', '16'),"
        "('cherry', '8000', 'FRONT', '255', '80', '25'),"
        "('cherry', '8000', 'REAR', '255', '80', '25'),"
        "('cherry', '5000', 'REAR', '255', '60', '16'),"
        "('banana', '5000', 'FRONT', '255', '60', '16'),"
        "('banana', '5000', 'REAR', '255', '60', '16')"
    )


def test_list_tires_of_owners(session_factory):
    session = session_factory()
    insert_tires(session)
    session.commit()

    owner_id = "cherry"
    uow = SqlTireUnitOfWork(session_factory)
    with uow:
        tires = uow.tires.list_of(owner_id)

        assert_that(len(tires)).is_equal_to(4)
        assert_that(tires[0]).is_instance_of(models.Tire)
