from pathlib import Path

import bit_flags
import config
import hit_object
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
        super().__init__()

        self.gamefield_width = 640
        self.gamefield_height = 480
        self.gamefield_shift = 8

        # https://www.reddit.com/r/osugame/comments/ff6n01/resolution_of_the_playfield/
        self.playfield_height = int(0.8 * config.height)
        self.playfield_width = int(self.playfield_height * 4 / 3)

        self.playfield_top_left = (
            (config.width - self.playfield_width) // 2,
            (config.height - self.playfield_height) // 2
        )
        self.playfield_bottom_right = (
            self.playfield_top_left[0] + self.playfield_width,
            self.playfield_top_left[1] + self.playfield_height
        )

        self.playfield_centre = (
            (self.playfield_top_left[0] + self.playfield_bottom_right[0]) // 2,
            (self.playfield_top_left[1] + self.playfield_bottom_right[1]) // 2
        )

        self.dot_osu_path = dot_osu_path
        self.noosu: NoosuObject = parse_osu_file(self.dot_osu_path)
        self.all_sprites_list = pygame.sprite.Group()
        self.hit_obj_index = 0

    def setup(self):
        pygame.mixer.music.load("assets/355322 nekodex - circles!/nekodex - circles! (pishifat) [Audio].mp3") # TODO: extract from noosu object?
        pygame.mixer.music.play(0)

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

        scale_x = self.playfield_width / 512
        scale_y = self.playfield_height / 384

        # screenspace_x = int((gamefield[0] * scale_x))
        # screenspace_y = int((gamefield[1] * scale_y))
        screenspace_x = int((gamefield[0] * scale_x) + self.playfield_top_left[0])
        screenspace_y = int((gamefield[1] * scale_y) + self.playfield_top_left[1] + self.gamefield_shift * scale_y)

        return screenspace_x, screenspace_y

    def screenspace_to_gamefield(self, screenspace: tuple[int, int]) -> tuple[int, int]:
        """
        A function that converts screen space coordinates to gamefield.
        Args:
            screenspace: tuple[int, int]

        Returns:
            gamefield: tuple[int, int]
        """
        # Calculate scaling factors for x and y
        scale_x = 512 / self.playfield_width
        scale_y = 384 / self.playfield_height

        # Convert screen space coordinates to gamefield
        gamefield_x = int((screenspace[0] - self.playfield_top_left[0]) * scale_x)
        gamefield_y = int((screenspace[1] - self.playfield_top_left[1] - self.gamefield_shift * scale_y) * scale_y)

        return gamefield_x, gamefield_y

    # def update(self, dt):
    #     hit_object = self.noosu.hit_objects[self.hit_obj_index]
    #     gamefield_coords: tuple[int, int] = hit_object.xy_position
    #
    #     print(gamefield_coords)
    #
    #     hit_circle = HitCircle(config.blue, self.gamefield_to_screenspace((256, 192)), 5)
    #
    #     if self.hit_obj_index + 1 < len(self.noosu.hit_objects):
    #         if self.noosu.hit_objects[self.hit_obj_index].type & bit_flags.HitObjectType.HIT_CIRCLE:
    #             self.all_sprites_list.add(hit_circle)
    #         self.hit_obj_index += 1

    def update(self, dt):
        # Get the current time when updating
        current_time = pygame.mixer.music.get_pos()

        # Iterate through hit objects to find the one that corresponds to the current time
        while self.hit_obj_index < len(self.noosu.hit_objects):
            hit_object = self.noosu.hit_objects[self.hit_obj_index]
            if hit_object.time > current_time:
                break  # Found the hit object corresponding to the current time
            self.hit_obj_index += 1

        # If there are more hit objects and the current hit object is a hit circle
        if self.hit_obj_index < len(self.noosu.hit_objects) and \
                self.noosu.hit_objects[self.hit_obj_index].type & bit_flags.HitObjectType.HIT_CIRCLE:
            hit_object = self.noosu.hit_objects[self.hit_obj_index]
            gamefield_coords = hit_object.xy_position

            # Convert gamefield coordinates to screen space
            screenspace_coords = self.gamefield_to_screenspace(gamefield_coords)

            # Create and add HitCircle object to the sprite group
            hit_circle = HitCircle(config.blue, screenspace_coords, 5)
            self.all_sprites_list.add(hit_circle)

    def render(self, screen):
        self.all_sprites_list.draw(screen)
