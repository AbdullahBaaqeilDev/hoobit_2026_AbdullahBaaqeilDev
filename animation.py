
import pygame
import os

class Animation:
    def __init__(self, x, y, speed=0.15, loop=True):
        self.x = x
        self.y = y
        self.speed = speed   # How fast the animation plays (increment value)
        self.loop = loop     # Should it restart when hitting the final frame?
        
        self.frames = []
        self.frame_index = 0.0
        self.is_playing = True

    def load_frames(self, folder_path, scale_size=None):
        """
        Scans a directory for all .png image assets, sorts them alphabetically, 
        and appends them scaled to the internal frame collection tracker.
        """
        self.frames.clear()
        self.frame_index = 0.0
        
        if not os.path.exists(folder_path):
            print(f"⚠️ Animation Error: Folder path '{folder_path}' does not exist.")
            return

        # Gather and alphabetically sort all files matching the criteria
        valid_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
        valid_files.sort()

        for filename in valid_files:
            full_path = os.path.join(folder_path, filename)
            try:
                img = pygame.image.load(full_path).convert_alpha()
                if scale_size:
                    img = pygame.transform.scale(img, scale_size)
                self.frames.append(img)
            except pygame.error as e:
                print(f"❌ Failed to load animation frame: {full_path}. Error: {e}")

        if not self.frames:
            print(f"⚠️ Animation Warning: No valid PNG frames found inside '{folder_path}'")

    def animate(self):
        """Advances the internal floating-point index frame tracker."""
        if not self.is_playing or not self.frames:
            return

        # Advance the index step frame dynamically using the speed scalar
        self.frame_index += self.speed

        # Handle reaching the end of the sequence array indices bounds
        if self.frame_index >= len(self.frames):
            if self.loop:
                self.frame_index = 0.0
            else:
                self.frame_index = float(len(self.frames) - 1)
                self.is_playing = False # Stop on the last frame

    def update(self):
        """Standard lifecycle hook. Drives calculation cycles forward."""
        self.animate()

    def play(self):
        self.is_playing = True

    def stop(self):
        self.is_playing = False
        self.frame_index = 0.0

    def draw(self, screen):
        """Renders the current active frame centered over the coordinates."""
        if not self.frames:
            return

        # Cast the float index down to a clean int index to pull from array lists
        current_idx = int(self.frame_index)
        current_frame = self.frames[current_idx]
        
        # Draw frame centered over target point coordinates
        rect = current_frame.get_rect(center=(self.x, self.y))
        screen.blit(current_frame, rect)