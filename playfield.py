from pathlib import Path

import bit_flags
import config
from scene import Scene
from parse_beatmap import parse_osu_file
from noosu_object import NoosuObject
from hit_circle import HitCircle
import pygame

"""
In osu!, circle size changes the size of hit circles and sliders, with higher values creating smaller hit objects. 
Spinners are unaffected by circle size. Circle size is derived through the following formula:

r = 54.4 - 4.48 * CS

Where r is the radius measured in osu!pixels, and CS is the circle size value.
-------
source: https://osu.ppy.sh/wiki/en/Beatmap/Circle_size
"""

class Playfield(Scene):
    def __init__(self, dot_osu_path: str):
        self.dot_osu_path = dot_osu_path
        self.noosu: NoosuObject = parse_osu_file(self.dot_osu_path)
        self.all_sprites_list = pygame.sprite.Group()
        self.hit_obj_index = 0

    def setup(self):
        # pygame.mixer.Sound
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Click")


    def gamefield_to_screenspace(self, gamefield: tuple[int, int]) -> tuple[int, int]:
        """
        A function that converts gamefield coordinates to screen space.
        Args:
            gamefield: tuple[int, int]

        Returns:
            screenspace: tuple[int, int]
        """
        pass

    def screenspace_to_gamefield(self, screenspace: tuple[int, int]) -> tuple[int, int]:
        """
        A function that converts screen space coordinates to gamefield.
        Args:
            screenspace: tuple[int, int]

        Returns:
            gamefield: tuple[int, int]
        """
        pass

    def update(self, dt):
        relative_coords: tuple[int, int] = self.noosu.hit_objects[self.hit_obj_index].xy_position
        # pos: tuple[int, int] = (relative_coords[0] + (config.width - 512) // 2, relative_coords[1] + (config.height - 364) // 2)

        x, y = relative_coords
        pos: tuple[int, int] = (config.width * 0.2 + x * 1.8, config.height * 0.12 + y * 1.8) # magic?
        print(f"{relative_coords=}\t{pos=}")
        hit_circle = HitCircle(config.blue, relative_coords, 1)
        # print(f"{len(self.noosu.hit_objects)=}")
        if self.hit_obj_index + 1 < len(self.noosu.hit_objects):
            if self.noosu.hit_objects[self.hit_obj_index].type & bit_flags.HitObjectType.HIT_CIRCLE:
                self.all_sprites_list.add(hit_circle)
            self.hit_obj_index += 1
    def render(self, screen):
        self.all_sprites_list.draw(screen)