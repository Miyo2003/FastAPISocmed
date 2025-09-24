from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserProfile(BaseModel):
    """Detailed user profile information"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None  # ISO format date string

class UserCreate(UserProfile):
    """Schema for creating a new user with profile"""
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str

class UserResponse(UserProfile):
    """Schema for returning user data"""
    id: str
    username: str
    email: EmailStr
    online: bool