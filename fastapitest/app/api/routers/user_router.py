from fastapi import APIRouter
from app.core.xlogger import xlogger


class UserRouter(APIRouter):
    def __init__(self):
        super().__init__()

        @self.get('/home')
        async def home():
            # return {'message': "Hello user"}
            xlogger.info("home:")
            return self.handle_home_response("heom test")

        @self.post("/login_json")
        async def login_json(phone: str, code: str):
            return {'message': "login_json"}

        @self.post("/login_form")
        async def login_form(phone: str, code: str):
            return {'message': "Hlogin_form"}

        @self.post("/regist")
        async def regist(phone: str, code: str):
            return {'message': "regist"}

        @self.post("/login")
        async def login(phone: str, code: str):
            return {'message': "login"}

    def handle_home_response(self, message):
        return {'message': message}
