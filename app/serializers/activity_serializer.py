from pydantic import TypeAdapter
from app.models.activity import ActivityLog

class ActivitySerializer:
    @staticmethod
    def serialize(activity_record) -> ActivityLog:
        """Convert Neo4j record to Pydantic model"""
        return TypeAdapter(ActivityLog).validate_python({
            "user_id": activity_record["user_id"],
            "type": activity_record["type"],
            "timestamp": activity_record["timestamp"],
            "details": activity_record["details"]
        })

    @staticmethod
    def deserialize(activity_log: ActivityLog) -> dict:
        """Convert Pydantic model to database-friendly dict"""
        return {
            "user_id": activity_log.user_id,
            "type": activity_log.type.value,
            "timestamp": activity_log.timestamp,
            "details": activity_log.details
        }