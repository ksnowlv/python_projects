

from fastapi import  APIRouter, FastAPI
from app.api.routers import user_routers
from app.api.routers import file_routers

def init_routers(app: FastAPI):
    api_routes = APIRouter()
    api_routes.include_router(user_routers, prefix='/user')
    api_routes.include_router(file_routers, prefix='/files')
    app.include_router(api_routes)

    return api_routes
