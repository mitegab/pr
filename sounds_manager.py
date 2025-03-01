"""Sound manager for handling sound effects in the application."""

import os
import platform
import threading
from pathlib import Path
from config import RESOURCES_DIR

# Try to import sound libraries based on platform
SOUND_BACKEND = "none"
if platform.system() == "Windows":
    try:
        import winsound
        SOUND_BACKEND = "winsound"
    except ImportError:
        print("Warning: winsound module not available. Sound effects will be disabled.")
else:
    # For Linux and MacOS
    try:
        import pygame
        pygame.mixer.init()
        SOUND_BACKEND = "pygame"
    except ImportError:
        print("Warning: pygame module not available. Sound effects will be disabled.")
        print("You can install it with: pip install pygame")

# Create sounds directory
SOUNDS_DIR = RESOURCES_DIR / "sounds"
SOUNDS_DIR.mkdir(exist_ok=True)

class SoundsManager:
    """Manages sound effects for typing test application."""
    
    def __init__(self):
        """Initialize sounds manager."""
        self.enabled = SOUND_BACKEND != "none"
        self.volume = 70  # Default volume (0-100)
        self.key_sounds_enabled = True
        self.error_sounds_enabled = True
        self.achievement_sounds_enabled = True
        
        # Create placeholder files if they don't exist
        self.ensure_sound_files_exist()
        
        # Preload sound files
        self.sounds = {}
        for sound_name in ["keypress", "error", "achievement", "level_up", "test_complete"]:
            self.sounds[sound_name] = self._load_sound(f"{sound_name}.wav")
    
    def ensure_sound_files_exist(self):
        """Ensure that basic sound files exist in the sounds directory."""
        sound_files = [
            "keypress.wav",
            "error.wav",
            "achievement.wav", 
            "level_up.wav",
            "test_complete.wav"
        ]
        
        for filename in sound_files:
            sound_path = SOUNDS_DIR / filename
            if not sound_path.exists():
                self._create_placeholder_sound(sound_path)
    
    def _load_sound(self, filename):
        """Load a sound file."""
        if not self.enabled:
            return None
        
        sound_path = SOUNDS_DIR / filename
        
        # Return None if file doesn't exist
        if not sound_path.exists():
            print(f"Warning: Sound file not found: {sound_path}")
            return None
        
        if SOUND_BACKEND == "pygame":
            try:
                sound = pygame.mixer.Sound(str(sound_path))
                sound.set_volume(self.volume / 100.0)  # Set initial volume
                return sound
            except Exception as e:
                print(f"Error loading sound with pygame: {filename} - {e}")
                return None
        else:
            # For winsound, just return the path
            return str(sound_path)
    
    def _create_placeholder_sound(self, path):
        """Create a placeholder sound file."""
        # This is a simple WAV file header for an empty sound
        # Real implementation would include actual sound files
        try:
            with open(path, 'wb') as f:
                # Write WAV header
                f.write(b'RIFF')
                f.write((36).to_bytes(4, 'little'))  # File size
                f.write(b'WAVE')
                f.write(b'fmt ')
                f.write((16).to_bytes(4, 'little'))  # Subchunk size
                f.write((1).to_bytes(2, 'little'))   # PCM
                f.write((1).to_bytes(2, 'little'))   # Mono
                f.write((8000).to_bytes(4, 'little'))  # Sample rate
                f.write((8000).to_bytes(4, 'little'))  # Byte rate
                f.write((1).to_bytes(2, 'little'))   # Block align
                f.write((8).to_bytes(2, 'little'))   # Bits per sample
                f.write(b'data')
                f.write((0).to_bytes(4, 'little'))   # Subchunk2 size
        except Exception as e:
            print(f"Error creating placeholder sound file {path}: {e}")
    
    def set_volume(self, volume):
        """Set volume level (0-100)."""
        self.volume = max(0, min(100, volume))
        
        if SOUND_BACKEND == "pygame":
            # Update volume for all loaded sounds
            for sound in self.sounds.values():
                if sound:
                    try:
                        sound.set_volume(self.volume / 100.0)
                    except Exception as e:
                        print(f"Error setting volume: {e}")
    
    def enable(self, enabled=True):
        """Enable or disable all sounds."""
        if SOUND_BACKEND == "none":
            self.enabled = False
        else:
            self.enabled = enabled
    
    def play_sound(self, sound_name):
        """Play a sound by name."""
        if not self.enabled:
            return
        
        sound = self.sounds.get(sound_name)
        if not sound:
            return
        
        # Play in a separate thread to avoid blocking
        thread = threading.Thread(target=self._play_sound_thread, args=(sound,))
        thread.daemon = True
        thread.start()
    
    def _play_sound_thread(self, sound):
        """Play sound in a separate thread."""
        try:
            if SOUND_BACKEND == "winsound":
                import winsound
                winsound.PlaySound(sound, winsound.SND_FILENAME)
            elif SOUND_BACKEND == "pygame":
                try:
                    sound.play()
                except Exception as e:
                    print(f"Error playing sound with pygame: {e}")
        except Exception as e:
            print(f"Error playing sound: {e}")
    
    def play_keypress(self):
        """Play keypress sound."""
        if self.key_sounds_enabled:
            self.play_sound("keypress")
    
    def play_error(self):
        """Play error sound."""
        if self.error_sounds_enabled:
            self.play_sound("error")
    
    def play_achievement(self):
        """Play achievement sound."""
        if self.achievement_sounds_enabled:
            self.play_sound("achievement")
    
    def play_level_up(self):
        """Play level up sound."""
        if self.achievement_sounds_enabled:
            self.play_sound("level_up")
    
    def play_test_complete(self):
        """Play test complete sound."""
        if self.enabled:
            self.play_sound("test_complete")
    
    def update_settings(self, settings):
        """Update sound settings from user settings."""
        self.enable(settings.get("sound_effects", True))
        self.set_volume(settings.get("volume", 70))
        self.key_sounds_enabled = settings.get("key_sounds", True)
        self.error_sounds_enabled = settings.get("error_sounds", True)
        self.achievement_sounds_enabled = settings.get("achievement_sounds", True)
