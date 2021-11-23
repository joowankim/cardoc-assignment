import abc
import re
from typing import List

import requests

from src.tires.domain import models
from src.tires.domain.models import TirePosition


def is_tire_format(tire_info: str) -> bool:
    if re.match(r'\d+/\d+R\d+$', tire_info):
        return True
    return False


class AbstractCarDataSource(abc.ABC):
    @abc.abstractmethod
    def get_tires_of(self, trim_id: int) -> List[models.TireInfo]:
        raise NotImplementedError


class WebCarDataSource(AbstractCarDataSource):
    def __init__(self, host: str, api_version: str):
        self.host = host
        self.api_version = api_version

    def get_tires_of(self, trim_id: int) -> List[models.TireInfo]:
        url = '/'.join([self.host, self.api_version, "trim", str(trim_id)])
        response = requests.get(url)
        car = response.json()

        front_tire = car["spec"]["driving"]["frontTire"]["value"]
        rear_tire = car["spec"]["driving"]["rearTire"]["value"]

        tires = []
        if is_tire_format(front_tire):
            width, flat, wheel = re.split('[/R]', front_tire)
            tires.append(
                models.TireInfo(
                    trim_id=trim_id, position=TirePosition.FRONT, width=width, flatness_ratio=flat, wheel_size=wheel
                )
            )
        if is_tire_format(rear_tire):
            width, flat, wheel = re.split('[/R]', rear_tire)
            tires.append(
                models.TireInfo(
                    trim_id=trim_id, position=TirePosition.REAR, width=width, flatness_ratio=flat, wheel_size=wheel
                )
            )
        return tires
