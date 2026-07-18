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

        self.main_menu_ui = MainMenuUI(self.start_game, self.open_settings, self.quit_game)
        self.end_ui = EndUI(lambda:0, lambda:0)
        self.wire_puzzle_1 = WirePuzzleUI(self.audio_system, 4, self.on_wires_puzzle_1_solve, self.close_puzzle)
        self.wire_puzzle_2 = WirePuzzleUI(self.audio_system, 8, self.on_wires_puzzle_2_solve, self.close_puzzle)
        self.vault_puzzle = VaultPuzzleUI(self.audio_system, ("V", "II", "III", "IV"), self.on_vault_puzzle_solve, self.close_puzzle)
        self.ai_chat_ui = AiChatUI(self.on_send, self.close_ai_chat)
        
        self.audio_system.change_song_to("25. Dark Factory")
        # self.current_state = "AI_CHAT"

    def start_game(self):
        self.current_state = "GAMEPLAY"
        self.level.start()
        # TODO: make the dialog about the game and start the timer after that with alarm sfx
        # TODO: 3.5 to 4 words per second make an auto message age option

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
    
    def on_send(self, player_message):
        print(player_message)

    def handle_events(self, event):
        if self.current_state == "MENU":
            self.main_menu_ui.handle_event(event)
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
        elif self.current_state == "AI_CHAT":
            self.ai_chat_ui.handle_event(event)

    def update(self):
        if self.current_state == "MENU":
            self.main_menu_ui.update()
        elif self.current_state == "GAMEPLAY":
            self.level.update()
        elif self.current_state == "END":
            self.end_ui.update()
        elif self.current_state == "WIRES_1":
            self.wire_puzzle_1.update()
        elif self.current_state == "WIRES_2":
            self.wire_puzzle_2.update()
        elif self.current_state == "VAULT":
            self.vault_puzzle.update()
        elif self.current_state == "AI_CHAT":
            self.ai_chat_ui.update()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.star_background.draw(screen)

        if self.current_state == "MENU":
            self.main_menu_ui.draw(screen)
        elif self.current_state == "GAMEPLAY":
            self.level.draw(screen)
        elif self.current_state == "END":
            self.end_ui.draw(screen)
        elif self.current_state == "WIRES_1":
            self.wire_puzzle_1.draw(screen)
        elif self.current_state == "WIRES_2":
            self.wire_puzzle_2.draw(screen)
        elif self.current_state == "VAULT":
            self.vault_puzzle.draw(screen)
        elif self.current_state == "AI_CHAT":
            self.ai_chat_ui.draw(screen)