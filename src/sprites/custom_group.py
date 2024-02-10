from pygame.sprite import Group

"""
I need a custom draw method for SongMetadataButton
"""
class CustomGroup(Group):
    def __init__(self):
        super().__init__()

    def draw(self, surface):
        """
                Overwrite Group's draw method and call sprite's OWN draw method.
                :param surface:
                :return:
                """
        for sprite in self.sprites():
            sprite.draw(surface)
