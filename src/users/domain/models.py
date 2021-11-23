from pydantic import BaseModel, constr


class User(BaseModel):
    id: constr(min_length=1)
    password: constr(min_length=1)

    class Config:
        orm_mode = True
