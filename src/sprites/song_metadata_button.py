import pygame

from src.config import config, custom_events


class SongMetadataButton(pygame.sprite.Sprite):
    def __init__(self, metadata: tuple[str, str, str, str], left: int, top: int):
        super().__init__()
        self.metadata = {"title": metadata[0], "artist": metadata[1], "difficulty": metadata[2], "set_id": metadata[3]}

        self.font = pygame.font.Font(config.font_dir / "MetronicPro.ttf", 32)
        self.title_surface = self.font.render(f"Title: {self.metadata['title']}", True, config.Colour.light_purple)
        self.artist_surface = self.font.render(f"Artist: {self.metadata['artist']}", True, config.Colour.light_purple)
        self.difficulty_surface = self.font.render(f"Difficulty: {self.metadata['difficulty']}", True, config.Colour.light_purple)

        self.is_downloaded = False

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
        if not self.is_downloaded:
            # Draw the rectangle around the text surfaces
            fill_color = config.Colour.light_purple if self.hovered else config.Colour.purple
            pygame.draw.rect(surface, fill_color, self.rect, 8)

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
        else:
            fill_color = config.Colour.light_purple
            pygame.draw.rect(surface, fill_color, self.rect, 8)
            downloaded_surface = self.font.render("Downloaded!", True, config.Colour.foreground)
            x = self.rect.x + (self.rect.width - downloaded_surface.get_width()) // 2
            y = self.rect.y + (self.rect.height - downloaded_surface.get_height()) // 2
            surface.blit(downloaded_surface, (x, y))

    def update(self):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
                pygame.event.post(pygame.event.Event(custom_events.SET_ID_SUBMITTED, self.metadata))
            elif event.type == custom_events.DOWNLOAD_PACK_COMPLETED:
                if event.set_id == self.metadata["set_id"]:
                    self.is_downloaded = True
