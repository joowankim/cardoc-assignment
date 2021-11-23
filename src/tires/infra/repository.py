import abc
from typing import List

from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from src.tires.domain import models
from src.tires.infra import orm


class AbstractTireRepository(abc.ABC):
    @abc.abstractmethod
    def put(self, new_tires: List[models.Tire]) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def list_of(self, owner_id: str) -> List[models.Tire]:
        raise NotImplementedError


class SqlTireRepository(AbstractTireRepository):
    def __init__(self, session: Session):
        self.session = session

    def put(self, new_tires: List[models.Tire]) -> None:
        self.session.bulk_insert_mappings(orm.Tire, list(map(lambda tire: tire.dict(), new_tires)))

    def list_of(self, owner_id: str) -> List[models.Tire]:
        tires_orm = self.session.query(orm.Tire).filter(orm.Tire.owner_id == owner_id).all()
        return parse_obj_as(List[models.Tire], tires_orm)
