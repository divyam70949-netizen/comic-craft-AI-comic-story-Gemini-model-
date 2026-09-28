from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from .config import BASE_DIR, get_settings
from .demo import demo_outline, demo_story
from .exporters import save_pdf
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .schemas import Comic, PromptRequest
from .store import COMICS
from .utils import new_id

router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def _generate_comic(payload: PromptRequest) -> Comic:
    settings = get_settings()
    try:
        if settings.demo_mode or not settings.gemini_api_key:
            outline = demo_outline(payload)
            story = demo_story(payload, outline)
        else:
            outline = generate_outline(payload)
            story = generate_story(payload, outline)

        image_urls = [generate_image(panel.image_prompt, panel.panel_number) for panel in outline.panels]
        layout = build_comic_layout(outline, story, image_urls)
        comic_id = new_id()
        title = f"{payload.character_name}'s {payload.tone.title()} Adventure"
        pdf_url = save_pdf(title, layout)
        comic = Comic(id=comic_id, title=title, panels=layout, pdf_url=pdf_url)
        COMICS[comic_id] = comic
        return comic
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Comic generation failed: {exc}") from exc


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"settings": get_settings()})


@router.post("/generate", response_class=HTMLResponse)
async def generate_form(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        payload = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
    except ValidationError as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "Please fill in all fields correctly.", "settings": get_settings()},
            status_code=422,
        )

    comic = _generate_comic(payload)
    return templates.TemplateResponse(request=request, name="comic_preview.html", context={"comic": comic})


@router.post("/generate-comic/json")
async def generate_json(payload: PromptRequest):
    comic = _generate_comic(payload)
    return comic


@router.get("/comic/{comic_id}", response_class=HTMLResponse)
async def comic_preview(request: Request, comic_id: str):
    comic = COMICS.get(comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found. Generate a new comic.")
    return templates.TemplateResponse(request=request, name="comic_preview.html", context={"comic": comic})


@router.get("/download/{comic_id}")
async def download_comic(comic_id: str):
    comic = COMICS.get(comic_id)
    if not comic:
        raise HTTPException(status_code=404, detail="Comic not found.")
    file_path = BASE_DIR / comic.pdf_url.removeprefix("/static/")
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="PDF file no longer exists.")
    return FileResponse(file_path, media_type="application/pdf", filename=file_path.name)


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request):
    return templates.TemplateResponse(request=request, name="export_success.html", context={})


@router.get("/test-image")
async def test_image(prompt: str = "A brave fox exploring an enchanted forest, colorful comic book style"):
    try:
        path = generate_image(prompt, 0)
        return {"success": True, "image_url": path, "prompt": prompt}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
