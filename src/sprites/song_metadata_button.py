import pygame

from src.config import config


class SongMetadataButton(pygame.sprite.Sprite):
    def __init__(self, title: str, artist: str, difficulty: str, left: int, top: int):
        super().__init__()
        self.font = pygame.font.Font(config.font_dir / "MetronicPro.ttf", 32)
        self.title_surface = self.font.render(f"Title: {title}", True, config.Colour.light_purple)
        self.artist_surface = self.font.render(f"Artist: {artist}", True, config.Colour.light_purple)
        self.difficulty_surface = self.font.render(f"Difficulty: {difficulty}", True, config.Colour.light_purple)

        text_width = max(self.title_surface.get_width(),
                         self.artist_surface.get_width(),
                         self.difficulty_surface.get_width()
                         )
        text_height = (self.title_surface.get_height() +
                       self.artist_surface.get_height() +
                       self.difficulty_surface.get_height()
                       )
        self.padding = 40
        self.rect = pygame.Rect(left, top, text_width + 2 * self.padding, text_height + 2 * self.padding)
        self.hovered = False

    def draw(self, surface):
        # Draw the rectangle around the text surfaces
        fill_color = config.Colour.light_purple if self.hovered else config.Colour.purple
        pygame.draw.rect(surface, fill_color, self.rect, 2)

        # Blit the text surfaces onto the surface
        surface.blit(self.title_surface, (self.rect.x + self.padding, self.rect.y + self.padding))
        surface.blit(self.artist_surface,
                     (self.rect.x + self.padding,
                      self.rect.y + self.title_surface.get_height() + self.padding))
        surface.blit(self.difficulty_surface,
                     (self.rect.x + self.padding,
                      self.rect.y +
                      self.title_surface.get_height() +
                      self.artist_surface.get_height() +
                      self.padding)
                     )

    def update(self):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())

