from datetime import datetime
from typing import Dict, Any

from bson import ObjectId
from bson.errors import InvalidId

from dao.project import ProjectDao


class StatDao(ProjectDao):

    @classmethod
    async def get_stats(cls, project_ids: list[str], stat_type: str, start_date: datetime = None,
                        end_date: datetime = None) -> dict[str, Any]:

        project_ids = [ObjectId(pid) for pid in project_ids]

        base_filter = {"_id": {"$in": project_ids}}  # Фильтр по ID проекта

        pipeline = [
            {"$match": base_filter},  # Фильтр по ID
            {
                "$project": {
                    "_id": 1,
                    "filtered_items": {
                        "$filter": {
                            "input": {"$objectToArray": f"${stat_type}"},
                            "as": "item",
                            "cond": {
                                "$and": [
                                    {"$gte": ["$$item.v.created_at", start_date]} if start_date else {},
                                    {"$lte": ["$$item.v.created_at", end_date]} if end_date else {}
                                ]
                            }
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "count": {"$size": "$filtered_items"}
                }
            }
        ]


        cursor = cls.collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)

        return {str(result["_id"]): result["count"] for result in results}
