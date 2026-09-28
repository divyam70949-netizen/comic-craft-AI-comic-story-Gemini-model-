from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    story_prompt: str = Field(min_length=3, max_length=2000)
    character_name: str = Field(min_length=1, max_length=80)
    setting: str = Field(min_length=1, max_length=120)
    tone: str = Field(min_length=1, max_length=60)
    art_style: str = Field(min_length=1, max_length=80)


class PanelOutline(BaseModel):
    panel_number: int = Field(ge=1, le=5)
    title: str
    scene_description: str
    image_prompt: str


class OutlineResponse(BaseModel):
    panels: list[PanelOutline] = Field(min_length=5, max_length=5)


class PanelStory(BaseModel):
    panel_number: int = Field(ge=1, le=5)
    caption: str
    narration: str
    dialogue: str


class StoryResponse(BaseModel):
    panels: list[PanelStory] = Field(min_length=5, max_length=5)


class ComicPanel(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    image_prompt: str
    image_url: str
    caption: str
    narration: str
    dialogue: str


class Comic(BaseModel):
    id: str
    title: str
    panels: list[ComicPanel]
    pdf_url: str
