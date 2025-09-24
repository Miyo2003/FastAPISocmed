from pydantic import TypeAdapter
from ..database.neo4j import driver
from ..models.chat import MessageCreate
from ..serializers.message_serializer import MessageSerializer

class ChatService:
    def __init__(self):
        self.driver = driver
    
    async def send_message(self, message_data: MessageCreate) -> dict:
        """Send message to recipients"""
        # Convert Pydantic model to database-friendly dictionary
        serialized_data = MessageSerializer.deserialize(message_data)
        
        with self.driver.session() as session:
            # Create message node in Neo4j
            result = session.run(
                """
                MATCH (s:User {id: $sender_id}), (r:User {id: $receiver_id})
                CREATE (m:Message {
                    content: $content,
                    timestamp: datetime(),
                    sender_id: $sender_id,
                    receiver_id: $receiver_id
                })
                RETURN m
                """,
                sender_id=serialized_data["sender_id"],
                receiver_id=serialized_data["recipient_ids"][0],  # Single recipient for now
                content=serialized_data["content"]
            )
            message_record = result.single()["m"]
            
            return MessageSerializer.serialize(message_record)