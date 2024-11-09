import uuid
from datetime import datetime, timezone
from typing import Dict

from pydantic import BaseModel

from schemas.user import Worker
from schemas.utils import generate_id


class TaskCreate(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: str
    status: str

    class Config:
        from_attributes = True



class Task(TaskCreate):
    id: str
    start_date: datetime
    end_date: datetime
    workers: Dict[str, Worker] = {}
    created_at: datetime | None = datetime.now(timezone.utc)
    updated_at: datetime | None = datetime.now(timezone.utc)

    def add_worker(self, worker: Worker):
        self.workers[generate_id()] = worker
