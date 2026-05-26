from fastapi import WebSocket

<<<<<<< HEAD

class ConnectionManager:

    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):

        for connection in self.active_connections:
            await connection.send_text(message)
=======
class ConnectionManager:

    def __init__(self):

        self.active_connections = []


    async def connect(
        self,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.active_connections.append(
            websocket
        )


    def disconnect(
        self,
        websocket: WebSocket
    ):

        self.active_connections.remove(
            websocket
        )


    async def broadcast(
        self,
        message: dict
    ):

        for connection in self.active_connections:

            await connection.send_json(
                message
            )
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2


manager = ConnectionManager()