# src/level.py

import pygame
from platform import Platform # type: ignore
from enemy import Enemy

class Level:
    def __init__(self, platforms_config, enemies_config):
        """
        platforms_config: lista de dicts com chaves
            'x', 'y', 'width', 'height', 'collide_bottom' (default=False)
        enemies_config: lista de dicts com chaves
            'x', 'y', 'speed', 'patrol_width', 'killable' (default=False)
        """
        # Plataformas
        self.platforms = []
        for cfg in platforms_config:
            p = Platform(
                x=cfg['x'],
                y=cfg['y'],
                width=cfg['width'],
                height=cfg['height'],
                collide_bottom=cfg.get('collide_bottom', False)
            )
            self.platforms.append(p)

        # Inimigos
        self.enemies = []
        for cfg in enemies_config:
            e = Enemy(
                x=cfg['x'],
                y=cfg['y'],
                speed=cfg.get('speed', 2),
                patrol_width=cfg.get('patrol_width', 150),
                killable=cfg.get('killable', False)
            )
            self.enemies.append(e)

    def update(self):
        for enemy in self.enemies:
            enemy.update()

    def draw(self, surface):
        for plat in self.platforms:
            plat.draw(surface)
        for enemy in self.enemies:
            enemy.draw(surface)

    def reset_enemies(self):
        for enemy in self.enemies:
            enemy.rect.x = enemy.start_x
            enemy.direction = 1
            # Se quiser reviver inimigos killable, reative alive:
            if enemy.killable:
                enemy.alive = True
