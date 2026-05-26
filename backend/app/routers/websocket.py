<<<<<<< HEAD
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
=======
from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect
)
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2

from app.websocket.manager import manager

router = APIRouter()

<<<<<<< HEAD

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
=======
@router.websocket("/ws")

async def websocket_endpoint(
    websocket: WebSocket
):
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2

    await manager.connect(websocket)

    try:

        while True:

<<<<<<< HEAD
            data = await websocket.receive_text()

            await manager.broadcast(
                f"Message: {data}"
            )

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        print("WebSocket disconnected")
=======
            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect(websocket)
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
