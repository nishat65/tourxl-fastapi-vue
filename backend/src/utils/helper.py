import os
from datetime import datetime, timedelta, timezone
from typing import Union
from fastapi import HTTPException, Depends, status, Request

import jwt
from passlib.context import CryptContext
from src.config.deps import oauth_scheme
from src.utils.constant import auth
from src.config.db import get_db


def predefinedJsonRes(message, data, code=200):
    status = "success" if str(code).startswith("2") else "error"
    return {"message": message, "data": data, "status": status, "code": code}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.getenv("JWT_SECRET"), algorithm=os.getenv("ALGORITHM")
    )
    return encoded_jwt


def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(
            token, os.getenv("JWT_SECRET"), algorithms=[os.getenv("ALGORITHM")]
        )
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=predefinedJsonRes(
                message=auth["EXPIRED_TOKEN"],
                data=None,
                code=status.HTTP_401_UNAUTHORIZED,
            ),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=predefinedJsonRes(
                message=auth["INVALID_TOKEN"],
                data=None,
                code=status.HTTP_401_UNAUTHORIZED,
            ),
        )


async def verify_access_token(token: str = Depends(oauth_scheme)):
    user = decode_jwt(token=token)
    if not user:
        raise HTTPException(
            status_code=400,
            detail=predefinedJsonRes(message=auth["INVALID_CREDENTIALS"], data=None),
        )
    return user


async def getCookie(
    request: Request,
    db=Depends(get_db),
):
    token = request.cookies.get("access_token")
    token = token.split(" ")[1]
    user = await verify_access_token(token)
    authUser = await db.users.find_one({"email": user["sub"]})
    if not authUser:
        raise HTTPException(
            status_code=400,
            detail=predefinedJsonRes(message=auth["INVALID_CREDENTIALS"], data=None),
        )
    return request
