from pydantic import TypeAdapter
from app.models.user import UserCreate, UserResponse
import bcrypt

class UserSerializer:
    @staticmethod
    def serialize(user_record) -> UserResponse:
        """Convert Neo4j record to Pydantic model"""
        return TypeAdapter(UserResponse).validate_python({
            "id": user_record["id"],
            "username": user_record["username"],
            "email": user_record["email"],
            "online": user_record["online"],
            # Optional fields can be added here if present
            "first_name": user_record.get("first_name"),
            "last_name": user_record.get("last_name"),
            "age": user_record.get("age"),
            "gender": user_record.get("gender"),
            "date_of_birth": user_record.get("date_of_birth")
        })

    @staticmethod
    def deserialize(user_create: UserCreate) -> dict:
        """Convert Pydantic model to database-friendly dict"""
        return {
            "username": user_create.username,
            "email": user_create.email,
            "password_hash": bcrypt.hashpw(
                user_create.password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')
        }