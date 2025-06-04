import pygame

class Platform:
    def __init__(self, x, y, width, height, collide_bottom=False):
        """
        x, y, width, height   → definem o pygame.Rect
        collide_bottom        → se True, colisiona também por baixo
                               (bloqueia jogador que bate a cabeça);
                               se False, é 'one-way' (não bloqueia por baixo).
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.collide_bottom = collide_bottom

    def draw(self, surface):
        """
        Desenha a plataforma. Usamos cores diferentes para visualizarmos
        qual tipo é qual (apenas para debug; depois você pode usar sprites).
        """
        if self.collide_bottom:
            color = (150, 75, 0)    # marrom para plataforma sólida
        else:
            color = (0, 200, 0)     # verde para one-way
        pygame.draw.rect(surface, color, self.rect)
 # type: ignore