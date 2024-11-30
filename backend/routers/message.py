import asyncio
from typing import List, Dict

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from starlette.websockets import WebSocket, WebSocketDisconnect

from dao.messager import create_chat, get_chats_by_user_id, get_chat_by_id, get_chat_by_double_id, add_message_to_chat, \
    create_message, get_chat_messages
from dao.user import UserDao
from schemas.messager import FirstMessage, ChatResponse, CreateMessage, Message, MessageResponse
from schemas.user import User
from utils.token import get_current_user

router = APIRouter()

active_connections: Dict[str, WebSocket] = {}


@router.post("/create_chat", response_model=ChatResponse)
async def new_chat(first_message: FirstMessage, user: User = Depends(get_current_user)):
    user_receiver = await UserDao.find_user_by_id(first_message.id_receiver)
    if user_receiver is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Получатель не найден"
        )

    existing_chat = await get_chat_by_double_id(user.id, user_receiver.id)
    if existing_chat:
        return existing_chat

    chat = await create_chat(user, user_receiver, first_message.content)
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка в создании чата",
        )
    return chat


@router.get("/get_chats", response_model=List[ChatResponse])
async def get_chats(user: User = Depends(get_current_user)):
    chats = await get_chats_by_user_id(user.id)
    return chats


@router.get("/get_chat/{chat_id}", response_model=ChatResponse)
async def get_chat(chat_id: str, user: User = Depends(get_current_user)):
    chat = await get_chat_by_id(chat_id, user.id)
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Чата не существует"
        )
    return chat


@router.get("/check_chat/{user_id}", response_model=ChatResponse | None)
async def get_chat(user_id: str, user: User = Depends(get_current_user)):
    if user_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Одинаковые id пользователей"
        )
    chat = await get_chat_by_double_id(user_id, user.id)
    return chat


@router.get("/get_messages/{chat_id}", response_model=list[Message])
async def get_messages(chat_id: str, limit: int = 10, user: User = Depends(get_current_user)):
    messages = await get_chat_messages(chat_id, user.id, limit)
    if messages is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Чат не найден"
        )
    return messages


@router.post("/create_message", response_model=MessageResponse)
async def new_message(message_data: CreateMessage, user: User = Depends(get_current_user)):
    chat_id = await add_message_to_chat(user.id, message_data)
    if chat_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Чата не существует"
        )

    message = await create_message(user.id, message_data)
    if message is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка при добавлении сообщения"
        )
    
    await notify_user(user.id, message_data.model_dump())
    await notify_user(message_data.receiver, message_data.model_dump())

    return message


async def notify_user(user_id: str, message: dict):
    if user_id in active_connections:
        websocket = active_connections[user_id]
        await websocket.send_json(message)


@router.websocket("/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    active_connections[user_id] = websocket

    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        active_connections.pop(user_id)
