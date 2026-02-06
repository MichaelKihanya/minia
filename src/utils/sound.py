import pygame
import os

class SoundManager:
    """Manages all game audio"""
    def __init__(self):
        self.sounds = {}
        self.music = None
        self.music_playing = False
        self.sfx_volume = 0.7
        self.music_volume = 0.5
        self.enabled = True
    
    def load_sound(self, name, filepath):
        """Load a sound effect"""
        try:
            if os.path.exists(filepath):
                self.sounds[name] = pygame.mixer.Sound(filepath)
                self.sounds[name].set_volume(self.sfx_volume)
        except:
            print(f"Warning: Could not load sound {filepath}")
    
    def load_music(self, filepath):
        """Load background music"""
        try:
            if os.path.exists(filepath):
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.set_volume(self.music_volume)
        except:
            print(f"Warning: Could not load music {filepath}")
    
    def play_sound(self, name):
        """Play a sound effect"""
        if self.enabled and name in self.sounds:
            self.sounds[name].play()
    
    def play_music(self, loop=True):
        """Play background music"""
        if self.enabled:
            pygame.mixer.music.play(-1 if loop else 0)
            self.music_playing = True
    
    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        self.music_playing = False
    
    def set_sfx_volume(self, volume):
        """Set sound effect volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def toggle_audio(self):
        """Toggle all audio on/off"""
        self.enabled = not self.enabled
        if not self.enabled:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
        return self.enabled

# Procedural sound generation for simple chiptune-like sounds
def generate_beep(frequency=440, duration=0.1, sample_rate=22050):
    """Generate a simple beep sound"""
    import math
    
    frames = int(duration * sample_rate)
    arr = pygame.sndarray.array("C")
    
    for i in range(frames):
        value = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
        arr[i] = value
    
    return pygame.mixer.Sound(arr)

def generate_coin_sound():
    """Generate a coin collection sound"""
    # Simple up-bleep
    return pygame.mixer.Sound(pygame.sndarray.array("C"))

def generate_yoga_sound():
    """Generate a peaceful yoga sound"""
    # Sustained tone
    return pygame.mixer.Sound(pygame.sndarray.array("C"))
