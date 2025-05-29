# src/enemy.py

import pygame

class Enemy:
    def __init__(self, x, y, width=50, height=50, speed=2, patrol_width=200):
        """
        x, y            → posição inicial (top-left)
        width, height   → tamanho do inimigo
        speed           → pixels por frame
        patrol_width    → distância total de patrulha a partir de x
        """
        self.start_x = x
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = 1   # 1 → direita, -1 → esquerda
        self.patrol_width = patrol_width

    def update(self):
        # Move na direção atual
        self.rect.x += self.speed * self.direction

        # Se ultrapassar a região de patrulha, inverte direção
        if self.rect.x > self.start_x + self.patrol_width:
            self.rect.x = self.start_x + self.patrol_width
            self.direction = -1
        elif self.rect.x < self.start_x:
            self.rect.x = self.start_x
            self.direction = 1

    def draw(self, surface):
        # Desenha um retângulo azul
        pygame.draw.rect(surface, (0, 0, 255), self.rect)
