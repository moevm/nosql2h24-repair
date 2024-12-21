import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str

    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str


    DEFAULT_DATA_FILE: str
    
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        extra = "allow"
        
settings = Settings()