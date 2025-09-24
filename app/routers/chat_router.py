# app/routers/chat_router.py
from fastapi import APIRouter, Depends
from app.models.chat import MessageCreate
from app.services.chat_service import ChatService

chat_router = APIRouter()

@chat_router.post("/send-message")
async def send_message(
    message: MessageCreate,
    chat_service: ChatService = Depends(ChatService)
):
    return await chat_service.send_message(message)