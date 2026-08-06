from fastapi import APIRouter, Query
from services.command_queue import device_manager, Command
from auth import verify_api_key
import logging

logger = logging.getLogger("backend.commands")
router = APIRouter()


@router.get("/commands")
async def get_commands(
    device_id: str = Query(...),
    timeout: int = Query(default=30),
    x_api_key: str = Query(default="", alias="api_key"),
):
    if x_api_key:
        verify_api_key(x_api_key)

    device_manager.register_device(device_id, {"name": device_id})
    logger.info(f"Polling from device: {device_id}")

    command = await device_manager.wait_for_command(device_id, timeout=timeout)
    if command:
        logger.info(f"Sending command {command.id} ({command.type}) to {device_id}")
        return {"commands": [command.model_dump()]}

    return {"commands": []}
