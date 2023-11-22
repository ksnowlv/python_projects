from app.api.models.responsemodel import ResponseModel

USER_NOT_REGIST_MESSAGE = "该用户账号未注册，请先去注册!"


class UserRegistResponseModel(ResponseModel):
    def __init__(self, userId: str, token: str, code: int = 200, message: str = "成功"):
        data = {"userId": userId, "token": token}
        super().__init__(data, code, message)

# class TokenResponseModel(BaseModel):
#     token: str
#
# class UserResponseModel(BaseModel):
#     userId: str
#     token: str
#
# class CityResponseModel(BaseModel):
#     cityList: List[Dict]

# # Example usage
# token_response = TokenResponseModel(token="123456")
# print(token_response.dict())
#
# user_response = UserResponseModel(userId="789", token="654321")
# print(user_response.dict())
#
# city_response = CityResponseModel(cityList=[{"name": "New York", "population": 10000000}, {"name": "Tokyo", "population": 14000000}])
# response_model = ResponseModel(data=city_response.dict())
# print(response_model.dict())
