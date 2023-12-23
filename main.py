import config
from setup import Setup
import pygame

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()  ## For sound
    pygame.display.set_caption("noosu!")

    screen = pygame.display.set_mode((config.width, config.height))
    clock = pygame.time.Clock()
    running = True
    scene = Setup()
    scene.setup()

    ## Game loop
    while running:
        dt = clock.tick(config.fps)
        events = list(pygame.event.get())

        scene.handle_events(events)
        scene.update(dt)
        scene.render(screen)
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.flip()

    pygame.quit()