from fastapi import FastAPI

from app.core.xlogger import LogMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

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
    # 开启gzip压缩
    # 当请求的头信息 Accept-Encoding 字段带有"gzip"时，GZipMiddleware负责完成相应的返回结果处理。
    # GZipMiddleware 支持 minimum_size 参数：当返回结果大小小于指定值时不启用压缩。(单位为字节，默认值为500)
    # Accept-Encoding: gzip
    app.add_middleware(GZipMiddleware, minimum_size=100)
    #强制开启https
    #app.add_middleware(HTTPSRedirectMiddleware)

