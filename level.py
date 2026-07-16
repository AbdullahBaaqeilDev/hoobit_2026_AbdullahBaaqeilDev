from player import Player
from clickable_object import Clickable
from obstacle import Obstacle
from level_data import *
from random import choice


class Level:
    def __init__(self):
        self.room = "front"
        self.rooms_data = {
            "front": FRONT_ROOM_DATA,
            "back": BACK_ROOM_DATA,
        }
        self.obstacles = []
        self.clickables = []
        self.transition_area = []
        self.images = []
        self.player = Player()
        self.player_spawn = Vector2(0, 0)
        self.audio_system = None
        self.back_opened = False
        self.reload_data()

    def start(self):
        self.audio_system.change_song_to("JDSherbert - Ambiences Music Pack - Frost Mountain Aura")

    def load_level_data(self, level_data):
        self.obstacles = level_data.obstacles
        self.clickables = level_data.clickables
        self.images = level_data.images
        self.transition_area = level_data.transition_area
        self.player_spawn = level_data.player_spawn

    def reload_data(self):
        self.load_level_data(self.rooms_data[self.room])
        self.player.rect.center = self.player_spawn
    
    def go_to_room(self, room):
        if room == "back":
            self.audio_system.play_sfx("scary_air_sound")
            self.back_opened = True
        self.room = room
        self.reload_data()
        self.audio_system.play_sfx(f"electric-door-open_{choice((0, 1, 2))}")

    def handle_event(self):
        pass

    def handle_transition(self):
        if self.transition_area.check(self.player) and not self.transition_area.disabled:
            self.go_to_room(self.transition_area.go_to)

    def update(self):
        self.handle_transition()
        self.player.update(self.obstacles)
        for clickable in self.clickables:
            if clickable.update():
                self.audio_system.play_sfx("bubble_click")
        for obstacle in self.obstacles:
            obstacle.update()

    def draw(self):
        for image in self.images:
            image.draw()
        for clickable in self.clickables:
            # clickable.draw()
            clickable.draw_cursor()
        # self.transition_area.draw()
        # for obstacle in self.obstacles:
        #     obstacle.draw()
        self.player.draw()