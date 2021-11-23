from typing import List

from assertpy import assert_that
from pydantic import parse_obj_as
from sqlalchemy.exc import IntegrityError

from src.users.application.unit_of_work import SqlUserUnitOfWork
from src.users.domain import models
from src.users.exceptions import UserNotFoundException


def insert_user(session):
    session.execute(
        "INSERT INTO users (id, password)"
        " VALUES ('cherry', '123qwe')"
    )


def get_all_users(session):
    users = session.execute("SELECT * FROM users").all()
    return parse_obj_as(List[models.User], users)


def test_add_user_with_unique_id(session_factory):
    new_user = models.User(id="cherry", password="123qwe")
    uow = SqlUserUnitOfWork(session_factory)
    with uow:
        uow.users.add(new_user)
        uow.commit()

    session = session_factory()
    users = get_all_users(session)

    assert_that(users[0]).is_equal_to(new_user)


def test_add_user_with_duplicated_id(session_factory):
    session = session_factory()
    insert_user(session)
    session.commit()

    new_user = models.User(id="cherry", password="123qwe")
    uow = SqlUserUnitOfWork(session_factory)
    with uow:
        uow.users.add(new_user)
        assert_that(uow.commit).raises(IntegrityError).when_called_with()


def test_get_user_with_exist_id(session_factory):
    session = session_factory()
    insert_user(session)
    session.commit()

    exist_user_id = "cherry"
    uow = SqlUserUnitOfWork(session_factory)
    with uow:
        user = uow.users.get(exist_user_id)
        assert_that(user).is_instance_of(models.User)
        assert_that(user.id).is_equal_to(exist_user_id)


def test_get_user_with_not_exist_id(session_factory):
    non_exist_user_id = "cherry"
    uow = SqlUserUnitOfWork(session_factory)
    with uow:
        assert_that(uow.users.get).raises(UserNotFoundException).when_called_with(non_exist_user_id)

