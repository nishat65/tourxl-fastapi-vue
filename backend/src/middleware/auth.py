import time

from fastapi import Request


async def process_time_header(request: Request, call_next):
    print(request.headers.get("Authorization", None), "request")
    response = await call_next(request)
    return response
