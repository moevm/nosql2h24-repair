from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, Field, model_validator

from schemas.task import Task
from schemas.user import Contact
from schemas.utils import generate_id, get_date_now


class Stage(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    tasks: Dict[str, Task] = {}
    created_at: Optional[datetime] = Field(get_date_now())
    updated_at: Optional[datetime] = Field(get_date_now())

    def add_task(self, task: Task):
        self.tasks[generate_id()] = task

    class Config:
        from_attributes = True


class StageResponse(Stage):
    id: str


class Risk(BaseModel):
    name: str
    description: str
    created_at: Optional[datetime] = Field(get_date_now())
    updated_at: Optional[datetime] = Field(get_date_now())

    class Config:
        from_attributes = True


class RiskResponse(Risk):
    id: str


class Procurement(BaseModel):
    item_name: str
    quantity: int
    price: float
    inStock: Optional[bool] = Field(False)
    units: Optional[str] = Field(None)
    delivery_date: Optional[datetime] = Field(None)
    created_by: Optional[Contact] = Field(None)
    created_at: Optional[datetime] = Field(get_date_now())
    updated_at: Optional[datetime] = Field(get_date_now())


class ProcurementResponse(Procurement):
    id: str
    cost: Optional[float] = None

    @model_validator(mode='after')
    def calculate_cost(self):
        self.cost = self.quantity * self.price
        return self


class ProjectStatus(str, Enum):
    in_progress = "В процессе"
    done = "Готово"
    lateness = "Опоздание"
    none_status = "Нет статуса"


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = Field(None)
    start_date: Optional[datetime] = Field(None)
    end_date: Optional[datetime] = Field(None)
    status: ProjectStatus = Field(ProjectStatus.none_status)
    created_at: Optional[datetime] = Field(get_date_now())
    updated_at: Optional[datetime] = Field(get_date_now())
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


class ProjectResponse(ProjectCreate):
    id: str
