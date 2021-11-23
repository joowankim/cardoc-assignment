import abc

from sqlalchemy.orm import Session

from src.users.domain import models
from src.users.domain.models import User
from src.users.exceptions import UserNotFoundException
from src.users.infra import orm


class AbstractUserRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, new_user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, exist_user_id: str) -> models.User:
        raise NotImplementedError


class SqlUserRepository(AbstractUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, new_user: User):
        orm_new_user = orm.User(**new_user.dict())
        self.session.add(orm_new_user)

    def get(self, id: str) -> models.User:
        orm_user = self.session.query(orm.User).filter(orm.User.id == id).first()
        if not orm_user:
            raise UserNotFoundException(f"user {id} is not found")
        return models.User.from_orm(orm_user)
