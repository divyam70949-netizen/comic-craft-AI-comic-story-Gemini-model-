from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    debug: bool = True
    demo_mode: bool = True

    gemini_api_key: str = ""
    gemini_flash_model: str = "gemini-2.5-flash-lite"
    gemini_pro_model: str = "gemini-2.5-pro"

    hf_token: str = ""
    hf_image_model: str = "black-forest-labs/FLUX.1-schnell"
    hf_provider: str = "auto"

    max_panels: int = 5
    image_width: int = 768
    image_height: int = 768

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
