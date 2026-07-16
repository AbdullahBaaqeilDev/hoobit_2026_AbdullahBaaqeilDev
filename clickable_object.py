from entity import Entity
import pygame
from settings import *


class Clickable(Entity):

    temp_hover_surf = pygame.Surface((8, 8), pygame.SRCALPHA).convert_alpha()
    temp_hover_surf.set_alpha(128)

    def __init__(self, x = 0, y = 0, w = 0, h = 0, image = None):
        super().__init__(x, y)
        self.image = pygame.Surface((w, h))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.clicked = False
        self.disabled = False

    def click(self):
        self.clicked = True
        print(self, "was clicked")

    def input(self):
        mouse_l = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if mouse_l and not self.clicked:
                self.click()
                return True
        
        if not mouse_l:
            self.clicked = False

    def update(self):
        return self.input()

    def draw(self):
        if not self.visible:
            return
        self.screen.blit(self.image, self.rect)
        pygame.draw.rect(self.screen, (0, 255, 0), self.rect)
    
    def draw_cursor(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.circle(self.temp_hover_surf, (255, 0, 0), (4, 4), 4)
            self.screen.blit(self.temp_hover_surf, self.temp_hover_surf.get_rect(center = mouse_pos))