# app/controllers/user_controller.py
from fastapi import APIRouter, Depends
from ..services.user_service import UserService

router = APIRouter()

@router.get("/profile/{user_id}")
async def get_profile(user_id: int, user_service: UserService = Depends(UserService)):
    return await user_service.get_user_by_id(user_id)

@router.put("/profile/{user_id}")
async def update_profile(user_id: int, profile_data: dict, user_service: UserService = Depends(UserService)):
    return await user_service.update_profile(user_id, profile_data)