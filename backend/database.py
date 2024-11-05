import pymongo
from pymongo import mongo_client
from pymongo.errors import ConnectionFailure

from config import settings

print(settings.DATABASE_URL)
client = mongo_client.MongoClient(settings.DATABASE_URL, serverSelectionTimeoutMS=5000)

try:
    conn = client.server_info()
    print(f'Connected to MongoDB {conn.get("version")}')
except ConnectionFailure:
    print("Unable to connect to MongoDB")
    
db = client[settings.MONGO_INITDB_DATABASE]
User = db.users
User.create_index([("email", pymongo.ASCENDING)], unique=True)
