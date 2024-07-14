from pydantic import BaseModel, Field, ConfigDict, EmailStr
from pydantic_mongo import PydanticObjectId
from typing import Optional

# from src.utils.helper import PyObjectId


class AuthModel(BaseModel):
    email: EmailStr


class TokenModel(AuthModel):
    access_token: str


class AuthResponseModel(BaseModel):
    message: str
    data: list[AuthModel] | AuthModel | TokenModel
    code: int
    status: str

    class Config:
        from_attributes = True


class Login(AuthModel):
    password: str


class Register(AuthModel):
    password: str
    firstName: str
    lastName: str
    phone: str
