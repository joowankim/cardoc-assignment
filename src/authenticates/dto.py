from pydantic import BaseModel, constr


class LoginInfo(BaseModel):
    id: constr(min_length=1)
    password: constr(min_length=1)


class Authorized(BaseModel):
    access_token: str
