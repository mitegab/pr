"""Welcome screen for the typing test application."""

import tkinter as tk
from tkinter import ttk
from config import COLORS, SAMPLE_TEXTS
from simplified_ui import (
    create_label, create_button, create_frame, create_combobox
)

class WelcomeScreen:
    """Welcome screen showing user options after login."""
    
    def __init__(self, root, user_manager, typing_logic, current_user, 
                 on_start=None, on_settings=None, on_dashboard=None, on_logout=None):
        """Initialize welcome screen."""
        self.root = root
        self.user_manager = user_manager
        self.typing_logic = typing_logic
        self.current_user = current_user
        
        self.on_start = on_start
        self.on_settings = on_settings
        self.on_dashboard = on_dashboard
        self.on_logout = on_logout
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Create main content frame
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Top bar with user info and actions
        top_bar = ttk.Frame(main_frame, style="TFrame")
        top_bar.pack(fill=tk.X, pady=(0, 20))
        
        welcome_label = create_label(top_bar, f"Welcome, {self.current_user}!", font_size=20, weight="bold")
        welcome_label.pack(side=tk.LEFT)
        
        # Action buttons
        settings_button = create_button(
            top_bar,
            text="Settings",
            command=self.settings_click,
            style="SecondaryButton.TButton",
        )
        settings_button.pack(side=tk.RIGHT, padx=5)
        
        dashboard_button = create_button(
            top_bar,
            text="Dashboard",
            command=self.dashboard_click,
            style="SecondaryButton.TButton",
        )
        dashboard_button.pack(side=tk.RIGHT, padx=5)
        
        logout_button = create_button(
            top_bar,
            text="Logout",
            command=self.logout_click,
            style="SecondaryButton.TButton",
        )
        logout_button.pack(side=tk.RIGHT, padx=5)
        
        # Center content
        center_frame = create_frame(main_frame, padding=30, bg_color=COLORS["card_background"])
        center_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # App headline
        headline_label = create_label(
            center_frame, 
            "Improve Your Typing Speed", 
            font_size=28, 
            weight="bold"
        )
        headline_label.pack(pady=(0, 10))
        
        subheadline_label = create_label(
            center_frame,
            "Track your progress, analyze performance, and become a typing master",
            font_size=16
        )
        subheadline_label.pack(pady=(0, 30))
        
        # Difficulty selection
        difficulty_frame = ttk.Frame(center_frame, style="TFrame")
        difficulty_frame.pack(fill=tk.X, pady=10)
        
        difficulty_label = create_label(difficulty_frame, "Select Difficulty:", font_size=16)
        difficulty_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.difficulty_var = tk.StringVar(value=self.typing_logic.current_difficulty)
        
        # Load user's preferred difficulty if available
        user_settings = self.user_manager.get_user_settings(self.current_user)
        if user_settings and "default_difficulty" in user_settings:
            self.difficulty_var.set(user_settings["default_difficulty"])
            self.typing_logic.set_difficulty(user_settings["default_difficulty"])
        
        difficulty_combobox = create_combobox(
            difficulty_frame,
            values=list(SAMPLE_TEXTS.keys()),
            textvariable=self.difficulty_var,
            font_size=16,
        )
        difficulty_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        difficulty_combobox.bind("<<ComboboxSelected>>", self.update_difficulty)
        
        # Start button
        start_button = create_button(
            center_frame,
            text="Start Typing Test",
            command=self.start_test_click,
            style="PrimaryButton.TButton",
        )
        start_button.pack(pady=30, ipady=10, ipadx=20)
        
        # Recent stats if available
        user_stats = self.user_manager.get_user_stats(self.current_user)
        if user_stats and user_stats.get("total_tests", 0) > 0:
            stats_frame = create_frame(center_frame, padding=15, bg_color=COLORS["card_background"], border=True)
            stats_frame.pack(fill=tk.X, pady=20)
            
            stats_label = create_label(stats_frame, "Your Stats", font_size=16, weight="bold")
            stats_label.pack(anchor=tk.W, pady=(0, 10))
            
            stats_grid = ttk.Frame(stats_frame)
            stats_grid.pack(fill=tk.X)
            
            for i, (label, value) in enumerate([
                ("Best WPM", f"{user_stats.get('best_wpm', 0):.1f}"),
                ("Average WPM", f"{user_stats.get('average_wpm', 0):.1f}"),
                ("Best Accuracy", f"{user_stats.get('best_accuracy', 0):.1f}%"),
                ("Total Tests", str(user_stats.get('total_tests', 0))),
                ("Current Level", user_stats.get("level", "Novice"))
            ]):
                ttk.Label(stats_grid, text=label, style="TLabel").grid(row=i%3, column=(i//3)*2, sticky="e", padx=10, pady=5)
                ttk.Label(stats_grid, text=value, style="TLabel", font=("SF Pro Display", 12, "bold")).grid(row=i%3, column=(i//3)*2+1, sticky="w", padx=10, pady=5)
    
    def update_difficulty(self, event=None):
        """Update the current difficulty based on combobox selection."""
        self.typing_logic.set_difficulty(self.difficulty_var.get())
    
    def start_test_click(self):
        """Handle start test button click."""
        if self.on_start:
            self.on_start()
    
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
