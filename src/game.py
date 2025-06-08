import pygame
import sys
from enum import Enum
from pygame import Rect

from player import Player
from level import Level

# ——————————————————————————————————————————
class GameState(Enum):
    MAIN_MENU = 1
    PLAYING   = 2
    PAUSED    = 3
    GAME_OVER = 4
    VICTORY   = 5

# ——————————————————————————————————————————
def draw_text(surface, text, size, x, y, color=(255,255,255)):
    font = pygame.font.SysFont(None, size)
    txt  = font.render(text, True, color)
    surface.blit(txt, (x, y))

# ——————————————————————————————————————————
def main():
    pygame.init()
    W, H = 800, 600
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("My Platformer with States")
    clock = pygame.time.Clock()

    # — Mundo 5× largo, mesmas configs de Level/Player/Finish
    world_w = W * 5

    platforms_cfg = [
        {'x': 0,    'y':550,'width':world_w,'height':50, 'collide_bottom':True},
        {'x': 300,  'y':450,'width':100,       'height':20, 'collide_bottom':False},
        {'x': 800,  'y':400,'width':150,       'height':20, 'collide_bottom':True},
        {'x': 1400, 'y':350,'width':200,       'height':20, 'collide_bottom':False},
        {'x': 2000, 'y':450,'width':120,       'height':20, 'collide_bottom':True},
        {'x': 2800, 'y':300,'width':180,       'height':20, 'collide_bottom':False},
        {'x': 3500, 'y':400,'width':150,       'height':20, 'collide_bottom':True},
    ]
    enemies_cfg = [
        {'x': 500,  'y':500,'speed':3,'patrol_width':200,'killable':True},
        {'x': 1100, 'y':500,'speed':2,'patrol_width':150,'killable':False},
        {'x': 1900, 'y':500,'speed':3,'patrol_width':100,'killable':True},
        {'x': 2600, 'y':500,'speed':2,'patrol_width':200,'killable':False},
        {'x': 3300, 'y':500,'speed':3,'patrol_width':150,'killable':True},
    ]
    player_spawn = (100, 500)
    finish_rect  = Rect(world_w - 50, 500, 50, 50)

    def spawn_level_and_player():
        lvl = Level(platforms_cfg, enemies_cfg)
        ply = Player(player_spawn[0], player_spawn[1], lives=3)
        return lvl, ply

    # — Estado inicial
    state    = GameState.MAIN_MENU
    menu_idx = 0
    level, player = None, None

    MAIN_MENU_ITEMS = ["Start Game", "Quit"]
    PAUSE_MENU_ITEMS = ["Resume", "Main Menu"]

    # — Loop principal
    while True:
        # — Eventos
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Tecla ESC em PLAYING pausa
            if state == GameState.PLAYING and ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    state = GameState.PAUSED
                    menu_idx = 0

            # Navegação em MAIN_MENU
            if state == GameState.MAIN_MENU and ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    menu_idx = (menu_idx - 1) % len(MAIN_MENU_ITEMS)
                if ev.key == pygame.K_DOWN:
                    menu_idx = (menu_idx + 1) % len(MAIN_MENU_ITEMS)
                if ev.key == pygame.K_RETURN:
                    if menu_idx == 0:  # Start Game
                        level, player = spawn_level_and_player()
                        state = GameState.PLAYING
                    else:              # Quit
                        pygame.quit()
                        sys.exit()

            # Navegação em PAUSED
            if state == GameState.PAUSED and ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    menu_idx = (menu_idx - 1) % len(PAUSE_MENU_ITEMS)
                if ev.key == pygame.K_DOWN:
                    menu_idx = (menu_idx + 1) % len(PAUSE_MENU_ITEMS)
                if ev.key == pygame.K_RETURN:
                    if menu_idx == 0:  # Resume
                        state = GameState.PLAYING
                    else:              # Main Menu
                        state = GameState.MAIN_MENU
                        menu_idx = 0

            # Reiniciar com R após GAME_OVER ou VICTORY
            if state in (GameState.GAME_OVER, GameState.VICTORY) and ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    state = GameState.MAIN_MENU
                    menu_idx = 0

        # — Lógica de Jogo
        if state == GameState.PLAYING:
            prev_bot = player.rect.bottom
            player.update(level.platforms)
            level.update()

            # colisão com inimigos
            for enemy in level.enemies:
                if not enemy.alive:
                    continue
                if player.rect.colliderect(enemy.rect):
                    # colisão por cima em killable
                    if (enemy.killable and
                        player.vel_y > 0 and
                        prev_bot <= enemy.rect.top and
                        player.rect.right > enemy.rect.left and
                        player.rect.left < enemy.rect.right):
                        
                        enemy.kill()
                        player.vel_y = -player.jump_strength / 1.5
                        player.on_ground = False
                    else:
                        player.lose_life()
                        if player.lives <= 0:
                            state = GameState.GAME_OVER
                        else:
                            level.reset_enemies()
                            player.reset()
                    break

            # colisão com chegada
            if player.rect.colliderect(finish_rect):
                state = GameState.VICTORY

        # — Desenho
        

        if state == GameState.MAIN_MENU:
            screen.fill((0, 0, 0))
            draw_text(screen, "MY PLATFORMER", 72, 240, 150, (255,255,0))
            for i, item in enumerate(MAIN_MENU_ITEMS):
                color = (255,255,255) if i == menu_idx else (180,180,180)
                draw_text(screen, item, 48, 300, 300 + i*60, color)

        elif state == GameState.PLAYING:
            # calcula câmera
            screen.fill((100, 149, 237))
            cam_x = player.rect.centerx - W//2
            cam_x = max(0, min(cam_x, world_w - W))

            # desenha plataformas
            for plat in level.platforms:
                r = Rect(plat.rect.x - cam_x, plat.rect.y, plat.rect.width, plat.rect.height)
                color = (150,75,0) if plat.collide_bottom else (0,200,0)
                pygame.draw.rect(screen, color, r)

            # desenha inimigos vivos
            for enemy in level.enemies:
                if not enemy.alive: continue
                r = Rect(enemy.rect.x - cam_x, enemy.rect.y, enemy.rect.width, enemy.rect.height)
                col = (0,0,255) if not enemy.killable else (255,0,255)
                pygame.draw.rect(screen, col, r)

            # desenha chegada
            rf = Rect(finish_rect.x - cam_x, finish_rect.y, finish_rect.width, finish_rect.height)
            pygame.draw.rect(screen, (255,215,0), rf)

            # desenha player
            rp = Rect(player.rect.x - cam_x, player.rect.y, player.rect.width, player.rect.height)
            pygame.draw.rect(screen, (255,0,0), rp)

            # HUD
            draw_text(screen, f"Vidas: {player.lives}", 36, 10, 10)

        elif state == GameState.PAUSED:
            screen.fill((30, 30, 30))
            # desenha último frame de PLAYING em fundo escuro? simplificar:
            draw_text(screen, "PAUSED", 72, 300, 150, (255,255,255))
            for i, item in enumerate(PAUSE_MENU_ITEMS):
                color = (255,255,255) if i == menu_idx else (180,180,180)
                draw_text(screen, item, 48, 300, 300 + i*60, color)

        elif state == GameState.GAME_OVER:
            draw_text(screen, "GAME OVER", 72, 240, 200, (255,50,50))
            draw_text(screen, "Press R to return to Menu", 36, 220, 300)

        elif state == GameState.VICTORY:
            draw_text(screen, "YOU WIN!", 72, 280, 200, (50,255,50))
            draw_text(screen, "Press R to return to Menu", 36, 220, 300)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
