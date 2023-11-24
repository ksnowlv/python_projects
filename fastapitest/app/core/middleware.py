from fastapi import FastAPI

from app.core.xlogger import LogMiddleware
from fastapi.middleware.cors import CORSMiddleware

def init_middleware(app: FastAPI):
    app.add_middleware(LogMiddleware)
    # 配置跨域资源共享（CORS）
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 设置允许的来源，可以是 '*' 表示允许所有来源，也可以是列表
        allow_credentials=True,
        allow_methods=["*"],  # 设置允许的 HTTP 方法，可以是 '*' 表示允许所有方法，也可以是列表
        allow_headers=["*"],  # 设置允许的 HTTP 头部，可以是 '*' 表示允许所有头部，也可以是列表
    )

