# main.py

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

def format_time(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    cs = int((seconds - int(seconds)) * 100)
    return f"{m:02d}:{s:02d}:{cs:02d}"

# ——————————————————————————————————————————
def main():
    pygame.init()
    W, H = 800, 600
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("My Platformer with Timer & Score Multiplier")
    clock = pygame.time.Clock()

    # — Time limit por tentativa (em segundos) para multiplicador
    LEVEL_TIME_LIMIT = 120

    # — Estado de pontuação e timer
    score = 0
    start_ticks = None
    phase_start_ticks = None
    final_score = None
    final_multiplier = 1.0
    final_time = None


    # — Local de spawn fixo do player
    player_spawn = (100, 500)

    # —–––––––––––––––––––––––––––––
    # Configs de todas as fases
    # ––––––––––––––––––––––––––––––
    phases = [
        {
            'world_w': W * 5,
            'platforms': [
                {'x': 0,    'y':550,'width':W*5,'height':50, 'collide_bottom':True},
                {'x': 300,  'y':450,'width':100, 'height':20, 'collide_bottom':False},
                {'x': 800,  'y':400,'width':150, 'height':20, 'collide_bottom':True},
                {'x': 1400, 'y':350,'width':200, 'height':20, 'collide_bottom':False},
                {'x': 2000, 'y':450,'width':120, 'height':20, 'collide_bottom':True},
                {'x': 2800, 'y':300,'width':180, 'height':20, 'collide_bottom':False},
                {'x': 3500, 'y':400,'width':150, 'height':20, 'collide_bottom':True},
            ],
            'enemies': [
                {'x': 500,  'y':500,'speed':3,'patrol_width':200,'killable':True},
                {'x': 1100, 'y':500,'speed':2,'patrol_width':150,'killable':False},
                {'x': 1900, 'y':500,'speed':3,'patrol_width':100,'killable':True},
                {'x': 2600, 'y':500,'speed':2,'patrol_width':200,'killable':False},
                {'x': 3300, 'y':500,'speed':3,'patrol_width':150,'killable':True},
            ]
        },
        {
            'world_w': W * 6,
            'platforms': [
                {'x': 0,    'y':550,'width':W*6,'height':50, 'collide_bottom':True},
                {'x': 400,  'y':450,'width':120, 'height':20, 'collide_bottom':False},
                {'x': 900,  'y':400,'width':160, 'height':20, 'collide_bottom':True},
                {'x': 1600, 'y':350,'width':220, 'height':20, 'collide_bottom':False},
                {'x': 2300, 'y':450,'width':140, 'height':20, 'collide_bottom':True},
                {'x': 3200, 'y':300,'width':200, 'height':20, 'collide_bottom':False},
                {'x': 4000, 'y':400,'width':170, 'height':20, 'collide_bottom':True},
            ],
            'enemies': [
                {'x': 600,  'y':500,'speed':4,'patrol_width':250,'killable':True},
                {'x': 1200, 'y':500,'speed':3,'patrol_width':180,'killable':False},
                {'x': 2000, 'y':500,'speed':4,'patrol_width':120,'killable':True},
                {'x': 2800, 'y':500,'speed':3,'patrol_width':250,'killable':False},
                {'x': 3500, 'y':500,'speed':4,'patrol_width':180,'killable':True},
            ]
        }
    ]

    phase_times = [0] * len(phases)

    def spawn_phase(idx):
        cfg = phases[idx]
        world_w = cfg['world_w']  
        lvl = Level(cfg['platforms'], cfg['enemies'])
        ply = Player(player_spawn[0], player_spawn[1], lives=3, world_width = world_w)
        finish = Rect(cfg['world_w'] - 50, 500, 50, 50)
        return lvl, ply, finish

    # — Estado inicial
    current_phase = 0
    level, player, finish_rect = spawn_phase(current_phase)
    state    = GameState.MAIN_MENU
    menu_idx = 0

    MAIN_MENU_ITEMS  = ["Start Game", "Quit"]
    PAUSE_MENU_ITEMS = ["Resume", "Main Menu"]

    # — Loop principal
    while True:
        # — Eventos
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ESC pausa em PLAYING
            if state == GameState.PLAYING and ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    state = GameState.PAUSED
                    menu_idx = 0

            # Main Menu
            if state == GameState.MAIN_MENU and ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    menu_idx = (menu_idx - 1) % len(MAIN_MENU_ITEMS)
                if ev.key == pygame.K_DOWN:
                    menu_idx = (menu_idx + 1) % len(MAIN_MENU_ITEMS)
                if ev.key == pygame.K_RETURN:
                    if menu_idx == 0:  # Start Game
                        current_phase = 0
                        level, player, finish_rect = spawn_phase(current_phase)
                        score = 100
                        start_ticks = pygame.time.get_ticks()
                        phase_start_ticks = start_ticks
                        final_score = None
                        final_multiplier = 1.0
                        final_time = None
                        state = GameState.PLAYING
                    else:              # Quit
                        pygame.quit()
                        sys.exit()

            # Pause Menu
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

            # Reiniciar com R em GAME_OVER ou VICTORY
            if state in (GameState.GAME_OVER, GameState.VICTORY) and ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    state = GameState.MAIN_MENU
                    menu_idx = 0

        # — Lógica de jogo
        if state == GameState.PLAYING:
            prev_bot = player.rect.bottom
            player.update(level.platforms)
            level.update()

            # colisão com inimigos
            for enemy in level.enemies:
                if not enemy.alive:
                    continue
                if player.rect.colliderect(enemy.rect):
                    # killable por cima
                    if (enemy.killable and
                        player.vel_y > 0 and
                        prev_bot <= enemy.rect.top and
                        player.rect.right > enemy.rect.left and
                        player.rect.left < enemy.rect.right):
                        
                        enemy.kill()
                        player.vel_y = -player.jump_strength / 1.5
                        player.on_ground = False
                        score += 100
                    else:
                        player.lose_life()
                        if player.lives <= 0:
                            # game over: grava resultados sem multiplicar
                            if start_ticks is not None:
                                final_time = (pygame.time.get_ticks() - start_ticks) / 1000
                            final_multiplier = 1.0
                            final_score = score
                            state = GameState.GAME_OVER
                        else:
                            # reset timer e score ao perder vida
                            # start_ticks = pygame.time.get_ticks()
                            if (score - 100) >= 100:
                                score = score -100
                            else: 
                                score = 100 
                            level.reset_enemies()
                            player.reset()
                    break

            # colisão com chegada
            if player.rect.colliderect(finish_rect):
                phase_times[current_phase] = (pygame.time.get_ticks() - phase_start_ticks) / 1000
                # grava tempo final e aplica multiplicador
                if start_ticks is not None:
                    elapsed = (pygame.time.get_ticks() - start_ticks) / 1000
                    final_time = elapsed
                    time_left = max(0, LEVEL_TIME_LIMIT - elapsed)
                    final_multiplier = 1 + (time_left / LEVEL_TIME_LIMIT)
                    final_score = int(score * final_multiplier)

                # avança para a próxima fase ou vitória final
                if current_phase + 1 < len(phases):
                    old_lives = player.lives
                    current_phase += 1
                    level, player, finish_rect = spawn_phase(current_phase)
                    #score = 100
                    #start_ticks = pygame.time.get_ticks()
                    phase_start_ticks = pygame.time.get_ticks()
                    player.lives = old_lives + 1
                    state = GameState.PLAYING
                else:
                    state = GameState.VICTORY

        # — Render por estado —
        if state == GameState.MAIN_MENU:
            screen.fill((0, 0, 0))
            draw_text(screen, "MY PLATFORMER", 72, 240, 150, (255,255,0))
            for i, item in enumerate(MAIN_MENU_ITEMS):
                color = (255,255,255) if i == menu_idx else (180,180,180)
                draw_text(screen, item, 48, 300, 300 + i*60, color)

        elif state == GameState.PLAYING:
            screen.fill((100, 149, 237))
            cam_x = player.rect.centerx - W//2
            cam_x = max(0, min(cam_x, phases[current_phase]['world_w'] - W))

            # plataformas
            for plat in level.platforms:
                r = Rect(plat.rect.x - cam_x, plat.rect.y,
                         plat.rect.width, plat.rect.height)
                color = (150,75,0) if plat.collide_bottom else (0,200,0)
                pygame.draw.rect(screen, color, r)

            # inimigos
            for enemy in level.enemies:
                if not enemy.alive: continue
                r = Rect(enemy.rect.x - cam_x, enemy.rect.y,
                         enemy.rect.width, enemy.rect.height)
                col = (0,0,255) if not enemy.killable else (255,0,255)
                pygame.draw.rect(screen, col, r)

            # chegada
            rf = Rect(finish_rect.x - cam_x, finish_rect.y,
                      finish_rect.width, finish_rect.height)
            pygame.draw.rect(screen, (255,215,0), rf)

            # player
            rp = Rect(player.rect.x - cam_x, player.rect.y,
                      player.rect.width, player.rect.height)
            pygame.draw.rect(screen, (255,0,0), rp)

            # HUD: vidas, pontuação bruta, timer
            draw_text(screen, f"Vidas: {player.lives}", 24, 10, 10)
            draw_text(screen, f"Pontos: {score}", 24, 10, 40)
            if start_ticks is not None:
                total_sec = (pygame.time.get_ticks() - start_ticks) / 1000
                draw_text(screen, f"Tempo Total: {format_time(total_sec)}", 24, 10, 70)
            # tempo de fase
            if phase_start_ticks is not None:
                phase_sec = (pygame.time.get_ticks() - phase_start_ticks) / 1000
                draw_text(screen, f"Tempo Fase: {format_time(phase_sec)}", 24, 10, 100)


        elif state == GameState.PAUSED:
            screen.fill((30, 30, 30))
            draw_text(screen, "PAUSED", 72, 300, 150, (255,255,255))
            for i, item in enumerate(PAUSE_MENU_ITEMS):
                color = (255,255,255) if i == menu_idx else (180,180,180)
                draw_text(screen, item, 48, 300, 300 + i*60, color)

        elif state == GameState.GAME_OVER:
            screen.fill((30, 30, 30))
            draw_text(screen, "GAME OVER", 72, 240, 150, (255,50,50))
            draw_text(screen,
                      f"{score} * {final_multiplier:.2f} = {final_score}",
                      36, 220, 260)
            if final_time is not None:
                draw_text(screen,
                          f"Tempo Final: {format_time(final_time)}",
                          36, 220, 320)
            draw_text(screen, "Press R to return to Menu", 36, 220, 400)

        elif state == GameState.VICTORY:
            screen.fill((30, 30, 30))
            draw_text(screen, "YOU WIN!", 72, 280, 150, (50,255,50))
            draw_text(screen,
                      f"{score} * {final_multiplier:.2f} = {final_score}",
                      36, 220, 260)
            if final_time is not None:
                draw_text(screen,
                          f"Tempo Final: {format_time(final_time)}",
                          36, 220, 320)
                # exibe cada tempo de fase num loop
                for i, t in enumerate(phase_times):
                    draw_text(screen,
                              f"Tempo Fase {i+1}: {format_time(t)}",
                              36, 220, 360 + i*40)
            y_press_r = 360 + len(phase_times) * 40 + 20
            draw_text(screen, f"Press R to return to Menu", 36, 220, y_press_r)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
