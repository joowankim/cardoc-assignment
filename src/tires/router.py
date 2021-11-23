from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from src.authenticates.router import authorize
from src.configs.data_source import CAR_DATA_SOURCE_HOST, CAR_DATA_SOURCE_API_VERSION
from src.dependencies import get_session_factory
from src.tires.application.services import TireCheckroom
from src.tires.application.unit_of_work import SqlTireUnitOfWork
from src.tires.domain.models import Tire
from src.tires.dto import Owner
from src.tires.infra.data_source import WebCarDataSource
from src.users.domain import models
from src.users.domain.models import User

tires_router = APIRouter(prefix="/tires")


@tires_router.post("", status_code=status.HTTP_200_OK)
def create_tire(
        user: User = Depends(authorize),
        owners: List[Owner] = None,
        session_factory=Depends(get_session_factory)
):
    tire_checkroom = TireCheckroom(
        uow=SqlTireUnitOfWork(session_factory),
        data_source=WebCarDataSource(host=CAR_DATA_SOURCE_HOST, api_version=CAR_DATA_SOURCE_API_VERSION)
    )
    tire_checkroom.check_in(owners)


@tires_router.get("", status_code=status.HTTP_200_OK, response_model=List[Tire])
def list_tires(
        user: User = Depends(authorize),
        session_factory=Depends(get_session_factory)
):
    tire_checkroom = TireCheckroom(
        uow=SqlTireUnitOfWork(session_factory),
        data_source=WebCarDataSource(host=CAR_DATA_SOURCE_HOST, api_version=CAR_DATA_SOURCE_API_VERSION)
    )
    return tire_checkroom.tires_of(user.id)
