import datetime
from pydantic import BaseModel

class FriendRequest(BaseModel):
    """Schema for friend requests"""
    requester_id: int
    requested_id: int

class Friendship(BaseModel):
    """Schema for friendship data"""
    user_id: int
    friend_id: int
    since: datetime