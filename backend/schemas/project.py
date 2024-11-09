import uuid
from datetime import datetime, timezone
from typing import Dict

from pydantic import BaseModel

from schemas.task import Task
from schemas.user import Contact
from schemas.utils import generate_id


class StageCreate(BaseModel):
    name: str
    start_date: str
    end_date: str

    class Config:
        from_attributes = True


class Stage(StageCreate):
    id: str
    start_date: datetime
    end_date: datetime
    tasks: Dict[str, Task] = {}
    created_at: datetime | None = datetime.now(timezone.utc)
    updated_at: datetime | None = datetime.now(timezone.utc)

    def add_task(self, task: Task):
        self.tasks[generate_id()] = task


class RiskCreate(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True


class Risk(RiskCreate):
    id: str
    created_at: datetime | None = datetime.now(timezone.utc)
    updated_at: datetime | None = datetime.now(timezone.utc)


class ProcurementCreate(BaseModel):
    item_name: str
    quantity: int
    price: float
    delivery_date: str
    created_by: str


class Procurement(ProcurementCreate):
    id: str
    delivery_date: datetime
    created_at: datetime | None = datetime.now(timezone.utc)
    updated_at: datetime | None = datetime.now(timezone.utc)


class ProjectCreate(BaseModel):
    name: str
    description: str | None
    start_date: str | None = None
    end_date: str | None = None
    status: str | None

    class Config:
        from_attributes = True


class Project(ProjectCreate):
    created_at: datetime | None = datetime.now(timezone.utc)
    updated_at: datetime | None = datetime.now(timezone.utc)
    contacts: Dict[str, Contact] = {}
    stages: Dict[str, Stage] = {}
    procurements: Dict[str, Procurement] = {}
    risks: Dict[str, Risk] = {}

    def add_contact(self, contact: Contact):
        self.contacts[generate_id()] = contact

    def add_stage(self, stage: Stage):
        self.stages[generate_id()] = stage

    def add_procurement(self, procurement: Procurement):
        self.procurements[generate_id()] = procurement

    def add_risk(self, risk: Risk):
        self.risks[generate_id()] = risk

class ProjectResponse(Project):
    id: str