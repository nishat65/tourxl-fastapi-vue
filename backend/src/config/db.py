import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi


uri = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(uri, server_api=ServerApi("1"))


def get_db():
    return client["tourxl"]


async def ping_server():
    try:
        await client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
