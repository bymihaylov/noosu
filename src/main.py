from pathlib import Path

from config import config
from src.scene.playfield import Playfield
from src.scene.setup_scene import Setup
import pygame

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("noosu!")

    screen = pygame.display.set_mode((config.width, config.height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    running = True

    scene = Playfield(Path("assets/355322 nekodex - circles!/nekodex - circles! (pishifat) [insane!].osu"))
    # scene = Setup()

    scene.setup()

    ## Game loop
    while running:
        dt = clock.tick(config.fps)
        events = list(pygame.event.get())

        scene.handle_events(events)
        scene.update(dt)
        scene.render(screen)

        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                running = False

        pygame.display.flip()

    pygame.quit()
# project deadline: 11.02
