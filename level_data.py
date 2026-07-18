import pygame
from pathlib import Path
from pygame.math import Vector2
from clickable_object import Clickable
from obstacle import Obstacle
from entity import Entity
from transition_area import TransitionArea


class LevelData:
    def __init__(self, obstacles, clickables, images, transition_area, player_spawn) -> None:
        self.obstacles = obstacles
        self.clickables = clickables
        self.images = images  
        self.player_spawn = player_spawn
        self.transition_area = transition_area
    
    def copy(self):
        level = LevelData(
            obstacles = [Obstacle(o.rect.x, o.rect.y, o.rect.width, o.rect.height) for o in self.obstacles],
            clickables = [Clickable(c.action_id, c.rect.x, c.rect.y, c.rect.w, c.rect.h) for c in self.clickables],
            images = self.images,
            transition_area = TransitionArea(
                self.transition_area.target,
                self.transition_area.rect.x,
                self.transition_area.rect.y,
                self.transition_area.rect.w,
                self.transition_area.rect.h,
            ),
            player_spawn = self.player_spawn.copy(),
        )
        return level

def load_room_images(room):
    images = {}
    for image_path in Path(f"assets/images/{room}_room").glob("*.png"):
        images[Path(image_path).stem] = Entity(0, 0, pygame.transform.scale2x(pygame.image.load(image_path)))
    return images

FRONT_ROOM_DATA = LevelData(
    [
        Obstacle(0, 225, 444, 100),
        Obstacle(410, 50, 100, 300),
        Obstacle(0, 30, 390, 50),
    ],
    [
        Clickable("comp_1_action", 119, 83, 54, 36),
        Clickable("comp_2_action", 226, 84, 53, 35),
        Clickable("control_panal_1_action", 406, 115, 16, 113),
        Clickable("comp_3_action", 45, 226, 40, 35),
        Clickable("front_storage_action", 123, 230, 46, 30),
        Clickable("vault_action", 203, 231, 61, 28),
        Clickable("comp_4_action", 308, 229, 58, 31),
        Clickable("batteries_action", 405, 247, 45, 23),
        Clickable("ai_action", 446, 124, 90, 99),
        Clickable("control_panal_2_action", 329, 96, 56, 23),
    ],
    load_room_images("front"),
    TransitionArea("back", 0, 120, 20, 100),
    Vector2(200, 160)
)

BACK_ROOM_DATA = LevelData(
    [
        Obstacle(203, 295, 433, 37),
        Obstacle(208, 27, 98, 297),
        Obstacle(204, 29, 429, 26),
        Obstacle(541, 39, 90, 73),
        Obstacle(549, 248, 48, 47),
        Obstacle(304, 251, 30, 46),
    ],
    [
        Clickable("electricity_vault_action", 547, 71, 53, 44),
        Clickable("oxygen_vault_action", 548, 248, 44, 45),
        Clickable("trash_can_action", 308, 254, 40, 38),
        Clickable("engine_fire_n_action", 96, 56, 106, 67),
        Clickable("engine_fire_s_action", 98, 230, 102, 73),
        Clickable("back_storage_action", 374, 54, 30, 27),
        Clickable("electricity_panal_action", 416, 55, 42, 27),
        Clickable("vent_action", 453, 165, 34, 35),
        Clickable("higher_engine_action", 247, 96, 56, 168/3),
        Clickable("middle_engine_action", 247, 96 + 168/3, 56, 168/3),
        Clickable("lower_engine_action", 247, 96 + 168*2/3, 56, 168/3),
    ],
    load_room_images("back"),
    TransitionArea("front", 620, 142, 58, 81),
    Vector2(500, 175)
)