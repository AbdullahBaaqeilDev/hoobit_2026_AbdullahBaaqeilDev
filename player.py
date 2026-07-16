from entity import Entity
import pygame
from settings import *
from pathlib import Path


class Player(Entity):

    player_animations_path = "assets/images/player"
    animation_speed = 0.2

    def __init__(self): 
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect(topleft = (0, 0))
        self.rect.w -= 12
        self.x, self.y = 0, 0
        self.status = "down"
        self.animations = {
            "up_idle": [],
            "right_idle": [],
            "down_idle": [],
            "left_idle": [],
            "up_walk": [],
            "right_walk": [],
            "down_walk": [],
            "left_walk": [],
        }
        self.frame_index = 0
        self.load_animations()

    def load_animations(self):
        for animation in self.animations.keys():
            for animation_path in Path(self.player_animations_path + "/" + animation).glob("*.png"):
                self.animations[animation].append(
                    pygame.transform.scale2x(
                        pygame.image.load(animation_path).convert_alpha()
                    )
                )

    def input(self):
        keys = pygame.key.get_pressed()

        # movement input
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = "right"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = "left"
        else:
            self.direction.x = 0

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not "_idle" in self.status:
                if "_walk" in self.status:
                    self.status = self.status.replace("_walk", "_idle")
                    return
                self.status = self.status + "_idle"
        else:
            self.status = self.status + "_walk"

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        self.rect.w -= 12
          
    def update(self, obstacle_sprites):
        self.input()
        self.get_status()
        self.animate()
        self.move(PLAYER_SPEED, obstacle_sprites)