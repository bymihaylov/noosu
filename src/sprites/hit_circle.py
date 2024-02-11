import pygame
from src.config import config

"""
In osu!, circle size changes the size of hit circles and sliders, with higher values creating smaller hit objects. 
Spinners are unaffected by circle size. Circle size is derived through the following formula:

r = 54.4 - 4.48 * CS

Where r is the radius measured in osu!pixels, and CS is the circle size value.
-------
source: https://osu.ppy.sh/wiki/en/Beatmap/Circle_size
"""


class HitCircle(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], circle_size: float):
        super().__init__()

        self.radius = 54.4 - 4.48 * circle_size
        scaled_size = (int(self.radius * 4), int(self.radius * 4))
        self.image = pygame.image.load(config.ui_dir / "hit_circle.tiff")
        self.image = pygame.transform.smoothscale(self.image, scaled_size).convert_alpha()

        self.rect = self.image.get_rect(center=position)
