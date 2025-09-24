# app/controllers/activity_controller.py
from fastapi import APIRouter, Depends
from app.models.activity import ActivityLog
from app.services.activity_service import ActivityService

router = APIRouter()

@router.post("/")
async def log_activity(activity: ActivityLog, activity_service: ActivityService = Depends(ActivityService)):
    return await activity_service.log_activity(activity)

@router.get("/")
async def get_recent_activities(user_id: int, activity_service: ActivityService = Depends(ActivityService)):
    return await activity_service.get_recent_activities(user_id)