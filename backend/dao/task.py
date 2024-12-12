from datetime import datetime
import re
from bson import ObjectId

from dao.base import BaseDao
from database import db
from schemas.task import Task, TaskResponse, TaskStatus, TaskUpdate, TaskStatusUpdate, ProjectTaskResponse
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

        updated_id = await cls._update_with_query(
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
                    f"stages.{stage_id}.tasks.{task_id}.updated_at": get_date_now(),
                }
            }
        )

        if updated_id is None:
            return None

        return await cls.get_task_by_id(project_id, stage_id, task_id)

    @classmethod
    async def update_task_status(cls, project_id: str, stage_id: str, task_id: str,
                                 task_update: TaskStatusUpdate) -> TaskResponse | None:
        update_data = task_update.model_dump()

        updated_id = await cls._update_with_query(
            {
                "_id": ObjectId(project_id),
                f"stages.{stage_id}.tasks.{task_id}": {"$exists": True}
            },
            {
                "$set": {
                    f"stages.{stage_id}.tasks.{task_id}.status": update_data["status"],
                    f"stages.{stage_id}.tasks.{task_id}.updated_at": get_date_now(),
                }
            }
        )

        if updated_id is None:
            return None

        return await cls.get_task_by_id(project_id, stage_id, task_id)

    @classmethod
    async def get_tasks_by_stage_id(cls, project_id: str, stage_id: str, task_name: str = "", project_name: str = "",
                                    task_status: TaskStatus = TaskStatus.none_status,
                                    start_date: datetime = None, end_date: datetime = None) -> list[TaskResponse] | \
                                                                                               list[None]:
        project = await cls.collection.find_one(
            {
                "_id": ObjectId(project_id),
                f"stages.{stage_id}.tasks": {"$exists": True}
            }
        )

        if not project or "stages" not in project or stage_id not in project["stages"]:
            return []

        tasks = []

        for task_id, task in project["stages"][stage_id].get("tasks", {}).items():

            if task_name:
                name_match = re.search(task_name, task["name"], re.IGNORECASE)
                print(f'name match is: {name_match}')
            else:
                name_match = True

            if task_status:
                status_match = task_status == task["status"]
                print(f'status match is: {status_match}')
            else:
                status_match = True

            if start_date:
                start_date_match = start_date <= task["start_date"]
            else:
                start_date_match = True

            if end_date:
                end_date_match = end_date >= task["end_date"]
            else:
                end_date_match = True

            if status_match and name_match and start_date_match and end_date_match:
                tasks.append(TaskResponse(
                    id=task_id,
                    **task
                ))
        return tasks

    @classmethod
    async def get_all_tasks_by_user(cls, user_id: str, task_name: str = "", project_name: str = "",
                                    task_status: TaskStatus = TaskStatus.none_status,
                                    start_date: datetime = None, end_date: datetime = None) -> list[
                                                                                                   ProjectTaskResponse] | \
                                                                                               list[None]:
        cursor = cls.collection.find(
            {
                "stages": {
                    "$exists": True
                }
            }
        )

        search_params = {}

        if task_name:
            search_params["name"] = task_name
        if project_name:
            search_params["project_name"] = project_name
        if task_status:
            search_params["status"] = task_status
        if start_date is not None:
            search_params["start_date"] = start_date
        if end_date is not None:
            search_params["end_date"] = end_date

        tasks = []
        async for project in cursor:

            if "project_name" in search_params:
                project_match = re.search(search_params["project_name"], project["name"], re.IGNORECASE)
                print(f'project match is: {project_match}')
            else:
                project_match = True

            if project_match is None:
                continue

            for stage_id, stage in project.get("stages", {}).items():
                for task_id, task in stage.get("tasks", {}).items():
                    for worker_id, worker in task.get("workers", {}).items():
                        if worker_id == user_id:

                            if "name" in search_params:
                                name_match = re.search(search_params["name"], task["name"], re.IGNORECASE)
                                print(f'name match is: {name_match}')
                            else:
                                name_match = True

                            if "status" in search_params:
                                status_match = search_params["status"] == task["status"]
                                print(f'status match is: {status_match}')
                            else:
                                status_match = True

                            if "start_date" in search_params:
                                start_date_match = search_params["start_date"] <= task["start_date"]
                            else:
                                start_date_match = True

                            if "end_date" in search_params:
                                end_date_match = search_params["end_date"] >= task["end_date"]
                            else:
                                end_date_match = True

                            if status_match and name_match and start_date_match and end_date_match:
                                tasks.append(ProjectTaskResponse(
                                    id=task_id,
                                    project_id=str(project["_id"]),
                                    project_name=project["name"],
                                    stage_id=str(stage_id),
                                    **task
                                ))

        print(f'Finded tasks: {len(tasks)}')
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
