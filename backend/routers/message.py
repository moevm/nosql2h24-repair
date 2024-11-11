from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from dao.messager import create_chat, get_chats_by_user_id
from dao.user import find_user_by_id
from schemas.messager import CreateChatResponse, FirstMessage, ChatResponse
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

