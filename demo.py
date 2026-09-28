from .schemas import OutlineResponse, PanelOutline, PanelStory, PromptRequest, StoryResponse


def demo_outline(request: PromptRequest) -> OutlineResponse:
    titles = ["The Call", "Into the Unknown", "A Sudden Twist", "The Brave Choice", "A New Beginning"]
    scenes = [
        f"{request.character_name} discovers something unusual in {request.setting}.",
        f"{request.character_name} follows the mystery deeper into {request.setting}.",
        f"A surprising obstacle appears, testing {request.character_name}'s courage.",
        f"{request.character_name} finds a clever way through the challenge.",
        f"The adventure ends with a hopeful new beginning in {request.setting}.",
    ]
    return OutlineResponse(
        panels=[
            PanelOutline(
                panel_number=i + 1,
                title=titles[i],
                scene_description=scenes[i],
                image_prompt=(
                    f"Comic book illustration, {request.art_style}, {request.tone} mood, "
                    f"main character {request.character_name}, setting {request.setting}. "
                    f"Panel {i + 1}: {scenes[i]}"
                ),
            )
            for i in range(5)
        ]
    )


def demo_story(request: PromptRequest, outline: OutlineResponse) -> StoryResponse:
    return StoryResponse(
        panels=[
            PanelStory(
                panel_number=p.panel_number,
                caption=f"In {request.setting}...",
                narration=p.scene_description,
                dialogue=(
                    f"{request.character_name}: This could be the beginning of something amazing!"
                    if p.panel_number in (1, 5)
                    else f"{request.character_name}: I have to keep going!"
                ),
            )
            for p in outline.panels
        ]
    )
