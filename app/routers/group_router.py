# app/routers/group_router.py
from fastapi import APIRouter, Depends
from app.models.group import GroupCreate
from app.services.group_service import GroupService

group_router = APIRouter()

@group_router.post("/")
async def create_group(
    group: GroupCreate,
    group_service: GroupService = Depends(GroupService)
):
    return await group_service.create_group(group)