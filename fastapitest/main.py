
import uvicorn
from fastapi import FastAPI
from app.core import config
from app.core.middleware import init_middleware
from app.api import init_routers
from app.db.database import *
from app.core.xredis import init_redis, close_redis
from app.db.xgridfs import XGridFS

def create_app():

    app = FastAPI(title=config.PROJECT_NAME, debug=config.DEBUG, version=config.VERSION)
    init_middleware(app)
    init_db()
    init_routers(app)
    return app


app = create_app()

@app.on_event("startup")
async def startup():
    await init_redis()
    XGridFS.shared_gridfs()


@app.on_event("shutdown")
async def shutdown():
    await close_redis()

# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     start_time = time.time()
#
#     # 等待请求主体数据的返回
#     request_body = await request.body()
#     request_dict = {
#         "url": str(request.url),
#         "headers": dict(request.headers),
#         "query_params": dict(request.query_params),
#         "body": request_body.decode(),
#     }
#
#     response = await call_next(request)
#
#     end_time = time.time()
#
#     response_body = await response.body()
#     response_dict = {
#         "headers": dict(response.headers),
#         "body": response_body.decode(),
#     }
#
#     log_dict = {
#         "request": request_dict,
#         "response": response_dict,
#         "duration": end_time - start_time,
#     }
#
#     xlogger.warning(log_dict)
#
#     # 构造新的响应，并将 body 设置为响应体的字节流
#     new_response = JSONResponse(
#         content=response.body,
#         status_code=response.status_code,
#         headers=dict(response.headers),
#         media_type=response.media_type,
#     )
#
#     return new_response




# main
if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=8081, log_level="debug", reload=True)
