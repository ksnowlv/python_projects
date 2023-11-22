from fastapi import APIRouter,Depends
from typing import Any
from app.core.xredis import  get_redis
import json
from ..models.responsemodel import ResponseBaseModel

router = APIRouter(
    prefix="/redis",
    tags=["redis测试接口"],
    responses={404: {"description": "Not found"}},
)

@router.post('/setKeyValue', response_model=ResponseBaseModel)
async def set_key_value(key:str, value:Any, redis=Depends(get_redis)):
    await redis.set(key, value)
    value = await redis.get(key)
    print(f"{key}:{value}")

    return ResponseBaseModel(data={key: value})


@router.post('/setKeysValues')
async def set_keys_values(pairs: dict, redis=Depends(get_redis)):
    pipe = redis.pipeline()
    for k, v in pairs.items():
        pipe.set(k, v)
    await pipe.execute()

    return ResponseBaseModel(data=pairs)

@router.post('/setJsonKeyValues')
async def set_json_key_values(key: str, value: dict, redis=Depends(get_redis)):
    json_data = json.dumps(value)  # 将字典转换为 JSON 字符串
    await redis.set(key, json_data)
    res_value = await redis.get(key)
    json_obj = json.loads(res_value)
    return ResponseBaseModel(data={key: json_obj})

@router.post('/getKey')
async def get_key(key: str, redis=Depends(get_redis)):
    value = await redis.get(key)
    return ResponseBaseModel(data={key: value})

