import pygame
import sys
from player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("My Platformer")

    clock = pygame.time.Clock()

    # Cria o player e uma plataforma estática
    player = Player(100, 400)
    ground = pygame.Rect(0, 550, 800, 50)
    platforms = [ground]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Atualiza o player
        player.update(platforms)

        # Desenha tudo
        screen.fill((100, 149, 237))
        # plataforma
        pygame.draw.rect(screen, (0, 200, 0), ground)
        # player
        player.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
