import pygame
import config


class HitCircle(pygame.sprite.Sprite):
    def __init__(self, color: tuple[int, int, int], position: tuple[int, int], radius: float):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the player, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface((radius * 2, radius * 2))
        self.image.fill(config.white)
        self.image.set_colorkey(config.white)

        self.color = color

        # Draw the hit circle
        pygame.draw.circle(self.image, self.color, (radius, radius), radius)

        self.rect = self.image.get_rect(center=position)
