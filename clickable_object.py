from entity import Entity
import pygame
from settings import *


class Clickable(Entity):
    temp_hover_surf = pygame.Surface((8, 8), pygame.SRCALPHA).convert_alpha()
    temp_hover_surf.set_alpha(128)

    def __init__(self, action_id, x, y, w, h):
        super().__init__(x, y)
        self.action_id = action_id
        self.rect = pygame.Rect(x, y, w, h)
        self.clicked = False
        self.disabled = False

    def click(self):
        self.clicked = True

    def handle_event(self, event, action_handler):
        if event.type != pygame.MOUSEBUTTONUP:
            return

        if self.rect.collidepoint(event.pos):
            self.click()
            action_handler(self.action_id)
            return True

    def update(self):
        pass

    def draw(self, screen):
        if not self.visible:
            return
        # pygame.draw.rect(screen, (0, 255, 0), self.rect)
        screen.blit(
            pygame.font.Font(None, 25).render(
                self.action_id[: min(len(self.action_id), 10)], 0, "white"
            ),
            self.rect.center,
        )

    def draw_cursor(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.circle(self.temp_hover_surf, (255, 0, 0), (4, 4), 4)
            screen.blit(
                self.temp_hover_surf, self.temp_hover_surf.get_rect(center=mouse_pos)
            )
