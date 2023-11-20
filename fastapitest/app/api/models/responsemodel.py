import http
from typing import Optional, List, Dict
from typing import Optional
from pydantic import BaseModel, Field


class ResponseModel:
    def __init__(self, data: Dict, code: int = http.HTTPStatus.OK, message: str = "成功"):
        self.code = code
        self.message = message
        self.data = data


class ResponseBaseModel(BaseModel):
    code: int = Field(http.HTTPStatus.OK, description="请求状态码")
    message: str = Field('请求成功', description="请求状态描述")
    data: Dict[str, object] = Field(None, description="User data, if any")

# class ResponseModel(BaseModel):
#     code: int = 200
#     message: str = "成功"
#     data: Dict