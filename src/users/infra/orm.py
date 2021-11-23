from sqlalchemy import Column, Integer, String

from src.configs.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, unique=True)
    password = Column(String)
