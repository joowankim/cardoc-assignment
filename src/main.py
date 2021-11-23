from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from src.users.exception_handlers import user_id_duplicated_exception
from src.users.exceptions import UserIdDuplicatedException
from src.users.router import users_router

app = FastAPI()

app.include_router(users_router)

app.add_exception_handler(UserIdDuplicatedException, user_id_duplicated_exception)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
