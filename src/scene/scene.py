import pygame
from src.config import config


class Scene:
    def __init__(self):
        self.next = self
        self.gradient_light = pygame.image.load(config.ui_dir / "gradient-light.png").convert()
        self.gradient_light_rect = self.gradient_light.get_rect()
        self.gradient_dark = pygame.image.load(config.ui_dir / "gradient-dark.png").convert()
        self.gradient_dark_rect = self.gradient_light.get_rect()

    def setup(self):
        """ Load everything in and initialize attributes """

    def handle_events(self, events: list[pygame.event.Event]):
        """ Handle the events for this scene """

    def update(self, dt: int):
        """ Run logic """

    def render(self, screen: pygame.surface.Surface):
        """ Draw to the screen """
        screen.blit(self.gradient_light, self.gradient_light_rect)

    def switch_to_scene(self, next_scene):
        self.next = next_scene
