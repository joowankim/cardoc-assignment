from starlette import status
from starlette.responses import JSONResponse


def data_source_error_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(exc)})
