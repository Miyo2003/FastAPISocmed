from pydantic import TypeAdapter
from app.models.chat import MessageCreate, MessageResponse

class MessageSerializer:
    @staticmethod
    def serialize(message_record) -> MessageResponse:
        """Convert Neo4j record to Pydantic model"""
        return TypeAdapter(MessageResponse).validate_python({
            "id": message_record.id,
            "content": message_record["content"],
            "sender_id": message_record["sender_id"],
            "recipient_ids": message_record["recipient_ids"],
            "type": message_record["type"],
            "timestamp": message_record["timestamp"]
        })

    @staticmethod
    def deserialize(message_create: MessageCreate) -> dict:
        """Convert Pydantic model to database-friendly dict"""
        return {
            "content": message_create.content,
            "sender_id": message_create.sender_id,
            "recipient_ids": message_create.recipient_ids,
            "type": message_create.type
        }