from fastapi_camelcase import CamelModel


class Owner(CamelModel):
    id: str
    trim_id: int
