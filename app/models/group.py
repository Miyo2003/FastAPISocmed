from datetime import datetime
from pydantic import BaseModel
from typing import List

class GroupCreate(BaseModel):
    """Schema for creating a new group chat"""
    name: str
    member_ids: List[int]  # User IDs to add to the group

class GroupResponse(GroupCreate):
    """Schema for returning group data"""
    id: int
    created_at: datetime
    admin_id: int  # User who created the group