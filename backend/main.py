import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import db
from routers import auth, user

app = FastAPI()
app.database = db

origins = [
    settings.CLIENT_ORIGIN,
    "http://172.18.0.3:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=['Auth'], prefix="/api/auth")
app.include_router(user.router, tags=['User'], prefix="/api/user")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)