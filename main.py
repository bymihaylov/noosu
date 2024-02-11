from src.config import config
from src.scene.setup_scene import Setup
import pygame

if __name__ == "__main__":

    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("noosu!")

    screen = pygame.display.set_mode((config.width, config.height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    running = True

    scene = Setup()

    ## Game loop
    while running:
        dt = clock.tick(config.fps)
        events = list(pygame.event.get())

        scene.handle_events(events)
        scene.update(dt)
        scene.render(screen)

        scene = scene.next

        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                running = False

        pygame.display.flip()

    pygame.quit()
# project deadline: 11.02
