from datetime import datetime, timezone

from bson import ObjectId
from dns.opcode import STATUS

from database import db
from schemas.messager import Participant, LastMessage, Chat, Message, CreateChatResponse, ChatResponse, CreateMessage, \
    StatusMsg
from schemas.user import UserDao


async def create_chat(user_sender: UserDao, user_receiver: UserDao, content: str) -> CreateChatResponse | None:
    chat_collection = db.get_collection('chat')
    message_collection = db.get_collection('message')

    participant_sender = Participant(
        name=f"{user_sender.lastname} {user_sender.name} {user_sender.middlename}",
    )
    participant_receiver = Participant(
        name=f"{user_receiver.lastname} {user_receiver.name} {user_receiver.middlename}",
    )

    last_message = LastMessage(
        content=content,
        sender=user_sender.id,
    )

    new_chat = Chat(
        lastMessage=last_message,
    )
    new_chat.add_participant(user_sender.id, participant_sender)
    new_chat.add_participant(user_receiver.id, participant_receiver)

    result_chat = await chat_collection.insert_one(new_chat.model_dump())

    if not result_chat.acknowledged:
        return None

    message = Message(
        chatId=str(result_chat.inserted_id),
        receiver=user_receiver.id,
        **last_message.model_dump()
    )

    result_message = await message_collection.insert_one(message.model_dump())

    if not result_message.acknowledged:
        return None

    return CreateChatResponse(
        chat_id=str(result_chat.inserted_id),
        message_id=str(result_message.inserted_id),
    )


async def get_chats_by_user_id(user_id: str) -> list[ChatResponse]:
    chat_collection = db.get_collection('chat')
    cursor = chat_collection.find({"participants." + user_id: {"$exists": True}})
    chats = await cursor.to_list(length=None)
    chat_list = [
        ChatResponse(id=str(chat["_id"]), **chat) for chat in chats
    ]

    return chat_list


async def get_chat_by_id(chat_id: str, user_id: str) -> ChatResponse:
    chat_collection = db.get_collection('chat')
    chat = await chat_collection.find_one({
        '_id': ObjectId(chat_id),
        "participants." + user_id: {"$exists": True}
        })
    if chat is None:
        return None
    return ChatResponse(**chat)


async def add_message_to_chat(user_id: str, message_data: CreateMessage) -> str | None:
    chat_collection = db.get_collection('chat')

    chat = await chat_collection.find_one(
        {
            "_id": ObjectId(message_data.chatId),
            "$and": [
                {"participants." + user_id: {"$exists": True}},
                {"participants." + message_data.receiver: {"$exists": True}},
            ]
        },
    )
    
    if chat is None:
        return None

    last_message = LastMessage(
        content=message_data.content,
        sender=user_id,
        status=StatusMsg.unread
    )

    result = await chat_collection.find_one_and_update(
        {"_id": ObjectId(message_data.chatId)},
        {
            "$set": {
                "lastMessage": last_message.model_dump(),
                "updated_at": datetime.now(timezone.utc)
            }
        },
        return_document=True
    )

    if result is None:
        return None

    return str(result["_id"])


async def create_message(user_id: str, message_data: CreateMessage):
    message_collection = db.get_collection('message')

    message = Message(
        chatId=message_data.chatId,
        receiver=message_data.receiver,
        sender=user_id,
        content=message_data.content,
        status=StatusMsg.unread,
        timestamp=datetime.now(timezone.utc)
    )

    insert_result = await message_collection.insert_one(message.model_dump())

    if not insert_result.acknowledged:
        return None

    return str(insert_result.inserted_id)
