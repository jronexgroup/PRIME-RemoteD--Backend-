from fastapi import APIRouter, Request
from services.command_queue import device_manager, CommandResult
from telegram import send_message, send_photo
import logging

logger = logging.getLogger("backend.results")
router = APIRouter()


@router.post("/result")
async def receive_result(request: Request):
    data = await request.json()
    result = CommandResult(**data)
    device_manager.store_result(result)
    logger.info(f"Received result for command {result.id}: {result.status}")

    devices = device_manager.get_devices()
    for device_id, info in devices.items():
        chat_id = info.get("chat_id")
        if chat_id:
            if result.data and result.data.get("file_path"):
                pass
            else:
                await send_message(chat_id, f"📨 {result.message}")
            break

    return {"ok": True}
