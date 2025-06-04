# src/level.py

import pygame
from enemy import Enemy

class Level:
    def __init__(self, platforms, enemies_config):
        """
        platforms: lista de pygame.Rect representando chão/blocos.
        enemies_config: lista de dicionários com chaves:
            'x', 'y', 'speed', 'patrol_width'
        """
        self.platforms = platforms

        # Cria instâncias de Enemy a partir da configuração
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
        Desenha as plataformas e os inimigos na surface informada.
        Plataformas são retângulos verdes, inimigos retângulos azuis.
        """
        # Desenha plataformas
        for plat in self.platforms:
            pygame.draw.rect(surface, (0, 200, 0), plat)
        # Desenha inimigos
        for enemy in self.enemies:
            enemy.draw(surface)

    def reset_enemies(self):
        """
        Reposiciona cada inimigo de volta ao X inicial e reinicia direção.
        (útil quando o player perde vida)
        """
        for enemy in self.enemies:
            enemy.rect.x = enemy.start_x
            enemy.direction = 1
