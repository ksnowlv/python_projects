# 自定义的 Loguru 日志封装模块 xlogger.py
import logging
import time

from fastapi import Response
from loguru import logger as xlogger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class LogMiddleware(BaseHTTPMiddleware):
    FILES_API = "/file/"

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        # 关闭 FastAPI 内置日志输出
        logging.getLogger("uvicorn").setLevel(logging.ERROR)
        logging.getLogger("uvicorn.access").setLevel(logging.ERROR)
        # 配置 loguru 日志记录器
        xlogger.add("app.log", rotation="500 MB", compression="zip", format="{time} {level} {message}")

    # async def before_request(self, request: Request) -> Optional[Request]:
    #         # 如果请求是一个断点续传的 GET 请求，则返回 None，不进行处理
    #     if "Range" in request.headers and request.method == "GET":
    #         return None
    #     return request

    async def dispatch(self, request, call_next):
        cur_time = time.time()
        xlogger.info(f"Request: {request.method} {request.url} {request.headers}")
        # xlogger.debug(f"Request Headers: {request.headers}")
        query_params = dict(request.query_params)
        xlogger.debug(f"Request query_params: {query_params}")

        response: Response = await call_next(request)

        # 参考https://cloud.tencent.com/developer/ask/sof/106878776#
        # loguru_logger.info(f"Response Status Code: {response.status_code}")
        # loguru_logger.debug(f"Response Headers: {response.headers}")
        # response_body = [chunk async for chunk in response.body_iterator]
        # response.body_iterator = iterate_in_threadpool(iter(response_body))
        # print(f"response_body={response_body[0].decode()}")
        delta_time = time.time() - cur_time

        if delta_time > 0.3:
            xlogger.error(f"total time cost: {delta_time}")
        else:
            xlogger.warning(f"total time cost: {delta_time}")

        xlogger.info(f"Response status code: {response.status_code} Response headers: {response.headers}")

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        xlogger.info(f"Response Body: {response_body}")
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
