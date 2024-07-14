from pydantic import BaseModel, Field
from typing import List, Optional
from .auth import AuthModel


class UsersResponse(BaseModel):
    message: str
    data: List[AuthModel]
    code: int

    # class Config:
    #     orm_mode = True


class UserResponse(BaseModel):
    message: str
    data: Optional[AuthModel]
    code: int


class UserBaseSchema(BaseModel):
    username: str = Field(default="john", description="Name of the user", min_length=3)
    password: str = Field(
        default="*****", description="Password of the user", min_length=6
    )


class UserGetSchema(BaseModel):
    username: str = Field(description="Name of the user", min_length=3)


class UserResponseModel(BaseModel):
    message: str
    data: UserGetSchema
    code: int
    status: str


class UserPostSchema(UserBaseSchema):
    pass
