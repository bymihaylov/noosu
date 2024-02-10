import pygame

from src.config import config
from src.config import custom_events


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = None
        self.rect = None
        self.active = False
        self.font = pygame.font.Font(config.font_dir / "MetronicPro.ttf", 32)
        self.text = ""
        self.width = 500
        self.render_text()

    def render_text(self):
        text_surface = self.font.render(self.text, True, config.Colour.foreground)
        self.image = pygame.Surface((max(self.width, text_surface.get_width() + 10), text_surface.get_height() + 10),
                                    pygame.SRCALPHA)

        self.image.blit(text_surface, (5, 5))
        pygame.draw.rect(self.image, config.Colour.foreground, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft=((config.width - self.width) / 2, 40))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
                self.render_text()  # Render text when box becomes active
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    pygame.event.post(pygame.event.Event(custom_events.TEXT_INPUT_SUBMITTED, {"text": self.text}))
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_text()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
