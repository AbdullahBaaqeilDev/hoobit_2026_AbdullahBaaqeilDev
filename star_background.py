import pygame


class StarBackground:

    STAR_BACKGROUND_X_SPEED = -2

    def __init__(self):
        self.star_background = pygame.image.load("assets/images/star_background.png").convert_alpha()
        self.star_background = pygame.transform.scale2x(self.star_background)
        self.image_w = self.star_background.get_width()
        self.offset_x = 0

    def draw(self, screen):
        self.offset_x += self.STAR_BACKGROUND_X_SPEED
        if self.offset_x < -self.image_w:
            self.offset_x = 0
            
        screen.blit(self.star_background, (self.offset_x, 0))
        screen.blit(self.star_background, (self.image_w + self.offset_x, 0))