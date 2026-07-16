import os
import sys
import pygame


class Text:
    def __init__(self, text, x, y, font_size = 36, color = (255, 255, 255), font_name = None):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size) if font_name else pygame.font.Font(None, font_size)
        self.recreate_surface()

    def recreate_surface(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center = (self.x, self.y))

    def update_text(self, new_text):
        self.text = new_text
        self.recreate_surface()

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


class Button:
    def __init__(self, normal_image_path, hover_image_path, x, y, action = None):
        self.x = x
        self.y = y
        self.action = action  # Python function to call when clicked
        
        self.image_normal = self.load_button_image(normal_image_path, (200, 60), (70, 130, 180))
        self.image_hover = self.load_button_image(hover_image_path, (200, 60), (100, 180, 220))
        
        self.rect = self.image_normal.get_rect(center = (x, y))
        self.is_hovered = False

    def load_button_image(self, path, fallback_size, fallback_color):
        if os.path.exists(path):
            return pygame.image.load(path).convert_alpha()
        else:
            surf = pygame.Surface(fallback_size)
            surf.fill(fallback_color)
            return surf

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click
            if self.is_hovered and self.action:
                self.action()

    def draw(self, screen):
        current_image = self.image_hover if self.is_hovered else self.image_normal
        screen.blit(current_image, self.rect)


class MainMenuUI:
    def __init__(self, on_play, on_settings, on_quit):
        # Title of the game
        self.title_text = Text("SPACE ADVENTURE", x=400, y=100, font_size=56, color=(255, 255, 255))
        
        # Instantiate your three buttons, feeding them the callbacks directly!
        # Adjust x and y coordinates to stack them beautifully in the center
        self.play_button = Button(
            "assets/play_normal.png", "assets/play_hover.png", 
            x=400, y=220, action=on_play
        )
        
        self.settings_button = Button(
            "assets/settings_normal.png", "assets/settings_hover.png", 
            x=400, y=300, action=on_settings
        )
        
        self.quit_button = Button(
            "assets/quit_normal.png", "assets/quit_hover.png", 
            x=400, y=380, action=on_quit
        )
        
        # Keep a clean list of buttons to iterate over easily
        self.buttons = [self.play_button, self.settings_button, self.quit_button]

    def handle_event(self, event):
        # Pass the events to all of our buttons
        for button in self.buttons:
            button.handle_event(event)

    def update(self, mouse_pos):
        # Update hover status on all buttons using the current mouse coordinates
        for button in self.buttons:
            button.check_hover(mouse_pos)

    def draw(self, screen):
        # Draw our decorative background, title text, and buttons
        screen.fill((15, 15, 25))  # Smooth dark menu background
        
        self.title_text.draw(screen)
        
        for button in self.buttons:
            button.draw(screen)