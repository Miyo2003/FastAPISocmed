import os
from pydantic import TypeAdapter

from app.serializers.relationship_serializer import RelationshipSerializer
from ..database.neo4j import driver
from ..models.relationship import FriendRequest, Friendship

class RelationshipService:
    def __init__(self):
        self.driver = driver
    
    async def create_friend_request(self, friend_request: FriendRequest) -> dict:
        """Create friend request in Neo4j"""
        serialized_data = RelationshipSerializer.deserialize(friend_request)
        
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $requester_id})
                MATCH (f:User {id: $requested_id})
                CREATE (fr:FriendRequest {
                    created_at: datetime()
                })
                RETURN fr
                """,
                requester_id=serialized_data["requester_id"],
                requested_id=serialized_data["requested_id"]
            )
            friend_request_record = result.single()["fr"]
            
            return RelationshipSerializer.serialize(friend_request_record)
    
    async def accept_friend_request(self, user_id: int, friend_id: int) -> dict:
        """Accept friend request"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $user_id})
                MATCH (f:User {id: $friend_id})
                CREATE (u)-[:ACCEPTS]->(f)
                RETURN f
                """,
                user_id=user_id,
                friend_id=friend_id
            )
            friendship_record = result.single()["f"]
            
            return RelationshipSerializer.serialize(friendship_record)
    
    async def get_friends(self, user_id: int) -> list:
        """Get user's friends"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $user_id})
                MATCH (f:User)-[:FRIEND_OF]->(u)
                RETURN f
                """,
                user_id=user_id
            )
            friends = [record["f"] for record in result]
            return [RelationshipSerializer.serialize(f) for f in friends]