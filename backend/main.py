import uvicorn
import time
from app.util.validate_config import validate_config_vars
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.config.logging_config import get_logger
from app.config.database_config import Base, engine
from app.controller import all_routers
from app.exception.exception_handler import add_exception_handler
from app.config.config import settings
from app.config.base import *

validate_config_vars()

logger = get_logger(class_name=__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    description='Hotel Management API Documentation',
    version="1.0",
    title='Hotel Management API',)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"]
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    logger.debug(
        f"{request.url} | {request.method} | {response.status_code} | Execution Time: {(time.time() - start_time) * 1000}ms")
    return response


Base.metadata.create_all(bind=engine)

app.include_router(all_routers)
add_exception_handler(app)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
