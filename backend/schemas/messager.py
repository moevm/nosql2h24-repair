from datetime import datetime, timezone
from enum import Enum
from typing import Dict

from bson import ObjectId
from pydantic import BaseModel, Field


class Participant(BaseModel):
    name: str
    lastSeen: datetime | None = None


class StatusMsg(str, Enum):
    unread = "unread"
    read = "read"


class LastMessage(BaseModel):
    content: str
    sender: str
    status: StatusMsg
    timestamp: datetime | None = datetime.now(timezone.utc)


class ChatCreateSchema(BaseModel):
    participants: Dict[ObjectId, Participant]
    lastMessage: LastMessage

    class Config:
        from_attributes = True


class Chat(ChatCreateSchema):
    id: str
    createdAt: datetime | None = datetime.now(timezone.utc)
    updatedAt: datetime | None = None
