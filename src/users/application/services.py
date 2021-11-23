from src.users.application.unit_of_work import AbstractUserUnitOfWork
from src.users.domain.models import User


class UserRegistry:
    def __init__(self, uow: AbstractUserUnitOfWork):
        self.uow = uow

    def register(self, user: User):
        pass

    def user(self, id: str):
        pass
