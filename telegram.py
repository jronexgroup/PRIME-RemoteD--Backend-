import httpx
from config import settings

TELEGRAM_API_BASE = "https://api.telegram.org/bot{token}"


async def send_message(chat_id: int, text: str, reply_markup: dict | None = None) -> bool:
    url = f"{TELEGRAM_API_BASE.format(token=settings.TELEGRAM_BOT_TOKEN)}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        return resp.status_code == 200


async def send_photo(chat_id: int, photo: bytes, caption: str = "") -> bool:
    url = f"{TELEGRAM_API_BASE.format(token=settings.TELEGRAM_BOT_TOKEN)}/sendPhoto"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            data={"chat_id": chat_id, "caption": caption},
            files={"photo": ("screenshot.png", photo, "image/png")},
        )
        return resp.status_code == 200


async def send_document(chat_id: int, document: bytes, filename: str, caption: str = "") -> bool:
    url = f"{TELEGRAM_API_BASE.format(token=settings.TELEGRAM_BOT_TOKEN)}/sendDocument"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            data={"chat_id": chat_id, "caption": caption},
            files={"document": (filename, document)},
        )
        return resp.status_code == 200


async def send_video(chat_id: int, video: bytes, caption: str = "") -> bool:
    url = f"{TELEGRAM_API_BASE.format(token=settings.TELEGRAM_BOT_TOKEN)}/sendVideo"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            data={"chat_id": chat_id, "caption": caption},
            files={"video": ("recording.avi", video, "video/avi")},
        )
        return resp.status_code == 200


async def answer_callback_query(callback_query_id: str, text: str = "") -> bool:
    url = f"{TELEGRAM_API_BASE.format(token=settings.TELEGRAM_BOT_TOKEN)}/answerCallbackQuery"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json={"callback_query_id": callback_query_id, "text": text})
        return resp.status_code == 200


def build_main_menu() -> dict:
    return {
        "inline_keyboard": [
            [{"text": "🖥 Devices", "callback_data": "devices"}],
            [
                {"text": "⚡ Power", "callback_data": "power"},
                {"text": "📸 Screenshot", "callback_data": "screenshot"},
            ],
            [
                {"text": "📂 Files", "callback_data": "files"},
                {"text": "📋 Clipboard", "callback_data": "clipboard"},
            ],
            [
                {"text": "🔊 Volume", "callback_data": "volume"},
                {"text": "⚙ System", "callback_data": "system"},
            ],
            [
                {"text": "🌐 Apps", "callback_data": "apps"},
                {"text": "⌨️ Keyboard", "callback_data": "keyboard"},
            ],
            [
                {"text": "🖱 Mouse", "callback_data": "mouse"},
                {"text": "💻 Terminal", "callback_data": "terminal"},
            ],
            [
                {"text": "📜 Scripts", "callback_data": "scripts"},
                {"text": "🎬 Record", "callback_data": "record"},
            ],
            [
                {"text": "📺 Show", "callback_data": "show"},
                {"text": "📤 Upload", "callback_data": "upload"},
            ],
        ]
    }


def build_power_menu() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "🔴 Shutdown", "callback_data": "power_shutdown"},
                {"text": "🟡 Restart", "callback_data": "power_restart"},
            ],
            [
                {"text": "🔵 Sleep", "callback_data": "power_sleep"},
                {"text": "🟢 Lock", "callback_data": "power_lock"},
            ],
            [{"text": "◀ Back", "callback_data": "main_menu"}],
        ]
    }


def build_volume_menu() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "🔊 Volume Up", "callback_data": "volume_up"},
                {"text": "🔉 Volume Down", "callback_data": "volume_down"},
            ],
            [
                {"text": "🔇 Mute", "callback_data": "volume_mute"},
                {"text": "🔊 Unmute", "callback_data": "volume_unmute"},
            ],
            [{"text": "◀ Back", "callback_data": "main_menu"}],
        ]
    }


def build_clipboard_menu() -> dict:
    return {
        "inline_keyboard": [
            [{"text": "📋 Get Clipboard", "callback_data": "clipboard_get"}],
            [{"text": "📋 Set Clipboard", "callback_data": "clipboard_set"}],
            [{"text": "◀ Back", "callback_data": "main_menu"}],
        ]
    }


def build_apps_menu() -> dict:
    return {
        "inline_keyboard": [
            [{"text": "🌐 Open URL", "callback_data": "open_url"}],
            [{"text": "📱 Open App", "callback_data": "open_app"}],
            [{"text": "◀ Back", "callback_data": "main_menu"}],
        ]
    }


def build_keyboard_menu() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "Enter", "callback_data": "key_enter"},
                {"text": "Tab", "callback_data": "key_tab"},
                {"text": "Esc", "callback_data": "key_esc"},
                {"text": "Space", "callback_data": "key_space"},
            ],
            [
                {"text": "↑", "callback_data": "key_up"},
                {"text": "↓", "callback_data": "key_down"},
                {"text": "←", "callback_data": "key_left"},
                {"text": "→", "callback_data": "key_right"},
            ],
            [
                {"text": "Ctrl+C", "callback_data": "key_ctrl+c"},
                {"text": "Ctrl+V", "callback_data": "key_ctrl+v"},
                {"text": "Alt+Tab", "callback_data": "key_alt+tab"},
            ],
            [{"text": "◀ Back", "callback_data": "main_menu"}],
        ]
    }


def build_mouse_menu() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "🔙 Back", "callback_data": "mouse_preset:browser_back"},
                {"text": "🔜 Forward", "callback_data": "mouse_preset:browser_forward"},
                {"text": "🔄 Refresh", "callback_data": "mouse_preset:browser_refresh"},
            ],
            [
                {"text": "📍 Address Bar", "callback_data": "mouse_preset:browser_address"},
                {"text": "⭐ Bookmark", "callback_data": "mouse_preset:browser_bookmark"},
            ],
            [
                {"text": "➕ New Tab", "callback_data": "mouse_preset:browser_new_tab"},
                {"text": "❌ Close Tab", "callback_data": "mouse_preset:browser_close_tab"},
            ],
            [
                {"text": "➖ Minimize", "callback_data": "mouse_preset:browser_minimize"},
                {"text": "⬜ Maximize", "callback_data": "mouse_preset:browser_maximize"},
                {"text": "❌ Close", "callback_data": "mouse_preset:browser_close"},
            ],
            [
                {"text": "⋮ Menu", "callback_data": "mouse_preset:browser_menu"},
                {"text": "👤 Profile", "callback_data": "mouse_preset:browser_profile"},
            ],
            [
                {"text": "📍 Click Custom", "callback_data": "mouse_click_mode"},
                {"text": "🔄 Scroll Up", "callback_data": "mouse_scroll_up"},
                {"text": "🔄 Scroll Down", "callback_data": "mouse_scroll_down"},
            ],
            [{"text": "◀ Back", "callback_data": "main_menu"}],
        ]
    }


def build_record_menu() -> dict:
    return {
        "inline_keyboard": [
            [{"text": "⏱ 5 seconds", "callback_data": "record_5"}],
            [{"text": "⏱ 10 seconds", "callback_data": "record_10"}],
            [{"text": "⏱ 30 seconds", "callback_data": "record_30"}],
            [{"text": "◀ Back", "callback_data": "main_menu"}],
        ]
    }


def build_files_menu(path: str = "C:\\") -> dict:
    return {
        "inline_keyboard": [
            [{"text": "⬆️ Up", "callback_data": f"files_up:{path}"}],
            [{"text": "🔄 Refresh", "callback_data": f"files_refresh:{path}"}],
            [{"text": "◀ Back", "callback_data": "main_menu"}],
        ]
    }


def build_show_menu() -> dict:
    return {
        "inline_keyboard": [
            [{"text": "📝 Send Text", "callback_data": "show_text"}],
            [{"text": "🎵 Send Audio", "callback_data": "show_audio"}],
            [{"text": "◀ Back", "callback_data": "main_menu"}],
        ]
    }
