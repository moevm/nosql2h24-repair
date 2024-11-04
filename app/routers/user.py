from bson import ObjectId
from fastapi import APIRouter, Depends

from app import schemas
from app.database import User
from app.serializers.userSerializers import user_response_entity

router = APIRouter()
