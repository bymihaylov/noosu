import os
from pathlib import Path
import pygame
from src.config import config
from src.scene.scene import Scene
from src.noosu.parse_beatmap import parse_osu_file
from src.scene.playfield import Playfield

class SongSelectMenu(Scene):
    def __init__(self):
        super().__init__()
        self.songs_folders = os.listdir(config.assets_dir)
        self.song_index = 0
        self.difficulty_index = 0
        self.noosu_obj = None
        self.image = None
        self.image_rect = None
        self.osu_files = []
        self.font_path = config.font_dir
        self.font = pygame.font.Font(Path(self.font_path) / "MetronicPro.ttf", 32)
        self.song_caption_text = None
        self.song_caption_text_rect = None
        self.load_song()
        self.should_render_img_and_text = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.play_choosen_song()
                elif event.key == pygame.K_RIGHT:
                    self.song_index = (self.song_index + 1) % len(self.songs_folders)
                    self.load_song()
                elif event.key == pygame.K_LEFT:
                    self.song_index = (self.song_index - 1) % len(self.songs_folders)
                    self.load_song()

                elif event.key == pygame.K_DOWN:
                    self.difficulty_index = (self.difficulty_index + 1) % len(self.osu_files)
                elif event.key == pygame.K_UP:
                    self.difficulty_index = (self.difficulty_index - 1) % len(self.osu_files)

    def load_song(self):
        song_folder = config.assets_dir / self.songs_folders[self.song_index]
        self.osu_files = list(song_folder.glob("*.osu"))
        self.noosu_obj = parse_osu_file(self.osu_files[0])
        self.image = pygame.image.load(self.noosu_obj.image_path)
        self.image = pygame.transform.smoothscale(self.image, config.song_select_menu_image_resolution)
        self.image_rect = self.image.get_rect(center=(config.width / 2, config.height / 2 - 40 * 3))
        self.render_text(self.noosu_obj.metadata["TitleUnicode"], config.green)

    def render(self, screen):
        screen.fill(color=config.black)

        if self.should_render_img_and_text:
            screen.blit(self.image, self.image_rect)
            screen.blit(self.song_caption_text, self.song_caption_text_rect)
            self.render_osu_files(screen)

    def render_text(self, text: str, color: tuple[int, int, int] = config.white):
        self.song_caption_text = self.font.render(text, True, color)
        self.song_caption_text_rect = self.song_caption_text.get_rect(center=(config.width / 2, config.height / 2 + 40 * 8))

    def render_osu_files(self, screen):
        y_offset = config.height / 2 + 40 * 8 + 100
        for i, osu_file in enumerate(self.osu_files):
            text = self.get_difficulty(osu_file)
            if i == self.difficulty_index:
                text = f">  {text}"
            text_surface = self.font.render(text, True, config.white)
            text_rect = text_surface.get_rect(center=(config.width / 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 40

    def get_difficulty(self, osu_file):
        str = osu_file.stem
        start_index = str.find("[")
        end_index = str.find("]", start_index + 1)

        if start_index != -1 and end_index != -1 and end_index + 1 <= len(str):
            return str[start_index:end_index + 1]

        return str


    def play_choosen_song(self):
        self.should_render_img_and_text = False
        self.noosu_obj = parse_osu_file(self.osu_files[self.difficulty_index])
        self.switch_to_scene(Playfield(self.noosu_obj))