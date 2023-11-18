from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import Session
from typing import Optional


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userid = Column(String(64), primary_key=True, index=True)
    name = Column(String(50), index=True)
    age = Column(Integer)
    phone = Column(String(20), index=True)
    verification_code = Column(String(6))
    token = Column(String(256), index=True, unique=True)


class UserDbModel:
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, userid: str) -> Optional[UserDB]:
        return self.session.query(UserDB).filter(UserDB.userid == userid).first()

    def get_user_by_token(self, token: str) -> Optional[UserDB]:
        return self.session.query(UserDB).filter(UserDB.token == token).first()

    def get_user_by_phone(self, phone: str) -> Optional[UserDB]:
        return self.session.query(UserDB).filter(UserDB.phone == phone).first()

    def create_user(self, userid: str, name: str, age: int, phone: str, verification_code: str, token: str) -> UserDB:
        user = UserDB(userid=userid, name=name, age=age, phone=phone, verification_code=verification_code, token=token)
        self.session.add(user)
        self.session.commit()
        return user

    def update_user_token(self, user: UserDB, token: str) -> UserDB:
        user.token = token
        self.session.commit()
        return user

    def delete_user(self, user: UserDB) -> None:
        self.session.delete(user)
        self.session.commit()
