# app/services/__init__.py
"""Service package initialization"""

from .auth_service import AuthService
from .avatar_service import AvatarService
from .chat_service import ChatService
from .group_service import GroupService
from .notification_service import NotificationService
from .activity_service import ActivityService
from .user_service import UserService  # Add this line

__all__ = [
    "AuthService",
    "AvatarService",
    "ChatService",
    "GroupService",
    "NotificationService",
    "ActivityService",
    "UserService"  # Add this line
]