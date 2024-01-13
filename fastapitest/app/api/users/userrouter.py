import http

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.userdb import UserDbModel
from app.db.userschemas import UserCreate, UserUpdate
from app.utils.tokentools import *
from .usermodel import USER_NOT_REGIST_MESSAGE
from ..models.responsemodel import ResponseBaseModel

router = APIRouter(
    prefix="/user",
    tags=["用户接口"],
    responses={404: {"description": "Not found"}},
)


@router.get('/home')
async def home():
    # return {'message': "Hello user"}
    return  {'message': "hello fastapitest"}

@router.post("/regist", response_model=ResponseBaseModel)
async def regist(user: UserCreate, db: Session = Depends(get_db)):
    user_dbmodel = UserDbModel(db)
    existing_user = user_dbmodel.get_user_by_phone(user.phone)

    if existing_user:
        response_data = {
            "registResult": 0,
            "userid": "",
            "token": ""
        }

        return ResponseBaseModel(message=USER_NOT_REGIST_MESSAGE, data=response_data)
    else:
        userid = generate_userid()
        token = generate_token(userid)

        try:
            res_user = user_dbmodel.create_user(userid=userid,
                                                name=user.name,
                                                age=user.age,
                                                phone=user.phone,
                                                verification_code=user.verification_code,
                                                token=token)

            response_data = {
                "registResult": 1,
                "userid": res_user.userid,
                "token": res_user.token
            }
            return ResponseBaseModel(data=response_data)
        except Exception as e:
            print(f"发生了未知错误:{str(e)}")
            response_data = {
                "registResult": 0,
                "userid": "",
                "token": ""
            }
            return ResponseBaseModel(code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
                                     message="请求失败",
                                     data=response_data)


@router.post("/login", response_model=ResponseBaseModel)
async def login(user: UserCreate, db: Session = Depends(get_db)):
    user_dbmodel = UserDbModel(db)
    existing_user = user_dbmodel.get_user_by_phone(user.phone)
    if existing_user:
        if existing_user.verification_code == user.verification_code:
            token = generate_token(existing_user.userid)
            res_user = user_dbmodel.update_user_token(existing_user, token)
            response_data = {
                "userid": res_user.userid,
                "token": res_user.token
            }
            return ResponseBaseModel(data=response_data)
        else:
            return ResponseBaseModel(code=http.HTTPStatus.NOT_FOUND, message="手机验证码错误，请检查后再试")

    else:
        return ResponseBaseModel(code=http.HTTPStatus.NOT_FOUND, message=USER_NOT_REGIST_MESSAGE, data={ "userid": "",
                "token": "", "gzip":"test gzip 1dkkdkkddkdkdkddkdkdkdkddkkkkkkkklds;'sa;lsl;skfa00000000000011111111"})


@router.post("/getSMSCode", response_model=ResponseBaseModel)
async def get_sms_code(phone: str, db: Session = Depends(get_db)):
    user_model = UserDbModel(db)
    existing_user = user_model.get_user_by_phone(phone)

    if existing_user:
        existing_user.verification_code = "123456"
        response_data = {
            "userid": existing_user.userid,
            "verification_code": existing_user.verification_code
        }

        return ResponseBaseModel(data=response_data)
    else:
        return ResponseBaseModel(code=http.HTTPStatus.NOT_FOUND, message=USER_NOT_REGIST_MESSAGE)


@router.put("/updateUser", response_model=ResponseBaseModel)
async def update_user(token: str, user: UserUpdate, db: Session = Depends(get_db)):
    if user.verification_code is None:
        return ResponseBaseModel(code=http.HTTPStatus.NOT_FOUND, message="验证码不能为空!")

    if user.name is None and user.age is None and user.phone is None:
        return ResponseBaseModel(code=http.HTTPStatus.NOT_FOUND, message="您暂无需要更新的个人信息!")

    user_model = UserDbModel(db)
    existing_user = user_model.get_user_by_token(token)
    if existing_user:

        if user.name:
            existing_user.name = user.name

        if user.age:
            existing_user.age = user.age

        if user.phone:
            existing_user.phone = user.phone

        existing_user.verification_code = user.verification_code
        user_model.session.commit()
        return ResponseBaseModel(message="个人信息更新成功!")
    else:
        return ResponseBaseModel(message="该用户暂时查询不到！!")


@router.delete("/deleteUser", response_model=ResponseBaseModel)
async def delete_user(token: str, db: Session = Depends(get_db)):
    user_model = UserDbModel(db)
    existing_user = user_model.get_user_by_token(token)
    if existing_user:
        user_model.delete_user(existing_user)
        return ResponseBaseModel(message="用户已注销!")
    else:
        return ResponseBaseModel(code=http.HTTPStatus.NOT_FOUND, message="用户查询不到，注销失败!")
