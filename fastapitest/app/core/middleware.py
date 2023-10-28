
from fastapi import FastAPI
from app.core.logging import LogMiddleware

from fastapi.middleware import Middleware

def init_middleware(app: FastAPI):
    app.add_middleware(LogMiddleware)