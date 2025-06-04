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

    # --- CONFIGURAÇÃO FIXA DO NÍVEL ---
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

    # Área de chegada
    finish_rect = Rect(750, 500, 50, 50)

    def spawn_level_and_player():
        """Cria e retorna um novo Level e Player com as configurações iniciais."""
        lvl = Level(platforms_config, enemies_config)
        ply = Player(player_spawn[0], player_spawn[1], lives=3)
        return lvl, ply

    # --- ESTADO DE JOGO ---
    level, player = spawn_level_and_player()
    game_over = False
    victory = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Se estiver em Game Over ou Victory, permitir restart com R
            if event.type == pygame.KEYDOWN and (game_over or victory):
                if event.key == pygame.K_r:
                    # Reset total: recria nível e player e zera flags
                    level, player = spawn_level_and_player()
                    game_over = False
                    victory = False

        if not game_over and not victory:
            # --- LÓGICA NORMAL ---
            player.update(level.platforms)
            level.update()

            # Colisão jogador-inimigo
            for enemy in level.enemies:
                if player.rect.colliderect(enemy.rect):
                    player.lose_life()
                    if player.lives <= 0:
                        game_over = True
                    else:
                        level.reset_enemies()
                        player.reset()
                    break

            # Colisão com área de chegada
            if player.rect.colliderect(finish_rect):
                victory = True

        # --- DESENHO ---
        screen.fill((100, 149, 237))
        level.draw(screen)

        # Desenha área de chegada
        pygame.draw.rect(screen, (255, 215, 0), finish_rect)

        player.draw(screen)

        # HUD de vidas
        draw_text(screen, f"Vidas: {player.lives}", 36, 10, 10)

        # Mensagens de fim
        if game_over:
            draw_text(screen, "GAME OVER", 72, 800//2 - 180, 600//2 - 36, (255, 50, 50))
            draw_text(screen, "Pressione R para reiniciar", 36,
                      800//2 - 180, 600//2 + 40, (255, 255, 255))
        elif victory:
            draw_text(screen, "YOU WIN!", 72, 800//2 - 150, 600//2 - 36, (50, 255, 50))
            draw_text(screen, "Pressione R para jogar novamente", 36,
                      800//2 - 200, 600//2 + 40, (255, 255, 255))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
