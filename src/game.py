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

    # 1) Configuração do nível atual
    platforms_config = [
        {'x': 0,   'y': 550, 'width': 800, 'height': 50,  'collide_bottom': True},  # chão
        {'x': 200, 'y': 450, 'width': 100, 'height': 20,  'collide_bottom': False}, # one-way
        {'x': 400, 'y': 350, 'width': 150, 'height': 20,  'collide_bottom': True},  # sólida
    ]
    enemies_config = [
        {'x': 300, 'y': 500, 'speed': 3, 'patrol_width': 150},
        {'x': 600, 'y': 500, 'speed': 2, 'patrol_width': 100},
    ]
    player_spawn = (100, 500)

    # 1.1) Define a "chegada" (área de vitória)
    # Por exemplo, um quadrado 50×50 em (750, 500)
    finish_rect = Rect(750, 500, 50, 50)

    # 2) Cria Level e Player
    level = Level(platforms_config, enemies_config)
    player = Player(player_spawn[0], player_spawn[1], lives=3)

    game_over = False
    victory = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over and not victory:
            # Atualiza lógica de player e level
            player.update(level.platforms)
            level.update()

            # Verifica colisão com inimigos
            for enemy in level.enemies:
                if player.rect.colliderect(enemy.rect):
                    player.lose_life()
                    if player.lives <= 0:
                        game_over = True
                    else:
                        level.reset_enemies()
                        player.reset()
                    break

            # Verifica colisão com a área de chegada
            if player.rect.colliderect(finish_rect):
                victory = True

        # Desenha a cena
        screen.fill((100, 149, 237))
        level.draw(screen)

        # Desenha a área de chegada (por exemplo, cor amarela)
        pygame.draw.rect(screen, (255, 215, 0), finish_rect)

        player.draw(screen)

        # HUD: vidas
        draw_text(screen, f"Vidas: {player.lives}", 36, 10, 10)

        if game_over:
            draw_text(screen, "GAME OVER", 72, 800//2 - 180, 600//2 - 36, (255, 50, 50))
        elif victory:
            draw_text(screen, "YOU WIN!", 72, 800//2 - 150, 600//2 - 36, (50, 255, 50))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
