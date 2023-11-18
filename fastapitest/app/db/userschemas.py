from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    age: int
    phone: str
    verification_code: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    verification_code: Optional[str] = None


class UserResponse(BaseModel):
    userid: str
    name: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    token: str


class UserVerificationCode(BaseModel):
    userid: str
    verification_code: str
