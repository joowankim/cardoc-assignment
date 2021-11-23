from assertpy import assert_that

from src.users.domain import models
from src.users.exceptions import UserIdDuplicatedException, UserNotFoundException


def test_register_user_with_unique_id(user_registry):
    new_user = models.User(id="cherry", password="123qwe")
    user_registry.register(new_user)

    assert_that(user_registry.uow.committed).is_equal_to(True)


def test_register_user_with_duplicated_id(user_registry):
    new_user = models.User(id="cherry", password="123qwe")
    user_registry.register(new_user)

    duplicated_id_user = models.User(id="cherry", password="23wqeqwe")
    assert_that(user_registry.register).raises(UserIdDuplicatedException).when_called_with(duplicated_id_user)


def test_get_user_with_exist_id(user_registry):
    new_user = models.User(id="cherry", password="123qwe")
    user_registry.register(new_user)

    user = user_registry.user(new_user.id)
    assert_that(user).is_equal_to(new_user)


def test_get_user_with_non_exist_id(user_registry):
    non_exist_user_id = "cherry"
    assert_that(user_registry.user).raises(UserNotFoundException).when_called_with(non_exist_user_id)
