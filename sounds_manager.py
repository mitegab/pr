"""Sound effects manager for the typing test application."""

import os
import threading
from pathlib import Path
import random
from config import RESOURCES_DIR

# Try importing sound libraries, fall back if not available
try:
    from playsound import playsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

try:
    import simpleaudio as sa
    SIMPLEAUDIO_AVAILABLE = True
except ImportError:
    SIMPLEAUDIO_AVAILABLE = False

# Define sounds directory
SOUNDS_DIR = RESOURCES_DIR / "sounds"
SOUNDS_DIR.mkdir(exist_ok=True)

class SoundsManager:
    """Manages sound effects for the typing test application."""
    
    def __init__(self):
        """Initialize the sounds manager."""
        self.sounds_enabled = True
        
        # Create default sound paths
        self.sounds = {
            "keypress": SOUNDS_DIR / "keypress.wav",
            "error": SOUNDS_DIR / "error.wav",
            "achievement": SOUNDS_DIR / "achievement.wav",
            "level_up": SOUNDS_DIR / "level_up.wav",
            "test_complete": SOUNDS_DIR / "test_complete.wav"
        }
        
        # Check if sounds exist, use defaults if not
        self._ensure_sound_files()
        
    def _ensure_sound_files(self):
        """Create default sound paths and make sure files exist."""
        # Check if the directory exists
        SOUNDS_DIR.mkdir(exist_ok=True)
        
        # The sound files should be provided by the user
        # This method would ideally check if the files exist and extract them from resources if not
        
        # For now, we'll just check if the files exist
        for sound_name, sound_path in self.sounds.items():
            if not sound_path.exists():
                print(f"Warning: Sound file {sound_path} not found.")
    
    def update_settings(self, settings):
        """Update sound settings."""
        self.sounds_enabled = settings.get("sound_effects", True)
    
    def play_sound(self, sound_name):
        """Play a sound by name."""
        if not self.sounds_enabled or not SOUND_AVAILABLE:
            return
            
        sound_path = self.sounds.get(sound_name)
        if not sound_path or not sound_path.exists():
            return
            
        # Play sound in a separate thread to avoid UI blocking
        threading.Thread(target=self._play_sound_file, args=(sound_path,), daemon=True).start()
    
    def _play_sound_file(self, sound_path):
        """Play a sound file using the appropriate library."""
        try:
            if SIMPLEAUDIO_AVAILABLE:
                wave_obj = sa.WaveObject.from_wave_file(str(sound_path))
                play_obj = wave_obj.play()
                # Don't wait for it to finish
            elif SOUND_AVAILABLE:
                playsound(str(sound_path), block=False)
            else:
                # Fallback - just print that we would play a sound
                print(f"Playing sound: {sound_path}")
        except Exception as e:
            print(f"Error playing sound: {e}")
    
    def play_keypress(self):
        """Play keypress sound."""
        self.play_sound("keypress")
    
    def play_error(self):
        """Play error sound."""
        self.play_sound("error")
    
    def play_achievement(self):
        """Play achievement sound."""
        self.play_sound("achievement")
    
    def play_level_up(self):
        """Play level up sound."""
        self.play_sound("level_up")
    
    def play_test_complete(self):
        """Play test complete sound."""
        self.play_sound("test_complete")
