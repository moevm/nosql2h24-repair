from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, Field

from schemas.user import Worker
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

    def add_worker(self, worker: Worker):
        self.workers[generate_id()] = worker
        class Config:
            from_attributes = True


class TaskResponse(Task):
    id: str
    

class TaskUpdate(BaseModel):
    description: str
    status: TaskStatus = TaskStatus.none_status
    start_date: Optional[datetime] = Field(None)
    end_date: Optional[datetime] = Field(None)

