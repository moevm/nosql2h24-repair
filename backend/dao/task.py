from bson import ObjectId

from dao.base import BaseDao
from database import db
from schemas.task import Task, TaskResponse, TaskUpdate
from schemas.user import Worker
from schemas.utils import generate_id, get_date_now


class TaskDAO(BaseDao):
    collection = db.get_collection('project')

    @classmethod
    async def add_task(cls, project_id: str, stage_id, task_create: Task) -> TaskResponse | None:
        task_id = generate_id()
        result = await cls.collection.update_one(
            {"_id": ObjectId(project_id), f"stages.{stage_id}": {"$exists": True}},
            {
                "$set": {f"stages.{stage_id}.tasks.{task_id}": task_create.model_dump()}
            }
        )
        if result.modified_count > 0:
            return TaskResponse(id=task_id, **task_create.model_dump())
        return None

    @classmethod
    async def remove_task(cls, project_id: str, stage_id: str, task_id: str) -> str | None:
        deleted_id = await cls._update_with_query(
            {
                "_id": ObjectId(project_id),
                f"stages.{stage_id}.tasks.{task_id}": {"$exists": True}
            },
            {
                "$unset": {f"stages.{stage_id}.tasks.{task_id}": ""}
            }
        )
        return deleted_id

    @classmethod
    async def get_task_by_id(cls, project_id: str, stage_id: str, task_id: str) -> TaskResponse | None:
        project = await cls.collection.find_one(
            {
                "_id": ObjectId(project_id),
                f"stages.{stage_id}.tasks.{task_id}": {"$exists": True}
            },
            {
                f"stages.{stage_id}.tasks.{task_id}": 1
            }
        )

        if project:
            task = project["stages"][stage_id]["tasks"][task_id]
            return TaskResponse(id=task_id, **task)
        return None

    @classmethod
    async def update_task_by_id(cls, project_id: str, stage_id: str, task_id: str,
                                task_update: TaskUpdate) -> TaskResponse | None:

        update_data = task_update.model_dump()
        update_data["updated_at"] = get_date_now()

        result = await cls.collection.update_one(
            {
                "_id": ObjectId(project_id),
                f"stages.{stage_id}.tasks.{task_id}": {"$exists": True}
            },
            {
                "$set": {
                    f"stages.{stage_id}.tasks.{task_id}.name": update_data["name"],
                    f"stages.{stage_id}.tasks.{task_id}.description": update_data["description"],
                    f"stages.{stage_id}.tasks.{task_id}.status": update_data["status"],
                    f"stages.{stage_id}.tasks.{task_id}.start_date": update_data["start_date"],
                    f"stages.{stage_id}.tasks.{task_id}.end_date": update_data["end_date"],
                    f"stages.{stage_id}.tasks.{task_id}.updated_at": update_data["updated_at"],
                }
            }
        )

        if result.modified_count == 0:
            return None

        return await cls.get_task_by_id(project_id, stage_id, task_id)

    @classmethod
    async def get_tasks_by_stage_id(cls, project_id: str, stage_id: str) -> list[TaskResponse] | list[None]:
        project = await cls.collection.find_one(
            {
                "_id": ObjectId(project_id),
                f"stages.{stage_id}.tasks": {"$exists": True}
            }
        )

        if not project or "stages" not in project or stage_id not in project["stages"]:
            return []

        tasks = project["stages"][stage_id].get("tasks", {})

        tasks_list = [
            TaskResponse(id=task_id, **task_data) for task_id, task_data in tasks.items()
        ]
        return tasks_list

    @classmethod
    async def get_all_tasks_by_user(cls, user_id: str) -> list[Task] | list[None]:
        cursor = cls.collection.find(
            {
                "stages": {
                    "$exists": True
                }
            }
        )

        tasks = []
        async for project in cursor:
            for stage_id, stage in project.get("stages", {}).items():
                for task_id, task in stage.get("tasks", {}).items():
                    for worker_id, worker in task.get("workers", {}).items():
                        if worker_id == user_id:
                            tasks.append(TaskResponse(id=task_id, **task))

        return tasks

    @classmethod
    async def add_worker_to_task(cls, project_id: str, stage_id: str, task_id: str, worker_id: str,
                                 worker: Worker) -> TaskResponse | dict[str: str]:
        update_result = await cls.collection.update_one(
            {
                "_id": ObjectId(project_id),
                f"stages.{stage_id}.tasks.{task_id}": {"$exists": True}
            },
            {
                "$set": {
                    f"stages.{stage_id}.tasks.{task_id}.workers.{worker_id}": {
                        "name": worker.name,
                        "role": worker.role,
                    }
                }
            }
        )

        if update_result.modified_count == 0:
            return None

        return await cls.get_task_by_id(project_id, stage_id, task_id)

    @classmethod
    async def delete_worker_from_task(cls, project_id: str, stage_id: str, task_id: str, worker_id: str) -> str | None:
        delete_result = await cls.collection.update_one(
            {
                "_id": ObjectId(project_id),
                f"stages.{stage_id}.tasks.{task_id}": {"$exists": True}
            },
            {
                "$unset": {
                    f"stages.{stage_id}.tasks.{task_id}.workers.{worker_id}": ""
                }
            }
        )

        if delete_result.modified_count == 0:
            return None

        return task_id
