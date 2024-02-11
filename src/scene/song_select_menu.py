import os
from pathlib import Path
import pygame
from src.config import config
from src.scene.download_beatmaps import DownloadBeatmaps
from src.scene.scene import Scene
from src.noosu.parse_beatmap import parse_osu_file
from src.scene.playfield import Playfield

class SongSelectMenu(Scene):
    def __init__(self):
        super().__init__()
        pygame.mouse.set_visible(True)
        self.songs_folders = os.listdir(config.assets_dir)
        self.song_index = 0
        self.difficulty_index = 0
        self.noosu_obj = None
        self.image = None
        self.image_rect = None
        self.osu_files = []
        self.font_path = config.font_dir
        self.font = pygame.font.Font(config.font_dir / "MetronicPro.ttf", 32)
        self.song_caption_text = None
        self.song_caption_text_rect = None
        self.load_song()
        self.should_render_img_and_text = True

        self.download_img = pygame.image.load(config.ui_dir / "download_beatmaps.tiff")
        self.download_img_rect = self.download_img.get_rect()
        self.download_img_hover = pygame.image.load(config.ui_dir / "download_beatmaps-hover.tiff")
        self.download_img_hover_rect = self.download_img.get_rect()
        self.is_dowload_hovered = False

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
            if event.type == pygame.MOUSEBUTTONDOWN and self.is_dowload_hovered:
                self.switch_to_scene(DownloadBeatmaps())

    def load_song(self):
        song_folder = config.assets_dir / self.songs_folders[self.song_index]
        self.osu_files = list(song_folder.glob("*.osu"))
        self.noosu_obj = parse_osu_file(self.osu_files[0])
        pygame.mixer.music.load(self.noosu_obj.general["AudioFilename"])
        pygame.mixer.music.play()
        if self.noosu_obj.image_path:
            self.image = pygame.image.load(self.noosu_obj.image_path)
            self.image = pygame.transform.smoothscale(self.image, config.song_select_menu_image_resolution)
            self.image_rect = self.image.get_rect(center=(config.width / 2, config.height / 2 - 40 * 3))
        text = f'{self.noosu_obj.metadata["ArtistUnicode"]} - {self.noosu_obj.metadata["TitleUnicode"]}'

        self.render_text(text, config.Colour.light_purple)

    def update(self, dt: int):
        self.is_dowload_hovered = self.download_img_rect.collidepoint(pygame.mouse.get_pos())

    def render(self, screen):
        # screen.fill(color=config.Colour.backround)
        screen.blit(self.gradient_light, self.gradient_light_rect)

        if self.should_render_img_and_text:
            if self.noosu_obj.image_path:
                screen.blit(self.image, self.image_rect)
            screen.blit(self.song_caption_text, self.song_caption_text_rect)
            self.render_osu_files(screen)

            # if config.CLIENT_ID and config.CLIENT_SECRET:
            #     if self.is_dowload_hovered:
            #         screen.blit(self.download_img_hover, self.download_img_hover_rect)
            #     else:
            #         screen.blit(self.download_img, self.download_img_rect)
            if self.is_dowload_hovered:
                screen.blit(self.download_img_hover, self.download_img_hover_rect)
            else:
                screen.blit(self.download_img, self.download_img_rect)

    def render_text(self, text: str, color: config.Colour = config.Colour.foreground):
        self.song_caption_text = self.font.render(text, True, color)
        self.song_caption_text_rect = self.song_caption_text.get_rect(center=(config.width / 2, config.height / 2 + 40 * 8))

    def render_osu_files(self, screen):
        y_offset = config.height / 2 + 40 * 8 + 100
        for i, osu_file in enumerate(self.osu_files):
            text = self.get_difficulty(osu_file)
            if i == self.difficulty_index:
                text = f">  {text}"
            text_surface = self.font.render(text, True, config.Colour.foreground)
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