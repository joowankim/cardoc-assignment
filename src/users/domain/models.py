from pydantic import BaseModel


class User(BaseModel):
    id: str
    password: str

    class Config:
        orm_mode = True
