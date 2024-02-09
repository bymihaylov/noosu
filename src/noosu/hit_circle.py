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
    def __init__(self, color: tuple[int, int, int], position: tuple[int, int], circle_size: float):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.radius = 54.4 - 4.48 * circle_size
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        # Set the background color and set it to be transparent
        self.image.fill(config.white)
        self.image.set_colorkey(config.white)

        self.color = color

        # Draw the hit circle
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

        self.rect = self.image.get_rect(center=position)
