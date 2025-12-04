import os
from typing import Optional
from dotenv import load_dotenv
from security import get_api_key
load_dotenv()
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat, files
app = FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files.router, dependencies=[Depends(get_api_key)])
# did not use auth for chat because react EventSource does not support custom headers
app.include_router(chat.router)

@app.get("/api/health")
async def read_root():
    return {"message": "Hello, FastAPI!"}




