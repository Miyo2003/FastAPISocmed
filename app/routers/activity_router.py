# app/routers/activity_router.py
from fastapi import APIRouter, Depends, Query
from app.models.activity import ActivityLog
from app.services.activity_service import ActivityService

activity_router = APIRouter(prefix="/activities", tags=["Activities"])

@activity_router.post("/")
async def log_activity(
    activity: ActivityLog,
    activity_service: ActivityService = Depends(ActivityService)
):
    return await activity_service.log_activity(activity)

@activity_router.get("/")
async def get_recent_activities(
    user_id: int = Query(..., description="ID of the user to fetch activities for"),
    activity_service: ActivityService = Depends(ActivityService)
):
    return await activity_service.get_recent_activities(user_id)