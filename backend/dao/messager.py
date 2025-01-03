from bson import ObjectId

from database import db
from schemas.messager import Participant, LastMessage, Chat, Message, ChatResponse, CreateMessage, \
    StatusMsg, MessageResponse
from schemas.user import User
from schemas.utils import get_date_now


async def create_chat(user_sender: User, user_receiver: User, content: str) -> ChatResponse | None:
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

    return ChatResponse(
        id=str(result_chat.inserted_id),
        **new_chat.model_dump()
    )


async def get_chats_by_user_id(user_id: str) -> list[ChatResponse]:
    chat_collection = db.get_collection('chat')
    cursor = chat_collection.find({"participants." + user_id: {"$exists": True}})
    chats = await cursor.to_list(length=None)
    chat_list = [
        ChatResponse(id=str(chat["_id"]), **chat) for chat in chats
    ]

    return chat_list


async def get_chat_by_id(chat_id: str, user_id: str) -> ChatResponse | None:
    chat_collection = db.get_collection('chat')
    chat = await chat_collection.find_one({
        '_id': ObjectId(chat_id),
        "participants." + user_id: {"$exists": True}
    })
    if chat is None:
        return None
    return ChatResponse(id=str(chat["_id"]), **chat)


async def get_chat_messages(chat_id: str, user_id: str, limit: int = 10) -> list[Message] | list[None] | None:
    chat = await get_chat_by_id(chat_id, user_id)
    if chat is None:
        return None
    message_collection = db.get_collection('message')

    try:
        cursor = message_collection.find(
            {"chatId": chat_id}
        ).sort("timestamp", -1).limit(limit)

        messages = await cursor.to_list(length=limit)
        messages.reverse()

        return [
            Message(
                id=str(msg["_id"]),
                **msg
            )
            for msg in messages
        ]
    except Exception as e:
        print(f"Ошибка при получении сообщений: {e}")
        return None


async def get_chat_by_double_id(first_id: str, second_id: str) -> ChatResponse | None:
    chat_collection = db.get_collection('chat')
    chat = await chat_collection.find_one({
        "participants." + first_id: {"$exists": True},
        "participants." + second_id: {"$exists": True}
    })
    if chat is None:
        return None
    return ChatResponse(id=str(chat["_id"]), **chat)


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
                "updated_at": get_date_now()
            }
        },
        return_document=True
    )

    if result is None:
        return None

    return str(result["_id"])


async def create_message(user_id: str, message_data: CreateMessage) -> MessageResponse | None:
    message_collection = db.get_collection('message')

    message = Message(
        chatId=message_data.chatId,
        receiver=message_data.receiver,
        sender=user_id,
        content=message_data.content,
        status=StatusMsg.unread,
        timestamp=get_date_now()
    )

    insert_result = await message_collection.insert_one(message.model_dump())

    if not insert_result.acknowledged:
        return None

    return MessageResponse(id=str(insert_result.inserted_id), **message.model_dump())
