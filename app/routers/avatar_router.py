# app/routers/avatar_router.py
from fastapi import APIRouter, Depends
from app.models.avatar import AvatarUpdate
from app.services.avatar_service import AvatarService

avatar_router = APIRouter()

@avatar_router.put("/{user_id}/position")
async def update_avatar_position(
    user_id: int,
    position: AvatarUpdate,
    avatar_service: AvatarService = Depends(AvatarService)
):
    return await avatar_service.update_avatar_position(user_id, position)

@avatar_router.put("/{user_id}/appearance")
async def change_avatar_appearance(
    user_id: int,
    appearance: dict,
    avatar_service: AvatarService = Depends(AvatarService)
):
    return await avatar_service.change_avatar_appearance(user_id, appearance)

@avatar_router.get("/nearby-avatars/{user_id}")
async def get_nearby_avatars(
    user_id: int,
    radius: float = 100.0,
    avatar_service: AvatarService = Depends(AvatarService)
):
    return await avatar_service.get_nearby_avatars(user_id, radius)

@avatar_router.post("/{user_id}/animations/{animation_type}")
async def trigger_animation(
    user_id: int,
    animation_type: str,
    avatar_service: AvatarService = Depends(AvatarService)
):
    return await avatar_service.trigger_animation(user_id, animation_type)