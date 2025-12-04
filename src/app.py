import os
from typing import Optional
from dotenv import load_dotenv
from security import get_api_key
load_dotenv()
print(os.getenv("SERVER_API_KEY"))
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
app.include_router(chat.router)
#, dependencies=[Depends(get_api_key)])

@app.get("/api/health")
async def read_root():
    return {"message": "Hello, FastAPI!\n"}

@app.get("/chat_start")
async def start_chat():
    return {"message": "Chat started"}


