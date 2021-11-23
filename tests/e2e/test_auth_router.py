import unittest

from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status
from starlette.testclient import TestClient

from src import dependencies
from src.configs.database import Base
from src.main import app
from src.users.domain import models


class TestAuthRouter(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})

        def test_session_factory():
            Base.metadata.create_all(bind=self.engine)
            return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        app.dependency_overrides[dependencies.get_session_factory] = test_session_factory
        self.client = TestClient(app)
        self.user = models.User(id="cherry", password="123qwe")
        self.create_user(id=self.user.id, password=self.user.password)

    def tearDown(self) -> None:
        Base.metadata.drop_all(bind=self.engine)

    def create_user(self, id, password):
        data = {"id": id, "password": password}
        self.client.post("/users", json=data)

    def send_sign_in_request_with(self, data):
        return self.client.post("/auth", json=data)

    def test_sign_in_with_correct_login_info(self):
        correct_login_info = {
            "id": self.user.id,
            "password": self.user.password
        }

        response = self.send_sign_in_request_with(correct_login_info)
        response_body = response.json()
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(response_body).contains_key("access_token")

    def test_sign_in_with_wrong_password(self):
        wrong_password_info = {
            "id": self.user.id,
            "password": "wrong_password"
        }

        response = self.send_sign_in_request_with(wrong_password_info)
        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)

    def test_sign_in_with_non_exist_user(self):
        non_exist_user_info = {
            "id": "non-exist-user",
            "password": "123qew"
        }

        response = self.send_sign_in_request_with(non_exist_user_info)
        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)
