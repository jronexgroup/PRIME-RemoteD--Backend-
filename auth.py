from fastapi import Header, HTTPException
from config import settings


def verify_api_key(x_api_key: str = Header(...)) -> str:
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


def is_authorized_telegram_user(user_id: int) -> bool:
    allowed_ids = settings.get_allowed_user_ids()
    if not allowed_ids:
        return False
    return user_id in allowed_ids
