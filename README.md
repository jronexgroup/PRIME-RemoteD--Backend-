# PRIME REMOTE D - Backend

FastAPI backend for the PRIME REMOTE D remote control system.

## Quick Start

### Local Development

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### Environment Variables

Create `.env` file:

```bash
TELEGRAM_BOT_TOKEN=your_bot_token
ALLOWED_TELEGRAM_USER_IDS=your_telegram_id
API_KEY=your_api_key
```

### Deploy to Render

1. Push to GitHub
2. Create Web Service on Render
3. Set environment variables in dashboard
4. Visit `/set-webhook` to register bot

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/telegram/webhook` | POST | Receives Telegram updates |
| `/commands` | GET | Long polling for agents |
| `/result` | POST | Command execution results |
| `/health` | GET | Health check |
| `/set-webhook` | POST | Register Telegram webhook |

## Project Structure

```
backend/
├── main.py              # FastAPI app
├── config.py            # Settings
├── auth.py              # Security
├── telegram.py          # Telegram API
├── routes/
│   ├── webhook.py       # Webhook handler
│   ├── commands.py      # Long polling
│   ├── results.py       # Results handler
│   └── health.py        # Health check
├── services/
│   └── command_queue.py # Command queue
├── requirements.txt
└── render.yaml
```
