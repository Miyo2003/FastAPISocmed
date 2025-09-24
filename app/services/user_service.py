# app/services/user_service.py
import os
from fastapi import status, HTTPException
from pydantic import TypeAdapter
from typing import List

from ..database.neo4j import driver
from ..models.user import UserCreate, UserResponse
from ..serializers.user_serializer import UserSerializer

class UserService:
    def __init__(self):
        self.driver = driver

    async def get_user_by_id(self, user_id: int) -> dict:
        """Retrieve user by ID"""
        with self.driver.session() as session:
            result = session.run(
                "MATCH (u:User {id: $user_id}) RETURN u",
                user_id=user_id
            )
            user_record = result.single()
            
            if not user_record or "u" not in user_record:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {user_id} not found"
                )

            return UserSerializer.serialize(user_record["u"])

    async def update_profile(self, user_id: int, profile_data: dict) -> dict:
        """Update user profile information"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $user_id})
                SET u += $profile_data
                RETURN u
                """,
                user_id=user_id,
                profile_data=profile_data
            )
            user_record = result.single()
            return UserSerializer.serialize(user_record["u"])

    async def set_online_status(self, user_id: int, online: bool = True) -> dict:
        """Set user's online status"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {id: $user_id})
                SET u.online = $online
                RETURN u
                """,
                user_id=user_id,
                online=online
            )
            user_record = result.single()
            return UserSerializer.serialize(user_record["u"])