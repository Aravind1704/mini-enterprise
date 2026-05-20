from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Query
)

from jose import jwt, JWTError

import json
import logging

from datetime import datetime

from app.websocket.manager import manager

from app.core.config import settings


router = APIRouter()

logger = logging.getLogger(__name__)


# =========================================================
# VERIFY JWT TOKEN
# =========================================================

async def verify_ws_token(token: str):

    try:

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        user_id = payload.get("sub")

        if not user_id:

            raise ValueError("Invalid token")

        return {

            "user_id": user_id
        }

    except JWTError:

        raise ValueError("Invalid or expired token")


# =========================================================
# NOTIFICATION WEBSOCKET
# =========================================================

@router.websocket("/ws/notifications/{org_id}")

async def websocket_notifications(

    websocket: WebSocket,

    org_id: int,

    token: str = Query(...)
):

    user_id = None

    connection_id = None

    try:

        # ==========================================
        # VERIFY TOKEN
        # ==========================================

        token_data = await verify_ws_token(token)

        user_id = token_data["user_id"]

        # ==========================================
        # ACCEPT CONNECTION
        # ==========================================

        await websocket.accept()

        # ==========================================
        # REGISTER CONNECTION
        # ==========================================

        connection_id = await manager.connect(

            websocket=websocket,

            user_id=user_id,

            org_id=org_id,

            connection_type="notifications"
        )

        # ==========================================
        # SEND CONNECTED MESSAGE
        # ==========================================

        await websocket.send_json({

            "type": "connection_established",

            "user_id": user_id,

            "org_id": org_id,

            "timestamp": datetime.utcnow().isoformat()
        })

        # ==========================================
        # RECEIVE LOOP
        # ==========================================

        while True:

            raw_data = await websocket.receive_text()

            message = json.loads(raw_data)

            msg_type = message.get("type")

            # ======================================
            # PING
            # ======================================

            if msg_type == "ping":

                await websocket.send_json({

                    "type": "pong"
                })

            # ======================================
            # NOTIFICATION
            # ======================================

            elif msg_type == "notification":

                broadcast_message = {

                    "type": "notification",

                    "from_user_id": user_id,

                    "content": message.get("content"),

                    "timestamp": datetime.utcnow().isoformat()
                }

                await manager.broadcast(

                    org_id=org_id,

                    message=broadcast_message,

                    sender_id=user_id,

                    connection_type="notifications"
                )

            # ======================================
            # UNKNOWN TYPE
            # ======================================

            else:

                await websocket.send_json({

                    "type": "error",

                    "message": "Unknown message type"
                })

    # =====================================================
    # DISCONNECT
    # =====================================================

    except WebSocketDisconnect:

        logger.info(f"User disconnected: {user_id}")

        if user_id:

            await manager.disconnect(

                org_id=org_id,

                user_id=user_id,

                connection_type="notifications",

                connection_id=connection_id
            )

    # =====================================================
    # GENERAL ERROR
    # =====================================================

    except Exception as e:

        logger.error(str(e))

        try:

            await websocket.close()

        except:

            pass