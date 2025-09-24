from fastapi import APIRouter, Depends

from app.models.chat import MessageCreate
from ..services.chat_service import ChatService

router = APIRouter()

@router.post("/messages")
async def send_message(message: MessageCreate, chat_service: ChatService = Depends(ChatService)):
    return await chat_service.send_message(message)