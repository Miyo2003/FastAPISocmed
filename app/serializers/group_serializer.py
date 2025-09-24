from pydantic import TypeAdapter
from app.models.group import GroupCreate, GroupResponse

class GroupSerializer:
    @staticmethod
    def serialize(group_record) -> GroupResponse:
        """Convert Neo4j record to Pydantic model"""
        return TypeAdapter(GroupResponse).validate_python({
            "id": group_record.id,
            "name": group_record["name"],
            "created_at": group_record["created_at"],
            "admin_id": group_record["admin_id"],
            "member_ids": group_record["member_ids"]
        })

    @staticmethod
    def deserialize(group_create: GroupCreate) -> dict:
        """Convert Pydantic model to database-friendly dict"""
        return {
            "name": group_create.name,
            "member_ids": group_create.member_ids
        }