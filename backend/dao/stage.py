from bson import ObjectId

from dao.project import get_project_by_id
from database import db
from schemas.project import Stage
from schemas.utils import object_id_to_str, generate_id


async def add_stage_to_project(project_id: str, stage_create: Stage):
    project_collection = db.get_collection('project')
    result = await project_collection.update_one(
        {'_id': ObjectId(project_id)},
        {
            "$set": {f"stages.{generate_id()}": stage_create.model_dump()}
        }
    )
    return await get_project_by_id(project_id)
