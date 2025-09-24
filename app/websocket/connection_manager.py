# app/websocket/connection_manager.py
import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from ..services.avatar_service import AvatarService
from ..database.neo4j import driver
from ..models.avatar import AvatarUpdate

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}
        self.driver = driver
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Establish WebSocket connection for user"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        
        # Send initial nearby avatars to client
        nearby_avatars = await self._get_initial_nearby_avatars(user_id)
        await websocket.send_json({
            "type": "initial_avatars",
            "avatars": nearby_avatars
        })
    
    def disconnect(self, user_id: int):
        """Remove disconnected user from active connections"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    
    async def _get_initial_nearby_avatars(self, user_id: int) -> list:
        """Get initial nearby avatars for connected user"""
        with self.driver.session() as session:
            # First get current user's position
            result = session.run(
                "MATCH (u:User {id: $user_id})-[:HAS_AVATAR]->(a:Avatar) RETURN a",
                user_id=user_id
            )
            user_avatar = result.single()["a"]
            
            if not user_avatar:
                return []
            
            # Find nearby avatars
            nearby_result = session.run(
                """
                MATCH (a:Avatar)
                WHERE distance(point({x: $x, y: $y}), point({x: a.x, y: a.y})) <= $radius
                AND NOT EXISTS((a)<-[:HAS_AVATAR]-(:User {id: $user_id}))
                RETURN a
                """,
                x=user_avatar["x"],
                y=user_avatar["y"],
                radius=100.0  # Default search radius
            )
            
            return [dict(record["a"]) for record in nearby_result]
    
    async def broadcast_position(self, user_id: int, position: dict):
        """Broadcast avatar position to all connected clients"""
        with self.driver.session() as session:
            # Update avatar position in database
            session.run(
                """
                MATCH (u:User {id: $user_id})
                MATCH (a:Avatar)-[:HAS_AVATAR]->(u)
                SET a.x = $x, a.y = $y
                """,
                user_id=user_id,
                x=position["x"],
                y=position["y"]
            )
            
            # Get updated avatar info
            result = session.run(
                """
                MATCH (u:User {id: $user_id})-[:HAS_AVATAR]->(a:Avatar)
                RETURN a
                """,
                user_id=user_id
            )
            updated_avatar = result.single()["a"]
            
            # Broadcast to all connected clients
            for conn_id, connection in self.active_connections.items():
                if conn_id != user_id:
                    await connection.send_json({
                        "type": "avatar_move",
                        "user_id": user_id,
                        "position": {
                            "x": updated_avatar["x"],
                            "y": updated_avatar["y"]
                        }
                    })
    
    async def notify_new_nearby_avatars(self, user_id: int):
        """Notify user about new nearby avatars"""
        with self.driver.session() as session:
            # Get current user's position
            result = session.run(
                "MATCH (u:User {id: $user_id})-[:HAS_AVATAR]->(a:Avatar) RETURN a",
                user_id=user_id
            )
            user_avatar = result.single()["a"]
            
            if not user_avatar:
                return
            
            # Find newly appeared nearby avatars
            nearby_result = session.run(
                """
                MATCH (a:Avatar)
                WHERE distance(point({x: $x, y: $y}), point({x: a.x, y: a.y})) <= $radius
                AND NOT EXISTS((a)<-[:HAS_AVATAR]-(:User {id: $user_id}))
                RETURN a
                """,
                x=user_avatar["x"],
                y=user_avatar["y"],
                radius=100.0
            )
            
            new_avatars = [dict(record["a"]) for record in nearby_result]
            
            if new_avatars:
                await self.active_connections[user_id].send_json({
                    "type": "new_nearby_avatars",
                    "avatars": new_avatars
                })