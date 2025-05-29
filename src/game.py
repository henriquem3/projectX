import pygame
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("My Platformer")

    clock = pygame.time.Clock()

    # Loop principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Preenche o fundo com uma cor
        screen.fill((100, 149, 237))  # cornflower blue

        # Atualiza o display
        pygame.display.flip()

        # Limita a 60 FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
