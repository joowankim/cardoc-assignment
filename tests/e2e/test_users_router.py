import unittest

from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status
from starlette.testclient import TestClient

from src import dependencies
from src.configs.database import Base
from src.main import app


class TestUserRouter(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})

        def test_session_factory():
            Base.metadata.create_all(bind=self.engine)
            return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        app.dependency_overrides[dependencies.get_session_factory] = test_session_factory
        self.client = TestClient(app)

    def tearDown(self) -> None:
        Base.metadata.drop_all(bind=self.engine)

    def send_signup_request_with(self, data):
        return self.client.post(
            "/users",
            json=data
        )

    def test_signup_with_valid_info(self):
        data = {
            "id": "cherry",
            "password": "123qwe"
        }

        response = self.send_signup_request_with(data)
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

    def test_signup_with_empty_id(self):
        data = {
            "id": "",
            "password": "123qwe"
        }

        response = self.send_signup_request_with(data)
        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)

    def test_signup_with_empty_password(self):
        data = {
            "id": "cherry",
            "password": ""
        }

        response = self.send_signup_request_with(data)
        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)

    def test_signup_with_duplicated_id(self):
        data = {
            "id": "cherry",
            "password": "123qwe"
        }
        self.send_signup_request_with(data)

        response = self.send_signup_request_with(data)
        assert_that(response.status_code).is_equal_to(status.HTTP_400_BAD_REQUEST)
