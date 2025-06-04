# src/game.py

import pygame
import sys
from pygame import Rect

from player import Player
from level import Level

def draw_text(surface, text, size, x, y, color=(255,255,255)):
    font = pygame.font.SysFont(None, size)
    txt = font.render(text, True, color)
    surface.blit(txt, (x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("My Platformer")
    clock = pygame.time.Clock()

    # 1) Defina as plataformas e inimigos para o nível atual
    platforms = [
        Rect(0, 550, 800, 50),     # chão
        Rect(200, 450, 100, 20),   # plataforma intermediária
        Rect(400, 350, 150, 20),   # outra plataforma
    ]
    enemies_config = [
        {'x': 300, 'y': 500, 'speed': 3, 'patrol_width': 150},
        {'x': 600, 'y': 500, 'speed': 2, 'patrol_width': 100},
    ]
    player_spawn = (100, 500)

    # 2) Crie instâncias de Level e Player
    level = Level(platforms, enemies_config)
    player = Player(player_spawn[0], player_spawn[1], lives=3)

    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            # Atualiza lógica do player e do nível
            player.update(level.platforms)
            level.update()

            # Verifica colisão com qualquer inimigo
            for enemy in level.enemies:
                if player.rect.colliderect(enemy.rect):
                    player.lose_life()
                    if player.lives <= 0:
                        game_over = True
                    else:
                        # ainda tem vidas: reseta inimigos e player
                        level.reset_enemies()
                        player.reset()
                    break  # sai do for assim que colidiu

        # Desenha cena inteira
        screen.fill((100, 149, 237))
        level.draw(screen)
        player.draw(screen)

        # HUD: número de vidas
        draw_text(screen, f"Vidas: {player.lives}", 36, 10, 10)

        if game_over:
            # Mensagem de Game Over no centro da tela
            draw_text(
                screen,
                "GAME OVER",
                72,
                800//2 - 180,
                600//2 - 36,
                color=(255, 50, 50)
            )

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
