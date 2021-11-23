import pytest
from assertpy import assert_that

from src.configs.data_source import CAR_DATA_SOURCE_HOST, CAT_DATA_SOURCE_API_VERSION
from src.tires.domain import models
from src.tires.domain.models import TirePosition
from src.tires.infra.data_source import WebCarDataSource


@pytest.fixture
def car_data_source():
    return WebCarDataSource(CAR_DATA_SOURCE_HOST, CAT_DATA_SOURCE_API_VERSION)


def test_get_tire_with_trim_id(car_data_source):
    tires = car_data_source.get_tires_of(5000)
    expected = [
        models.TireInfo(trim_id=5000, position=TirePosition.FRONT, width=225, flatness_ratio=60, wheel_size=16),
        models.TireInfo(trim_id=5000, position=TirePosition.REAR, width=225, flatness_ratio=60, wheel_size=16)
    ]
    assert_that(tires).is_equal_to(expected)
