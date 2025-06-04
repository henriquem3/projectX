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
    pygame.display.set_caption("My Platformer (Mundo Estendido)")

    clock = pygame.time.Clock()

    # ------------------------------------------------------
    # 1) DEFINIÇÕES FIXAS DO MUNDO
    # ------------------------------------------------------

    # Largura do mundo: 5×800 = 4000px; altura permanece 600px
    world_width  = screen_width * 5
    world_height = screen_height

    # Configurações de plataformas (x, y, w, h, collide_bottom)
    # • A primeira plataforma é o "chão" contínuo por toda a largura do mundo
    platforms_config = [
        {'x': 0,                'y': 550, 'width': world_width, 'height': 50,  'collide_bottom': True},   # chão
        {'x': 300,              'y': 450, 'width': 100,         'height': 20,  'collide_bottom': False},  # one-way
        {'x': 800,              'y': 400, 'width': 150,         'height': 20,  'collide_bottom': True},   # sólida
        {'x': 1400,             'y': 350, 'width': 200,         'height': 20,  'collide_bottom': False},  # one-way
        {'x': 2000,             'y': 450, 'width': 120,         'height': 20,  'collide_bottom': True},   # sólida
        {'x': 2800,             'y': 300, 'width': 180,         'height': 20,  'collide_bottom': False},  # one-way
        {'x': 3500,             'y': 400, 'width': 150,         'height': 20,  'collide_bottom': True},   # sólida
    ]

    # Configurações de inimigos espalhados no mundo
    enemies_config = [
        {'x': 500,  'y': 500, 'speed': 3, 'patrol_width': 200},
        {'x': 1100, 'y': 500, 'speed': 2, 'patrol_width': 150},
        {'x': 1900, 'y': 500, 'speed': 3, 'patrol_width': 100},
        {'x': 2600, 'y': 500, 'speed': 2, 'patrol_width': 200},
        {'x': 3300, 'y': 500, 'speed': 3, 'patrol_width': 150},
    ]

    # Ponto de spawn inicial do player (x, y)
    player_spawn = (100, 500)

    # Área de chegada: um retângulo 50×50 em x = world_width - 50
    finish_rect = Rect(world_width - 50, 500, 50, 50)

    # ------------------------------------------------------
    # 2) FUNÇÃO AUXILIAR PARA RESETAR LEVEL E PLAYER
    # ------------------------------------------------------
    def spawn_level_and_player():
        lvl = Level(platforms_config, enemies_config)
        ply = Player(player_spawn[0], player_spawn[1], lives=3)
        return lvl, ply

    # ------------------------------------------------------
    # 3) INICIALIZAÇÃO DO JOGO
    # ------------------------------------------------------
    level, player = spawn_level_and_player()
    game_over = False
    victory   = False

    # ------------------------------------------------------
    # 4) LOOP PRINCIPAL
    # ------------------------------------------------------
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Se já for game_over ou victory, permitir reiniciar com R
            if event.type == pygame.KEYDOWN and (game_over or victory):
                if event.key == pygame.K_r:
                    level, player = spawn_level_and_player()
                    game_over = False
                    victory   = False

        # ------ LÓGICA DO JOGO (quando não está em fim de jogo) ------
        if not game_over and not victory:
            # 1. Atualiza posicao do player considerando plataformas "one-way" e sólidas
            player.update(level.platforms)

            # 2. Atualiza todos os inimigos do nível
            level.update()

            # 3. Checa colisão jogador × inimigos
            for enemy in level.enemies:
                if player.rect.colliderect(enemy.rect):
                    player.lose_life()
                    if player.lives <= 0:
                        game_over = True
                    else:
                        level.reset_enemies()
                        player.reset()
                    break

            # 4. Checa colisão jogador × finish_rect
            if player.rect.colliderect(finish_rect):
                victory = True

        # ------ CÁLCULO DA CÂMERA ------
        # Queremos centralizar a câmera no player (horizontalmente),
        # mas nunca sair do mundo [0..world_width - screen_width].
        camera_x = player.rect.centerx - (screen_width // 2)
        if camera_x < 0:
            camera_x = 0
        if camera_x > world_width - screen_width:
            camera_x = world_width - screen_width

        # (Não vamos mover verticalmente: world_height = screen_height,
        #  então camera_y = 0 sempre – se no futuro ampliar vertical, adicionar análogo.)

        # ------ DESENHO DE TODA A CENA (com offset da câmera) ------
        screen.fill((100, 149, 237))

        # 1. Desenha cada plataforma na posição (plat.rect.x - camera_x, plat.rect.y)
        for plat in level.platforms:
            adjusted_rect = Rect(
                plat.rect.x - camera_x,
                plat.rect.y,
                plat.rect.width,
                plat.rect.height
            )
            # cor conforme plat.collide_bottom (Platform.draw usa marrom ou verde),
            # mas aqui basta checar a flag:
            color = (150, 75, 0) if plat.collide_bottom else (0, 200, 0)
            pygame.draw.rect(screen, color, adjusted_rect)

        # 2. Desenha cada inimigo na posição ajustada
        for enemy in level.enemies:
            adjusted_rect = Rect(
                enemy.rect.x - camera_x,
                enemy.rect.y,
                enemy.rect.width,
                enemy.rect.height
            )
            pygame.draw.rect(screen, (0, 0, 255), adjusted_rect)

        # 3. Desenha a área de chegada (finish_rect) ajustada
        adjusted_finish = Rect(
            finish_rect.x - camera_x,
            finish_rect.y,
            finish_rect.width,
            finish_rect.height
        )
        pygame.draw.rect(screen, (255, 215, 0), adjusted_finish)

        # 4. Desenha o player (vermelho) na posição ajustada
        adjusted_player = Rect(
            player.rect.x - camera_x,
            player.rect.y,
            player.rect.width,
            player.rect.height
        )
        pygame.draw.rect(screen, (255, 0, 0), adjusted_player)

        # 5. Desenha HUD de vidas (sem offset)
        draw_text(screen, f"Vidas: {player.lives}", 36, 10, 10)

        # 6. Se game_over ou victory, desenha mensagem no centro
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
