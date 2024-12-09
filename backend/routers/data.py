import json
from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from database import db
from schemas.user import User
from utils.role import get_admin_role

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
async def export_json(admin: User = Depends(get_admin_role)):
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


@router.post("/import")
async def import_database(file: UploadFile):
    """
    Импортирует коллекции из JSON-файла в MongoDB с проверкой существования коллекций.

    :param file: JSON-файл с данными
    """
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files are allowed")

    try:
        # Считываем содержимое файла
        file_content = await file.read()
        data = json.loads(file_content)

        if not isinstance(data, dict):
            raise HTTPException(status_code=400, detail="JSON file must contain a dictionary of collections")

        # Получаем список существующих коллекций
        existing_collections = db.list_collection_names()

        # Проверка каждой коллекции в JSON
        for collection_name in data.keys():
            if collection_name not in existing_collections:
                raise HTTPException(
                    status_code=400,
                    detail=f"Collection '{collection_name}' does not exist in the database."
                )

        # Импорт данных
        for collection_name, documents in data.items():
            if not isinstance(documents, list):
                raise HTTPException(status_code=400, detail=f"Collection '{collection_name}' must contain a list of documents")

            # Преобразование _id в ObjectId
            for doc in documents:
                if "_id" in doc:
                    doc["_id"] = ObjectId(doc["_id"])

            # Вставка данных в коллекцию
            collection = db[collection_name]
            collection.insert_many(documents)

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")

    return {"message": "Database imported successfully"}