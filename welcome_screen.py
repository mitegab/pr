"""Welcome screen for the typing test application."""

import tkinter as tk
from tkinter import ttk
from config import COLORS, FONTS
from simplified_ui import (
    create_label, create_button, create_frame
)
from home_screen import HomeScreen

class WelcomeScreen:
    """Welcome screen shown after login."""
    
    def __init__(self, root, user_manager, typing_logic, current_user, 
                 on_start=None, on_settings=None, on_dashboard=None, on_logout=None):
        """Initialize the welcome screen."""
        self.root = root
        self.user_manager = user_manager
        self.typing_logic = typing_logic
        self.current_user = current_user
        
        self.on_start = on_start
        self.on_settings = on_settings
        self.on_dashboard = on_dashboard
        self.on_logout = on_logout
        
        # Initialize home screen as our main interface
        self.home_screen = HomeScreen(
            root, 
            user_manager, 
            current_user,
            on_learning_mode=self.learning_mode_click,
            on_speed_mode=self.speed_mode_click,
            on_accuracy_mode=self.accuracy_mode_click,
            on_practice_mode=self.practice_mode_click,
            on_settings=on_settings,
            on_dashboard=on_dashboard,
            on_logout=on_logout
        )
    
    def learning_mode_click(self):
        """Handle learning mode button click."""
        from learning_mode import LearningMode
        
        self.clear_screen()
        from lesson_manager import LessonManager
        from sounds_manager import SoundsManager
        
        lesson_manager = LessonManager()
        sounds_manager = SoundsManager()
        
        LearningMode(
            self.root,
            self.user_manager,
            lesson_manager,
            sounds_manager,
            self.current_user,
            on_back=self.show_home_screen
        )
    
    def speed_mode_click(self):
        """Handle speed mode button click."""
        from speed_mode import SpeedMode
        from sounds_manager import SoundsManager
        
        self.clear_screen()
        sounds_manager = SoundsManager()
        
        SpeedMode(
            self.root,
            self.user_manager,
            self.typing_logic,
            sounds_manager,
            self.current_user,
            on_back=self.show_home_screen
        )
    
    def accuracy_mode_click(self):
        """Handle accuracy mode button click."""
        from accuracy_mode import AccuracyMode
        from sounds_manager import SoundsManager
        
        self.clear_screen()
        sounds_manager = SoundsManager()
        
        AccuracyMode(
            self.root,
            self.user_manager,
            self.typing_logic,
            sounds_manager,
            self.current_user,
            on_back=self.show_home_screen
        )
    
    def practice_mode_click(self):
        """Handle practice mode button click."""
        from practice_mode import PracticeMode
        from sounds_manager import SoundsManager
        
        self.clear_screen()
        sounds_manager = SoundsManager()
        
        PracticeMode(
            self.root,
            self.user_manager,
            sounds_manager,
            self.current_user,
            on_back=self.show_home_screen
        )
    
    def show_home_screen(self):
        """Show the home screen."""
        self.clear_screen()
        self.home_screen = HomeScreen(
            self.root, 
            self.user_manager, 
            self.current_user,
            on_learning_mode=self.learning_mode_click,
            on_speed_mode=self.speed_mode_click,
            on_accuracy_mode=self.accuracy_mode_click,
            on_practice_mode=self.practice_mode_click,
            on_settings=self.on_settings,
            on_dashboard=self.on_dashboard,
            on_logout=self.on_logout
        )
    
    def clear_screen(self):
        """Clear all widgets from the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()
