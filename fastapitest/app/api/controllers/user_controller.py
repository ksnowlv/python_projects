
class User_Controllers(object):

    def __init__(self):
        pass

    def handle_user_login_json(self, phone: str, code: str):

        if len(phone) == 0:

            return {"code": 404, "message": "手机号为空!"}

        if len(code) == 0:
            return {"code": 404, "message": "验证码为空!"}


        return {"code": 200, "message": "登录成功!"}
