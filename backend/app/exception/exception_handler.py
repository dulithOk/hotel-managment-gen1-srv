from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
from app.config.logging_config import get_logger
from app.exception.base_exception import BaseAppException
from app.model.generic_response import GenericResponse

logger = get_logger(class_name=__name__)


def add_exception_handler(app: FastAPI):
    @app.exception_handler(BaseAppException)
    async def handle_unauthorized_exception(request: Request, exc: BaseAppException):
        logger.error(exc.message)
        return JSONResponse(status_code=exc.status,
                            content=GenericResponse.failed(message=exc.message, results=[],
                                                           status_code=exc.status).to_dict())

    @app.exception_handler(Exception)
    async def handle_generic_exception(request: Request, exc: Exception):
        logger.exception(exc)
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST,
                            content=GenericResponse.failed(message=str(exc), results=[],
                                                           status_code=HTTP_400_BAD_REQUEST).to_dict())
