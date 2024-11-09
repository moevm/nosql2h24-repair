from motor.motor_asyncio import AsyncIOMotorClient

from config import settings

client = AsyncIOMotorClient(settings.DATABASE_URL, serverSelectionTimeoutMS=5000)
db = client.get_database(settings.MONGO_INITDB_DATABASE)