from pathlib import Path

import bit_flags
import config
from scene import Scene
from parse_beatmap import parse_osu_file
from noosu_object import NoosuObject
from hit_circle import HitCircle
import pygame


class Playfield(Scene):
    def __init__(self, dot_osu_path: str):
        self.dot_osu_path = dot_osu_path
        self.noosu: NoosuObject = parse_osu_file(self.dot_osu_path)
        self.all_sprites_list = pygame.sprite.Group()
        self.hit_obj_index = 0

    def setup(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Click")

    def update(self, dt):
        hit_circle = HitCircle(config.blue, self.noosu.hit_objects[self.hit_obj_index].xy_position, 1)
        # print(f"{len(self.noosu.hit_objects)=}")
        if self.hit_obj_index + 1 < len(self.noosu.hit_objects):
            if self.noosu.hit_objects[self.hit_obj_index].type & bit_flags.HitObjectType.HIT_CIRCLE:
                self.all_sprites_list.add(hit_circle)
            self.hit_obj_index += 1
    def render(self, screen):
        self.all_sprites_list.draw(screen)