import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, Field

from schemas.task import Task
from schemas.user import Contact
from schemas.utils import generate_id


class Stage(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    tasks: Dict[str, Task] = {}
    created_at: Optional[datetime] = Field(datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(datetime.now(timezone.utc))

    def add_task(self, task: Task):
        self.tasks[generate_id()] = task

    class Config:
        from_attributes = True



class Risk(BaseModel):
    name: str
    description: str
    created_at: Optional[datetime] = Field(datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(datetime.now(timezone.utc))

    class Config:
        from_attributes = True


class Procurement(BaseModel):
    item_name: str
    quantity: int
    price: float
    delivery_date: Optional[datetime] = Field(None)
    created_by: Optional[str] = Field(None)
    created_at: Optional[datetime] = Field(datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(datetime.now(timezone.utc))


class ProjectStatus(str, Enum):
    in_progress = "В процессе"
    done = "Готово"
    lateness = "Опоздание"


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = Field(None)
    start_date: Optional[datetime] = Field(None)
    end_date: Optional[datetime] = Field(None)
    status: ProjectStatus
    created_at: Optional[datetime] = Field(datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(datetime.now(timezone.utc))
    contacts: Dict[str, Contact] = {}
    stages: Dict[str, Stage] = {}
    procurements: Dict[str, Procurement] = {}
    risks: Dict[str, Risk] = {}

    def add_contact(self, contact_id: str, contact: Contact):
        self.contacts[contact_id] = contact

    def add_stage(self, stage: Stage):
        self.stages[generate_id()] = stage

    def add_procurement(self, procurement: Procurement):
        self.procurements[generate_id()] = procurement

    def add_risk(self, risk: Risk):
        self.risks[generate_id()] = risk

    class Config:
        from_attributes = True


class Project(ProjectCreate):
    id: str
