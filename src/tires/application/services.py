from typing import List

from src.tires.application.unit_of_work import AbstractTireUnitOfWork
from src.tires.domain import models
from src.tires.dto import Owner
from src.tires.infra.data_source import AbstractCarDataSource


class TireCheckroom:
    def __init__(self, uow: AbstractTireUnitOfWork, data_source: AbstractCarDataSource):
        self.uow = uow
        self.data_source = data_source

    def check_in(self, owners: List[Owner]):
        tires = []
        for owner in owners:
            for tire_info in self.data_source.get_tires_of(owner.trim_id):
                tires.append(models.Tire(owner_id=owner.id, **tire_info.dict()))
        with self.uow:
            self.uow.tires.put(tires)
            self.uow.commit()

    def tires_of(self, owner_id: str) -> List[models.Tire]:
        with self.uow:
            return self.uow.tires.list_of(owner_id)
