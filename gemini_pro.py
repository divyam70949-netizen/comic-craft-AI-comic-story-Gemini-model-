from google import genai
from google.genai import types

from .config import get_settings
from .schemas import OutlineResponse, PromptRequest, StoryResponse


def _client() -> genai.Client:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=settings.gemini_api_key)


def generate_story(request: PromptRequest, outline: OutlineResponse) -> StoryResponse:
    """Expand the outline into captions, narration, and dialogue for each panel."""
    settings = get_settings()
    outline_json = outline.model_dump_json(indent=2)
    prompt = f"""
Write the complete narration and dialogue for this 5-panel comic.

Character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}
Original idea: {request.story_prompt}

Outline:
{outline_json}

Requirements:
- Return exactly one story object for each panel, numbered 1 through 5.
- Keep character names and events consistent with the outline.
- caption: one short ambient comic caption, suitable for a caption box.
- narration: 1-3 concise sentences describing the action/emotion.
- dialogue: natural spoken dialogue; if no dialogue is needed, use an empty string.
- Keep the writing family-friendly and visually compatible with a comic page.
""".strip()

    response = _client().models.generate_content(
        model=settings.gemini_pro_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=StoryResponse,
            temperature=0.85,
        ),
    )
    if getattr(response, "parsed", None):
        return response.parsed
    return StoryResponse.model_validate_json(response.text)
