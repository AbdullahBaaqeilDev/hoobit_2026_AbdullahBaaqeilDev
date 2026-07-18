from sys import exit
from level import Level
from ui import *
from audio_system import AudioSystem
from star_background import StarBackground
from settings import *


class GameManager:
    def __init__(self):
        self.current_state = "MENU"

        self.star_background = StarBackground()
        self.audio_system = AudioSystem()
        self.level = Level(self)
        self.level.audio_system = self.audio_system

        self.main_menu_ui = MainMenuUI(self.start_game, self.open_settings, self.quit_game)
        self.end_ui = EndUI(lambda:0, lambda:0)
        self.wire_puzzle_1 = WirePuzzleUI(4, self.on_wires_puzzle_solve)
        self.wire_puzzle_2 = WirePuzzleUI(8, self.on_wires_puzzle_solve)
        self.vault_puzzle = VaultPuzzleUI(self.audio_system, ("V", "II", "III", "IV"), self.on_vault_puzzle_solve)
        
        self.audio_system.change_song_to("25. Dark Factory")
        self.current_state = "WIRES_1"

    def start_game(self):
        self.current_state = "GAMEPLAY"
        self.level.start()
        self.level.create_message("wow", 2)

    def open_menu(self):
        self.current_state = "MENU"
    
    def open_settings(self):
        self.current_state = "SETTINGS"
    
    def quit_game(self):
        pygame.quit()
        exit()

    def on_wires_puzzle_solve(self):
        self.current_state = "GAMEPLAY"

    def on_vault_puzzle_solve(self):
        self.current_state = "GAMEPLAY"

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