from app.websocket.manager import manager


async def send_task_update(
    task
):

    await manager.broadcast({

        "type": "TASK_UPDATED",

        "task": {
            "id": task.id,
            "title": task.title,
            "status": task.status,
            "priority": task.priority
        }
    })