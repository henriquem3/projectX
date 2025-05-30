import pygame
import sys
from player import Player
from enemy import Enemy

def draw_text(surface, text, size, x, y, color=(255,255,255)):
    font = pygame.font.SysFont(None, size)
    txt = font.render(text, True, color)
    surface.blit(txt, (x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("My Platformer")
    clock = pygame.time.Clock()

    # pontos de spawn e entidades
    player = Player(100, 400, lives=3)
    ground = pygame.Rect(0, 550, 800, 50)
    platforms = [ground]
    enemy = Enemy(300, 500, speed=3, patrol_width=200)

    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            # lógica de jogo normal
            player.update(platforms)
            enemy.update()

            # colisão
            if player.rect.colliderect(enemy.rect):
                player.lose_life()
                if player.lives <= 0:
                    game_over = True

        # desenho
        screen.fill((100, 149, 237))
        pygame.draw.rect(screen, (0, 200, 0), ground)
        enemy.draw(screen)
        player.draw(screen)

        # vidas na tela (HUD)
        draw_text(screen, f"Vidas: {player.lives}", 36, 10, 10)

        if game_over:
            # mensagem centralizada de Game Over
            draw_text(screen, "GAME OVER", 72,
                      800//2 - 180, 600//2 - 36, color=(255,50,50))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
