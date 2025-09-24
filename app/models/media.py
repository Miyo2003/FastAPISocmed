from pydantic import BaseModel, HttpUrl

class MediaUpload(BaseModel):
    """Schema for uploading media files"""
    file: bytes
    filename: str
    content_type: str

class MediaResponse(BaseModel):
    """Schema for returning media URLs"""
    url: HttpUrl
    width: int
    height: int
    size: int  # in bytes