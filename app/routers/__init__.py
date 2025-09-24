# app/routers/__init__.py
from .activity_router import activity_router
from .avatar_router import avatar_router
from .chat_router import chat_router
from .group_router import group_router
from .notification_router import notification_router

__all__ = [
    "activity_router",
    "avatar_router",
    "chat_router",
    "group_router",
    "notification_router"
]