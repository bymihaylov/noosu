import pygame

width = 1280
height = 720
fps = 60

# Colours
black = 0, 0, 0

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()  ## For sound
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("noosu!")
    clock = pygame.time.Clock()  ## For syncing the FPS

    ## Game loop
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()