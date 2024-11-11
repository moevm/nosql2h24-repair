from dao.user import find_user_by_id
from database import db
from schemas.messager import FirstMessage, Participant, LastMessage, Chat, Message, CreateChatResponse, ChatResponse
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
    
