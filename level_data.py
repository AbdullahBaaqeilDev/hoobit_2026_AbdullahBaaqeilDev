import pygame
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

FRONT_ROOM_DATA = LevelData(
    [
        Obstacle(0, 230, 444, 100),
        Obstacle(410, 50, 100, 300),
        Obstacle(0, 30, 390, 90),
    ],
    [
        Clickable(119, 83, 54, 36),
        Clickable(226, 84, 53, 35),
        Clickable(406, 115, 16, 113),
        Clickable(45, 226, 40, 35),
        Clickable(123, 230, 46, 30),
        Clickable(203, 231, 61, 28),
        Clickable(308, 229, 58, 31),
        Clickable(405, 247, 45, 23),
        Clickable(446, 124, 90, 99),
        Clickable(329, 96, 56, 23),
    ],
    [
        Entity(0, 0, pygame.transform.scale2x(pygame.image.load("assets/images/front_room/default.png")))
    ],
    TransitionArea(
        "back",
        0, 120,
        50, 100
    ),
    Vector2(200, 160)
)

BACK_ROOM_DATA = LevelData(
    [
        Obstacle(203, 298, 433, 37),
        Obstacle(208, 27, 98, 297),
        Obstacle(204, 29, 429, 52),
        Obstacle(541, 39, 90, 73),
        Obstacle(549, 248, 48, 47),
        Obstacle(304, 251, 47, 46),
    ],
    [
        Clickable(547, 71, 53, 44),
        Clickable(548, 248, 44, 45),
        Clickable(308, 254, 40, 38),
        Clickable(96, 56, 106, 67),
        Clickable(98, 230, 102, 73),
        Clickable(374, 54, 30, 27),
        Clickable(416, 55, 42, 27),
        Clickable(453, 165, 34, 35),
        Clickable(247, 96, 56, 168),
    ],
    [
        Entity(0, 0, pygame.transform.scale2x(pygame.image.load("assets/images/back_room/default.png")))
    ],
    TransitionArea("front", 600, 142, 58, 81),
    Vector2(500, 175)
)