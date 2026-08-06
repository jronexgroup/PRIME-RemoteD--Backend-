from fastapi import APIRouter, Request
from fastapi.responses import Response
from services.command_queue import device_manager, Command
import logging
import base64

logger = logging.getLogger("backend.health")
router = APIRouter()


@router.get("/health")
async def health_check():
    devices = device_manager.get_devices()
    return {
        "status": "healthy",
        "service": "PRIME REMOTE D",
        "version": "1.0.0",
        "connected_devices": len(devices),
    }


@router.get("/set-webhook")
async def set_webhook():
    from config import settings
    import httpx

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook"
    webhook_url = "https://prime-remoted-backend.onrender.com/telegram/webhook"

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json={"url": webhook_url})
        return resp.json()


@router.post("/screen")
async def receive_screen(request: Request):
    data = await request.json()
    device_id = data.get("device_id", "")
    screen_data = data.get("screen", "")

    if device_id in device_manager.get_devices():
        device_manager.get_devices()[device_id]["last_screen"] = screen_data

    return {"ok": True}


@router.get("/screen")
async def get_screen():
    devices = device_manager.get_devices()
    for device_id, info in devices.items():
        screen = info.get("last_screen")
        if screen:
            img_data = base64.b64decode(screen)
            return Response(content=img_data, media_type="image/png")

    return Response(content=b"", media_type="image/png")


@router.post("/command")
async def send_command_direct(request: Request):
    data = await request.json()
    device_id = data.get("device_id", "")
    cmd_type = data.get("type", "")
    cmd_args = data.get("args", {})

    if not device_id:
        return {"ok": False, "message": "No device_id"}

    cmd = Command(type=cmd_type, device_id=device_id, args=cmd_args)
    await device_manager.enqueue_command(device_id, cmd)

    return {"ok": True, "message": f"Command {cmd_type} sent"}
