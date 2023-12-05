
from fastapi import APIRouter, FastAPI

from .files import filerouter
from .users import userrouter
from .redis import redisrouter
from .kafka import kafkarouter
from .hdfs import hdfsrouter


def init_routers(app: FastAPI):
    api_routes = APIRouter()
    api_routes.include_router(userrouter.router)
    api_routes.include_router(filerouter.router)
    api_routes.include_router(redisrouter.router)
    api_routes.include_router(kafkarouter.router)
    api_routes.include_router(hdfsrouter.router)
    app.include_router(api_routes)
    return api_routes
