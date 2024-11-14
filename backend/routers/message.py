from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from dao.messager import create_chat, get_chats_by_user_id, get_chat_by_id, add_message_to_chat, create_message
from dao.user import find_user_by_id
from schemas.messager import CreateChatResponse, FirstMessage, ChatResponse, CreateMessage
from schemas.user import UserDao
from utils.token import get_current_user

router = APIRouter()


@router.post("/create_chat", response_model=CreateChatResponse)
async def new_chat(first_message: FirstMessage, user: UserDao = Depends(get_current_user)):
    user_receiver = await find_user_by_id(first_message.id_receiver)
    if user_receiver is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Получатель не найден"
        )

    chat = await create_chat(user, user_receiver, first_message.content)
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка в создании чата",
        )
    return chat


@router.get("/get_chats", response_model=List[ChatResponse])
async def get_chats(user: UserDao = Depends(get_current_user)):
    chats = await get_chats_by_user_id(user.id)
    return chats


@router.get("/get_chat/{chat_id}", response_model=ChatResponse)
async def get_chat(chat_id: str, user: UserDao = Depends(get_current_user)):
    chat = await get_chat_by_id(chat_id)
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Чата не существует"
        )


@router.post("/create_message", response_model=CreateChatResponse)
async def new_message(message_data: CreateMessage, user: UserDao = Depends(get_current_user)):
    chat_id = await add_message_to_chat(user.id, message_data)
    if chat_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Чата не существует"
        )

    message_id = await create_message(user.id, message_data)
    if message_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка при добавлении сообщения"
        )

    return CreateChatResponse(chat_id=chat_id, message_id=message_id)
