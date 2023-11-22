from fastapi import FastAPI

from app.core.xlogger import LogMiddleware


def init_middleware(app: FastAPI):
    app.add_middleware(LogMiddleware)
    pass
