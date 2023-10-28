# 自定义的 Loguru 日志封装模块 mylogging.py
from loguru import logger as loguru_logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp, Message
from fastapi import Request, Response
import time
from starlette.concurrency import iterate_in_threadpool

# 配置 loguru 日志记录器

loguru_logger.add("app.log", rotation="500 MB", compression="zip", format="{time} {level} {message}")


class LogMiddleware(BaseHTTPMiddleware):
    FILES_API = "/files/"

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request, call_next):
        cur_time = time.time()
        loguru_logger.info(f"Request: {request.method} {request.url}")
        loguru_logger.debug(f"Request Headers: {request.headers}")
        query_params = dict(request.query_params)
        loguru_logger.debug(f"Request query_params: {query_params}")

        if LogMiddleware.FILES_API in str(request.url):
            print(f"File API")
        else:
            body = await request.body()
            loguru_logger.debug(f"Request Body: {body.decode('utf-8', 'ignore')}")

        response: Response = await call_next(request)

        # 参考https://cloud.tencent.com/developer/ask/sof/106878776#
        # loguru_logger.info(f"Response Status Code: {response.status_code}")
        # loguru_logger.debug(f"Response Headers: {response.headers}")
        # response_body = [chunk async for chunk in response.body_iterator]
        # response.body_iterator = iterate_in_threadpool(iter(response_body))
        # print(f"response_body={response_body[0].decode()}")

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        loguru_logger.debug(f"Response Body: {response_body}")
        delta_time = time.time() - cur_time
        loguru_logger.debug(f"total time cost: {delta_time}")
        return Response(content=response_body, status_code=response.status_code,
                        headers=dict(response.headers), media_type=response.media_type)


# 提供对外的接口
def info(message):
    loguru_logger.info(message)


def debug(message):
    loguru_logger.debug(message)


def warning(message):
    loguru_logger.warning(message)


def error(message):
    loguru_logger.error(message)


def exception(message):
    loguru_logger.exception(message)
