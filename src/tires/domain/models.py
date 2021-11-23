from enum import Enum

from fastapi_camelcase import CamelModel
from pydantic import conint, BaseModel


class TirePosition(Enum):
    FRONT = "FRONT"
    REAR = "REAR"


class Tire(CamelModel):
    owner_id: str
    trim_id: int
    position: TirePosition
    width: conint(gt=0)
    flatness_ratio: conint(gt=0)
    wheel_size: conint(gt=0)

    class Config:
        orm_mode = True


class TireInfo(BaseModel):
    trim_id: int
    position: TirePosition
    width: conint(gt=0)
    flatness_ratio: conint(gt=0)
    wheel_size: conint(gt=0)
