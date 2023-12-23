import config
import parse_beatmap
from scene import Scene
import os
from pathlib import Path
import pygame

class Setup(Scene):
    def __init__(self):

        self.assets_dir: os.PathLike  = config.assets_dir
        self.external_packs: os.PathLike =  config.external_packs_dir
        self.font_path : os.PathLike = config.font_dir
        self.font = pygame.font.Font(self.font_path / "MetronicPro.ttf", 28)
        self.text_surface = None
        self.text_position = (20, 20)
        self.render_text("Setup...")
    
    def setup(self):
        ext_packs_was_initially_missing: bool = self.create_dir_if_missing(self.external_packs)
        assets_dir_was_initially_missing: bool = self.create_dir_if_missing(self.assets_dir)
        
        if ext_packs_was_initially_missing:
            # requests logic to pull some .osz packs
            pass
        
        if assets_dir_was_initially_missing:
            # get in a list all .osz archives and pass on them 
            for archive in self.external_packs.glob('*.osz'):
                self.render_text(f"Extracting '{archive}'...")
                parse_beatmap.uncompress_archive(archive)
        else:
            self.extract_missing_packs()

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
        # for event in events:
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_RETURN:
        #             pass

    
    def update(self, dt):
        pass

    def render(self, screen):
        if self.text_surface != None:
            screen.fill(color=config.black)
            screen.blit(self.text_surface, self.text_position)

    def render_text(self, text: str, color: tuple[int, int, int] = config.white):
        self.text_surface = self.font.render(text, True, color)


    def does_dir_exists(self, path: os.PathLike) -> bool:
        return os.path.isdir(path)
    
    def create_dir_if_missing(self, path: os.PathLike) -> bool:
        if not self.does_dir_exists(path):
            msg = f"'{path}' not found. Creating '{path}' directory..."
            self.render_text(msg)
            os.mkdir(path)
            return True
        return False