import time
from timer import Timer
from player import Player
from level_data import *
from ui import Message
from random import choice, randrange


class Level:
    def __init__(self, manager):
        self.manager = manager

        self.room_name = "front"
        self.rooms_data = {
            "front": FRONT_ROOM_DATA.copy(),
            "back": BACK_ROOM_DATA.copy(),
        }
        self.timers = {
            "sun_crash": Timer(self.sun_crash, 60),
            "footsteps_cooldown": Timer(self.check_footsteps_cooldown, 0.5, True)
        }
        self.start_time = 0
        self.player = Player()
        self.audio_system = None
        self.player.rect.center = self.room.player_spawn
        self.inventory = [
            "note"
        ]
        self.status = {
            "vault_open": False,
            "batteries_on": False,
            "comp_1_on": False,
            "comp_2_on": False,
            "comp_3_on": False,
            "comp_4_on": False,
            "ai_on": False,
            "first_comp_disorder": True,
            "back_open": False,
            "entered_back": False,
            "trash_can_open": False,
            "front_storage_open": False,
            "back_storage_open": False,
            "higher_engine_fixed": False,
            "middle_engine_fixed": False,
            "lower_engine_fixed": False,
            "ai_persuaded": False
        }
        self.messages = {}

    @property
    def room(self):
        return self.rooms_data[self.room_name]

    def reset_data(self):
        self.rooms_data = {
            "front": FRONT_ROOM_DATA.copy(),
            "back": BACK_ROOM_DATA.copy(),
        }

    def start(self):
        self.start_time = time.time()
        self.audio_system.change_song_to("JDSherbert - Ambiences Music Pack - Frost Mountain Aura")

    def create_timer(self, name, callback, delay_s, periodic = False):
        self.timers[name] = Timer(callback, delay_s, periodic)

    def del_timer(self, name):
        del self.timers[name]

    def go_to_room(self, room):
        if room == "back":
            if self.status["back_open"]:
                if not self.status["entered_back"]:
                    self.audio_system.play_sfx("scary_air_sound")
                    self.status["entered_back"] = True
                self.audio_system.change_song_to("back_ambience")
            else:
                self.audio_system.play_sfx("hit")
                self.player.rect.center = self.room.player_spawn
                return
        if room == "front":
            self.audio_system.change_song_to("18. The Old Magician")
        self.room_name = room
        self.audio_system.play_sfx(f"electric-door-open_{choice((0, 1, 2))}")
        self.player.rect.center = self.room.player_spawn

    def sun_crash(self):
        print("crashed the sun")

    def create_message(self, text, age = "auto", name = None):
        while not name or name in self.messages.keys():
            name = str(randrange(0, 1_000_000_000))

        self.messages[name] = Message(
            text,
            pygame.display.get_window_size()[0],
            age if age != "auto" else text.count(" ") / 4,
            center_image_path = "assets/images/gui/message_center.png",
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            self.manager.open_ai_chat()

        for clickable in self.room.clickables:
            if clickable.handle_event(event, self.on_clickable_interacted):
                self.audio_system.play_sfx(f"bubble_click_{choice((1, 2, 3))}")

    def handle_transition(self):
        if self.room.transition_area.check(self.player) and not self.room.transition_area.disabled:
            self.go_to_room(self.room.transition_area.target)

    def first_comp_disorder_action(self):

        if self.status["batteries_on"]:
            if self.num_comp_on() == 0:
                self.audio_system.play_sfx("spell_fail")
                self.status["first_comp_disorder"] = False
                return
            
            if self.status["first_comp_disorder"]:
                self.create_message("Maybe there is an order")

            self.audio_system.play_sfx(f"{choice(("marimba_fail", "trumpet_fail"))}")
            self.status["comp_1_on"] = False
            self.status["comp_2_on"] = False
            self.status["comp_3_on"] = False
            self.status["comp_4_on"] = False
            self.status["first_comp_disorder"] = False

    def num_comp_on(self):
        num = 0
        for i in range(1, 5):
            if self.status[f"comp_{i}_on"]: num += 1
        return num

    def on_clickable_interacted(self, action_id):
        
        def turn_on_ai():
            if self.room_name == "front":
                self.audio_system.change_song_to("18. The Old Magician")
            else:
                self.audio_system.change_song_to("back_ambience")
            self.audio_system.set_song_volume(0.5)
            self.audio_system.play_sfx("recharge")
            self.status["ai_on"] = True

        match action_id:
            case "vault_action":
                if not self.status["vault_open"]:
                    self.manager.open_puzzle("VAULT")
            case "batteries_action": 
                if "batteries" in self.inventory and not self.status["batteries_on"]:
                    self.audio_system.play_sfx("power_on_sfx")
                    self.status["batteries_on"] = True
                    self.inventory.remove("batteries")
                    self.status["back_open"] = True
                    self.create_message("The [red]'Engine Room'[white] is now open")
                    self.create_timer(
                        "open_comp",
                        lambda: self.create_message("Try to open the 'Computers'"),
                        2.5
                    )
            case "comp_1_action":
                if self.status["batteries_on"] and not self.status["comp_1_on"]:
                    self.status["comp_1_on"] = True
                    self.audio_system.play_sfx(f"comp_{self.num_comp_on()}_on_sfx")
            case "comp_2_action":
                if self.status["batteries_on"] and not self.status["comp_2_on"] and self.status["comp_1_on"]:
                    self.status["comp_2_on"] = True
                    self.audio_system.play_sfx(f"comp_{self.num_comp_on()}_on_sfx")
                elif not self.status["comp_2_on"]: self.first_comp_disorder_action()
            case "comp_3_action":
                if self.status["batteries_on"] and not self.status["comp_3_on"] and self.status["comp_2_on"]:
                    self.status["comp_3_on"] = True
                    self.audio_system.play_sfx(f"comp_{self.num_comp_on()}_on_sfx")
                elif not self.status["comp_3_on"]: self.first_comp_disorder_action()
            case "comp_4_action":
                if self.status["batteries_on"] and not self.status["comp_4_on"] and self.status["comp_3_on"]:
                    self.status["comp_4_on"] = True
                    self.audio_system.play_sfx(f"comp_{self.num_comp_on()}_on_sfx")
                elif not self.status["comp_4_on"]: self.first_comp_disorder_action()
            case "ai_action" : 
                if self.status["batteries_on"] and not self.status["ai_on"] and self.status["comp_4_on"]:
                    self.create_message("Press 'Tap' or 'Left Click' the AI screen to Talk")
                    self.audio_system.play_sfx("ai_on_sfx")
                    self.audio_system.set_song_volume(0.0)
                    self.create_timer(
                        "second_ai_sfx",
                        turn_on_ai,
                        3)
                elif self.status["ai_on"]:
                    self.manager.open_ai_chat()
            case "front_storage_action":
                if not self.status["front_storage_open"]:
                    self.manager.open_puzzle("STORAGE")
            case "control_panal_1_action":
                # TODO: make it end the game when the ai is persuaded
                pass
            case "control_panal_2_action":
                # TODO: make it end the game when the ai is persuaded
                pass
            case "electricity_vault_action":
                # TODO: make the ai make a comment store that comment and replay it later
                pass
            case "oxygen_vault_action":
                # TODO: make the ai make a comment store that comment and replay it later
                pass
            case "trash_can_action":
                if not self.status["trash_can_open"]:
                    self.status["trash_can_open"] = True
                    self.inventory.append("heat_chamber")
                    self.inventory.append("dirty_note")
                else:
                    # TODO: make a messsage show up
                    print("empty")
            case "engine_fire_higher_action":
                # TODO: make a messsage show up
                print("How did your hands reah there?!")
            case "engine_fire_lower_action":
                # TODO: make the ai make a comment store that comment and replay it later
                print("Ouch!! it's hot")
            case "back_storage_action":
                # TODO: make a puzzle appear. and add if solved to the condition
                if not self.status["back_storage_open"]:
                    self.status["back_storage_open"] = True
                    self.inventory.append("wires")
                else:
                    # TODO: make a messsage show up
                    print("empty")
            case "electricity_panal_action":
                # TODO: make the ai make a comment store that comment and replay it later
                pass
            case "vent_action":
                # TODO: make the ai make a comment store that comment and replay it later
                print("Good thing the ventilation system didn't break")
            case "higher_engine_action": 
                if "wires" in self.inventory and not self.status["higher_engine_fixed"]:
                    self.manager.open_puzzle("WIRES_2")
            case "middle_engine_action":
                if "heat_chamber" in self.inventory and not self.status["middle_engine_fixed"]:
                    self.inventory.remove("heat_chamber")
                    self.status["middle_engine_fixed"] = True
                    self.audio_system.play_sfx("connected")
            case "lower_engine_action": 
                if "wires" in self.inventory and not self.status["lower_engine_fixed"]:
                    self.manager.open_puzzle("WIRES_1")

    def get_correct_room_image(self):
        
        if self.room_name == "front":
            status_k_array = ("v", "s", "b", "c", "c", "c", "c", "a")
            status_translate = (
                ("c", "o"), 
                ("c", "o"), 
                ("f", "n"), 
                ("f", "n"), 
                ("f", "n"), 
                ("f", "n"), 
                ("f", "n"), 
                ("f", "n")
            )
            status_v_array = (
                self.status["vault_open"],
                self.status["front_storage_open"],
                self.status["batteries_on"],
                self.status["comp_1_on"],
                self.status["comp_2_on"],
                self.status["comp_3_on"],
                self.status["comp_4_on"],
                self.status["ai_on"],
            )
        elif self.room_name == "back":
            status_k_array = ("t", "s", "h", "m", "l")
            status_translate = (
                ("c", "o"), 
                ("c", "o"), 
                ("b", "f"), 
                ("b", "f"), 
                ("b", "f"), 
            )
            status_v_array = (
                self.status["trash_can_open"],
                self.status["back_storage_open"],
                self.status["higher_engine_fixed"],
                self.status["middle_engine_fixed"],
                self.status["lower_engine_fixed"],
            )

        image_name = ""
        for i in range(len(status_k_array)):
            image_name += status_k_array[i] + status_translate[i][status_v_array[i]] + "_"
        image_name = image_name[:-1]
        
        return self.room.images[image_name]

    def update_timers(self):
        expired_timers = []
        for name, timer in self.timers.items():
            timer.update()
            if timer.ran and not timer.periodic:
                expired_timers.append(name)
        for name in expired_timers:
            self.del_timer(name)

    def check_footsteps_cooldown(self):
        if "walk" in self.player.status:
            self.audio_system.play_sfx("footsteps")

    def update(self):
        self.update_timers()
        self.handle_transition()
        self.player.update(self.room.obstacles)
        for obstacle in self.room.obstacles:
            obstacle.update()
        for message in self.messages.values():
            message.update()

    def draw(self, screen):
        self.get_correct_room_image().draw(screen)
        for clickable in self.room.clickables:
            clickable.draw_cursor(screen)
        self.player.draw(screen)
        for message in self.messages.values():
            message.draw(screen)