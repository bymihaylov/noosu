import src.scene.song_select_menu
from src.config import config
from src.config import custom_events
from src.noosu import bit_flags
from src.scene.scene import Scene
from src.noosu.noosu_object import NoosuObject
from src.sprites.hit_circle import HitCircle
import pygame

"""
In osu!, circle size changes the size of hit circles and sliders, with higher values creating smaller hit objects. 
Spinners are unaffected by circle size. Circle size is derived through the following formula:

r = 54.4 - 4.48 * CS

Where r is the radius measured in osu!pixels, and CS is the circle size value.
-------
source: https://osu.ppy.sh/wiki/en/Beatmap/Circle_size
"""



class Playfield(Scene):
    def __init__(self, noosu_obj: NoosuObject):
        super().__init__()

        pygame.mouse.set_visible(False)

        self.gamefield_width = 640
        self.gamefield_height = 480
        self.gamefield_shift = 8

        # https://www.reddit.com/r/osugame/comments/ff6n01/resolution_of_the_playfield/
        self.playfield_height = int(0.8 * config.height)
        self.playfield_width = int(self.playfield_height * 4 / 3)

        self.playfield_top_left = (
            (config.width - self.playfield_width) // 2,
            (config.height - self.playfield_height) // 2
        )
        self.playfield_bottom_right = (
            self.playfield_top_left[0] + self.playfield_width,
            self.playfield_top_left[1] + self.playfield_height
        )

        self.playfield_centre = (
            (self.playfield_top_left[0] + self.playfield_bottom_right[0]) // 2,
            (self.playfield_top_left[1] + self.playfield_bottom_right[1]) // 2
        )

        self.noosu: NoosuObject = noosu_obj
        self.all_sprites_list = pygame.sprite.Group()
        self.hit_obj_index = 0

        self.cursor_img = pygame.image.load(config.ui_dir / "cursor.tiff")
        cursor_img_radius: float = 54.4 - 4.48 * self.noosu.difficulty["CircleSize"]
        scaled_size: tuple[int, int] = int(cursor_img_radius * 4), int(cursor_img_radius * 4)
        self.cursor_img = pygame.transform.smoothscale(self.cursor_img, scaled_size).convert_alpha()
        # self.cursor_img_rect = self.cursor_img.get_rect()
        self.cursor_pos = [pygame.mouse.get_pos()]

        self.score = 0
        self.font_path = config.font_dir
        self.font = pygame.font.Font(config.font_dir / "MetronicPro.ttf", 32)
        self.score_text = None
        self.score_text_rect = None
        self.score_text_position = 1920 - 40 * 6, 1080

        self.setup()

    def setup(self):
        pygame.mixer.music.load(self.noosu.general["AudioFilename"])
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_endevent(custom_events.SONG_ENDED)

    def handle_events(self, events):
        for event in events:
           if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.K_z or pygame.K_x:
                for hit_circle in self.all_sprites_list:
                    if hit_circle.rect.collidepoint(pygame.mouse.get_pos()):
                        self.all_sprites_list.remove(hit_circle)
                        self.score += 1
                        self.str_to_surface(f"Score: {self.score}")
           elif event.type == custom_events.SONG_ENDED:
               self.switch_to_scene(src.scene.song_select_menu.SongSelectMenu())

    def gamefield_to_screenspace(self, gamefield: tuple[int, int]) -> tuple[int, int]:
        """
        A function that converts gamefield coordinates to screen space.
        Args:
            gamefield: tuple[int, int]

        Returns:
            screenspace: tuple[int, int]
        """

        scale_x = self.playfield_width / 512
        scale_y = self.playfield_height / 384

        # screenspace_x = int((gamefield[0] * scale_x))
        # screenspace_y = int((gamefield[1] * scale_y))
        screenspace_x = int((gamefield[0] * scale_x) + self.playfield_top_left[0])
        screenspace_y = int((gamefield[1] * scale_y) + self.playfield_top_left[1] + self.gamefield_shift * scale_y)

        return screenspace_x, screenspace_y

    def screenspace_to_gamefield(self, screenspace: tuple[int, int]) -> tuple[int, int]:
        """
        A function that converts screen space coordinates to gamefield.
        Args:
            screenspace: tuple[int, int]

        Returns:
            gamefield: tuple[int, int]
        """
        # Calculate scaling factors for x and y
        scale_x = 512 / self.playfield_width
        scale_y = 384 / self.playfield_height

        # Convert screen space coordinates to gamefield
        gamefield_x = int((screenspace[0] - self.playfield_top_left[0]) * scale_x)
        gamefield_y = int((screenspace[1] - self.playfield_top_left[1] - self.gamefield_shift * scale_y) * scale_y)

        return gamefield_x, gamefield_y


    def update(self, dt):
        # Get the current time when updating
        current_time = pygame.mixer.music.get_pos()

        # Iterate through hit objects to find the one that corresponds to the current time
        while self.hit_obj_index < len(self.noosu.hit_objects):
            hit_object = self.noosu.hit_objects[self.hit_obj_index]
            if hit_object.time > current_time:
                break  # Found the hit object corresponding to the current time
            self.hit_obj_index += 1

        # If there are more hit objects and the current hit object is a hit circle
        if self.hit_obj_index < len(self.noosu.hit_objects) and \
                self.noosu.hit_objects[self.hit_obj_index].type & bit_flags.HitObjectType.HIT_CIRCLE:
            hit_object = self.noosu.hit_objects[self.hit_obj_index]
            gamefield_coords = hit_object.xy_position

            # Convert gamefield coordinates to screen space
            screenspace_coords = self.gamefield_to_screenspace(gamefield_coords)

            # Create and add HitCircle object to the sprite group
            hit_circle = HitCircle(screenspace_coords, self.noosu.difficulty["CircleSize"])
            self.all_sprites_list.add(hit_circle)

        x, y = pygame.mouse.get_pos()
        x -= self.cursor_img.get_width() / 2
        y -= self.cursor_img.get_height() / 2

        self.cursor_pos = [x, y]

    def str_to_surface(self, text: str, color: config.Colour = config.Colour.foreground):
        self.score_text = self.font.render(text, True, color)
        self.score_text_rect = self.score_text.get_rect(center=self.score_text_position)

    def render(self, screen):
        # screen.fill(config.Colour.backround)
        screen.blit(self.gradient_dark, self.gradient_dark_rect)
        if self.score_text and self.score_text_rect:
            screen.blit(self.score_text, self.score_text_rect)
        self.all_sprites_list.draw(screen)
        screen.blit(self.cursor_img, self.cursor_pos)


