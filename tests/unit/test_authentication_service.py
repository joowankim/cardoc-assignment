from assertpy import assert_that
from jose import jwt

from src.authenticates.dto import LoginInfo
from src.authenticates.exceptions import InvalidPasswordException
from src.configs import authenticate
from src.users.domain import models
from src.users.exceptions import UserNotFoundException


def insert_user(user_registry, new_user):
    user_registry.register(new_user)


def access_token(user):
    return "Bearer " + jwt.encode({"user_id": user.id}, key=authenticate.SECRET, algorithm=authenticate.ALGORITHM)


def test_get_access_token_with_valid_login_info(authentication_service):
    new_user = models.User(id="cherry", password="123qwe")
    insert_user(authentication_service.registry, new_user)

    login_info = LoginInfo(id=new_user.id, password=new_user.password)
    actual = authentication_service.access_token(login_info)
    expected = access_token(new_user)
    assert_that(actual.access_token).is_equal_to(expected)


def test_get_access_token_with_wrong_password(authentication_service):
    new_user = models.User(id="cherry", password="123qwe")
    insert_user(authentication_service.registry, new_user)

    login_info = LoginInfo(id=new_user.id, password="wrong_password")
    assert_that(authentication_service.access_token).raises(InvalidPasswordException).when_called_with(login_info)


def test_get_access_token_with_non_exist_id(authentication_service):
    non_exist_user = models.User(id="cherry", password="123qwe")
    login_info = LoginInfo(id=non_exist_user.id, password=non_exist_user.password)
    assert_that(authentication_service.access_token).raises(UserNotFoundException).when_called_with(login_info)
