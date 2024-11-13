from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, Field

class FirstMessage(BaseModel):
    id_receiver: str = Field(...)
    content: str = Field(...)


class Participant(BaseModel):
    name: str
    lastSeen: datetime = Field(datetime.now(timezone.utc))


class StatusMsg(str, Enum):
    unread = "Не прочитано"
    read = "Прочитано"


class LastMessage(BaseModel):
    content: str
    sender: str
    status: StatusMsg = StatusMsg.unread
    timestamp: Optional[datetime] = Field(datetime.now(timezone.utc))


class Chat(BaseModel):
    participants: Dict[str, Participant] = {}
    lastMessage: LastMessage
    created_at: Optional[datetime] = Field(datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(datetime.now(timezone.utc))

    class Config:
        from_attributes = True

    def add_participant(self, id: str, participant: Participant):
        self.participants[id] = participant


class ChatResponse(Chat):
    id: str
    
class CreateChatResponse(BaseModel):
    chat_id: str
    message_id: str
    
class Message(LastMessage):
    chatId: str
    receiver: str
    
class CreateMessage(BaseModel):
    chatId: str
    receiver: str
    content: str
