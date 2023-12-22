import config
from parse_beatmap import uncompress_beatmap_to_dest
from pathlib import Path
import pygame

if __name__ == "__main__":

    uncompress_beatmap_to_dest("external_packs/891596 Noisestorm - Crab Rave.osz")

    pygame.init()
    pygame.mixer.init()  ## For sound
    screen = pygame.display.set_mode((config.width, config.height))
    pygame.display.set_caption("noosu!")
    clock = pygame.time.Clock()  ## For syncing the FPS

    ## Game loop
    running = True
    while running:
        clock.tick(config.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()