from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt
import uuid

# 定义密钥
SECRET_KEY = "dikdklqaed134dkdkd349kd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


def generate_userid():
    # 生成用户ID的逻辑
    return str(uuid.uuid4())


def generate_token(user_id: str):
    # 生成令牌的逻辑
    secret_key = SECRET_KEY
    algorithm = "HS256"
    payload = {"sub": user_id}

    # 设置 token 过期时间
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    # 添加过期时间到 payload
    payload.update({"exp": expire})

    access_token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return access_token


# # 定义生成 token 的函数
# def create_token(data: dict):
#     # 设置 token 过期时间
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#
#     # 添加过期时间到 payload
#     data.update({"exp": expire})
#     # 生成 token
#     encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
#
#     return encoded_jwt

# 定义获取当前用户的函数
async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id:
            return {"userId": user_id, "error": "TOKEN令牌无效"}
        else:
            return {"userId": "", "error": "TOKEN令牌无效"}
    except jwt.ExpiredSignatureError:
        return {"userId": "", "error": "TOKEN令牌已过期"}


