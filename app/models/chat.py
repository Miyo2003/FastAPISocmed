from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MessageContent(BaseModel):
    """Base content structure for messages"""
    text: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None

class MessageCreate(MessageContent):
    """Schema for creating a new message"""
    sender_id: int
    recipient_ids: List[int]  # Multiple recipients for group chats
    type: str = Field(default="text")  # text, image, video, etc.

class MessageResponse(MessageContent):
    """Schema for returning message data"""
    id: int
    sender_id: int
    recipient_ids: List[int]
    type: str
    timestamp: datetime
    read_by: List[int] = []  # User IDs who have read this message