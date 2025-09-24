import os
import bcrypt
from datetime import timedelta
from jose import jwt
from fastapi import HTTPException, status
from ..database.neo4j import driver
from ..models.user import UserCreate, UserResponse
from ..serializers.user_serializer import UserSerializer

class AuthService:
    def __init__(self):
        self.driver = driver
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Register new user with hashed password"""
        serialized_data = UserSerializer.deserialize(user_data)
        
        with self.driver.session() as session:
            result = session.run(
                """
                CREATE (u:User {
                    id: randomUUID(),
                    username: $username,
                    email: $email,
                    password_hash: $password_hash,
                    created_at: datetime(),
                    online: false
                })
                RETURN u
                """,
                username=serialized_data["username"],
                email=serialized_data["email"],
                password_hash=serialized_data["password_hash"]
            )
            user_record = result.single()["u"]
            
            return UserSerializer.serialize(user_record)
    
    async def authenticate_user(self, credentials: dict) -> dict:
        """Verify user credentials and return access token"""
        with self.driver.session() as session:
            result = session.run(
                "MATCH (u:User {username: $username}) RETURN u",
                username=credentials["username"]
            )
            user_record = result.single()["u"]
            
            if not user_record:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            if not bcrypt.checkpw(
                credentials["password"].encode('utf-8'),
                user_record["password_hash"].encode('utf-8')
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect password"
                )
            
            # Generate JWT token
            access_token_expires = timedelta(minutes=30)
            access_token = jwt.encode(
                {"sub": user_record["username"]},
                os.getenv("JWT_SECRET_KEY"),
                algorithm=os.getenv("JWT_ALGORITHM")
            )
            
            return {"access_token": access_token, "token_type": "bearer"}