import os

from fastapi import FastAPI, APIRouter
from fastapi.routing import APIRoute
from motor import motor_asyncio
from starlette.requests import Request

from hello_world.app.users.schemas import UserRegisterSchema
from hello_world.app.users.utils import get_password_hash

app = FastAPI()

client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.get_database("repair_db")
user_collection = db.get_collection("users")


async def ping() -> dict:
    return {"Ping": "Pong!"}


async def mainpage() -> str:
    return "YOU ARE ON THE MAIN PAGE"


async def get_users(request: Request) -> list:
    cursor = user_collection.find({})
    res = []
    for document in await cursor.to_list(length=100):
        document["_id"] = str(document["_id"])
        res.append(document)
    return res


@app.post("/register")
async def register(user_data: UserRegisterSchema) -> dict:
    data = user_data.model_dump()
    data["password"] = get_password_hash(user_data.password)
    await user_collection.insert_one(data)
    return {"Success": True}


routes = [
    APIRoute(path="/ping", endpoint=ping, methods=["GET"]),
    APIRoute(path="/", endpoint=mainpage, methods=["GET"]),
    APIRoute(path="/get_users", endpoint=get_users, methods=["GET"]),
]

app.include_router(APIRouter(routes=routes))
