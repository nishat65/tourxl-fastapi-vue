import logging

from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

load_dotenv()

from src.config.db import ping_server, client
from src.router import auth
from src.router import user
from src.utils.helper import predefinedJsonRes
from src.middleware.auth import process_time_header

app = FastAPI(
    title="TourXL",
    description="TourXL API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
)

logging.getLogger("passlib").setLevel(logging.ERROR)


@app.on_event("startup")
async def startup_db_client():
    await ping_server()


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=predefinedJsonRes(
            message="Validation error",
            data=exc.errors(),
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    )


@app.exception_handler(AttributeError)
async def all_exception_handler(request, exc):
    print(f"AttributeError: ", {exc.error()})
    return JSONResponse(
        status_code=500,
        content=predefinedJsonRes(
            message="Internal server error",
            data=exc.error(),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ),
    )


app.include_router(auth.router, prefix="/api/v1", tags=["AUTH"])
app.include_router(user.router, prefix="/api/v2", tags=["USER"])
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     return await process_time_header(request, call_next)


@app.get("/")
async def root():
    return {"message": "Hello from tourxl-fastapi-vue!"}
