from pygame.sprite import Group

"""
I need a custom draw method for SongMetadataButton and TextInputBox
Also handle_events for TextInputBox
"""
class CustomGroup(Group):
    def __init__(self):
        super().__init__()

    def handle_events(self, events):
        for spr in self.sprites():
            # Check if the sprite has a `handle_event` method.
            if hasattr(spr, 'handle_events'):
                spr.handle_events(events)

    def draw(self, surface):
        """
                Overwrite Group's draw method and call sprite's OWN draw method.
                :param surface:
                :return:
                """
        for sprite in self.sprites():
            sprite.draw(surface)
