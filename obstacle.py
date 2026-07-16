from entity import Entity
import pygame
from settings import *


class Obstacle(Entity):
    def __init__(self, x = 0, y = 0, w = 0, h = 0, image = None):
        super().__init__(x, y)
        self.image = pygame.Surface((w, h))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft = (x, y))