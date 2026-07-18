from pygame.math import Vector2
import pygame


class Entity:
    def __init__(self, x = 0, y = 0, image = None):
        self.image = image
        self.rect = pygame.Rect(x, y, 0, 0)
        self.direction = Vector2()
        self.visible = True

    def set_image(self, image):
        self.image = image
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        
    def move(self, speed, obstacle_sprites):
        self.rect.x += self.direction.x * speed
        self.collision("h", obstacle_sprites)
        self.rect.y += self.direction.y * speed
        self.collision("v", obstacle_sprites)

    def collision(self, direction, obstacle_sprites):
        if direction == "h":
            for sprite in obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: # moving right
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right

        if direction == "v":
            for sprite in obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: # moving down
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: # moving up
                        self.rect.top = sprite.rect.bottom
    
    def draw(self, screen):
        if not self.visible:
            return
        screen.blit(self.image, self.rect)

    def update(self):
        pass