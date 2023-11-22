
from fastapi import APIRouter, FastAPI

from .files import filerouter
from .users import userrouter
from .redis import redisrouter


def init_routers(app: FastAPI):
    api_routes = APIRouter()
    api_routes.include_router(userrouter.router)
    api_routes.include_router(filerouter.router)
    api_routes.include_router(redisrouter.router)
    app.include_router(api_routes)
    return api_routes
