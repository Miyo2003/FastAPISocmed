from pydantic import TypeAdapter
from app.models.avatar import AvatarResponse, AvatarUpdate

class AvatarSerializer:
    @staticmethod
    def serialize(avatar_record) -> AvatarResponse:
        """Convert Neo4j record to Pydantic model with extended appearance"""
        return TypeAdapter(AvatarResponse).validate_python({
            "user_id": avatar_record["user_id"],
            "position": {
                "x": avatar_record["x"],
                "y": avatar_record["y"]
            },
            "color": avatar_record.get("color", "blue"),
            "size": avatar_record.get("size", 50.0),
            "shape": avatar_record.get("shape", "circle"),
            "glow_effect": avatar_record.get("glow_effect"),
            "particle_trail": avatar_record.get("particle_trail")
        })

    @staticmethod
    def deserialize(avatar_update: AvatarUpdate) -> dict:
        """Convert Pydantic model to database-friendly dict with extended appearance"""
        appearance_data = {
            "color": avatar_update.appearance.color,
            "size": avatar_update.appearance.size,
            "shape": avatar_update.appearance.shape,
            "glow_effect": avatar_update.appearance.glow_effect,
            "particle_trail": avatar_update.appearance.particle_trail
        }

        return {
            "x": avatar_update.position.x,
            "y": avatar_update.position.y,
            **appearance_data
        }