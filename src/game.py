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
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("My Platformer (Tipos de Inimigos)")

    clock = pygame.time.Clock()

    # ------------------------------------------------------
    # CONFIGURAÇÃO FIXA DO MUNDO
    # ------------------------------------------------------
    world_width  = screen_width * 5
    world_height = screen_height

    # Plataformas (x, y, w, h, collide_bottom)
    platforms_config = [
        {'x': 0,                'y': 550, 'width': world_width, 'height': 50,  'collide_bottom': True},
        {'x': 300,              'y': 450, 'width': 100,         'height': 20,  'collide_bottom': False},
        {'x': 800,              'y': 400, 'width': 150,         'height': 20,  'collide_bottom': True},
        {'x': 1400,             'y': 350, 'width': 200,         'height': 20,  'collide_bottom': False},
        {'x': 2000,             'y': 450, 'width': 120,         'height': 20,  'collide_bottom': True},
        {'x': 2800,             'y': 300, 'width': 180,         'height': 20,  'collide_bottom': False},
        {'x': 3500,             'y': 400, 'width': 150,         'height': 20,  'collide_bottom': True},
    ]

    # Inimigos: note o killable True para alguns
    enemies_config = [
        {'x': 500,  'y': 500, 'speed': 3, 'patrol_width': 200, 'killable': True},   # mata se pular por cima
        {'x': 1100, 'y': 500, 'speed': 2, 'patrol_width': 150, 'killable': False},  # invencível
        {'x': 1900, 'y': 500, 'speed': 3, 'patrol_width': 100, 'killable': True},
        {'x': 2600, 'y': 500, 'speed': 2, 'patrol_width': 200, 'killable': False},
        {'x': 3300, 'y': 500, 'speed': 3, 'patrol_width': 150, 'killable': True},
    ]

    player_spawn = (100, 500)
    finish_rect  = Rect(world_width - 50, 500, 50, 50)

    def spawn_level_and_player():
        lvl = Level(platforms_config, enemies_config)
        ply = Player(player_spawn[0], player_spawn[1], lives=3)
        return lvl, ply

    level, player = spawn_level_and_player()
    game_over = False
    victory   = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Reiniciar com R se já terminou
            if event.type == pygame.KEYDOWN and (game_over or victory):
                if event.key == pygame.K_r:
                    level, player = spawn_level_and_player()
                    game_over = False
                    victory   = False

        if not game_over and not victory:
            # 1) Guarda posição anterior da base do player
            previous_bottom = player.rect.bottom

            # 2) Atualiza player e inimigos
            player.update(level.platforms)
            level.update()

            # 3) Checa colisões com inimigos
            for enemy in level.enemies:
                if not enemy.alive:
                    continue

                if player.rect.colliderect(enemy.rect):
                    # colisão por cima?
                    if (enemy.killable and
                        player.vel_y > 0 and
                        previous_bottom <= enemy.rect.top and
                        player.rect.right > enemy.rect.left and
                        player.rect.left < enemy.rect.right):
                        
                        # kill no inimigo e bounce no player
                        enemy.kill()
                        player.vel_y = -player.jump_strength / 1.5
                        player.on_ground = False
                    else:
                        # player leva dano
                        player.lose_life()
                        if player.lives <= 0:
                            game_over = True
                        else:
                            level.reset_enemies()
                            player.reset()
                    break  # sai do loop de inimigos

            # 4) Checa vitória
            if player.rect.colliderect(finish_rect):
                victory = True

        # ------ CÁLCULO DA CÂMERA ------
        camera_x = player.rect.centerx - (screen_width // 2)
        if camera_x < 0:
            camera_x = 0
        if camera_x > world_width - screen_width:
            camera_x = world_width - screen_width

        # ------ DESENHO COM OFFSET ------
        screen.fill((100, 149, 237))

        # Desenha plataformas
        for plat in level.platforms:
            adjusted = Rect(
                plat.rect.x - camera_x,
                plat.rect.y,
                plat.rect.width,
                plat.rect.height
            )
            color = (150, 75, 0) if plat.collide_bottom else (0, 200, 0)
            pygame.draw.rect(screen, color, adjusted)

        # Desenha inimigos vivos
        for enemy in level.enemies:
            if not enemy.alive:
                continue
            adjusted = Rect(
                enemy.rect.x - camera_x,
                enemy.rect.y,
                enemy.rect.width,
                enemy.rect.height
            )
            col = (0, 0, 255) if not enemy.killable else (255, 0, 255)
            pygame.draw.rect(screen, col, adjusted)

        # Desenha área de chegada
        adjusted_finish = Rect(
            finish_rect.x - camera_x,
            finish_rect.y,
            finish_rect.width,
            finish_rect.height
        )
        pygame.draw.rect(screen, (255, 215, 0), adjusted_finish)

        # Desenha player
        adjusted_player = Rect(
            player.rect.x - camera_x,
            player.rect.y,
            player.rect.width,
            player.rect.height
        )
        pygame.draw.rect(screen, (255, 0, 0), adjusted_player)

        # HUD de vidas
        draw_text(screen, f"Vidas: {player.lives}", 36, 10, 10)

        # Mensagens de fim
        if game_over:
            draw_text(
                screen,
                "GAME OVER",
                72,
                screen_width//2 - 180,
                screen_height//2 - 36,
                (255, 50, 50)
            )
            draw_text(
                screen,
                "Pressione R para reiniciar",
                36,
                screen_width//2 - 180,
                screen_height//2 + 40,
                (255, 255, 255)
            )
        elif victory:
            draw_text(
                screen,
                "YOU WIN!",
                72,
                screen_width//2 - 150,
                screen_height//2 - 36,
                (50, 255, 50)
            )
            draw_text(
                screen,
                "Pressione R para jogar novamente",
                36,
                screen_width//2 - 200,
                screen_height//2 + 40,
                (255, 255, 255)
            )

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
