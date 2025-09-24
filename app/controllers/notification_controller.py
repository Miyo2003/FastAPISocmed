from fastapi import APIRouter, Depends

from app.models.notification import NotificationCreate
from ..services.notification_service import NotificationService

router = APIRouter()

@router.post("/notifications")
async def send_notification(notification: NotificationCreate, notification_service: NotificationService = Depends(NotificationService)):
    return await notification_service.create_notification(notification)