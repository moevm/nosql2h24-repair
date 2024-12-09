from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, Field

from schemas.user import Worker, WorkerResponse, WorkerCreate
from schemas.utils import generate_id, get_date_now


class TaskStatus(str, Enum):
    in_progress = "В процессе"
    done = "Готово"
    lateness = "Опоздание"
    none_status = "Нет статуса"


class Task(BaseModel):
    name: str
    description: str
    status: TaskStatus = TaskStatus.none_status
    start_date: Optional[datetime] = Field(None)
    end_date: Optional[datetime] = Field(None)
    workers: Dict[str, Worker] = {}
    created_at: Optional[datetime] = Field(get_date_now())
    updated_at: Optional[datetime] = Field(get_date_now())


class TaskResponse(Task):
    id: str
    
class ProjectTaskResponse(TaskResponse):
    id: str
    project_id: str
    project_name: str
    stage_id: str
    

class TaskUpdate(BaseModel):
    name: str
    description: str
    status: TaskStatus = TaskStatus.none_status
    start_date: Optional[datetime] = Field(None)
    end_date: Optional[datetime] = Field(None)
    
class TaskStatusUpdate(BaseModel):
    status: TaskStatus

