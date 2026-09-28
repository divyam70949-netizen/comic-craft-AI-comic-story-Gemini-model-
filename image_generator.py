from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from huggingface_hub import InferenceClient

from .config import get_settings, BASE_DIR
from .utils import safe_filename


def _font(size: int):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _demo_image(prompt: str, output_path: Path, panel_number: int) -> None:
    """Create a local placeholder so the whole application can be tested without paid APIs."""
    settings = get_settings()
    image = Image.new("RGB", (settings.image_width, settings.image_height), "#f5efe0")
    draw = ImageDraw.Draw(image)
    margin = 55
    draw.rounded_rectangle(
        (margin, margin, settings.image_width - margin, settings.image_height - margin),
        radius=28,
        outline="#222222",
        width=8,
    )
    title = f"COMICCRAFT\nPANEL {panel_number}"
    draw.multiline_text((margin + 35, margin + 35), title, font=_font(46), fill="#111111", spacing=8)
    preview = prompt[:220].replace("\n", " ")
    draw.text((margin + 35, settings.image_height // 2), preview, font=_font(24), fill="#333333")
    draw.text((margin + 35, settings.image_height - margin - 55), "DEMO MODE — add HF_TOKEN for AI images", font=_font(18), fill="#555555")
    image.save(output_path, "PNG")


def generate_image(prompt: str, panel_number: int) -> str:
    settings = get_settings()
    filename = f"panel_{panel_number}_{safe_filename(prompt)}.png"
    output_path = BASE_DIR / "static" / "panels" / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if settings.demo_mode or not settings.hf_token:
        _demo_image(prompt, output_path, panel_number)
    else:
        client = InferenceClient(api_key=settings.hf_token, provider=settings.hf_provider)
        image = client.text_to_image(
            prompt,
            model=settings.hf_image_model,
            width=settings.image_width,
            height=settings.image_height,
        )
        image.save(output_path)

    return f"/static/panels/{filename}"
