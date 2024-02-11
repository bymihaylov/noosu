import pygame

import src.scene.setup_scene
from src.api_client.search import search_beatmap
from src.api_client.download import download_by_set_id
from src.scene.scene import Scene
from src.config import config
from src.config import custom_events

from src.sprites.custom_group import CustomGroup
from src.sprites.song_metadata_button import SongMetadataButton
from src.sprites.text_input_box import TextInputBox


class DownloadBeatmaps(Scene):
    def __init__(self):
        super().__init__()
        # assert config.CLIENT_ID is not None and config.CLIENT_SECRET is not None
        self.sprite_group = CustomGroup()
        self.go_back_image = pygame.image.load(config.ui_dir / "go_back.tiff")
        x = config.width - 256 - 40
        self.go_back_image_rect = self.go_back_image.get_rect().move(x, 0)
        self.go_back_image_hover = pygame.image.load(config.ui_dir / "go_back-hover.tiff")
        self.go_back_image_hover_rect = self.go_back_image.get_rect().move(x, 0)

        self.is_hovered = False

        self.setup()

    def setup(self):
        """ Load everything in and initialize attributes """

        text_input_box = TextInputBox()
        self.sprite_group.add(text_input_box)

    def handle_events(self, events: list[pygame.event.Event]):
        """ Handle the events for this scene """
        self.sprite_group.handle_events(events)
        for event in events:
            if event.type == custom_events.TEXT_INPUT_SUBMITTED:
                self.add_song_metadata_buttons(event.text)
            elif event.type == custom_events.SET_ID_SUBMITTED:
                download_by_set_id(event.set_id, event.artist, event.title)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
                self.switch_to_scene(src.scene.setup_scene.Setup())


    def add_song_metadata_buttons(self, search_query: str):
        metadata_list: list[tuple[str, str, str, str]] = search_beatmap(search_query)
        padding = 200
        left = 100
        top = 100
        i = 0
        for tuple_element in metadata_list:
            self.sprite_group.add(SongMetadataButton(tuple_element, left, top + padding * i))
            i += 1

    def update(self, dt: int):
        """ Run logic """
        self.sprite_group.update()
        self.is_hovered = self.go_back_image_rect.collidepoint(pygame.mouse.get_pos())


    def render(self, screen: pygame.surface.Surface):
        screen.blit(self.gradient_light, self.gradient_light_rect)
        if self.is_hovered:
            screen.blit(self.go_back_image, self.go_back_image_rect)
        else:
            screen.blit(self.go_back_image_hover, self.go_back_image_hover_rect)
        self.sprite_group.draw(screen)

