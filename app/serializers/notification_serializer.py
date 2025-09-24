from pydantic import TypeAdapter
from app.models.notification import NotificationCreate, NotificationResponse

class NotificationSerializer:
    @staticmethod
    def serialize(notification_record) -> NotificationResponse:
        """Convert Neo4j record to Pydantic model"""
        return TypeAdapter(NotificationResponse).validate_python({
            "id": notification_record.id,
            "user_id": notification_record["user_id"],
            "type": notification_record["type"],
            "related_id": notification_record["related_id"],
            "read": notification_record["read"],
            "timestamp": notification_record["timestamp"]
        })

    @staticmethod
    def deserialize(notification_create: NotificationCreate) -> dict:
        """Convert Pydantic model to database-friendly dict"""
        return {
            "user_id": notification_create.user_id,
            "type": notification_create.type.value,
            "related_id": notification_create.related_id
        }