from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum

class NotificationType(str, Enum):
    NEW_MESSAGE = "new_message"
    FRIEND_REQUEST = "friend_request"
    GROUP_INVITE = "group_invite"
    AVATAR_UPDATE = "avatar_update"

class NotificationCreate(BaseModel):
    """Schema for creating notifications"""
    user_id: int
    type: NotificationType
    related_id: Optional[int] = None  # ID of related item (message, group, etc.)

class NotificationResponse(NotificationCreate):
    """Schema for returning notifications"""
    id: int
    read: bool
    timestamp: datetime