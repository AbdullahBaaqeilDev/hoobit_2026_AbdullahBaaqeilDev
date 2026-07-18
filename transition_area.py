import pygame
from entity import Entity


class TransitionArea(Entity):
    def __init__(self, go_to="front", x=0, y=0, w=0, h=0):
        super().__init__(x, y)
        self.image = pygame.Surface((w, h))
        self.image.fill((0, 255, 255))
        self.rect = pygame.Rect(x, y, w, h)
        self.target = go_to
        self.disabled = False

    def check(self, player):
        if self.rect.colliderect(player.rect):
            return True
