
import uvicorn
from fastapi import FastAPI

from app.database import db

app = FastAPI()
app.database = db


@app.get("/api/healthchecker")
async def ping() -> dict:
    return {"Ping": "Pong!"}



if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True)