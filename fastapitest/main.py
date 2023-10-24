
from typing import Union

from fastapi import FastAPI, APIRouter
import uvicorn
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from app.core import config

from app.api.routers.user_routers import user_routers
from app.api.routers.file_routers import file_routers

def create_app():
    app = FastAPI(title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION)

    api_routes = APIRouter()
    api_routes.include_router(user_routers, prefix='/user')
    api_routes.include_router(file_routers, prefix='/files' )
    app.include_router(api_routes)

    return app

app = create_app()

@app.get('/')
async def root():
    return {'message': "Hello fastapitest!"}

# main
if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=8081, log_level="debug", reload=True)