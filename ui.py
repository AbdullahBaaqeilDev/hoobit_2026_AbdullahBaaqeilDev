import os
import pygame
import re
import time
import math
import random


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
    def __init__(self, normal_image_path, x, y, action = None, fallback_size = (200, 60)):
        self.x = x
        self.y = y
        self.action = action
        
        self.image_normal = self.load_button_image(normal_image_path, fallback_size, (70, 130, 180))
        hover_image_path = normal_image_path.replace("_normal", "_hover")
        self.image_hover = self.load_button_image(hover_image_path, fallback_size, (100, 180, 220))
        pressed_image_path = normal_image_path.replace("_normal", "_pressed")
        self.image_pressed = self.load_button_image(pressed_image_path, fallback_size, (100, 180, 220))
        
        self.rect = self.image_normal.get_rect(center = (x, y))
        self.is_hovered = False
        self.is_pressed = False

    def load_button_image(self, path, fallback_size, fallback_color):
        if os.path.exists(path):
            return pygame.transform.scale2x(pygame.image.load(path)).convert_alpha()
        else:
            surf = pygame.Surface(fallback_size)
            surf.fill(fallback_color)
            return surf

    def update(self):
        self.is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            self.is_pressed = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_hovered and self.action:
                self.action()
            self.is_pressed = False

    def draw(self, screen):
        current_image = self.image_normal
        if self.is_hovered:
            current_image = self.image_hover
        if self.is_pressed:
            current_image = self.image_pressed
        screen.blit(current_image, self.rect)


class Entry:
    def __init__(self, x, y, width, height, font_size=22, placeholder="Type here..."):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.placeholder = placeholder
        self.text = ""
        
        # Focus state
        self.is_active = False
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        
        try:
            self.font = pygame.font.SysFont("consolas", font_size)
        except Exception:
            self.font = pygame.font.Font(None, font_size + 4)
            
        # Cursor blink
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        # Check for mouse click to toggle selection focus
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_active = True
                # Start text input system context
                pygame.txtinput.start() if hasattr(pygame, 'txtinput') else None
            else:
                self.is_active = False

        # Capture keyboard inputs only if box is selected/active
        if self.is_active:
            if event.type == pygame.TEXTINPUT:
                self.text += event.text
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

    def update(self):
        # Blink cursor every 30 frames (~0.5 seconds)
        if self.is_active:
            self.cursor_timer += 1
            if self.cursor_timer >= 30:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
        else:
            self.cursor_visible = False

    def get_text(self):
        return self.text

    def clear(self):
        self.text = ""

    def draw(self, screen):
        # Background box
        bg_color = (20, 24, 30) if self.is_active else (15, 18, 22)
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=6)
        
        # Border outline
        border_color = (100, 180, 220) if self.is_active else (50, 55, 65)
        pygame.draw.rect(screen, border_color, self.rect, width=2, border_radius=6)

        # Render Text inside box
        if self.text == "":
            # Render empty placeholder hint text
            text_surf = self.font.render(self.placeholder, True, (80, 85, 95))
        else:
            text_surf = self.font.render(self.text, True, (230, 235, 245))

        # Clamp text position inside the left padding margin
        text_rect = text_surf.get_rect(midleft=(self.rect.left + 12, self.rect.centery))
        screen.blit(text_surf, text_rect)

        if self.cursor_visible:
            cursor_x = text_rect.right + 2 if self.text != "" else self.rect.left + 12
            pygame.draw.line(
                screen, 
                (100, 180, 220), 
                (cursor_x, self.rect.top + 10), 
                (cursor_x, self.rect.bottom - 10), 
                width=2
            )

class Message:
    def __init__(self, text, screen_width, age, padding = 20, height = 40, center_image_path = "message_center.png", font_size = 20, font_name = None):
        self.text = text
        self.screen_width = screen_width
        self.padding = padding
        self.height = height
        self.font = pygame.font.SysFont(font_name, font_size) if font_name else pygame.font.Font(None, font_size)
        
        # Load the 3-piece background (Left, Center, Right)
        left_path = center_image_path.replace("_center", "_left")
        right_path = center_image_path.replace("_center", "_right")
        
        fallback_color = (50, 50, 80)
        self.img_left = self.load_image(left_path, (20, self.height), fallback_color)
        self.img_center = self.load_image(center_image_path, (20, self.height), fallback_color)
        self.img_right = self.load_image(right_path, (20, self.height), fallback_color)
        
        # Target dimensions and positions
        self.target_width = screen_width - (padding * 2)
        self.target_y = padding
        
        # Target starting state definitions
        self.start_width = 0
        self.start_y = -self.height
        
        # Current rendering states
        self.current_width = self.target_width
        self.current_y = self.target_y
        
        # Easing Time & State Management
        self.is_animating = False
        self.animation_direction = "down"
        self.start_time = 0.0
        self.duration = 0.5   # Total time for the animation in seconds
        self.current_t = 0.0  # Normalized progress tracking variable (0.0 to 1.0)

        self.age = age
        self.birth_time = time.time() # Separate timestamp to handle expiration cleanly
        
        # Pre-render text surface
        self.text_surface = self.render_colored_text(self.text)
        
        self.surface = pygame.Surface((self.current_width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=(padding, self.current_y))
        self.update_visuals()
        self.start_transition()

    def load_image(self, path, fallback_size, fallback_color):
        if os.path.exists(path):
            original_image = pygame.image.load(path)
            return pygame.transform.scale(original_image, (original_image.get_width() * 2, self.height)).convert_alpha()
        else:
            surf = pygame.Surface(fallback_size, pygame.SRCALPHA)
            surf.fill(fallback_color)
            return surf

    def render_colored_text(self, text):
        parts = re.split(r'\[(.*?)\]', text)
        chunks = []
        current_color = (255, 255, 255)
        total_width = 0
        max_height = 0
        
        for i, part in enumerate(parts):
            if i % 2 == 1:
                try:
                    if ',' in part:
                        current_color = tuple(map(int, part.split(',')))
                    else:
                        current_color = pygame.Color(part)
                except ValueError:
                    pass
            else:
                if part:
                    surf = self.font.render(part, True, current_color)
                    chunks.append((surf, total_width))
                    total_width += surf.get_width()
                    max_height = max(max_height, surf.get_height())
                    
        combined_surf = pygame.Surface((max(1, total_width), max(1, max_height)), pygame.SRCALPHA)
        for surf, x_pos in chunks:
            combined_surf.blit(surf, (x_pos, 0))
            
        return combined_surf

    def start_transition(self, duration=0.5):
        """Prepares animation parameters and marks the start time."""
        self.duration = duration
        self.animation_direction = "down"
        self.is_animating = True
        
        # Offset start time based on current positions to allow mid-air reversals
        self.start_time = time.time() - (self.current_t * self.duration)

    def reverse_transition(self, duration=0.5):
        """Reverses the banner back up into the screen ceiling while shrinking."""
        self.duration = duration
        self.animation_direction = "up"
        self.is_animating = True
        
        # Offset start time using inverse current progress matrix 
        self.start_time = time.time() - ((1.0 - self.current_t) * self.duration)

    def animate(self):
        """Applies a Cubic Out easing formula based on time progression."""
        if not self.is_animating:
            return

        # Calculate normalized time progression elapsed (from 0.0 to 1.0)
        elapsed = time.time() - self.start_time
        
        if self.animation_direction == "down":
            self.current_t = min(1.0, elapsed / self.duration)
        else:
            self.current_t = max(0.0, 1.0 - (elapsed / self.duration))

        cubic_out = 1 - (1 - self.current_t) ** 3
        
        # Interpolate variables using the cubic progress multiplier
        self.current_width = self.start_width + (self.target_width - self.start_width) * cubic_out
        self.current_y = self.start_y + (self.target_y - self.start_y) * cubic_out
        
        # End animation sequence once target thresholds are broken
        if (self.animation_direction == "down" and self.current_t >= 1.0) or \
           (self.animation_direction == "up" and self.current_t <= 0.0):
            self.is_animating = False
            if self.animation_direction == "up":
                self.current_width = self.start_width
                self.current_y = self.start_y
            else:
                self.current_width = self.target_width
                self.current_y = self.target_y
            
        self.update_visuals()

    def update_visuals(self):
        width = int(self.current_width)
        if width <= 0:
            return
            
        self.surface = pygame.Surface((width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(midtop=(self.screen_width // 2, int(self.current_y)))
        
        lw = self.img_left.get_width()
        rw = self.img_right.get_width()
        
        if width >= lw + rw:
            center_width = width - lw - rw
            scaled_center = pygame.transform.scale(self.img_center, (center_width, self.height))
            self.surface.blit(self.img_left, (0, 0))
            self.surface.blit(scaled_center, (lw, 0))
            self.surface.blit(self.img_right, (lw + center_width, 0))
        else:
            temp_bg = pygame.Surface((lw + rw, self.height), pygame.SRCALPHA)
            temp_bg.blit(self.img_left, (0, 0))
            temp_bg.blit(self.img_right, (lw, 0))
            scaled_bg = pygame.transform.scale(temp_bg, (width, self.height))
            self.surface.blit(scaled_bg, (0, 0))
            
        if width > 50:
            text_rect = self.text_surface.get_rect(center=(width // 2, self.height // 2))
            clip_rect = pygame.Rect(0, 0, width, self.height)
            self.surface.set_clip(clip_rect)
            self.surface.blit(self.text_surface, text_rect)
            self.surface.set_clip(None)

    def update_text(self, new_text):
        self.text = new_text
        self.text_surface = self.render_colored_text(self.text)
        self.update_visuals()

    def update(self):
        # Run the active animation frame calculations
        self.animate()
        
        # Check if the message has expired (if age tracking is enabled via passing anything except -1)
        if self.age != -1 and not hasattr(self, 'auto_reversed'):
            # Total lifespan equals the arrival animation time + the requested visible age
            if time.time() - self.birth_time >= (self.duration + self.age):
                self.auto_reversed = True
                self.reverse_transition() # Naturally begin shrinking/retreating upwards

    def draw(self, screen):
        # Simply check if the banner has visual dimensions and is within screen bounds
        if self.current_width > 0 and self.rect.bottom > 0:
            screen.blit(self.surface, self.rect)


class MainMenuUI:
    def __init__(self, on_play, on_settings, on_quit):
        self.title_text = Text("SPACE ADVENTURE", x=320, y=50, font_size=56, color=(255, 255, 255), font_name="consolas")
        
        self.play_button = Button(
            "assets/images/gui/play_normal.png",
            x=320, y=150, action=on_play
        )

        # self.settings_button = Button(
        #     "assets/images/gui/settings_normal.png",
        #     x=320, y=225, action=on_settings
        # )
        
        self.quit_button = Button(
            "assets/images/gui/quit_normal.png",
            x=320, y=225, action=on_quit
        )
        
        self.buttons = [
            self.play_button, 
            # self.settings_button, 
            self.quit_button]

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self):
        for button in self.buttons:
            button.update()

    def draw(self, screen):
        self.title_text.draw(screen)
        
        for button in self.buttons:
            button.draw(screen)

class EndUI:
    def __init__(self, on_restart, on_quit):
        self.title_text = Text("THE END", x = 320, y = 50, font_size = 56, color = (255, 255, 255), font_name = "consolas")
        
        self.restart_button = Button(
            "assets/images/gui/restart_normal.png",
            x = 320, y = 150, action = on_restart
        )
        
        self.quit_button = Button(
            "assets/images/gui/quit_normal.png",
            x = 320, y = 300, action = on_quit
        )
        
        self.buttons = [self.restart_button, self.quit_button]

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self):
        for button in self.buttons:
            button.update()

    def draw(self, screen):
        self.title_text.draw(screen)
        
        for button in self.buttons:
            button.draw(screen)


class WirePuzzleUI:
    def __init__(self, audio_system, num_wires=4, on_solve=None, on_close=None):
        self.audio_system = audio_system
        self.num_wires = num_wires
        self.on_solve = on_solve
        self.on_close = on_close
        self.is_solved = False
        
        # Enforced Box Dimensions (Wider Layout: 360 wide, 360 high)
        self.box_width = 360
        self.box_height = 360
        
        # Position the bounding box dynamically in the center of the screen
        screen_size = pygame.display.get_surface().get_size() if pygame.display.get_surface() else (800, 600)
        self.box_x = (screen_size[0] - self.box_width) // 2
        self.box_y = (screen_size[1] - self.box_height) // 2
        
        # Side metal panels adjusted outward to match the wider frame
        self.panel_width = 45
        self.panel_height = 220
        self.left_panel_pos = (120, 60)
        self.right_panel_pos = (520, 60)
        
        # Well-proportioned dimensions for the wider screen interface
        self.slot_size = (22, 22) 
        self.node_radius = 6      
        self.wire_thickness = 100 / num_wires
        self.click_tolerance = 32
        
        # Load asset graphics safely
        try:
            self.left_metal_img = pygame.image.load("assets/images/gui/metal_left.png").convert_alpha()
            self.left_metal_img = pygame.transform.scale2x(self.left_metal_img)
            
            self.right_metal_img = pygame.image.load("assets/images/gui/metal_right.png").convert_alpha()
            self.right_metal_img = pygame.transform.scale2x(self.right_metal_img)
            
            self.background = pygame.image.load("assets/images/gui/wires_puzzle_background.png").convert_alpha()
            self.background = pygame.transform.scale2x(self.background)
            # raise pygame.error
        except (pygame.error, FileNotFoundError):
            self.left_metal_img = None
            self.right_metal_img = None
            self.background = None

        # Setup Bright Colors & Node Arrays
        self.colors = self._generate_bright_colors(self.num_wires)
        self.left_nodes = []
        self.right_nodes = []
        self._init_nodes()
        
        # Micro Interaction State
        self.active_wire = None 
        self.mouse_pos = (0, 0)
        
    def _generate_bright_colors(self, count, min_distance=90):
        """Generates bright colors that are guaranteed to be distinct using a safe loop."""
        colors = []
        attempts = 0
        max_attempts = 200
        
        current_C = min_distance

        while len(colors) < count and attempts < max_attempts:
            new_color = self._make_single_bright_color()
            attempts += 1
            
            # Check if this new color is far enough from all colors already in list
            is_distinct = True
            for existing_color in colors:
                r_diff = new_color[0] - existing_color[0]
                g_diff = new_color[1] - existing_color[1]
                b_diff = new_color[2] - existing_color[2]
                distance = math.sqrt(r_diff**2 + g_diff**2 + b_diff**2)
                
                if distance < current_C:
                    is_distinct = False
                    break
            
            if is_distinct:
                colors.append(new_color)
                
            # Loop protection: If struggling to find perfect colors after 100 tries,
            # slightly lower the strictness threshold C so the game doesn't hang.
            if attempts > 100 and current_C > 50:
                current_C -= 5

        # Fallback: If the safety cap hit and we don't have enough colors, just fill the rest
        while len(colors) < count:
            colors.append(self._make_single_bright_color())

        return colors

    def _make_single_bright_color(self):
        """Helper to generate one bright neon-like color."""
        base = [random.randint(200, 255), random.randint(120, 255), random.randint(0, 60)]
        random.shuffle(base)
        return tuple(base)
    
    def _init_nodes(self):
        available_height = self.panel_height
        step = available_height // max(1, (self.num_wires - 1)) if self.num_wires > 1 else 0
        
        # Spawning wire attachments inside the inner borders
        for i in range(self.num_wires):
            x = self.left_panel_pos[0]
            y = self.left_panel_pos[1] + (i * step)
            self.left_nodes.append({
                "id": i,
                "color": self.colors[i],
                "pos": (x, y),
                "connected": False,
                "target_pos": None
            })
            
        shuffled_indices = list(range(self.num_wires))
        random.shuffle(shuffled_indices)
        
        for idx, wire_id in enumerate(shuffled_indices):
            x = self.right_panel_pos[0]
            y = self.right_panel_pos[1] + (idx * step)
            self.right_nodes.append({
                "id": wire_id,
                "color": self.colors[wire_id],
                "pos": (x, y),
                "connected": False
            })

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.on_close()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            self.is_solved = True
            if self.on_solve:
                self.on_solve()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for node in self.left_nodes:
                if not node["connected"] and self._is_near(mouse_pos, node["pos"]):
                    self.active_wire = node
                    break
                    
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.active_wire:
                mouse_pos = pygame.mouse.get_pos()
                for right_node in self.right_nodes:
                    if self._is_near(mouse_pos, right_node["pos"]):
                        # if right_node["id"] == self.active_wire["id"]:
                        self.active_wire["connected"] = True
                        self.active_wire["target_pos"] = right_node["pos"]
                        right_node["connected"] = True
                        self._check_victory()
                        self.audio_system.play_sfx(f"connect_light_{random.choice((1, 2, 3, 4))}")
                        break
                self.active_wire = None

        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            mouse_pos = pygame.mouse.get_pos()
            for right_node in self.right_nodes:
                if self._is_near(mouse_pos, right_node["pos"]) and right_node["connected"]:
                    right_node["connected"] = False
                    for left_node in self.left_nodes:
                        if left_node["target_pos"] == right_node["pos"]:
                            left_node["connected"] = False
                            self.audio_system.play_sfx(f"electric_shock_{random.choice((1, 2, 3))}")
                            break
                    self._check_victory()
                    break

    def update(self):
        if self.active_wire:
            self.mouse_pos = pygame.mouse.get_pos()

    def _check_victory(self):
        for left in self.left_nodes:
            for right in self.right_nodes:
                if right["pos"] == left["target_pos"]:
                    if right["color"] != left["color"]:
                        return
                if not right["connected"]: return
            if not left["connected"]: return
        self.is_solved = True
        if self.on_solve:
            self.on_solve()

    def _is_near(self, pos1, pos2):
        return math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1]) <= self.click_tolerance

    def draw_wire(self, screen, start, target, color, shading_count = 10):
        x0, y0 = start
        x1, y1 = target
        r, g, b = color
        step = 1 / shading_count
        for i in range(shading_count):
            pygame.draw.line(
                screen, 
                (int(r * (shading_count - i)*step), int(g * (shading_count - i)*step), int(b * (shading_count - i)*step)), 
                (x0, y0 + (self.wire_thickness*i*step)), 
                (x1, y1 + (self.wire_thickness*i*step)), 
                width=int(self.wire_thickness*(shading_count / (i+shading_count)))
            )

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            pygame.draw.rect(screen, (30, 32, 38), (self.box_x, self.box_y, self.box_width, self.box_height), border_radius=12)
            pygame.draw.rect(screen, (50, 55, 65), (self.box_x, self.box_y, self.box_width, self.box_height), width=2, border_radius=12)


        # Sockets
        for node in self.left_nodes + self.right_nodes:
            # slot_x = node["pos"][0] - (self.slot_size[0] // 2)
            # slot_y = node["pos"][1] - (self.slot_size[1] // 2)
            
            pygame.draw.circle(screen, (20, 22, 26), node["pos"], self.slot_size[0] // 2)
            pygame.draw.circle(screen, (70, 75, 85), node["pos"], self.slot_size[0] // 2, width=1)

        # Connected Lines
        for node in self.left_nodes:
            if node["connected"] and node["target_pos"]:
                self.draw_wire(screen, node["pos"], node["target_pos"], node["color"])

        # Active Dragging Line
        if self.active_wire:
            self.draw_wire(screen, self.active_wire["pos"], self.mouse_pos, self.active_wire["color"])
        
        # Side Metal Strips
        if self.left_metal_img and self.right_metal_img:
            screen.blit(self.left_metal_img, (0, 0))
            screen.blit(self.right_metal_img, self.right_metal_img.get_rect(topright = (screen.get_width(), 0)))
        else:
            pygame.draw.rect(screen, (45, 48, 54), (*self.left_panel_pos, self.panel_width, self.panel_height), border_radius=4)
            pygame.draw.rect(screen, (45, 48, 54), (*self.right_panel_pos, self.panel_width, self.panel_height), border_radius=4)

        # Wire Pin Headers
        for node in self.left_nodes:
            pygame.draw.circle(screen, node["color"], node["pos"], self.node_radius)
        for node in self.right_nodes:
            if node["connected"]:
                pygame.draw.circle(screen, node["color"], node["pos"], self.node_radius)
            else:
                pygame.draw.circle(screen, (60, 65, 70), node["pos"], self.node_radius)

class VaultPuzzleUI:
    def __init__(self, audio_system, solution=None, on_solve=None, on_close=None):
        self.audio_system = audio_system
        self.solution = solution if solution else ["I", "II", "III", "IV"]
        self.on_solve = on_solve
        self.on_close = on_close
        self.is_solved = False
        self.current_input = []
        
        # Calculator Casing Dimensions
        self.box_width = 260
        self.box_height = 240
        
        # Center
        screen_size = pygame.display.get_surface().get_size() if pygame.display.get_surface() else (800, 600)
        self.box_x = 140
        self.box_y = 60
        
        # Black Screen Surface Dimensions (Top of calculator)
        self.screen_rect = pygame.Rect(self.box_x + 10, self.box_y + 9, 250, 40)
        
        # Setup Fonts for Display Screen
        try:
            self.font = pygame.font.SysFont("consolas", 32, bold=True)
        except Exception:
            self.font = pygame.font.Font(None, 38)
            
        # Initialize the 6 Calculator Buttons using your Button class
        self.buttons = []
        self._init_buttons()

        self.background = pygame.transform.scale2x(pygame.image.load("assets/images/gui/vault_puzzle_background.png").convert_alpha())
        
        # UI Feedback State
        self.error_timer = 0 # Used to flash the screen red on wrong answer

    def _init_buttons(self):
        # We use standard strings for labels.
        # Ensure you have files like: "assets/images/gui/1_normal.png", "assets/images/gui/send_normal.png", etc.
        labels = ["I", "II", "III", "IV", "V", "insert"]
        
        grid_start_y = self.box_y + 75
        btn_w = 60
        btn_h = 60
        gap_x = 25
        gap_y = 15
        
        for idx, label in enumerate(labels):
            col = idx % 3
            row = idx // 3
            
            # Calculate center X and Y for your Button's center-based rect
            center_x = self.box_x + 20 + (col * (btn_w + gap_x)) + (btn_w // 2)
            center_y = grid_start_y + (row * (btn_h + gap_y)) + (btn_h // 2)
            
            # Construct exact asset path expected by your Button class
            image_path = f"assets/images/gui/{label}_normal.png"
            
            # Create action callback binding the specific label to the click handler
            action_callback = lambda l=label: self._on_button_click(l)
            
            # Instantiate your exact Button class!
            btn = Button(
                normal_image_path=image_path,
                x=center_x,
                y=center_y,
                action=action_callback,
                fallback_size=(60, 60)
            )
            
            self.buttons.append(btn)

    def _on_button_click(self, label):
        self.audio_system.play_sfx(f"rusty_click_{random.choice((1, 2, 3))}")
        if label == "insert":
            # Check if input matches the 4-digit solution!
            if \
                len(self.current_input) == len(self.solution) and\
                all([self.current_input[i] == self.solution[i] for i in range(len(self.current_input))]):

                self.is_solved = True
                if self.on_solve:
                    self.on_solve()
                self.audio_system.play_sfx(f"vault_success")
            else:
                # Wrong answer: Flash red and clear input
                self.error_timer = 30 # Flash for 30 frames (~0.5 seconds)
                self.current_input = []
                self.audio_system
                self.audio_system.play_sfx(f"vault_fail_{random.choice((1, 2, 3))}")
        else:
            # It's a numeral button ("I" through "V")
            # Only allow typing up to 4 digits (matching the 4 Xs)
            if len(self.current_input) < 4:
                self.current_input.append(label)

    def handle_event(self, event):       
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.on_close()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            self.is_solved = True
            if self.on_solve:
                self.on_solve()
            self.audio_system.play_sfx(f"vault_success")

        # Pass events directly to your Button instances
        for btn in self.buttons:
            btn.handle_event(event)

    def update(self):
        if self.is_solved:
            return

        # Update hover states on your Button instances
        for btn in self.buttons:
            btn.update()
            
        # Count down error flash timer
        if self.error_timer > 0:
            self.error_timer -= 1

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Draw Calculator Outer Casing
        # pygame.draw.rect(screen, (35, 38, 45), (self.box_x, self.box_y, self.box_width, self.box_height), border_radius=15)
        # pygame.draw.rect(screen, (60, 65, 75), (self.box_x, self.box_y, self.box_width, self.box_height), width=3, border_radius=15)

        # Draw Black Display Screen
        # If error_timer is active, give the screen a red warning tint!
        if self.error_timer > 0:
            screen_color = (60, 15, 15) if self.error_timer > 0 else (10, 12, 15)
            pygame.draw.rect(screen, screen_color, self.screen_rect, border_radius=8)
            pygame.draw.rect(screen, (80, 85, 95), self.screen_rect, width=2, border_radius=8)

        # Render the 4 Digits / Xs on the Display Screen
        self._draw_screen_text(screen)

        # Draw Your Custom Calculator Buttons
        for btn in self.buttons:
            btn.draw(screen)

    def _draw_screen_text(self, screen):
        # Construct a 4-slot display array
        display_slots = []
        for i in range(4):
            if i < len(self.current_input):
                display_slots.append(("-", (0, 255, 150))) # Bright cyan/green for entered code
            else:
                display_slots.append(("X", (70, 75, 85))) # Dim gray for un-entered Xs

        # Draw each slot evenly spaced across the black screen
        slot_width = self.screen_rect.width // 4
        for idx, (text_str, color) in enumerate(display_slots):
            # Override color to red if error flash is active
            if self.error_timer > 0:
                color = (255, 80, 80)
                
            text_surf = self.font.render(text_str, True, color)
            text_rect = text_surf.get_rect(center=(
                self.screen_rect.left + (idx * slot_width) + (slot_width // 2),
                self.screen_rect.centery
            ))
            screen.blit(text_surf, text_rect)


class StoragePuzzleUI:
    def __init__(self, audio_system, solution=None, on_solve=None, on_close=None):
        self.audio_system = audio_system
        self.solution = solution if solution else ["I", "II", "III", "IV"]
        self.on_solve = on_solve
        self.on_close = on_close
        self.is_solved = False
        self.current_input = []
        
        # Calculator Casing Dimensions
        self.box_width = 260
        self.box_height = 240
        
        # Center dynamically on screen
        screen_size = pygame.display.get_surface().get_size() if pygame.display.get_surface() else (800, 600)
        self.box_x = 140
        self.box_y = 60
        
        # Black Screen Surface Dimensions (Top of calculator)
        self.screen_rect = pygame.Rect(self.box_x + 10, self.box_y + 9, 250, 40)
        
        # Setup Fonts for Display Screen
        try:
            self.font = pygame.font.SysFont("consolas", 32, bold=True)
        except Exception:
            self.font = pygame.font.Font(None, 38)
            
        # Initialize the 6 Calculator Buttons using your Button class
        self.buttons = []
        self._init_buttons()

        self.background = pygame.transform.scale2x(pygame.image.load("assets/images/gui/storage_puzzle_background.png").convert_alpha())
        
        # UI Feedback State
        self.error_timer = 0 # Used to flash the screen red on wrong answer

    def _init_buttons(self):
        # We use standard strings for labels.
        # Ensure you have files like: "assets/images/gui/1_normal.png", "assets/images/gui/send_normal.png", etc.
        labels = ["I", "II", "III", "IV", "V", "insert"]
        
        grid_start_y = self.box_y + 75
        btn_w = 60
        btn_h = 60
        gap_x = 25
        gap_y = 15
        
        for idx, label in enumerate(labels):
            col = idx % 3
            row = idx // 3
            
            # Calculate center X and Y for your Button's center-based rect
            center_x = self.box_x + 20 + (col * (btn_w + gap_x)) + (btn_w // 2)
            center_y = grid_start_y + (row * (btn_h + gap_y)) + (btn_h // 2)
            
            # Construct exact asset path expected by your Button class
            image_path = f"assets/images/gui/{label}_normal.png"
            
            # Create action callback binding the specific label to the click handler
            action_callback = lambda l=label: self._on_button_click(l)
            
            # Instantiate your exact Button class!
            btn = Button(
                normal_image_path=image_path,
                x=center_x,
                y=center_y,
                action=action_callback,
                fallback_size=(60, 60)
            )
            
            self.buttons.append(btn)

    def _on_button_click(self, label):
        self.audio_system.play_sfx(f"rusty_click_{random.choice((1, 2, 3))}")
        if label == "insert":
            # Check if input matches the 4-digit solution!
            if \
                len(self.current_input) == len(self.solution) and\
                all([self.current_input[i] == self.solution[i] for i in range(len(self.current_input))]):

                self.is_solved = True
                if self.on_solve:
                    self.on_solve()
                self.audio_system.play_sfx(f"vault_success")
            else:
                # Wrong answer: Flash red and clear input
                self.error_timer = 30 # Flash for 30 frames (~0.5 seconds)
                self.current_input = []
                self.audio_system
                self.audio_system.play_sfx(f"vault_fail_{random.choice((1, 2, 3))}")
        else:
            # It's a numeral button ("I" through "V")
            # Only allow typing up to 4 digits (matching the 4 Xs)
            if len(self.current_input) < 4:
                self.current_input.append(label)

    def handle_event(self, event):       
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.on_close()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            self.is_solved = True
            if self.on_solve:
                self.on_solve()
            self.audio_system.play_sfx(f"vault_success")

        # Pass events directly to your Button instances
        for btn in self.buttons:
            btn.handle_event(event)

    def update(self):
        if self.is_solved:
            return

        # Update hover states on your Button instances
        for btn in self.buttons:
            btn.update()
            
        # Count down error flash timer
        if self.error_timer > 0:
            self.error_timer -= 1

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Draw Calculator Outer Casing
        # pygame.draw.rect(screen, (35, 38, 45), (self.box_x, self.box_y, self.box_width, self.box_height), border_radius=15)
        # pygame.draw.rect(screen, (60, 65, 75), (self.box_x, self.box_y, self.box_width, self.box_height), width=3, border_radius=15)

        # Draw Black Display Screen
        # If error_timer is active, give the screen a red warning tint!
        if self.error_timer > 0:
            screen_color = (60, 15, 15) if self.error_timer > 0 else (10, 12, 15)
            pygame.draw.rect(screen, screen_color, self.screen_rect, border_radius=8)
            pygame.draw.rect(screen, (80, 85, 95), self.screen_rect, width=2, border_radius=8)

        # Render the 4 Digits / Xs on the Display Screen
        self._draw_screen_text(screen)

        # Draw Your Custom Calculator Buttons
        for btn in self.buttons:
            btn.draw(screen)

    def _draw_screen_text(self, screen):
        # Construct a 4-slot display array
        display_slots = []
        for i in range(4):
            if i < len(self.current_input):
                display_slots.append(("-", (0, 255, 150))) # Bright cyan/green for entered code
            else:
                display_slots.append(("X", (70, 75, 85))) # Dim gray for un-entered Xs

        # Draw each slot evenly spaced across the black screen
        slot_width = self.screen_rect.width // 4
        for idx, (text_str, color) in enumerate(display_slots):
            # Override color to red if error flash is active
            if self.error_timer > 0:
                color = (255, 80, 80)
                
            text_surf = self.font.render(text_str, True, color)
            text_rect = text_surf.get_rect(center=(
                self.screen_rect.left + (idx * slot_width) + (slot_width // 2),
                self.screen_rect.centery
            ))
            screen.blit(text_surf, text_rect)

class AiChatUI:
    def __init__(self, on_send=None, on_close=None):
        self.on_send = on_send
        self.on_close = on_close
        self.is_ai_active = False
        
        # Chat History Storage
        self.messages = [
            {"sender": "AI", "text": "Press ENTER to begin communication..."}
        ]
        
        # Screen boundaries setup
        screen_size = pygame.display.get_surface().get_size() if pygame.display.get_surface() else (800, 600)
        scr_w, scr_h = screen_size[0], screen_size[1]
        
        panel_y = scr_h - 45
        entry_w = int(scr_w * 0.70)
        entry_h = 45
        
        entry_center_x = (scr_w - 120) // 2
        button_center_x = scr_w - 70
        
        # Instantiate Sibling UI Components
        self.input_entry = Entry(
            x=entry_center_x, 
            y=panel_y, 
            width=entry_w, 
            height=entry_h, 
            placeholder="Ask your Spaceship AI something..."
        )
        
        self.send_button = Button(
            normal_image_path="assets/images/gui/send_normal.png",
            x=button_center_x,
            y=panel_y,
            action=self.submit_message
        )
        
        # Chat History Display Box Dimensions
        self.history_height = 220 # Slightly taller to give space for wrapped sentences
        self.history_rect = pygame.Rect(
            20, 
            scr_h - 70 - self.history_height - 10, 
            scr_w - 40, 
            self.history_height
        )
        
        # Setup Font
        try:
            self.chat_font = pygame.font.SysFont("consolas", 18, bold=True)
        except Exception:
            self.chat_font = pygame.font.Font(None, 22)

    def add_message(self, sender, text):
        self.messages.append({"sender": sender, "text": text})

    def submit_message(self):
        message = self.input_entry.get_text().strip()
        if message:
            self.add_message("PLAYER", message)
            if self.on_send:
                self.on_send(message)
            self.input_entry.clear()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.on_close:
                self.on_close()
            return
    
        self.input_entry.handle_event(event)
        self.send_button.handle_event(event)
        
        if event.type == pygame.KEYDOWN and self.input_entry.is_active:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.submit_message()

    def update(self):
        self.input_entry.update()
        self.send_button.update()

    def _wrap_text(self, text, max_width):
        """
        Splits a string of text into an array of lines that fit 
        comfortably within max_width pixels based on the active font.
        """
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            # Test what adding this word does to the width
            test_line = current_line + " " + word if current_line else word
            width, _ = self.chat_font.size(test_line)
            
            if width <= max_width:
                current_line = test_line
            else:
                # Line is full, save it and start a new line with the current word
                if current_line:
                    lines.append(current_line)
                current_line = word
                
        if current_line:
            lines.append(current_line)
            
        return lines

    def draw(self, screen):
        # DRAW CHAT HISTORY PANEL BACKING
        history_surface = pygame.Surface((self.history_rect.width, self.history_rect.height), pygame.SRCALPHA)
        history_surface.fill((10, 14, 20, 210)) 
        screen.blit(history_surface, self.history_rect.topleft)
        pygame.draw.rect(screen, (60, 70, 85), self.history_rect, width=2, border_radius=8)
        
        # PROCESS AND WRAP ALL TEXT
        # We need to turn our history into a clean list of ready-to-draw lines
        render_queue = []
        padding_margin = 30
        max_text_width = self.history_rect.width - padding_margin
        
        for msg in self.messages:
            prefix = "YOU: " if msg["sender"] == "PLAYER" else "AI: "
            color = (100, 220, 255) if msg["sender"] == "PLAYER" else (255, 120, 80)
            
            # Wrap the string based on our layout limits
            wrapped_lines = self._wrap_text(prefix + msg["text"], max_text_width)
            
            for line in wrapped_lines:
                render_queue.append({"text": line, "color": color})

        # RENDER ONLY THE MOST RECENT WRAPPED LINES FROM THE BOTTOM UP
        line_height = 24
        # Calculate exactly how many items we can display inside our box height
        max_lines_visible = (self.history_rect.height - 20) // line_height
        
        # Slice off everything except the very last lines to fit the view
        lines_to_draw = render_queue[-max_lines_visible:]
        
        start_y = self.history_rect.top + 12
        for idx, line_data in enumerate(lines_to_draw):
            text_surf = self.chat_font.render(line_data["text"], True, line_data["color"])
            screen.blit(text_surf, (self.history_rect.left + 15, start_y + (idx * line_height)))

        # DRAW BOTTOM INPUT TRAY
        tray_rect = pygame.Rect(0, screen.get_height() - 70, screen.get_width(), 70)
        tray_surface = pygame.Surface((tray_rect.width, tray_rect.height), pygame.SRCALPHA)
        tray_surface.fill((8, 10, 15, 230))
        screen.blit(tray_surface, tray_rect.topleft)
        
        self.input_entry.draw(screen)
        self.send_button.draw(screen)