# app/routers/notification_router.py
from fastapi import APIRouter, Depends
from app.models.notification import NotificationCreate
from app.services.notification_service import NotificationService

notification_router = APIRouter()

@notification_router.post("/")
async def send_notification(
    notification: NotificationCreate,
    notification_service: NotificationService = Depends(NotificationService)
):
    return await notification_service.create_notification(notification)