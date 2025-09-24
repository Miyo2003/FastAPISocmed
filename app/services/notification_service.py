import os
from pydantic import TypeAdapter
from ..database.neo4j import driver
from ..models.notification import NotificationCreate
from ..serializers.notification_serializer import NotificationSerializer

class NotificationService:
    def __init__(self):
        self.driver = driver
    
    async def create_notification(self, notification_data: NotificationCreate) -> dict:
        """Create notification for user"""
        serialized_data = NotificationSerializer.deserialize(notification_data)
        
        with self.driver.session() as session:
            result = session.run(
                """
                CREATE (n:Notification {
                    type: $type,
                    related_id: $related_id,
                    timestamp: datetime()
                })
                MATCH (u:User {id: $user_id})
                CREATE (u)-[:RECEIVED]->(n)
                RETURN n
                """,
                user_id=serialized_data["user_id"],
                type=serialized_data["type"].value,
                related_id=serialized_data["related_id"]
            )
            notification_record = result.single()["n"]
            
            return NotificationSerializer.serialize(notification_record)