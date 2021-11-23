from typing import List

from src.tires.application.unit_of_work import AbstractTireUnitOfWork
from src.tires.domain import models
from src.tires.dto import Owner


class TireCheckroom:
    def __init__(self, uow: AbstractTireUnitOfWork):
        self.uow = uow

    def check_in(self, tire: models.Tire):
        pass

    def tires_of(self, owners: List[Owner]):
        pass
