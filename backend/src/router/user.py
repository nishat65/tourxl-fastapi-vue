from enum import Enum
from typing import Union, Annotated
from fastapi import APIRouter, Query, Path, Header, status, Form

from src.utils.constant import users
from src.utils.helper import predefinedJsonRes
from src.schema.user import UserPostSchema, UserGetSchema, UserResponseModel

router = APIRouter(
    prefix="/users",
    # tags=["USERS"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def getUsers(
    skip: Annotated[int | None, Query(title="Skipping users", max=10)] = None,
    limit: Annotated[Union[int | None], Query(title="Limiting users", max=100)] = None,
):
    return predefinedJsonRes(message=users["USERS_FETCHED"], data=[])


@router.post("/", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
async def createUser(user: UserPostSchema, token: Annotated[str, Header()]) -> dict:
    user.dict().update({"token": token})
    return predefinedJsonRes(
        message=users["USER_CREATED"], data=user.dict(), status=201
    )


@router.patch("/{id}", response_model=UserResponseModel)
async def updateUser(
    id: Annotated[int, Path(title="Required ID of the users")],
    # user: Annotated[UserPostSchema, Body(embed=True)],
    user: UserPostSchema,
) -> dict:
    return predefinedJsonRes(message=users["USER_UPDATED"], data=user.dict())


# Enum
class UserType(str, Enum):
    admin = "admin"
    customer = "customer"
    guide = "guide"


@router.get("/type/{user_type}")
async def getUserType(user_type: UserType):
    return predefinedJsonRes(message=users["USER_FETCHED"], data=user_type)


@router.get("/{id}")
async def getUser(id: Annotated[int, Path(title="Required ID of the users")]):
    return predefinedJsonRes(message=users["USER_FETCHED"], data=id)
