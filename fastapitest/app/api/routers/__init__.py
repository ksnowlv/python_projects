from fastapi import APIRouter, FastAPI

from . import filerouter
from ..users import userrouter


def init_routers(app: FastAPI):
    api_routes = APIRouter()
    api_routes.include_router(userrouter.router)
    api_routes.include_router(filerouter.router)
    app.include_router(api_routes)
    return api_routes
