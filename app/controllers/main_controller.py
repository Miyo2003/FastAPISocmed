# app/controllers/main_controller.py
from fastapi import WebSocket, WebSocketDisconnect, Request
from app.websocket.connection_manager import ConnectionManager
import asyncio
import json

# Initialize connection manager for WebSocket
connection_manager = ConnectionManager()

# Root route handler
async def index(request: Request):
    return {"message": "Welcome to the Social Media Platform!"}

# WebSocket endpoint for real-time avatar movement
async def websocket_endpoint(user_id: int, websocket: WebSocket):
    await connection_manager.connect(websocket, user_id)
    
    try:
        while True:
            # Wait for position updates from client
            data = await websocket.receive_text()
            position_data = json.loads(data)

            # Process position update
            await connection_manager.broadcast_position(user_id, position_data)

            # Check for new nearby avatars periodically
            await asyncio.sleep(1)  # Throttle checks to avoid excessive DB calls
            await connection_manager.notify_new_nearby_avatars(user_id)

    except WebSocketDisconnect:
        connection_manager.disconnect(user_id)