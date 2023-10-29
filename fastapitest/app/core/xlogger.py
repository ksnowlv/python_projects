# 自定义的 Loguru 日志封装模块 xlogger.py
from loguru import logger as xlogger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp, Message
from fastapi import Request, Response
import time
import logging
from starlette.concurrency import iterate_in_threadpool

class LogMiddleware(BaseHTTPMiddleware):
    FILES_API = "/files/"

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        # 关闭 FastAPI 内置日志输出
        logging.getLogger("uvicorn").setLevel(logging.ERROR)
        logging.getLogger("uvicorn.access").setLevel(logging.ERROR)
        # 配置 loguru 日志记录器
        xlogger.add("app.log", rotation="500 MB", compression="zip", format="{time} {level} {message}")

    async def dispatch(self, request, call_next):
        cur_time = time.time()
        xlogger.info(f"Request: {request.method} {request.url}")
        xlogger.debug(f"Request Headers: {request.headers}")
        query_params = dict(request.query_params)
        xlogger.debug(f"Request query_params: {query_params}")

        if LogMiddleware.FILES_API in str(request.url):
            print(f"File API")
        else:
            body = await request.body()
            xlogger.debug(f"Request Body: {body.decode('utf-8', 'ignore')}")

        response: Response = await call_next(request)

        # 参考https://cloud.tencent.com/developer/ask/sof/106878776#
        # loguru_logger.info(f"Response Status Code: {response.status_code}")
        # loguru_logger.debug(f"Response Headers: {response.headers}")
        # response_body = [chunk async for chunk in response.body_iterator]
        # response.body_iterator = iterate_in_threadpool(iter(response_body))
        # print(f"response_body={response_body[0].decode()}")
        delta_time = time.time() - cur_time
        xlogger.info(f"total time cost: {delta_time}")
        xlogger.info(f"Response status code: {response.status_code}")
        xlogger.debug(f"Response headers: {response.headers}")
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        xlogger.debug(f"Response Body: {response_body}")
        return Response(content=response_body, status_code=response.status_code,
                        headers=dict(response.headers), media_type=response.media_type)


# 提供对外的接口
def info(message):
    xlogger.info(message)


def debug(message):
    xlogger.debug(message)


def warning(message):
    xlogger.warning(message)


def error(message):
    xlogger.error(message)


def exception(message):
    xlogger.exception(message)
