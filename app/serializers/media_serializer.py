from pydantic import TypeAdapter
from app.models.media import MediaUpload, MediaResponse

class MediaSerializer:
    @staticmethod
    def serialize(media_record) -> MediaResponse:
        """Convert Neo4j record to Pydantic model"""
        return TypeAdapter(MediaResponse).validate_python({
            "url": media_record["url"],
            "width": media_record["width"],
            "height": media_record["height"],
            "size": media_record["size"]
        })

    @staticmethod
    def deserialize(media_upload: MediaUpload) -> dict:
        """Convert Pydantic model to database-friendly dict"""
        return {
            "file": media_upload.file,
            "filename": media_upload.filename,
            "content_type": media_upload.content_type,
            "size": media_upload.size
        }