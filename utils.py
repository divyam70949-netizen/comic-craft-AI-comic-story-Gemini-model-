import re
from pathlib import Path
from uuid import uuid4


def new_id() -> str:
    return uuid4().hex


def safe_filename(value: str, max_length: int = 60) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip()).strip("_")
    return (cleaned[:max_length] or "panel").lower()


def ensure_directories(base_dir: Path) -> None:
    (base_dir / "static" / "panels").mkdir(parents=True, exist_ok=True)
    (base_dir / "static" / "exports").mkdir(parents=True, exist_ok=True)
