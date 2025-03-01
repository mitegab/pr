"""Settings screen for the typing test application."""

import tkinter as tk
from tkinter import ttk, colorchooser
from config import COLORS, FONTS, UI_SETTINGS, THEMES, save_user_settings
from ui_components import (
    create_label, create_entry, create_button, create_combobox,
    create_frame, load_icon
)

class SettingsScreen:
    """Settings screen for customization."""
    
    def __init__(self, root, user_manager, current_user, on_close=None):
        """Initialize with root window."""
        self.root = root
        self.user_manager = user_manager
        self.current_user = current_user
        self.on_close = on_close
        self.settings = {}
        self.load_settings()
        
    def load_settings(self):
        """Load user settings."""
        if self.current_user:
            self.settings = self.user_manager.get_user_settings(self.current_user) or {}
    
    def save_settings(self):
        """Save user settings."""
        if self.current_user and self.settings:
            self.user_manager.update_user_settings(self.current_user, self.settings)
            save_user_settings(self.current_user, self.settings)
    
    def show(self):
        """Show the settings screen."""
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("700x600")
        self.settings_window.resizable(False, False)
        self.settings_window.transient(self.root)
        self.settings_window.grab_set()
        
        # Center on parent
        x = self.root.winfo_x() + (self.root.winfo_width() - 700) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 600) // 2
        self.settings_window.geometry(f"+{x}+{y}")
        
        self.settings_window.config(background=COLORS["background"])
        self.create_settings_ui()
    
    def create_settings_ui(self):
        """Create the settings UI."""
        main_frame = create_frame(self.settings_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = create_label(main_frame, "Settings", font_size=24, weight="bold")
        title_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 20))
        
        # Settings notebook/tabs
        settings_notebook = ttk.Notebook(main_frame)
        settings_notebook.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=10)
        
        # General settings tab
        general_tab = create_frame(settings_notebook, padding=20)
        settings_notebook.add(general_tab, text="General")
        self.create_general_settings(general_tab)
        
        # Appearance tab
        appearance_tab = create_frame(settings_notebook, padding=20)
        settings_notebook.add(appearance_tab, text="Appearance")
        self.create_appearance_settings(appearance_tab)
        
        # Typing settings tab
        typing_tab = create_frame(settings_notebook, padding=20)
        settings_notebook.add(typing_tab, text="Typing")
        self.create_typing_settings(typing_tab)
        
        # Sound settings tab
        sound_tab = create_frame(settings_notebook, padding=20)
        settings_notebook.add(sound_tab, text="Sound")
        self.create_sound_settings(sound_tab)
        
        # Buttons at the bottom
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, sticky="se", pady=20)
        
        cancel_button = create_button(
            button_frame, 
            text="Cancel", 
            command=self.close_settings,
            style="SecondaryButton.TButton"
        )
        cancel_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        save_button = create_button(
            button_frame, 
            text="Save", 
            command=self.save_and_close,
            style="PrimaryButton.TButton"
        )
        save_button.pack(side=tk.RIGHT)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
    
    def create_general_settings(self, parent):
        """Create general settings UI."""
        # Username display (not editable)
        create_label(parent, "Username:", font_size=14).grid(row=0, column=0, sticky="w", pady=10)
        create_label(parent, self.current_user, font_size=14, weight="bold").grid(row=0, column=1, sticky="w", pady=10)
        
        # Default difficulty
        create_label(parent, "Default Difficulty:", font_size=14).grid(row=1, column=0, sticky="w", pady=10)
        self.difficulty_var = tk.StringVar(value=self.settings.get("default_difficulty", "Intermediate"))
        difficulty_combobox = create_combobox(
            parent, 
            values=["Beginner", "Intermediate", "Advanced", "Expert"],
            textvariable=self.difficulty_var
        )
        difficulty_combobox.grid(row=1, column=1, sticky="ew", pady=10)
        
        # Auto-save results
        create_label(parent, "Auto-save Results:", font_size=14).grid(row=2, column=0, sticky="w", pady=10)
        self.autosave_var = tk.BooleanVar(value=self.settings.get("auto_save", True))
        autosave_switch = ttk.Checkbutton(parent, variable=self.autosave_var, style="Switch.TCheckbutton")
        autosave_switch.grid(row=2, column=1, sticky="w", pady=10)
        
        # Show timer
        create_label(parent, "Show Timer:", font_size=14).grid(row=3, column=0, sticky="w", pady=10)
        self.show_timer_var = tk.BooleanVar(value=self.settings.get("show_timer", True))
        show_timer_switch = ttk.Checkbutton(parent, variable=self.show_timer_var, style="Switch.TCheckbutton")
        show_timer_switch.grid(row=3, column=1, sticky="w", pady=10)
        
        # Show WPM in real-time
        create_label(parent, "Show Real-time WPM:", font_size=14).grid(row=4, column=0, sticky="w", pady=10)
        self.show_realtime_wpm_var = tk.BooleanVar(value=self.settings.get("show_realtime_wpm", True))
        show_realtime_wpm_switch = ttk.Checkbutton(parent, variable=self.show_realtime_wpm_var, style="Switch.TCheckbutton")
        show_realtime_wpm_switch.grid(row=4, column=1, sticky="w", pady=10)
        
        parent.columnconfigure(1, weight=1)
    
    def create_appearance_settings(self, parent):
        """Create appearance settings UI."""
        # Theme selection
        create_label(parent, "Theme:", font_size=14).grid(row=0, column=0, sticky="w", pady=10)
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "light"))
        theme_frame = ttk.Frame(parent)
        theme_frame.grid(row=0, column=1, sticky="w", pady=10)
        
        light_rb = ttk.Radiobutton(theme_frame, text="Light", variable=self.theme_var, value="light")
        light_rb.pack(side=tk.LEFT, padx=(0, 20))
        
        dark_rb = ttk.Radiobutton(theme_frame, text="Dark", variable=self.theme_var, value="dark")
        dark_rb.pack(side=tk.LEFT)
        
        # Font size
        create_label(parent, "Font Size:", font_size=14).grid(row=1, column=0, sticky="w", pady=10)
        font_size_frame = ttk.Frame(parent)
        font_size_frame.grid(row=1, column=1, sticky="w", pady=10)
        
        self.font_size_var = tk.IntVar(value=self.settings.get("font_size", 14))
        font_size_scale = ttk.Scale(
            font_size_frame, 
            from_=10, 
            to=24, 
            orient=tk.HORIZONTAL,
            variable=self.font_size_var,
            length=200
        )
        font_size_scale.pack(side=tk.LEFT, padx=(0, 10))
        
        font_size_label = create_label(font_size_frame, "14", font_size=14)
        font_size_label.pack(side=tk.LEFT)
        
        # Update font size label when scale changes
        def update_font_size_label(event):
            font_size_label.config(text=str(self.font_size_var.get()))
        
        font_size_scale.bind("<Motion>", update_font_size_label)
        font_size_scale.bind("<ButtonRelease-1>", update_font_size_label)
        
        # Custom accent color
        create_label(parent, "Accent Color:", font_size=14).grid(row=2, column=0, sticky="w", pady=10)
        color_frame = ttk.Frame(parent)
        color_frame.grid(row=2, column=1, sticky="w", pady=10)
        
        self.accent_color = self.settings.get("accent_color", COLORS["accent"])
        self.accent_color_preview = tk.Canvas(
            color_frame, 
            width=30, 
            height=30, 
            bg=self.accent_color,
            highlightthickness=1,
            highlightbackground=COLORS["border"]
        )
        self.accent_color_preview.pack(side=tk.LEFT, padx=(0, 10))
        
        color_picker_button = create_button(
            color_frame,
            text="Choose Color",
            command=self.choose_accent_color,
            style="SecondaryButton.TButton"
        )
        color_picker_button.pack(side=tk.LEFT)
        
        # Font family
        create_label(parent, "Font Family:", font_size=14).grid(row=3, column=0, sticky="w", pady=10)
        self.font_family_var = tk.StringVar(value=self.settings.get("font_family", FONTS["primary"]))
        font_family_combobox = create_combobox(
            parent, 
            values=["SF Pro Display", "Helvetica Neue", "Arial", "Roboto", "Segoe UI", "Verdana"],
            textvariable=self.font_family_var
        )
        font_family_combobox.grid(row=3, column=1, sticky="ew", pady=10)
        
        # Monospace font family for typing
        create_label(parent, "Typing Font:", font_size=14).grid(row=4, column=0, sticky="w", pady=10)
        self.typing_font_var = tk.StringVar(value=self.settings.get("typing_font", FONTS["monospace"]))
        typing_font_combobox = create_combobox(
            parent, 
            values=["SF Mono", "Menlo", "Consolas", "Courier New", "Monaco", "Inconsolata"],
            textvariable=self.typing_font_var
        )
        typing_font_combobox.grid(row=4, column=1, sticky="ew", pady=10)
        
        # Animation toggle
        create_label(parent, "Use Animations:", font_size=14).grid(row=5, column=0, sticky="w", pady=10)
        self.use_animations_var = tk.BooleanVar(value=self.settings.get("use_animations", True))
        use_animations_switch = ttk.Checkbutton(parent, variable=self.use_animations_var, style="Switch.TCheckbutton")
        use_animations_switch.grid(row=5, column=1, sticky="w", pady=10)
        
        parent.columnconfigure(1, weight=1)
    
    def create_typing_settings(self, parent):
        """Create typing-specific settings UI."""
        # Keyboard layout
        create_label(parent, "Keyboard Layout:", font_size=14).grid(row=0, column=0, sticky="w", pady=10)
        self.keyboard_layout_var = tk.StringVar(value=self.settings.get("keyboard_layout", "QWERTY"))
        keyboard_layout_combobox = create_combobox(
            parent, 
            values=["QWERTY", "DVORAK", "COLEMAK", "AZERTY"],
            textvariable=self.keyboard_layout_var
        )
        keyboard_layout_combobox.grid(row=0, column=1, sticky="ew", pady=10)
        
        # Highlight current word
        create_label(parent, "Highlight Current Word:", font_size=14).grid(row=1, column=0, sticky="w", pady=10)
        self.highlight_word_var = tk.BooleanVar(value=self.settings.get("highlight_word", True))
        highlight_word_switch = ttk.Checkbutton(parent, variable=self.highlight_word_var, style="Switch.TCheckbutton")
        highlight_word_switch.grid(row=1, column=1, sticky="w", pady=10)
        
        # Error highlighting
        create_label(parent, "Error Highlighting:", font_size=14).grid(row=2, column=0, sticky="w", pady=10)
        error_highlight_frame = ttk.Frame(parent)
        error_highlight_frame.grid(row=2, column=1, sticky="w", pady=10)
        
        self.error_highlight_var = tk.StringVar(value=self.settings.get("error_highlight", "immediate"))
        immediate_rb = ttk.Radiobutton(error_highlight_frame, text="Immediate", variable=self.error_highlight_var, value="immediate")
        immediate_rb.pack(side=tk.LEFT, padx=(0, 20))
        
        at_end_rb = ttk.Radiobutton(error_highlight_frame, text="At End", variable=self.error_highlight_var, value="at_end")
        at_end_rb.pack(side=tk.LEFT, padx=(0, 20))
        
        none_rb = ttk.Radiobutton(error_highlight_frame, text="None", variable=self.error_highlight_var, value="none")
        none_rb.pack(side=tk.LEFT)
        
        # Cursor style
        create_label(parent, "Cursor Style:", font_size=14).grid(row=3, column=0, sticky="w", pady=10)
        self.cursor_style_var = tk.StringVar(value=self.settings.get("cursor_style", "vertical"))
        cursor_style_combobox = create_combobox(
            parent, 
            values=["vertical", "block", "underline", "none"],
            textvariable=self.cursor_style_var
        )
        cursor_style_combobox.grid(row=3, column=1, sticky="ew", pady=10)
        
        # Auto-focus typing area
        create_label(parent, "Auto-focus Typing Area:", font_size=14).grid(row=4, column=0, sticky="w", pady=10)
        self.auto_focus_var = tk.BooleanVar(value=self.settings.get("auto_focus", True))
        auto_focus_switch = ttk.Checkbutton(parent, variable=self.auto_focus_var, style="Switch.TCheckbutton")
        auto_focus_switch.grid(row=4, column=1, sticky="w", pady=10)
        
        # Smart practice (focus on weak keys)
        create_label(parent, "Smart Practice:", font_size=14).grid(row=5, column=0, sticky="w", pady=10)
        self.smart_practice_var = tk.BooleanVar(value=self.settings.get("smart_practice", True))
        smart_practice_switch = ttk.Checkbutton(parent, variable=self.smart_practice_var, style="Switch.TCheckbutton")
        smart_practice_switch.grid(row=5, column=1, sticky="w", pady=10)
        
        parent.columnconfigure(1, weight=1)
    
    def create_sound_settings(self, parent):
        """Create sound settings UI."""
        # Sound effects master toggle
        create_label(parent, "Sound Effects:", font_size=14).grid(row=0, column=0, sticky="w", pady=10)
        self.sound_effects_var = tk.BooleanVar(value=self.settings.get("sound_effects", True))
        sound_effects_switch = ttk.Checkbutton(parent, variable=self.sound_effects_var, style="Switch.TCheckbutton")
        sound_effects_switch.grid(row=0, column=1, sticky="w", pady=10)
        
        # Sound volume
        create_label(parent, "Volume:", font_size=14).grid(row=1, column=0, sticky="w", pady=10)
        volume_frame = ttk.Frame(parent)
        volume_frame.grid(row=1, column=1, sticky="w", pady=10)
        
        self.volume_var = tk.IntVar(value=self.settings.get("volume", 70))
        volume_scale = ttk.Scale(
            volume_frame, 
            from_=0, 
            to=100, 
            orient=tk.HORIZONTAL,
            variable=self.volume_var,
            length=200
        )
        volume_scale.pack(side=tk.LEFT, padx=(0, 10))
        
        volume_label = create_label(volume_frame, "70%", font_size=14)
        volume_label.pack(side=tk.LEFT)
        
        # Update volume label when scale changes
        def update_volume_label(event):
            volume_label.config(text=f"{self.volume_var.get()}%")
        
        volume_scale.bind("<Motion>", update_volume_label)
        volume_scale.bind("<ButtonRelease-1>", update_volume_label)
        
        # Key click sounds
        create_label(parent, "Key Click Sounds:", font_size=14).grid(row=2, column=0, sticky="w", pady=10)
        self.key_sounds_var = tk.BooleanVar(value=self.settings.get("key_sounds", True))
        key_sounds_switch = ttk.Checkbutton(parent, variable=self.key_sounds_var, style="Switch.TCheckbutton")
        key_sounds_switch.grid(row=2, column=1, sticky="w", pady=10)
        
        # Error sounds
        create_label(parent, "Error Sounds:", font_size=14).grid(row=3, column=0, sticky="w", pady=10)
        self.error_sounds_var = tk.BooleanVar(value=self.settings.get("error_sounds", True))
        error_sounds_switch = ttk.Checkbutton(parent, variable=self.error_sounds_var, style="Switch.TCheckbutton")
        error_sounds_switch.grid(row=3, column=1, sticky="w", pady=10)
        
        # Achievement sounds
        create_label(parent, "Achievement Sounds:", font_size=14).grid(row=4, column=0, sticky="w", pady=10)
        self.achievement_sounds_var = tk.BooleanVar(value=self.settings.get("achievement_sounds", True))
        achievement_sounds_switch = ttk.Checkbutton(parent, variable=self.achievement_sounds_var, style="Switch.TCheckbutton")
        achievement_sounds_switch.grid(row=4, column=1, sticky="w", pady=10)
        
        parent.columnconfigure(1, weight=1)
    
    def choose_accent_color(self):
        """Show color picker dialog for selecting accent color."""
        color = colorchooser.askcolor(initialcolor=self.accent_color, title="Choose Accent Color")
        if color and color[1]:  # Check if color was selected (not cancelled)
            self.accent_color = color[1]
            self.accent_color_preview.config(bg=color[1])
    
    def collect_settings(self):
        """Collect all settings from UI into a dictionary."""
        settings = {
            # General settings
            "default_difficulty": self.difficulty_var.get(),
            "auto_save": self.autosave_var.get(),
            "show_timer": self.show_timer_var.get(),
            "show_realtime_wpm": self.show_realtime_wpm_var.get(),
            
            # Appearance settings
            "theme": self.theme_var.get(),
            "font_size": self.font_size_var.get(),
            "accent_color": self.accent_color,
            "font_family": self.font_family_var.get(),
            "typing_font": self.typing_font_var.get(),
            "use_animations": self.use_animations_var.get(),
            
            # Typing settings
            "keyboard_layout": self.keyboard_layout_var.get(),
            "highlight_word": self.highlight_word_var.get(),
            "error_highlight": self.error_highlight_var.get(),
            "cursor_style": self.cursor_style_var.get(),
            "auto_focus": self.auto_focus_var.get(),
            "smart_practice": self.smart_practice_var.get(),
            
            # Sound settings
            "sound_effects": self.sound_effects_var.get(),
            "volume": self.volume_var.get(),
            "key_sounds": self.key_sounds_var.get(),
            "error_sounds": self.error_sounds_var.get(),
            "achievement_sounds": self.achievement_sounds_var.get(),
        }
        
        return settings
    
    def save_and_close(self):
        """Save settings and close the window."""
        self.settings = self.collect_settings()
        self.save_settings()
        self.close_settings(apply_settings=True)
    
    def close_settings(self, apply_settings=False):
        """Close the settings window."""
        if self.settings_window:
            self.settings_window.destroy()
            
        if apply_settings and self.on_close:
            self.on_close(self.settings)