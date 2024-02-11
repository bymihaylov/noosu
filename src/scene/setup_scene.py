from pathlib import Path

import src.scene.download_beatmaps
from src.config import config
from src.noosu import parse_beatmap
from src.scene.scene import Scene
from src.scene.song_select_menu import SongSelectMenu
import os
import pygame


class Setup(Scene):
    def __init__(self):
        super().__init__()

        self.assets_dir: os.PathLike = config.assets_dir
        self.external_packs: os.PathLike = config.external_packs_dir
        self.font_path: os.PathLike = config.font_dir
        self.font = pygame.font.Font(config.font_dir / "MetronicPro.ttf", 16)
        self.text_surface = None
        self.text_position = (20, 20)
        self.render_text("Setup...")

        self.setup()

    def setup(self):
        ext_packs_was_initially_missing: bool = self.create_dir_if_missing(self.external_packs)
        assets_dir_was_initially_missing: bool = self.create_dir_if_missing(self.assets_dir)

        if ext_packs_was_initially_missing:
            self.switch_to_scene(src.scene.download_beatmaps.DownloadBeatmaps())

        if assets_dir_was_initially_missing:
            for archive in self.external_packs.glob('*.osz'):
                self.render_text(f"Extracting '{archive}'...")
                parse_beatmap.uncompress_archive(archive)
        else:
            self.extract_missing_packs()

        self.render_text(f"Setup...done", color=config.Colour.foreground)

        self.switch_to_scene(SongSelectMenu())


    def extract_missing_packs(self):
        external_packs_names = {item.stem for item in self.external_packs.glob('*.osz')}
        assets_names = {item.stem for item in self.assets_dir.iterdir()}

        missing_packs = external_packs_names - assets_names

        for pack_name in missing_packs:
            pack_path = self.external_packs / f"{pack_name}.osz"
            self.render_text(f"Extracting '{pack_path}'...")
            parse_beatmap.uncompress_archive(pack_path)

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        if self.text_surface != None:
            screen.fill(color=config.black)
            screen.blit(self.text_surface, self.text_position)

    def render_text(self, text: str, color: config.Colour = config.Colour.foreground):
        self.text_surface = self.font.render(text, True, color)

    def create_dir_if_missing(self, path: os.PathLike) -> bool:
        if not os.path.isdir(path):
            self.render_text(f"'{path}' not found. Creating '{path}' directory...")
            os.mkdir(path)
            return True
        return False
