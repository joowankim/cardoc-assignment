from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from src.authenticates.exception_handlers import invalid_password_exception_handler, \
    invalid_access_token_exception_handler, empty_access_token_exception_handler
from src.authenticates.exceptions import InvalidPasswordException, InvalidAccessTokenException, \
    EmptyAccessTokenException
from src.authenticates.router import auth_router
from src.users.exception_handlers import user_id_duplicated_exception_handler, user_not_found_exception_handler
from src.users.exceptions import UserIdDuplicatedException, UserNotFoundException
from src.users.router import users_router

app = FastAPI()

app.include_router(users_router)
app.include_router(auth_router)

app.add_exception_handler(UserIdDuplicatedException, user_id_duplicated_exception_handler)
app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
app.add_exception_handler(InvalidPasswordException, invalid_password_exception_handler)
app.add_exception_handler(InvalidAccessTokenException, invalid_access_token_exception_handler)
app.add_exception_handler(EmptyAccessTokenException, empty_access_token_exception_handler)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
