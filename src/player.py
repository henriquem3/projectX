import pygame

class Player:
    def __init__(self, x, y, width=50, height=50,
                 speed=5, jump_strength=12, lives=3):
        # posição inicial de respawn
        self.initial_x = x
        self.initial_y = y

        # componente gráfico e física
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.jump_strength = jump_strength
        self.vel_y = 0
        self.on_ground = False
        self.gravity = 0.5

        # vidas
        self.lives = lives

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP])  and self.on_ground:
            self.vel_y = -self.jump_strength
            self.on_ground = False

    def apply_gravity(self, platforms):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_y > 0:
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.on_ground = True

    def update(self, platforms):
        self.handle_input()
        # mantém player dentro da tela (0 a 800px)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800

        self.apply_gravity(platforms)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

    def reset(self):
        """Reposiciona o jogador ao ponto inicial e zera velocidade."""
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.vel_y = 0
        self.on_ground = False

    def lose_life(self):
        """Decrementa uma vida e reseta posição."""
        self.lives -= 1
        self.reset()
