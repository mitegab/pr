"""Results screen for the typing test application."""

import tkinter as tk
from tkinter import ttk
from config import COLORS, USER_LEVELS
from simplified_ui import (
    create_label, create_button, create_frame
)

class ResultsScreen:
    """Screen for displaying typing test results."""
    
    def __init__(self, root, user_manager, wpm, accuracy, time_seconds, current_user, 
                 on_retry=None, on_stats=None, on_home=None):
        """Initialize results screen."""
        self.root = root
        self.user_manager = user_manager
        self.wpm = wpm
        self.accuracy = accuracy
        self.time_seconds = time_seconds
        self.current_user = current_user
        
        self.on_retry = on_retry
        self.on_stats = on_stats
        self.on_home = on_home
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Results header
        header_label = create_label(main_frame, "Test Results", font_size=28, weight="bold")
        header_label.pack(pady=(0, 30))
        
        # Results card
        results_frame = create_frame(main_frame, padding=30, bg_color=COLORS["card_background"])
        results_frame.pack(fill=tk.X, pady=20, padx=40)
        
        # WPM display with level indicator
        wpm_frame = ttk.Frame(results_frame)
        wpm_frame.pack(fill=tk.X, pady=10)
        
        wpm_label = create_label(wpm_frame, "Typing Speed", font_size=16)
        wpm_label.pack(anchor=tk.W)
        
        # Get user level based on WPM
        level = "Novice"
        level_color = USER_LEVELS["Novice"]["color"]
        for lvl, info in USER_LEVELS.items():
            if info["min_wpm"] <= self.wpm <= info["max_wpm"]:
                level = lvl
                level_color = info["color"]
                break
        
        wpm_display = ttk.Frame(wpm_frame)
        wpm_display.pack(anchor=tk.W, pady=5)
        
        wpm_value = create_label(wpm_display, f"{self.wpm:.1f}", font_size=36, weight="bold")
        wpm_value.pack(side=tk.LEFT)
        
        wpm_unit = create_label(wpm_display, "WPM", font_size=20)
        wpm_unit.pack(side=tk.LEFT, padx=10, pady=(8, 0))
        
        level_indicator = create_frame(wpm_display, padding=8, bg_color=level_color)
        level_indicator.pack(side=tk.LEFT, padx=20)
        
        level_label = create_label(level_indicator, level, font_size=14, weight="bold", foreground="#ffffff")
        level_label.pack()
        
        # Accuracy display
        accuracy_frame = ttk.Frame(results_frame)
        accuracy_frame.pack(fill=tk.X, pady=10)
        
        accuracy_label = create_label(accuracy_frame, "Accuracy", font_size=16)
        accuracy_label.pack(anchor=tk.W)
        
        accuracy_value = create_label(accuracy_frame, f"{self.accuracy:.1f}%", font_size=24, weight="bold")
        accuracy_value.pack(anchor=tk.W, pady=5)
        
        # Time taken
        time_frame = ttk.Frame(results_frame)
        time_frame.pack(fill=tk.X, pady=10)
        
        time_label = create_label(time_frame, "Time", font_size=16)
        time_label.pack(anchor=tk.W)
        
        minutes = self.time_seconds // 60
        seconds = self.time_seconds % 60
        time_value = create_label(time_frame, f"{minutes}:{seconds:02d}", font_size=24, weight="bold")
        time_value.pack(anchor=tk.W, pady=5)
        
        # User stats improvement
        user_stats = self.user_manager.get_user_stats(self.current_user)
        if user_stats and "best_wpm" in user_stats:
            improvement_frame = ttk.Frame(results_frame)
            improvement_frame.pack(fill=tk.X, pady=10)
            
            # Check if this is a new personal best
            if self.wpm > user_stats["best_wpm"]:
                improvement_label = create_label(
                    improvement_frame, 
                    "New Personal Best! 🎉", 
                    font_size=18, 
                    weight="bold",
                    foreground=COLORS["success"]
                )
                improvement_label.pack(anchor=tk.W)
                
                prev_best = user_stats["best_wpm"]
                improvement_pct = ((self.wpm - prev_best) / prev_best) * 100 if prev_best > 0 else 100
                improvement_text = create_label(
                    improvement_frame,
                    f"You improved by {improvement_pct:.1f}% from your previous best of {prev_best:.1f} WPM",
                    font_size=14
                )
                improvement_text.pack(anchor=tk.W, pady=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=30)
        
        retry_button = create_button(
            button_frame,
            text="Try Again",
            command=self.retry_click,
            style="PrimaryButton.TButton",
        )
        retry_button.pack(side=tk.RIGHT, padx=5)
        
        view_stats_button = create_button(
            button_frame,
            text="View Stats",
            command=self.view_stats_click,
            style="SecondaryButton.TButton",
        )
        view_stats_button.pack(side=tk.RIGHT, padx=5)
        
        home_button = create_button(
            button_frame,
            text="Home",
            command=self.home_click,
            style="SecondaryButton.TButton"
        )
        home_button.pack(side=tk.RIGHT, padx=5)
    
    def retry_click(self):
        """Handle try again button click."""
        if self.on_retry:
            self.on_retry()
    
    def view_stats_click(self):
        """Handle view stats button click."""
        if self.on_stats:
            self.on_stats()
    
    def home_click(self):
        """Handle home button click."""
        if self.on_home:
            self.on_home()
