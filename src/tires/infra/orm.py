from sqlalchemy import Column, Integer, String, ForeignKey, Enum

from src.configs.database import Base
from src.tires.domain.models import TirePosition


class Tire(Base):
    __tablename__ = "tires"

    tire_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(String, ForeignKey("users.id"))
    trim_id = Column(Integer)
    position = Column("position", Enum(TirePosition))
    width = Column(Integer)
    flatness_ratio = Column(Integer)
    wheel_size = Column(Integer)
