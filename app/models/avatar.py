from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Position coordinates with validation constraints
class AvatarPosition(BaseModel):
    """Represents the X,Y coordinates of an avatar"""
    x: float = Field(..., ge=0, le=1000)  # Constrained to reasonable screen space
    y: float = Field(..., ge=0, le=1000)

# Extended appearance properties for customization
class AvatarAppearance(BaseModel):
    """Defines visual properties of an avatar"""
    color: str = Field(default="blue", max_length=20)
    size: float = Field(default=50.0, gt=10, lt=200)
    shape: str = Field(default="circle", max_length=20)
    glow_effect: Optional[bool] = None  # For special effects
    particle_trail: Optional[bool] = None  # For motion trails

# Combined schema for updating avatar position AND appearance
class AvatarUpdate(AvatarAppearance):
    """Schema for updating avatar with extended appearance options"""
    position: Optional[AvatarPosition] = None  # Can update either position OR appearance

# Complete avatar data including position
class AvatarResponse(AvatarAppearance):
    """Schema for returning avatar with extended appearance data"""
    user_id: int
    position: AvatarPosition