from src.users.application.unit_of_work import AbstractUserUnitOfWork
from src.users.domain.models import User


class UserRegistry:
    def __init__(self, uow: AbstractUserUnitOfWork):
        self.uow = uow

    def register(self, user: User):
        with self.uow:
            self.uow.users.add(user)
            self.uow.commit()

    def user(self, id: str):
        with self.uow:
            user = self.uow.users.get(id)
        return user
