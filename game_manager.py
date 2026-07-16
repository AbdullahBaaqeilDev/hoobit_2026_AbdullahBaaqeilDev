
import time
from level import Level
from ui import *
from audio_system import AudioSystem
from star_background import StarBackground
from debug import debug
from settings import *


class GameManager:
    def __init__(self):
        self.current_state = "MENU"
        self.level = Level()
        self.current_state = "MENU"

        self.start_time = time.time()
        self.star_background = StarBackground()
        audio_system = AudioSystem()
        level = Level()
        level.audio_system = audio_system
        self.main_menu_ui = MainMenuUI(lambda:0, lambda:0, lambda:0)

        
        # Game state variables
        user_input_text = "Who are you?"
        ai_response_text = "Press ENTER to send the message to Groq."
        is_loading = False

        # Define UI buttons, passing internal methods as the action parameter!
        # self.play_button = Button(300, 250, 200, 50, "PLAY GAME", self.start_game)
        # self.repair_button = Button(300, 320, 200, 50, "REPAIR SHIP", self.repair_ship)

    # --- BUTTON ACTIONS (Callbacks) ---
    def start_game(self):
        self.current_state = "GAMEPLAY"

    def repair_ship(self):
        # The UI safely modifies the level data directly through the manager context!
        self.level.ship_health += 25
        print(f"Ship repaired! Health is now: {self.level.ship_health}")

    # --- SYSTEM ROUTERS ---
    def handle_events(self, event):
        if self.current_state == "MENU":
            # self.play_button.handle_event(event)
            # self.repair_button.handle_event(event)
            pass
        elif self.current_state == "GAMEPLAY":
            # If escape is pressed, return to menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.current_state = "MENU"

    def update(self):
        if self.current_state == "GAMEPLAY":
            self.level.update()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.star_background.draw(screen)

        if self.current_state == "MENU":
            # self.play_button.draw(screen)
            # self.repair_button.draw(screen)
            pass
        elif self.current_state == "GAMEPLAY":
            self.level.draw(screen)