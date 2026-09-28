from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import BASE_DIR, get_settings
from .routes import router
from .utils import ensure_directories


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_directories(BASE_DIR)
    yield


settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description="AI comic story creator using Gemini and Hugging Face image generation.",
    version="1.0.0",
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name, "demo_mode": settings.demo_mode}
