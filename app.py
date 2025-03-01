"""Main application class for Typing Speed Test."""

import tkinter as tk
from config import COLORS, USER_DATA_FILE, SAMPLE_TEXTS, THEMES
from user_manager import UserManager
from typing_test_logic import TypingTestLogic
from sounds_manager import SoundsManager

# Define a dummy load_icon function if needed
def load_icon(name, **kwargs):
    return None

class TypingSpeedTestApp:
    """Main application class for the Typing Speed Test."""
    
    def __init__(self, root):
        """Initialize the application with root window."""
        self.root = root
        self.root.geometry("1024x768")
        self.root.config(bg=COLORS["background"])
        
        # Set up components
        self.user_manager = UserManager(USER_DATA_FILE)
        self.typing_logic = TypingTestLogic(SAMPLE_TEXTS)
        self.sounds_manager = SoundsManager()
        
        self.current_user = None
        self.settings_screen = None
        self.dashboard_screen = None
        
        # Load icons
        self.icons = {
            "login": load_icon("login_icon.png"),
            "create_account": load_icon("create_account_icon.png"),
            "start": load_icon("start_icon.png"),
            "reset": load_icon("reset_icon.png"),
            "settings": load_icon("settings_icon.png"),
            "dashboard": load_icon("dashboard_icon.png"),
            "logout": load_icon("logout_icon.png")
        }
        
        # Initialize current screen
        self.current_screen = None
        
        # Show login screen
        self.show_login_screen()
    
    def clear_screen(self):
        """Clear all widgets from the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Show the login screen."""
        self.clear_screen()
        from login_screen import LoginScreen
        self.current_screen = LoginScreen(
            self.root, 
            self.user_manager,
            on_login=self.login_success,
            on_create_account=self.show_create_account_screen
        )
    
    def show_create_account_screen(self):
        """Show the create account screen."""
        self.clear_screen()
        from login_screen import LoginScreen
        self.current_screen = LoginScreen(
            self.root, 
            self.user_manager,
            mode="create",
            on_login=self.login_success,
            on_back=self.show_login_screen
        )
    
    def login_success(self, username):
        """Handle successful login."""
        self.current_user = username
        self.show_welcome_screen()
        self.sounds_manager.play_achievement()
    
    def show_welcome_screen(self):
        """Show the welcome screen."""
        self.clear_screen()
        from welcome_screen import WelcomeScreen
        self.current_screen = WelcomeScreen(
            self.root,
            self.user_manager,
            self.typing_logic,
            self.current_user,
            on_start=self.start_typing_test,
            on_settings=self.show_settings,
            on_dashboard=self.show_dashboard,
            on_logout=self.logout
        )
    
    def start_typing_test(self):
        """Start the typing test."""
        self.clear_screen()
        from test_screen import TestScreen
        self.current_screen = TestScreen(
            self.root,
            self.user_manager,
            self.typing_logic,
            self.sounds_manager,
            self.current_user,
            on_back=self.show_welcome_screen,
            on_finish=self.show_results
        )
    
    def show_results(self, wpm, accuracy, time_seconds):
        """Show the results screen."""
        self.clear_screen()
        from results_screen import ResultsScreen
        self.current_screen = ResultsScreen(
            self.root,
            self.user_manager,
            wpm,
            accuracy,
            time_seconds,
            self.current_user,
            on_retry=self.start_typing_test,
            on_stats=self.show_dashboard,
            on_home=self.show_welcome_screen
        )
    
    def show_settings(self):
        """Show the settings screen."""
        from settings_screen import SettingsScreen
        self.settings_screen = SettingsScreen(
            self.root, 
            self.user_manager, 
            self.current_user,
            self.apply_settings
        )
        self.settings_screen.show()
    
    def apply_settings(self, settings):
        """Apply updated settings."""
        # Update sound settings
        self.sounds_manager.update_settings(settings)
        
        # Update theme if changed
        theme = settings.get("theme", "light")
        global COLORS
        COLORS = THEMES[theme]
        
        # Refresh current screen to apply new settings
        from welcome_screen import WelcomeScreen
        from test_screen import TestScreen
        
        if isinstance(self.current_screen, WelcomeScreen):
            self.show_welcome_screen()
        elif isinstance(self.current_screen, TestScreen):
            self.start_typing_test()
    
    def show_dashboard(self):
        """Show the user dashboard."""
        from dashboard_screen import DashboardScreen
        self.dashboard_screen = DashboardScreen(
            self.root, 
            self.user_manager, 
            self.current_user,
            self.on_dashboard_close
        )
        self.dashboard_screen.show()
    
    def on_dashboard_close(self):
        """Handle dashboard close event."""
        # No specific action needed currently
        pass
    
    def logout(self):
        """Log out the current user."""
        self.user_manager.logout()
        self.current_user = None
        self.show_login_screen()
