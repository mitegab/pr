"""Settings screen for customizing application behavior."""

import tkinter as tk
from tkinter import ttk
from config import COLORS, FONTS, THEMES
from simplified_ui import (
    create_label, create_button, create_frame, create_entry
)

class SettingsScreen:
    """Settings screen for customizing application preferences."""
    
    def __init__(self, root, user_manager, current_user, on_save=None):
        """Initialize the settings screen."""
        self.root = root
        self.user_manager = user_manager
        self.current_user = current_user
        self.on_save = on_save
        
        # Load current settings
        self.settings = self.user_manager.get_user_settings(current_user) or {
            "theme": "light",
            "sound_effects": True,
            "keyboard_layout": "QWERTY",
            "default_difficulty": "Intermediate"
        }
        
    def show(self):
        """Show the settings screen."""
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("600x600")
        self.settings_window.transient(self.root)
        self.settings_window.grab_set()
        
        # Center on parent
        x = self.root.winfo_x() + (self.root.winfo_width() - 600) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 600) // 2
        self.settings_window.geometry(f"+{x}+{y}")
        
        self.settings_window.configure(bg=COLORS["background"])
        self.create_settings_ui()
    
    def create_settings_ui(self):
        """Create the settings UI."""
        main_frame = create_frame(self.settings_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = create_label(header_frame, "Settings", font_size=24, weight="bold")
        title_label.pack(side=tk.LEFT)
        
        close_button = create_button(
            header_frame,
            text="Close",
            command=self.close_settings,
            style="SecondaryButton.TButton"
        )
        close_button.pack(side=tk.RIGHT)
        
        # Create settings cards
        self.create_appearance_settings(main_frame)
        self.create_audio_settings(main_frame)
        self.create_typing_settings(main_frame)
        
        # Save button at the bottom
        save_button = create_button(
            main_frame,
            text="Save Settings",
            command=self.save_settings,
            style="PrimaryButton.TButton"
        )
        save_button.pack(pady=20)
    
    def create_appearance_settings(self, parent):
        """Create appearance settings card."""
        appearance_frame = create_frame(parent, padding=15, bg_color=COLORS["card_background"])
        appearance_frame.pack(fill=tk.X, pady=10)
        
        appearance_title = create_label(appearance_frame, "Appearance", font_size=18, weight="bold")
        appearance_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Theme selection
        theme_frame = ttk.Frame(appearance_frame)
        theme_frame.pack(fill=tk.X, pady=5)
        
        theme_label = create_label(theme_frame, "Theme:", font_size=14)
        theme_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "light"))
        
        theme_option_frame = ttk.Frame(theme_frame)
        theme_option_frame.pack(side=tk.LEFT)
        
        for theme in ["light", "dark"]:
            theme_rb = ttk.Radiobutton(
                theme_option_frame,
                text=theme.capitalize(),
                value=theme,
                variable=self.theme_var
            )
            theme_rb.pack(side=tk.LEFT, padx=10)
    
    def create_audio_settings(self, parent):
        """Create audio settings card."""
        audio_frame = create_frame(parent, padding=15, bg_color=COLORS["card_background"])
        audio_frame.pack(fill=tk.X, pady=10)
        
        audio_title = create_label(audio_frame, "Audio", font_size=18, weight="bold")
        audio_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Sound effects toggle
        sound_frame = ttk.Frame(audio_frame)
        sound_frame.pack(fill=tk.X, pady=5)
        
        sound_label = create_label(sound_frame, "Sound Effects:", font_size=14)
        sound_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.sound_var = tk.BooleanVar(value=self.settings.get("sound_effects", True))
        sound_check = ttk.Checkbutton(sound_frame, text="Enabled", variable=self.sound_var)
        sound_check.pack(side=tk.LEFT)
    
    def create_typing_settings(self, parent):
        """Create typing-related settings card."""
        typing_frame = create_frame(parent, padding=15, bg_color=COLORS["card_background"])
        typing_frame.pack(fill=tk.X, pady=10)
        
        typing_title = create_label(typing_frame, "Typing Settings", font_size=18, weight="bold")
        typing_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Keyboard layout
        layout_frame = ttk.Frame(typing_frame)
        layout_frame.pack(fill=tk.X, pady=5)
        
        layout_label = create_label(layout_frame, "Keyboard Layout:", font_size=14)
        layout_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.layout_var = tk.StringVar(value=self.settings.get("keyboard_layout", "QWERTY"))
        
        layout_option_frame = ttk.Frame(layout_frame)
        layout_option_frame.pack(side=tk.LEFT)
        
        for layout in ["QWERTY", "DVORAK", "COLEMAK"]:
            layout_rb = ttk.Radiobutton(
                layout_option_frame,
                text=layout,
                value=layout,
                variable=self.layout_var
            )
            layout_rb.pack(side=tk.LEFT, padx=10)
        
        # Default difficulty
        difficulty_frame = ttk.Frame(typing_frame)
        difficulty_frame.pack(fill=tk.X, pady=15)
        
        difficulty_label = create_label(difficulty_frame, "Default Difficulty:", font_size=14)
        difficulty_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.difficulty_var = tk.StringVar(value=self.settings.get("default_difficulty", "Intermediate"))
        
        difficulty_option_frame = ttk.Frame(difficulty_frame)
        difficulty_option_frame.pack(side=tk.LEFT)
        
        for diff in ["Beginner", "Intermediate", "Advanced", "Expert"]:
            diff_rb = ttk.Radiobutton(
                difficulty_option_frame,
                text=diff,
                value=diff,
                variable=self.difficulty_var
            )
            diff_rb.pack(side=tk.LEFT, padx=10)
    
    def save_settings(self):
        """Save the updated settings."""
        # Collect settings from UI elements
        updated_settings = {
            "theme": self.theme_var.get(),
            "sound_effects": self.sound_var.get(),
            "keyboard_layout": self.layout_var.get(),
            "default_difficulty": self.difficulty_var.get()
        }
        
        # Save to user settings
        self.user_manager.update_user_settings(self.current_user, updated_settings)
        
        # Call the callback function to update app settings
        if self.on_save:
            self.on_save(updated_settings)
        
        # Close the settings window
        self.settings_window.destroy()
    
    def close_settings(self):
        """Close the settings window without saving."""
        self.settings_window.destroy()