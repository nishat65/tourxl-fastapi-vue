import json
from fastapi import APIRouter, Depends, Response, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from src.utils.helper import (
    predefinedJsonRes,
    create_access_token,
    get_password_hash,
    verify_password,
    getCookie,
)
from src.utils.constant import auth
from src.config.db import get_db
from src.config.deps import oauth_scheme
from src.schema.auth import Login, Register, AuthResponseModel

router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=AuthResponseModel)
async def register(user: Register, db=Depends(get_db)):
    user = user.model_dump()
    user.update({"password": get_password_hash(user["password"])})
    await db.users.insert_one(user)
    return predefinedJsonRes(message=auth["REGISTER_SUCCESS"], data=user)


async def authenticate_user(user: object, password: str, db):
    user = await db.users.find_one({"email": user.username})
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


@router.post("/login", response_model=AuthResponseModel)
async def login(
    user: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    db=Depends(get_db),
):
    user = await authenticate_user(user, user.password, db)
    if not user:
        raise HTTPException(
            status_code=400,
            detail=predefinedJsonRes(message="Invalid username or password", data=None),
        )
    access_token = create_access_token(data={"sub": user["email"]})
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return predefinedJsonRes(message=auth["LOGIN_SUCCESS"], data=user)


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Successfully logged out"}


@router.get("/users", response_model=AuthResponseModel)
async def get_users(
    _token: str = Depends(oauth_scheme),
    _cookie: str = Depends(getCookie),
    db=Depends(get_db),
):

    users = await db.users.find().to_list(length=10)
    return predefinedJsonRes(message="USERS_FETCHED", data=users)


"""
{
  "email": "john@gmail.com",
  "password": "john",
  "firstName": "john",
  "lastName": "john",
  "phone": "001001001"
}
"""


# @router.get(
#     "/users",
#     response_model=UsersResponse,
# )
# async def get_users(db=Depends(get_db), limit: int = 5, skip: int = 0):
#     users = await db.customers.find().to_list(limit)
#     return predefinedJsonRes(message="success", data=users)


# @router.get(
#     "/users/{id}",
#     response_model=UserResponse,
# )
# async def get_user(id: str, db=Depends(get_db)):
#     user = await db.customers.find_one({"_id": ObjectId(id)})
#     return predefinedJsonRes(message="success", data=user)


# @router.post("/register")
# async def register(user: Register, db=Depends(get_db)):
#     await db.customers.insert_one(user.dict())
#     return predefinedJsonRes(message=auth["REGISTER_SUCCESS"], data=user.dict())
