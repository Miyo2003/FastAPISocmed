import os
import bcrypt
from datetime import timedelta
from jose import jwt
from fastapi import HTTPException, status
from ..database.neo4j import driver
from ..models.avatar import AvatarUpdate, AvatarResponse
from ..serializers.avatar_serializer import AvatarSerializer

class AvatarService:
    def __init__(self):
        self.driver = driver
    
    async def update_avatar_position(self, user_id: int, position: AvatarUpdate) -> dict:
        """Update avatar position in Neo4j"""
        serialized_data = AvatarSerializer.deserialize(position)
        
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $user_id})
                MERGE (a:Avatar {user_id: $user_id})
                ON CREATE SET a.created_at = datetime(), a.color = 'blue', a.size = 50.0
                SET a.x = $x, a.y = $y
                RETURN a
                """,
                user_id=user_id,
                x=serialized_data["position"]["x"],
                y=serialized_data["position"]["y"]
            )
            avatar_record = result.single()["a"]
            
            return AvatarSerializer.serialize(avatar_record)
    
    async def change_avatar_appearance(self, user_id: int, appearance: dict) -> dict:
        """Change avatar visual properties"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $user_id})
                MATCH (a:Avatar {user_id: $user_id})
                SET a += $appearance
                RETURN a
                """,
                user_id=user_id,
                appearance=appearance
            )
            avatar_record = result.single()["a"]
            
            return AvatarSerializer.serialize(avatar_record)
    
    async def get_nearby_avatars(self, user_id: int, radius: float = 100.0) -> list:
        """Get avatars near current user"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $user_id})
                MATCH (a:Avatar)
                WHERE distance(point({x: u.x, y: u.y}), point({x: a.x, y: a.y})) <= $radius
                RETURN a
                """,
                user_id=user_id,
                radius=radius
            )
            avatars = [record["a"] for record in result]
            return [AvatarSerializer.serialize(a) for a in avatars]
    
    async def trigger_animation(self, user_id: int, animation_type: str) -> dict:
        """Trigger special avatar animations"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $user_id})
                MATCH (a:Avatar {user_id: $user_id})
                CALL apoc.do.when(true, 
                  yield apoc.trigger.animation($animation_type, a))
                RETURN a
                """,
                user_id=user_id,
                animation_type=animation_type
            )
            avatar_record = result.single()["a"]
            
            return AvatarSerializer.serialize(avatar_record)