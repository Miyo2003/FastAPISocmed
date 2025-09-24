from fastapi import FastAPI, Request
from app.controllers.main_controller import index, websocket_endpoint
from app.routers.activity_router import activity_router
from app.routers.auth_router import auth_router
from app.routers.avatar_router import avatar_router
from app.routers.chat_router import chat_router
from app.routers.group_router import group_router
from app.routers.notification_router import notification_router

app = FastAPI()

# Root route
app.get("/")(index)

# WebSocket route
app.websocket("/ws/{user_id}")(websocket_endpoint)

# Include routers
app.include_router(auth_router)
app.include_router(avatar_router)
app.include_router(chat_router)
app.include_router(group_router)
app.include_router(notification_router)
app.include_router(activity_router)