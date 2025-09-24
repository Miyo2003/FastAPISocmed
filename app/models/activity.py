from typing import Optional
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class ActivityType(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    PROFILE_UPDATE = "profile_update"
    AVATAR_MOVED = "avatar_moved"

class ActivityLog(BaseModel):
    """Schema for activity logs"""
    user_id: int
    type: ActivityType
    timestamp: datetime
    details: Optional[dict] = None  # Additional context