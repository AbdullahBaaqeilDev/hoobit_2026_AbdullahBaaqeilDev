import ai_system
from sys import exit
from level import Level
from ui import *
from audio_system import AudioSystem
from star_background import StarBackground
from settings import *


class GameManager:
    def __init__(self):
        self.current_state = "MENU"
        self.global_status = {
            "opened_wires_puzzle_1": False,
            "opened_wires_puzzle_2": False,
            "opened_vault_puzzle": False,
            "opened_gameplay": False,
            "opened_settings": False,
            "opened_main_menu": False,
            "opened_end": False,
        }

        self.star_background = StarBackground()
        self.audio_system = AudioSystem()
        self.level = Level(self)
        self.level.audio_system = self.audio_system

        self.main_menu_ui = MainMenuUI(
            self.start_game, self.open_settings, self.quit_game
        )
        self.end_ui = EndUI(self.restart, self.quit_game)
        self.wire_puzzle_1 = WirePuzzleUI(
            self.audio_system, 4, self.on_wires_puzzle_1_solve, self.close_puzzle
        )
        self.wire_puzzle_2 = WirePuzzleUI(
            self.audio_system, 8, self.on_wires_puzzle_2_solve, self.close_puzzle
        )
        self.vault_puzzle = VaultPuzzleUI(
            self.audio_system,
            ("II", "I", "V", "IV"),
            self.on_vault_puzzle_solve,
            self.close_puzzle,
        )
        self.storage_puzzle = StoragePuzzleUI(
            self.audio_system,
            ("IV", "I", "III", "II"),
            self.on_storage_puzzle_solve,
            self.close_puzzle,
        )
        self.ai_chat_ui = AiChatUI(self.on_send, self.close_ai_chat)

        # Track what the AI said last so we know when a NEW response arrives
        self.last_known_text = ai_system.ai_data["text"]
        self.waiting_for_ai = False
        self.total_satisfaction = 0.5
        # self.trigger_ending()

    def start_game(self):
        self.current_state = "GAMEPLAY"
        self.level.start()

        delay_s = -1
        start_dialogs = [
            "You are the [red]last human[white] ",
            "You survived the [red]AI vs Human War[white]",
            "Your mission is to get back to earth",
            "And if you don't convince the sleeping ai to help you...",
            "[red]You will be melting in the [yellow]sun[white]    ",
            "btw it's the year [104,29,209]2[108,230,108]1[17,154,245]5[156,230,78]4[white]            ",
            "5:00  ",
            "4:59  ",
        ]
        for dialog in start_dialogs:
            self.level.create_message(dialog, delay_s=delay_s)
            delay_s += dialog.count(" ") / 4 + 1
        self.level.create_timer(
            "sun_crash", self.start_sun_crash_timer, delay_s=delay_s - 3
        )

    def start_sun_crash_timer(self):
        self.level.timers["sun_crash"].start()
        self.audio_system.play_sfx("classic_alarm")

    def restart(self):
        self.quit_game()

    def open_menu(self):
        self.current_state = "MENU"

    def open_settings(self):
        self.current_state = "SETTINGS"

    def open_puzzle(self, name):
        self.current_state = name

    def close_puzzle(self):
        self.current_state = "GAMEPLAY"

    def open_ai_chat(self):
        self.current_state = "AI_CHAT"

    def close_ai_chat(self):
        self.current_state = "GAMEPLAY"

    def quit_game(self):
        pygame.quit()
        exit()

    def on_wires_puzzle_1_solve(self):
        self.current_state = "GAMEPLAY"
        self.level.inventory.remove("wires")
        self.level.status["lower_engine_fixed"] = True
        self.audio_system.play_sfx("wires_success")

    def on_wires_puzzle_2_solve(self):
        self.current_state = "GAMEPLAY"
        self.level.inventory.remove("wires")
        self.level.status["higher_engine_fixed"] = True
        self.audio_system.play_sfx("wires_success")

    def on_vault_puzzle_solve(self):
        self.level.inventory.append("batteries")
        self.level.status["vault_open"] = True
        self.current_state = "GAMEPLAY"
        self.level.create_message("You got [21,226,237]'Batteries'      ")

    def on_storage_puzzle_solve(self):
        self.level.inventory.append("wires")
        self.level.status["front_storage_open"] = True
        self.current_state = "GAMEPLAY"
        self.level.create_message("You got A [237,39,21]'Pack of Wires'      ")

    def on_send(self, player_message):
        return ai_system.talk_to_ai(player_message)

    def handle_ai_response(self, new_data):
        self.total_satisfaction += new_data["satisfaction_change"]
        if new_data["help_human"] == True:
            self.trigger_ending()
    
    def trigger_ending(self):
        self.audio_system.change_song_to("25. Dark Factory")
        self.current_state = "END"
        if self.total_satisfaction < 1:
            self.end_ui.set_ending("MARS")
            self.level.create_message("GET SENT          ")
        else:
            self.end_ui.set_ending("EARTH")

    def trigger_lose(self):
        self.audio_system.change_song_to("25. Dark Factory")
        self.current_state = "END"
        self.end_ui.set_ending("SUN")

    def handle_events(self, event):
        if self.current_state == "MENU":
            self.main_menu_ui.handle_event(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.audio_system.change_song_to("25. Dark Factory")
        elif self.current_state == "GAMEPLAY":
            self.level.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.current_state = "MENU"
        elif self.current_state == "END":
            self.end_ui.handle_event(event)
        elif self.current_state == "WIRES_1":
            self.wire_puzzle_1.handle_event(event)
        elif self.current_state == "WIRES_2":
            self.wire_puzzle_2.handle_event(event)
        elif self.current_state == "VAULT":
            self.vault_puzzle.handle_event(event)
        elif self.current_state == "STORAGE":
            self.storage_puzzle.handle_event(event)
        elif self.current_state == "AI_CHAT":
            self.ai_chat_ui.handle_event(event)

    def update(self):
        if self.current_state == "MENU":
            self.main_menu_ui.update()
        elif self.current_state == "GAMEPLAY":
            self.level.update()
        elif self.current_state == "END":
            self.end_ui.update()
            self.level.update_messages()
        elif self.current_state == "WIRES_1":
            self.wire_puzzle_1.update()
        elif self.current_state == "WIRES_2":
            self.wire_puzzle_2.update()
        elif self.current_state == "VAULT":
            self.vault_puzzle.update()
        elif self.current_state == "STORAGE":
            self.storage_puzzle.update()
        elif self.current_state == "AI_CHAT":
            self.ai_chat_ui.update()

        if ai_system.is_thinking and not self.waiting_for_ai:
            self.waiting_for_ai = True
            self.ai_chat_ui.add_message("AI", "Thinking...")

        if self.waiting_for_ai and not ai_system.is_thinking:
            self.waiting_for_ai = False

            # Remove the temporary "Thinking..." string
            if self.ai_chat_ui.messages[-1]["text"] == "Thinking...":
                self.ai_chat_ui.messages.pop()

            # Push the real Llama 3.1 response directly onto the chat display
            new_reply = ai_system.ai_data["text"]
            self.ai_chat_ui.add_message("AI", new_reply)

            self.handle_ai_response(ai_system.ai_data)
        
        # Check if game ends
        if self.level.ready_to_end() and ai_system.ai_data["help_human"]:
            self.trigger_ending()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.star_background.draw(screen)

        if self.current_state == "MENU":
            self.main_menu_ui.draw(screen)
        elif self.current_state == "GAMEPLAY":
            self.level.draw(screen)
        elif self.current_state == "END":
            self.end_ui.draw(screen)
            self.level.draw_messages(screen)
        elif self.current_state == "WIRES_1":
            self.wire_puzzle_1.draw(screen)
        elif self.current_state == "WIRES_2":
            self.wire_puzzle_2.draw(screen)
        elif self.current_state == "VAULT":
            self.vault_puzzle.draw(screen)
        elif self.current_state == "STORAGE":
            self.storage_puzzle.draw(screen)
        elif self.current_state == "AI_CHAT":
            self.ai_chat_ui.draw(screen)
