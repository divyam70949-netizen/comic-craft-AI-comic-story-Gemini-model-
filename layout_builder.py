from .schemas import OutlineResponse, StoryResponse, ComicPanel


def build_comic_layout(outline: OutlineResponse, story: StoryResponse, image_urls: list[str]) -> list[ComicPanel]:
    story_by_panel = {panel.panel_number: panel for panel in story.panels}
    result: list[ComicPanel] = []

    for index, panel in enumerate(outline.panels):
        story_panel = story_by_panel.get(panel.panel_number)
        if story_panel is None:
            raise ValueError(f"Missing story data for panel {panel.panel_number}.")
        result.append(
            ComicPanel(
                panel_number=panel.panel_number,
                title=panel.title,
                scene_description=panel.scene_description,
                image_prompt=panel.image_prompt,
                image_url=image_urls[index],
                caption=story_panel.caption,
                narration=story_panel.narration,
                dialogue=story_panel.dialogue,
            )
        )
    return result
