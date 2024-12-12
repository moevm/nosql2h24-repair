from datetime import datetime
import json

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings

client = AsyncIOMotorClient(settings.DATABASE_URL, serverSelectionTimeoutMS=5000)
db = client.get_database(settings.MONGO_INITDB_DATABASE)


async def create_indexation():
    """
    Создает индексы для коллекций
    """
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

async def is_database_empty() -> bool:
    """
    Проверяет, пуста ли база данных.
    """
    collections = await db.list_collection_names()
    for collection_name in collections:
        if await db[collection_name].count_documents({}) > 0:
            return False
    return True


def load_default_data():
    """
    Загружает данные из JSON-файла в базу данных.
    """
    try:
        with open(settings.DEFAULT_DATA_FILE, "r") as file:
            data = json.load(file)

        def convert_dates(item):
            if isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, str):
                        # Попробуем распознать ISO формат
                        try:
                            item[key] = datetime.fromisoformat(value)
                        except ValueError:
                            pass  # Если это не дата, оставляем строку
                    elif isinstance(value, (list, dict)):
                        convert_dates(value)
            elif isinstance(item, list):
                for sub_item in item:
                    convert_dates(sub_item)

        for collection_name, documents in data.items():
            for doc in documents:
                convert_dates(doc)
                if "_id" in doc:
                    doc["_id"] = ObjectId(doc["_id"])

            collection = db[collection_name]
            collection.insert_many(documents)
        print("Default data has been loaded successfully.")
    except Exception as e:
        print(f"Error loading default data: {e}")