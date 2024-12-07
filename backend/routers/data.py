from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from database import db

router = APIRouter()

def convert_to_serializable(data):
    if isinstance(data, list):
        return [convert_to_serializable(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_to_serializable(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, datetime):
        return data.isoformat()
    return data

@router.get("/export/json")
async def export_json():
    """Экспорт всей базы данных в формате JSON."""
    collections = await db.list_collection_names()
    if not collections:
        raise HTTPException(
            status_code=404, 
            detail="Коллекции не найдены, база данных пуста!"
        )

    # Сбор данных из всех коллекций
    data = {}
    for collection_name in collections:
        collection = db[collection_name]
        documents = await collection.find().to_list(length=None)
        data[collection_name] = convert_to_serializable(documents)

    # Ответ в формате JSON
    return JSONResponse(content=data)