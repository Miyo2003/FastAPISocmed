# app/services/activity_service.py
from http.client import HTTPException
import os
from neo4j import GraphDatabase
from pydantic import TypeAdapter
from ..database.neo4j import driver
from ..models.activity import ActivityLog
from ..serializers.activity_serializer import ActivitySerializer

class ActivityService:
    def __init__(self):
        # Initialize Neo4j connection
        self.driver = driver
        
    async def log_activity(self, activity_data: ActivityLog) -> dict:
        """Record user activity in Neo4j database"""
        try:
            # Serialize Pydantic model to dictionary
            serialized_data = ActivitySerializer.deserialize(activity_data)
            
            with self.driver.session() as session:
                # Create activity node in Neo4j
                result = session.run(
                    """
                    CREATE (a:Activity {
                        type: $type,
                        timestamp: datetime(),
                        details: $details
                    })
                    MATCH (u:User {id: $user_id})
                    CREATE (u)-[:PERFORMED]->(a)
                    RETURN a
                    """,
                    user_id=serialized_data["user_id"],
                    type=serialized_data["type"].value,
                    details=serialized_data["details"]
                )
                
                # Get created activity record
                activity_record = result.single()["a"]
                
                # Return serialized activity data
                return ActivitySerializer.serialize(activity_record)
                
        except Exception as e:
            print(f"Error logging activity: {e}")
            raise HTTPException(status_code=500, detail=str(e))