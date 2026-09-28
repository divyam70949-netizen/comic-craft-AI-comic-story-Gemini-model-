from google import genai
from google.genai import types

from .config import get_settings
from .schemas import OutlineResponse, PromptRequest


def _client() -> genai.Client:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=settings.gemini_api_key)


def generate_outline(request: PromptRequest) -> OutlineResponse:
    """Generate exactly five connected comic panels with structured output."""
    settings = get_settings()
    prompt = f"""
Create a cohesive 5-panel comic outline.

User story idea: {request.story_prompt}
Main character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Requirements:
- Exactly 5 panels, numbered 1 through 5.
- Maintain the same main character, setting, and visual identity across panels.
- Give each panel a short memorable title.
- scene_description should explain the action and environment.
- image_prompt should be detailed enough for a text-to-image model and should explicitly include
  the requested art style, character identity, setting, composition, lighting, and mood.
- Do not put dialogue in image_prompt.
- The five panels must form a beginning, development, climax, and ending.
""".strip()

    response = _client().models.generate_content(
        model=settings.gemini_flash_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=OutlineResponse,
            temperature=0.9,
        ),
    )
    if getattr(response, "parsed", None):
        return response.parsed
    return OutlineResponse.model_validate_json(response.text)
