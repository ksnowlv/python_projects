import uvicorn
from fastapi import FastAPI
from app.core import config
from app.core.middleware import init_middleware
from app.api.routers import init_routers
from app.db.database import *


def create_app():
    # noinspection PyShadowingNames
    app = FastAPI(title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION)
    init_middleware(app)
    init_db()

    init_routers(app)
    return app


app = create_app()


# @app.middleware("http")
# async def loguru_middleware(request, call_next):
#     start_time = time.time()
#     query_params = dict(request.query_params)
#     body = await request.body()
#     loguru_logger.info({
#         "method": request.method,
#         "request.headers": dict(request.headers),
#         "path": request.url.path,
#         "query_params": query_params,
#         "body": body.decode('utf-8')
#     })
#
#     response = await call_next(request)
#     process_time = time.time() - start_time
#
#     loguru_logger.info({
#         "time_cost": process_time * 1000,
#         "status_code": response.status_code,
#         "response.headers": dict(response.headers),
#         # "response.content": await response.content(),
#     })
#
#
#     return response

@app.get('/')
async def root():
    return {'message': "Hello fastapitest!"}


# main
if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=8081, log_level="debug", reload=True)
