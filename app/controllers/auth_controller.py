# app/controllers/auth_controller.py
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status

from app.models.chat import MessageCreate
from app.models.group import GroupCreate
from app.models.notification import NotificationCreate
from app.models.user import UserCreate, UserLogin
from ..services.auth_service import AuthService
from ..services.chat_service import ChatService
from ..services.group_service import GroupService
from ..services.notification_service import NotificationService

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, auth_service: AuthService = Depends(AuthService)):
    """Register a new user"""
    return await auth_service.create_user(user)

@router.post("/login")
async def login(credentials: UserLogin, auth_service: AuthService = Depends(AuthService)):
    """Authenticate user and return access token"""
    return await auth_service.authenticate_user(credentials.dict())

@router.post("/send-message")
async def send_message(message: MessageCreate, chat_service: ChatService = Depends(ChatService)):
    """Send a message to chat"""
    return await chat_service.send_message(message)

@router.post("/create-group")
async def create_group(group: GroupCreate, group_service: GroupService = Depends(GroupService)):
    """Create a new group chat"""
    return await group_service.create_group(group)

@router.post("/send-notification")
async def send_notification(notification: NotificationCreate, notification_service: NotificationService = Depends(NotificationService)):
    """Send a notification to user"""
    return await notification_service.create_notification(notification)