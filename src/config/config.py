import os
from enum import Enum
from pathlib import Path
from dotenv import load_dotenv

import pygame.color

assets_dir = Path("assets")
external_packs_dir = Path("external_packs")
font_dir = Path("fonts")
ui_dir = Path("ui")

song_select_menu_image_resolution: tuple[int, int] = 1280, 720

load_dotenv()
CLIENT_ID = os.getenv("OSU_API_CLIENT_ID")
CLIENT_SECRET = os.getenv("OSU_API_CLIENT_SECRET")

## 640x480
# width = 640
# height = 480
## 1920x1080
width = 1920
height = 1080
## 1366x768
# width = 1366
# height = 768
## 1536x864
# width = 1536
# height = 868

fps = 60

# Colours
black = 0, 0, 0
red = 250, 0, 0
green = 0, 250, 0
blue = 0, 0, 250
white = 250, 250, 250


class Colour(pygame.color.Color):
    backround = 53, 47, 68
    purple = 92, 84, 112
    light_purple = 185, 180, 199
    foreground = 250, 240, 230
