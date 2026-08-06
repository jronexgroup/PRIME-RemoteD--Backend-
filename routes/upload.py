from fastapi import APIRouter, Request, UploadFile, File, Form
from telegram import send_photo, send_document, send_video, send_message
from services.command_queue import device_manager
import logging
import tempfile
import os
import httpx

logger = logging.getLogger("backend.upload")
router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    device_id: str = Form(default=""),
    file_type: str = Form(default="screenshot"),
):
    contents = await file.read()

    chat_id = None
    for did, info in device_manager.get_devices().items():
        chat_id = info.get("chat_id")
        if chat_id:
            break

    if not chat_id:
        return {"ok": False, "message": "No chat found"}

    if file_type == "screenshot":
        await send_photo(chat_id, contents, caption="📸 Screenshot")
    elif file_type == "video":
        await send_video(chat_id, contents, caption="🎬 Screen Recording")
    else:
        await send_document(chat_id, contents, filename=file.filename, caption=f"📄 {file.filename}")

    return {"ok": True, "message": "File sent to Telegram"}


@router.post("/download")
async def download_from_telegram(request: Request):
    data = await request.json()
    file_id = data.get("file_id", "")
    save_path = data.get("save_path", "C:\\Downloads")
    device_id = data.get("device_id", "")

    if not file_id:
        return {"ok": False, "message": "No file_id"}

    from config import settings

    get_file_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getFile"
    async with httpx.AsyncClient() as client:
        resp = await client.post(get_file_url, json={"file_id": file_id})
        if resp.status_code != 200:
            return {"ok": False, "message": "Failed to get file info"}

        file_info = resp.json().get("result", {})
        file_path = file_info.get("file_path", "")
        if not file_path:
            return {"ok": False, "message": "No file path"}

        download_url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_path}"
        file_resp = await client.get(download_url)
        if file_resp.status_code != 200:
            return {"ok": False, "message": "Failed to download file"}

        os.makedirs(save_path, exist_ok=True)
        local_path = os.path.join(save_path, file_path.split("/")[-1])
        with open(local_path, "wb") as f:
            f.write(file_resp.content)

    return {"ok": True, "message": f"Saved to {local_path}", "path": local_path}
