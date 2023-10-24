
from fastapi import APIRouter

user_routers = APIRouter()

@user_routers.get('/home')
async def user():
    return {'message': "Hello world"}

@user_routers.post("/login_json")
async def login_json(phone: str, code: str):
    return {'message': "Hello world"}

@user_routers.post("/login_form")
async def login_form(phone: str, code: str):
    return {'message': "Hello world"}

@user_routers.post("/regist")
async def regist(phone: str, code: str):
    return {'message': "Hello world"}

@user_routers.post("/login")
async def login(phone: str, code: str):
    return {'message': "Hello world"}
