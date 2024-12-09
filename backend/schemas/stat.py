from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class StatType(str, Enum):
    risks = "risks"
    procurements = "procurements"


class StatSchema(BaseModel):
    project_ids: List[str] = Field(..., min_length=1)
    stat_type: StatType
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
