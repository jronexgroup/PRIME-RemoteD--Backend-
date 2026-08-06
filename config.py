import os
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = ""
    ALLOWED_TELEGRAM_USER_IDS: str = ""  # Comma-separated: "123456,789012"
    API_KEY: str = ""
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    POLL_TIMEOUT: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_allowed_user_ids(self) -> list[int]:
        if not self.ALLOWED_TELEGRAM_USER_IDS:
            return []
        return [int(uid.strip()) for uid in self.ALLOWED_TELEGRAM_USER_IDS.split(",") if uid.strip()]


settings = Settings()
