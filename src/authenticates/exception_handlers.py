from starlette import status
from starlette.responses import JSONResponse


def invalid_password_exception_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)})
