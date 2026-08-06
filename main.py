import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from config import settings
from routes.webhook import router as webhook_router
from routes.commands import router as commands_router
from routes.results import router as results_router
from routes.health import router as health_router
from routes.upload import router as upload_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("backend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("PRIME REMOTE D Backend starting...")
    logger.info(f"Allowed Telegram users: {settings.ALLOWED_TELEGRAM_USER_IDS}")
    yield
    logger.info("PRIME REMOTE D Backend shutting down...")


app = FastAPI(title="PRIME REMOTE D", version="1.0.0", lifespan=lifespan)

app.include_router(webhook_router)
app.include_router(commands_router)
app.include_router(results_router)
app.include_router(health_router)
app.include_router(upload_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.BACKEND_HOST, port=settings.BACKEND_PORT, reload=True)
