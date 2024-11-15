import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from database import db
from routers import auth, user, project, task, message

app = FastAPI()
app.database = db

allowed_origins = [
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "OPTIONS", "PATCH", "DELETE"],
    allow_headers=["*"]
)

app.include_router(auth.router, tags=['Auth'], prefix="/api/auth")
app.include_router(user.router, tags=['User'], prefix="/api/user")
app.include_router(project.router, tags=['Project'], prefix="/api/projects")
app.include_router(task.router, tags=['Task'], prefix="/api/tasks")
app.include_router(message.router, tags=['Message'], prefix="/api/message")



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
