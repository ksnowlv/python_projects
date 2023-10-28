from fastapi import APIRouter, FastAPI

from app.api.routers.user_router import UserRouter
from app.api.routers.file_router import FileRouter


def init_routers(app: FastAPI):
    api_routes = APIRouter()
    api_routes.include_router(UserRouter(), prefix='/user')
    api_routes.include_router(FileRouter(), prefix='/files')
    app.include_router(api_routes)

    return api_routes
