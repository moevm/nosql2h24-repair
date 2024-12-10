from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import db, create_indexation, is_database_empty, load_default_data
from routers import (auth, user, project, task, message, risk,
                     stage, contact, procurement, stat, data)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.database = db
    if await is_database_empty():
        load_default_data()
    await create_indexation()
    yield


app = FastAPI(lifespan=lifespan)

allowed_origins = [
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:8080",
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
app.include_router(risk.router, tags=['Risk'], prefix="/api/projects")
app.include_router(stage.router, tags=['Stage'], prefix="/api/projects")
app.include_router(contact.router, tags=['Contact'], prefix="/api/projects")
app.include_router(procurement.router, tags=['Procurement'], prefix="/api/projects")
app.include_router(task.router, tags=['Task'], prefix="/api/tasks")

app.include_router(message.router, tags=['Message'], prefix="/api/message")
app.include_router(stat.router, tags=['Stats'], prefix="/api/statistic")
app.include_router(data.router, tags=['Data'], prefix="/api/data")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
