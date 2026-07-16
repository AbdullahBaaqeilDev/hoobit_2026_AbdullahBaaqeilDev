import pygame
from pathlib import Path


class AudioSystem:
    sfx_path = "assets/audio/sfx"
    music_path = "assets/audio/music"

    def __init__(self):
        self.audio_lib = {
            "sfx": {},
            "music": {} 
        }
        self.load_audio()

    def load_audio(self):
        sfx_dir = Path(self.sfx_path)
        if sfx_dir.exists():
            for sfx_file_path in sfx_dir.glob("*.ogg"):
                name = sfx_file_path.stem
                self.audio_lib["sfx"][name] = pygame.mixer.Sound(str(sfx_file_path))

        music_dir = Path(self.music_path)
        if music_dir.exists():
            for music_file_path in music_dir.glob("*.ogg"):
                name = music_file_path.stem
                self.audio_lib["music"][name] = str(music_file_path)

    def change_song_to(self, song_name):
        if song_name in self.audio_lib["music"]:
            song_path = self.audio_lib["music"][song_name]
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play(-1)
                print(f"Now playing song: {song_name}")
            except Exception as e:
                print(f"Error playing song {song_name}: {e}")
        else:
            print(f"The song '{song_name}' not found in library")

    def play_sfx(self, sfx_name):
        if sfx_name in self.audio_lib["sfx"]:
            self.audio_lib["sfx"][sfx_name].play()
        else:
            print(f"SFX '{sfx_name}' not found in library")