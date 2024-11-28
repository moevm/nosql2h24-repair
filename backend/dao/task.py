from bson import ObjectId

from database import db
from schemas.task import Task, TaskResponse, TaskUpdate
from schemas.user import Worker
from schemas.utils import generate_id, get_date_now


async def add_task(project_id: str, stage_id, task_create: Task) -> TaskResponse | None:
    project_collection = db.get_collection('project')
    task_id = generate_id()
    result = await project_collection.update_one(
        {"_id": ObjectId(project_id), f"stages.{stage_id}": {"$exists": True}},
        {
            "$set": {f"stages.{stage_id}.tasks.{task_id}": task_create.model_dump()}
        }
    )
    if result.modified_count > 0:
        return TaskResponse(id=task_id, **task_create.model_dump())
    return None


async def get_task_by_id(project_id: str, stage_id: str, task_id: str) -> TaskResponse | None:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one(
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


async def update_task_by_id(project_id: str, stage_id: str, task_id: str, task_update: TaskUpdate) -> TaskResponse | None:
    project_collection = db.get_collection('project')

    update_data = task_update.model_dump()
    update_data["updated_at"] = get_date_now()

    result = await project_collection.update_one(
        {
            "_id": ObjectId(project_id),
            f"stages.{stage_id}.tasks.{task_id}": {"$exists": True}
        },
        {
            "$set": {
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

    return await get_task_by_id(project_id, stage_id, task_id)


async def get_tasks_by_stage_id(project_id: str, stage_id: str) -> list[TaskResponse] | list[None]:
    project_collection = db.get_collection('project')
    project = await project_collection.find_one(
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


async def get_all_tasks_by_user(user_id: str) -> list[Task] | list[None]:
    project_collection = db.get_collection('project')
    cursor = project_collection.find(
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
                    if worker.get("user_id") == ObjectId(user_id):
                        tasks.append(TaskResponse(id=task_id, **task))

    return tasks


async def add_worker_to_task(project_id: str, stage_id: str, task_id: str, worker_id: str,
                             worker: Worker) -> TaskResponse | dict[str: str]:
    project_collection = db.get_collection('project')

    update_result = await project_collection.update_one(
        {
            "_id": ObjectId(project_id),
            f"stages.{stage_id}.tasks.{task_id}": {"$exists": True}
        },
        {
            "$set": {
                f"stages.{stage_id}.tasks.{task_id}.workers.{worker_id}": {
                    "user_id": ObjectId(worker_id),
                    "name": worker.name,
                    "role": worker.role,
                }
            }
        }
    )

    if update_result.modified_count == 0:
        return None

    return await get_task_by_id(project_id, stage_id, task_id)
