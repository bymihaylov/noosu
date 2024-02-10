import pygame

from src.api_client.search import search_beatmap
from src.api_client.download import download_by_set_id
from src.scene.scene import Scene
from src.config import config
from src.config import custom_events

import requests

from src.sprites.custom_group import CustomGroup
from src.sprites.song_metadata_button import SongMetadataButton
from src.sprites.text_input_box import TextInputBox


class DownloadBeatmaps(Scene):
    def __init__(self):
        super().__init__()
        # assert config.CLIENT_ID is not None and config.CLIENT_SECRET is not None
        self.sprite_group = CustomGroup()

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


    def add_song_metadata_buttons(self, search_query: str):
        metadata_list: list[tuple[str, str, str, str]] = search_beatmap(search_query)
        padding = 200
        position = 100
        i = 0
        for tuple_element in metadata_list:
            self.sprite_group.add(SongMetadataButton(tuple_element, position, position + padding * i))
            i += 1

    def update(self, dt: int):
        """ Run logic """
        self.sprite_group.update()


    def render(self, screen: pygame.surface.Surface):
        screen.blit(self.gradient_light, self.gradient_light_rect)
        self.sprite_group.draw(screen)

