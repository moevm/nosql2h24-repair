from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from schemas.utils import get_date_now


class BaseDao:
    collection: AsyncIOMotorCollection = None

    @classmethod
    async def _create(cls, data: dict) -> str:
        if cls.collection:
            data['updated_at'] = get_date_now()
            data['created_at'] = get_date_now()
            result = await cls.collection.insert_one(data)
            return str(result.inserted_id)

    @classmethod
    async def _get_by_id(cls, id: str) -> dict:
        if cls.collection:
            return await cls.collection.find_one({"_id": ObjectId(id)})

    @classmethod
    async def _update(cls, id: str, data: dict) -> str | None:
        if cls.collection:
            data['updated_at'] = get_date_now()
            result = await cls.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": data}
            )

            if result.modified_count == 0:
                return None
            return id

