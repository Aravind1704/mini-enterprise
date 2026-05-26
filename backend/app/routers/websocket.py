
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect
)


from app.websocket.manager import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):


    await manager.connect(websocket)

    try:

        while True:

            data = await websocket.receive_text()

            await manager.broadcast(
                f"Message: {data}"
            )

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        print("WebSocket disconnected")
        await manager.broadcast(
            "A user has disconnected"
        )