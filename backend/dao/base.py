from typing import Mapping, Any, Sequence

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from schemas.utils import get_date_now, object_id_to_str


class BaseDao:
    collection: AsyncIOMotorCollection = None

    @classmethod
    async def _create(cls, data: dict) -> str:
        if cls.collection is not None:
            data['updated_at'] = get_date_now()
            data['created_at'] = get_date_now()
            result = await cls.collection.insert_one(data)
            return str(result.inserted_id)

    @classmethod
    async def _get_one_by_id(cls, id: str) -> dict:
        if cls.collection is not None:
            data = await cls.collection.find_one({"_id": ObjectId(id)})
            return object_id_to_str(data)

    @classmethod
    async def _get_one_by_field(cls, field: str, data: str) -> dict:
        if cls.collection is not None:
            data = await cls.collection.find_one({field: data})
            return object_id_to_str(data)

    @classmethod
    async def _update(cls, id: str, data: dict) -> str | None:
        if cls.collection is not None:
            data['updated_at'] = get_date_now()
            result = await cls.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": data}
            )

            if result.modified_count == 0:
                return None
            return id
        
    @classmethod
    async def _update_with_query(cls, query: dict[str, Any], data: dict[str, Any]) -> str | None:
        if cls.collection is not None:
            result = await cls.collection.update_one(query, data)
            if result.modified_count == 0:
                return None
            return str(query["_id"])

    # @classmethod        
    # async def _find_with_filters(cls, query: dict) -> dict:
    #     if cls.collection:
    #
