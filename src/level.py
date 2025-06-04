# src/level.py

import pygame
from platform import Platform # type: ignore
from enemy import Enemy

class Level:
    def __init__(self, platforms_config, enemies_config):
        """
        platforms_config: lista de dicionários com chaves
            'x', 'y', 'width', 'height', 'collide_bottom' (opcional, default=False)
        enemies_config: lista de dicionários com chaves
            'x', 'y', 'speed', 'patrol_width'
        """
        # Cria instâncias de Platform
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

        # Cria instâncias de Enemy
        self.enemies = []
        for cfg in enemies_config:
            e = Enemy(
                x=cfg['x'],
                y=cfg['y'],
                speed=cfg.get('speed', 2),
                patrol_width=cfg.get('patrol_width', 150)
            )
            self.enemies.append(e)

    def update(self):
        """Atualiza todos os inimigos do nível."""
        for enemy in self.enemies:
            enemy.update()

    def draw(self, surface):
        """
        Desenha as plataformas (verde ou marrom) e inimigos (azul).
        """
        # Desenha plataformas
        for plat in self.platforms:
            plat.draw(surface)

        # Desenha inimigos
        for enemy in self.enemies:
            enemy.draw(surface)

    def reset_enemies(self):
        """
        Reposiciona cada inimigo de volta ao X inicial e reinicia direção.
        """
        for enemy in self.enemies:
            enemy.rect.x = enemy.start_x
            enemy.direction = 1
