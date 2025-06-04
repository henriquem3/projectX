# src/enemy.py

import pygame

class Enemy:
    def __init__(self, x, y, width=50, height=50,
                 speed=2, patrol_width=150, killable=False):
        """
        x, y            → posição inicial (top-left)
        width, height   → tamanho
        speed           → pixels por frame
        patrol_width    → distância de patrulha a partir de x
        killable        → se True, morre quando o jogador pular por cima
        """
        self.start_x = x
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = 1   # 1 → direita, -1 → esquerda
        self.patrol_width = patrol_width

        self.killable = killable
        self.alive = True

    def update(self):
        """Só patrulha se estiver vivo."""
        if not self.alive:
            return

        self.rect.x += self.speed * self.direction
        if self.rect.x > self.start_x + self.patrol_width:
            self.rect.x = self.start_x + self.patrol_width
            self.direction = -1
        elif self.rect.x < self.start_x:
            self.rect.x = self.start_x
            self.direction = 1

    def draw(self, surface):
        """Desenha só se alive."""
        if not self.alive:
            return

        color = (0, 0, 255) if not self.killable else (255, 0, 255)
        # Azul para invencível, magenta para killable (só p/ debug)
        pygame.draw.rect(surface, color, self.rect)

    def kill(self):
        """Mata o inimigo (não será mais desenhado ou atualizado)."""
        self.alive = False
        # Opcional: reposicionar fora da tela ou tocar som aqui
