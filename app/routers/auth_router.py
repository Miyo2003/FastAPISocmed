# app/routers/auth_router.py
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from app.models.chat import MessageCreate
from app.models.group import GroupCreate
from app.models.notification import NotificationCreate
from app.models.user import UserCreate
from app.services.chat_service import ChatService
from app.services.group_service import GroupService
from app.services.notification_service import NotificationService
from app.services.auth_service import AuthService

auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@auth_router.post("/register")
async def register(
    user: UserCreate,
    auth_service: AuthService = Depends(AuthService)
):
    return await auth_service.create_user(user)

@auth_router.post("/login")
async def login(
    credentials: dict,
    auth_service: AuthService = Depends(AuthService)
):
    return await auth_service.authenticate_user(credentials)

@auth_router.post("/send-message")
async def send_message(
    message: MessageCreate,
    chat_service: ChatService = Depends(ChatService)
):
    return await chat_service.send_message(message)

@auth_router.post("/create-group")
async def create_group(
    group: GroupCreate,
    group_service: GroupService = Depends(GroupService)
):
    return await group_service.create_group(group)

@auth_router.post("/send-notification")
async def send_notification(
    notification: NotificationCreate,
    notification_service: NotificationService = Depends(NotificationService)
):
    return await notification_service.create_notification(notification)