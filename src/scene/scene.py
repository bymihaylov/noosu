import pygame


class Scene:
    def __init__(self):
        self.next = self

    def setup(self):
        """ Load everything in and initialize attributes """

    def handle_events(self, events: list[pygame.event.Event]):
        """ Handle the events for this scene """

    def update(self, dt: int):
        """ Run logic """

    def render(self, screen: pygame.surface.Surface):
        """ Draw to the screen """

    def switch_to_scene(self, next_scene):
        self.next = next_scene
