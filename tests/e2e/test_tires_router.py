import unittest

from assertpy import assert_that
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status
from starlette.testclient import TestClient

from src import dependencies
from src.configs.database import Base
from src.main import app
from src.users.domain.models import User


class TestTiresRouter(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite:///test.db", connect_args={"check_same_thread": False})

        def test_session_factory():
            Base.metadata.create_all(bind=self.engine)
            return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        app.dependency_overrides[dependencies.get_session_factory] = test_session_factory
        self.client = TestClient(app)
        self.user = User(id="cherry", password="123qwe")
        self.create_user(id=self.user.id, password=self.user.password)

    def tearDown(self) -> None:
        Base.metadata.drop_all(bind=self.engine)

    def create_user(self, id: str, password: str):
        self.client.post("/users", json={"id": id, "password": password})

    def sign_in(self, id: str, password: str):
        data = self.client.post("/auth", json={"id": id, "password": password}).json()
        return data["access_token"]

    def create_tires_with(self, data):
        access_token = self.sign_in(id=self.user.id, password=self.user.password)
        self.send_create_tire_request_with(data=data, access_token=access_token)

    def send_create_tire_request_with(self, data, access_token):
        headers = {"Authorization": access_token}
        return self.client.post("/tires", json=data, headers=headers)

    def send_list_tires_request_with(self, access_token):
        headers = {"Authorization": access_token}
        return self.client.get("tires", headers=headers)

    def test_create_tire_with_valid_owners(self):
        access_token = self.sign_in(id=self.user.id, password=self.user.password)
        data = [
            {"id": "cherry", "trim_id": 5000},
            {"id": "cherry", "trim_id": 9000},
        ]
        response = self.send_create_tire_request_with(data=data, access_token=access_token)
        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)

    def test_create_tire_without_access_token(self):
        data = [
            {"id": "cherry", "trim_id": 5000},
            {"id": "cherry", "trim_id": 9000},
        ]
        response = self.client.post("/tires", json=data)
        assert_that(response.status_code).is_equal_to(status.HTTP_401_UNAUTHORIZED)

    def test_create_tire_with_invalid_access_token(self):
        access_token = "invalid access token"
        data = [
            {"id": "cherry", "trim_id": 5000},
            {"id": "cherry", "trim_id": 9000},
        ]
        response = self.send_create_tire_request_with(data=data, access_token=access_token)
        assert_that(response.status_code).is_equal_to(status.HTTP_401_UNAUTHORIZED)

    def test_list_tires_with_valid_access_token(self):
        data = [
            {"id": "cherry", "trim_id": 5000},
            {"id": "cherry", "trim_id": 9000},
            {"id": "mango", "trim_id": 11000}
        ]
        self.create_tires_with(data=data)

        access_token = self.sign_in(id=self.user.id, password=self.user.password)
        response = self.send_list_tires_request_with(access_token=access_token)
        data = response.json()

        assert_that(response.status_code).is_equal_to(status.HTTP_200_OK)
        assert_that(len(data)).is_equal_to(4)

    def test_list_tires_without_access_token(self):
        response = self.client.get("/tires")
        assert_that(response.status_code).is_equal_to(status.HTTP_401_UNAUTHORIZED)

    def test_list_tires_with_invalid_access_token(self):
        access_token = "invalid access token"
        response = self.send_list_tires_request_with(access_token=access_token)
        assert_that(response.status_code).is_equal_to(status.HTTP_401_UNAUTHORIZED)

