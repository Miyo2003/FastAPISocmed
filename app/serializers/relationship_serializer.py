from pydantic import TypeAdapter
from app.models.relationship import FriendRequest, Friendship

class RelationshipSerializer:
    @staticmethod
    def serialize(relationship_record) -> Friendship:
        """Convert Neo4j record to Pydantic model"""
        return TypeAdapter(Friendship).validate_python({
            "user_id": relationship_record["user_id"],
            "friend_id": relationship_record["friend_id"],
            "since": relationship_record["since"]
        })

    @staticmethod
    def deserialize(relationship_create: FriendRequest) -> dict:
        """Convert Pydantic model to database-friendly dict"""
        return {
            "requester_id": relationship_create.requester_id,
            "requested_id": relationship_create.requested_id
        }