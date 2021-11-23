from starlette import status
from starlette.responses import JSONResponse


def user_id_duplicated_exception(request, exc):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)})
