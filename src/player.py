# src/player.py

import pygame

class Player:
    def __init__(self, x, y, width=50, height=50,
                 speed=5, jump_strength=14, lives=3):
        # posição inicial para respawn
        self.initial_x = x
        self.initial_y = y

        # retângulo de colisão/desenho
        self.rect = pygame.Rect(x, y, width, height)

        # movimento e física
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
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = -self.jump_strength
            self.on_ground = False

    def apply_gravity(self, platforms):
        """
        Aplica gravidade e resolve colisões verticais
        considerando 'one-way' ou 'solid' conforme plataforma.collide_bottom.
        """
        # 1) Salva posições anteriores
        previous_bottom = self.rect.bottom
        previous_top    = self.rect.top

        # 2) Aplica gravidade
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # 3) Para cada plataforma, verifica colisão vertical
        for plat in platforms:
            # Se estiver caindo (vel_y > 0), checa colisão por cima
            if self.vel_y > 0:
                # Só pousa se a base estivesse acima do topo e agora cruza por baixo
                if (previous_bottom <= plat.rect.top and
                    self.rect.bottom >= plat.rect.top and
                    self.rect.right > plat.rect.left and
                    self.rect.left < plat.rect.right):
                    
                    # Snap: coloca a base exatamente no topo da plataforma
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0
                    self.on_ground = True

            # Se estiver subindo e a plataforma bloqueia por baixo, checa colisão por baixo
            elif self.vel_y < 0 and plat.collide_bottom:
                # Só ‘bate a cabeça’ se a parte de cima do player bater na base da plataforma
                if (previous_top >= plat.rect.bottom and
                    self.rect.top <= plat.rect.bottom and
                    self.rect.right > plat.rect.left and
                    self.rect.left < plat.rect.right):
                    
                    # Snap: coloca o topo logo abaixo da base da plataforma
                    self.rect.top = plat.rect.bottom
                    self.vel_y = 0
                    # on_ground permanece False, pois ele continua no ar

    def update(self, platforms):
        self.handle_input()

        # Mantém player dentro da largura da tela (0 a 800)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 4000:
            self.rect.right = 4000

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
