from datetime import datetime
from pathlib import Path

from fpdf import FPDF
from PIL import Image

from .config import BASE_DIR
from .schemas import ComicPanel


def _local_image(image_url: str) -> Path:
    relative = image_url.removeprefix("/static/")
    return BASE_DIR / "static" / relative


def save_pdf(title: str, panels: list[ComicPanel]) -> str:
    export_dir = BASE_DIR / "static" / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = export_dir / f"comiccraft_{timestamp}.pdf"

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in panels:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.multi_cell(0, 10, f"Panel {panel.panel_number}: {panel.title}")
        pdf.ln(2)

        image_path = _local_image(panel.image_url)
        if image_path.exists():
            with Image.open(image_path) as image:
                width, height = image.size
            max_w, max_h = 180, 105
            ratio = min(max_w / width, max_h / height)
            pdf.image(str(image_path), w=width * ratio, h=height * ratio)
        pdf.ln(5)

        pdf.set_font("Helvetica", "I", 10)
        pdf.multi_cell(0, 6, panel.scene_description.encode("latin-1", "replace").decode("latin-1"))
        pdf.ln(2)

        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 6, "Caption")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, panel.caption.encode("latin-1", "replace").decode("latin-1"))
        pdf.ln(2)

        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 6, "Narration")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, panel.narration.encode("latin-1", "replace").decode("latin-1"))
        if panel.dialogue:
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(0, 6, "Dialogue")
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 6, panel.dialogue.encode("latin-1", "replace").decode("latin-1"))

    pdf.output(str(path))
    return f"/static/exports/{path.name}"
