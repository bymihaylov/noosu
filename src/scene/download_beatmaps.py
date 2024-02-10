import pygame
from src.scene.scene import Scene
from src.config import config

import requests

from src.sprites.custom_group import CustomGroup
from src.sprites.song_metadata_button import SongMetadataButton


class DownloadBeatmaps(Scene):
    def __init__(self):
        super().__init__()
        # assert config.CLIENT_ID is not None and config.CLIENT_SECRET is not None
        self.search_beatmap("tetris", 1)
        self.sprite_group = CustomGroup()

        self.setup()

    def setup(self):
        """ Load everything in and initialize attributes """

        song_metadata_btn = SongMetadataButton("ala", "bala", "3")
        self.sprite_group.add(song_metadata_btn)
        print(self.sprite_group)

    def handle_events(self, events: list[pygame.event.Event]):
        """ Handle the events for this scene """

    def update(self, dt: int):
        """ Run logic """

    def render(self, screen: pygame.surface.Surface):
        screen.blit(self.gradient_light, self.gradient_light_rect)
        self.sprite_group.draw(screen)

    def search_beatmap(self, text: str, amount: int = 5):
        req = requests.get(config.api_search_url, params={
            "query": text,
            "amount": amount
        })

        print(req.json()["data"])
