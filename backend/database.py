from motor.motor_asyncio import AsyncIOMotorClient

from config import settings

client = AsyncIOMotorClient(settings.DATABASE_URL, serverSelectionTimeoutMS=5000)
db = client.get_database(settings.MONGO_INITDB_DATABASE)


async def create_indexation():
    users = db.get_collection('user')
    await users.create_index('email')
    
    chats = db.get_collection('chat')
    await chats.create_index('id')
    await chats.create_index(
        [
            ("id", 1),
            ("timestamp", -1),
        ]
    )