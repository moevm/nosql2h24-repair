from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, Field

from schemas.user import Worker
from schemas.utils import generate_id


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
    created_at: Optional[datetime] = Field(datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(datetime.now(timezone.utc))

    def add_worker(self, worker: Worker):
        self.workers[generate_id()] = worker
        class Config:
            from_attributes = True


class TaskResponse(Task):
    id: str

