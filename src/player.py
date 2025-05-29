# src/player.py

import pygame

class Player:
    def __init__(self, x, y, width=50, height=50, speed=5, jump_strength=12):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.jump_strength = jump_strength
        self.vel_y = 0
        self.on_ground = False
        self.gravity = 0.5

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        # pulo só se estiver no chão
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_strength
            self.on_ground = False

    def apply_gravity(self, platforms):
        # aplica gravidade
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # checa colisão com cada plataforma
        for plat in platforms:
            if self.rect.colliderect(plat):
                # se estiver caindo
                if self.vel_y > 0:
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.on_ground = True

    def update(self, platforms):
        self.handle_input()

        # ——> trava o X do jogador dentro de [0, 800-width]
        if self.rect.left  < 0:             self.rect.left  = 0
        if self.rect.right > 800:           self.rect.right = 800

        self.apply_gravity(platforms)


    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)  # player em vermelho
