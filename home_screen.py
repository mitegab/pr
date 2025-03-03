"""Home screen for the Typing Speed Test application."""

import tkinter as tk
from tkinter import ttk
from config import COLORS, FONTS
from simplified_ui import (
    create_label, create_button, create_frame
)

class HomeScreen:
    """Home screen for the application."""
    
    def __init__(self, root, user_manager, current_user, 
                 on_learning_mode=None, on_speed_mode=None, on_accuracy_mode=None,
                 on_practice_mode=None, on_settings=None, on_dashboard=None, on_logout=None):
        """Initialize the home screen."""
        self.root = root
        self.user_manager = user_manager
        self.current_user = current_user
        
        # Callbacks
        self.on_learning_mode = on_learning_mode
        self.on_speed_mode = on_speed_mode
        self.on_accuracy_mode = on_accuracy_mode
        self.on_practice_mode = on_practice_mode
        self.on_settings = on_settings
        self.on_dashboard = on_dashboard
        self.on_logout = on_logout
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header with user info and actions
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # App logo/title
        title_label = create_label(header_frame, "Typing Speed Test Pro", font_size=24, weight="bold")
        title_label.pack(side=tk.LEFT)
        
        # User info
        user_info_frame = ttk.Frame(header_frame)
        user_info_frame.pack(side=tk.RIGHT)
        
        welcome_label = create_label(user_info_frame, f"Welcome, {self.current_user}", font_size=14)
        welcome_label.pack(side=tk.LEFT, padx=10)
        
        # Settings button
        settings_button = create_button(
            user_info_frame,
            text="Settings",
            command=self.settings_click,
            style="SecondaryButton.TButton"
        )
        settings_button.pack(side=tk.LEFT, padx=5)
        
        # Dashboard button
        dashboard_button = create_button(
            user_info_frame,
            text="Dashboard",
            command=self.dashboard_click,
            style="SecondaryButton.TButton"
        )
        dashboard_button.pack(side=tk.LEFT, padx=5)
        
        # Logout button
        logout_button = create_button(
            user_info_frame,
            text="Logout",
            command=self.logout_click,
            style="SecondaryButton.TButton"
        )
        logout_button.pack(side=tk.LEFT, padx=5)
        
        # Create mode selection grid
        modes_frame = ttk.Frame(main_frame)
        modes_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid columns and rows to be equal
        for i in range(2):
            modes_frame.columnconfigure(i, weight=1, uniform="mode")
            modes_frame.rowconfigure(i, weight=1, uniform="mode")
        
        # Learning Mode Card
        self.create_mode_card(
            modes_frame,
            "Learning Mode",
            "Step-by-step typing lessons from beginner to advanced",
            "🎓",
            self.learning_mode_click,
            0, 0
        )
        
        # Speed Mode Card
        self.create_mode_card(
            modes_frame,
            "Speed Typing Mode",
            "Practice to increase your typing speed with timed tests",
            "⚡",
            self.speed_mode_click,
            0, 1
        )
        
        # Accuracy Mode Card
        self.create_mode_card(
            modes_frame,
            "Accuracy Mode",
            "Focus on improving typing precision and reducing errors",
            "🎯",
            self.accuracy_mode_click,
            1, 0
        )
        
        # Practice Mode Card
        self.create_mode_card(
            modes_frame,
            "Practice Mode",
            "Type real-world content from various genres",
            "📚",
            self.practice_mode_click,
            1, 1
        )
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        version_label = create_label(footer_frame, "v1.0.0", font_size=10, foreground=COLORS["muted_text"])
        version_label.pack(side=tk.RIGHT)
    
    def create_mode_card(self, parent, title, description, emoji, command, row, col):
        """Create a mode selection card."""
        card = create_frame(
            parent,
            padding=20,
            bg_color=COLORS["card_background"],
            shadow=True
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Emoji icon
        emoji_label = create_label(card, emoji, font_size=48)
        emoji_label.pack(pady=(0, 10))
        
        # Mode title
        title_label = create_label(card, title, font_size=18, weight="bold")
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = create_label(card, description, font_size=12)
        desc_label.pack(pady=(0, 20), fill=tk.X)
        
        # Start button
        start_button = create_button(
            card,
            text="Start",
            command=command,
            style="PrimaryButton.TButton"
        )
        start_button.pack()
        
        # Make the entire card clickable
        for widget in [card, emoji_label, title_label, desc_label]:
            widget.bind("<Button-1>", lambda e, cmd=command: cmd())
            widget.bind("<Enter>", lambda e, c=card: self.on_card_hover_enter(c))
            widget.bind("<Leave>", lambda e, c=card: self.on_card_hover_leave(c))
    
    def on_card_hover_enter(self, card):
        """Handle card hover enter event."""
        card.configure(style="HoverCard.TFrame")
    
    def on_card_hover_leave(self, card):
        """Handle card hover leave event."""
        card.configure(style="Card.TFrame")
    
    def learning_mode_click(self):
        """Handle learning mode button click."""
        if self.on_learning_mode:
            self.on_learning_mode()
    
    def speed_mode_click(self):
        """Handle speed mode button click."""
        if self.on_speed_mode:
            self.on_speed_mode()
    
    def accuracy_mode_click(self):
        """Handle accuracy mode button click."""
        if self.on_accuracy_mode:
            self.on_accuracy_mode()
    
    def practice_mode_click(self):
        """Handle practice mode button click."""
        if self.on_practice_mode:
            self.on_practice_mode()
    
    def settings_click(self):
        """Handle settings button click."""
        if self.on_settings:
            self.on_settings()
    
    def dashboard_click(self):
        """Handle dashboard button click."""
        if self.on_dashboard:
            self.on_dashboard()
    
    def logout_click(self):
        """Handle logout button click."""
        if self.on_logout:
            self.on_logout()
