"""Main module for the Typing Speed Test application."""

# Check dependencies and show warnings
import sys
import importlib.util
import tkinter as tk
from tkinter import messagebox

# Check essential dependencies
MISSING_DEPS = []
for module, pkg_name in [
    ('PIL', 'pillow'),
    ('matplotlib', 'matplotlib'),
    ('numpy', 'numpy')
]:
    if not importlib.util.find_spec(module):
        MISSING_DEPS.append((module, pkg_name))

if MISSING_DEPS:
    # We can continue with limited functionality, but show a warning
    deps_str = "\n".join([f"- {pkg} (pip install {pkg})" for module, pkg in MISSING_DEPS])
    print(f"Warning: Missing recommended dependencies:\n{deps_str}\n")
    print("Some features will be disabled or limited.")
    # The UI components have fallbacks, so we can continue

# Standard imports
import tkinter as tk
from tkinter import ttk, messagebox

from config import COLORS, USER_DATA_FILE, SAMPLE_TEXTS, ICON_PATH, USER_LEVELS, THEMES
from user_manager import UserManager
from ui_components import (
    create_label, create_entry, create_button, create_combobox,
    create_text_area, create_progressbar, create_frame, load_icon
)
from typing_test_logic import TypingTestLogic
from settings_screen import SettingsScreen
from dashboard_screen import DashboardScreen
from sounds_manager import SoundsManager

class TypingSpeedTest:
    """Main application class for Typing Speed Test."""
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("Typing Speed Test Pro")
        self.root.geometry("1024x768")
        self.root.minsize(800, 600)
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
        
        # Configure styles
        self.configure_styles()
        
        # Show the login screen
        self.show_login_screen()
    
    def clear_screen(self):
        """Clear all widgets from the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def configure_styles(self):
        """Configure ttk styles for a modern look."""
        style = ttk.Style(self.root)
        
        style.configure("TLabel", background=COLORS["background"], foreground=COLORS["text"], font=("SF Pro Display", 12))
        style.configure("TEntry", background=COLORS["input_bg"], foreground=COLORS["text"], fieldbackground=COLORS["input_bg"])
        style.configure("TCombobox", background=COLORS["input_bg"], foreground=COLORS["text"], fieldbackground=COLORS["input_bg"])
        style.map("TCombobox", fieldbackground=[("readonly", COLORS["input_bg"])])
        
        # Button styles
        style.configure("PrimaryButton.TButton", background=COLORS["primary_button"], foreground="white", font=("SF Pro Display", 12, "bold"))
        style.map("PrimaryButton.TButton", background=[("active", COLORS["highlight"]), ("disabled", COLORS["border"])])
        
        style.configure("SecondaryButton.TButton", background=COLORS["secondary_button"], foreground=COLORS["text"], font=("SF Pro Display", 12))
        style.map("SecondaryButton.TButton", background=[("active", COLORS["border"]), ("disabled", COLORS["border"])])
        
        # Switch style for checkbuttons
        style.configure("Switch.TCheckbutton", background=COLORS["background"], foreground=COLORS["text"])
        
        # Progressbar
        style.configure("TProgressbar", troughcolor=COLORS["progress_bg"], background=COLORS["primary_button"])
        
        # Notebook
        style.configure("TNotebook", background=COLORS["background"])
        style.configure("TNotebook.Tab", background=COLORS["secondary_button"], foreground=COLORS["text"], padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", COLORS["card_background"])])
        
        # Frame
        style.configure("TFrame", background=COLORS["background"])
        style.configure("Card.TFrame", background=COLORS["card_background"])
    
    def show_login_screen(self):
        """Display the login screen."""
        self.clear_screen()
        
        # Create a centered frame for login content
        center_frame = create_frame(self.root, padding=20, shadow=True)
        center_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=380)
        
        # App title
        title_label = create_label(center_frame, "Typing Speed Test Pro", font_size=24, weight="bold")
        title_label.pack(pady=(0, 30))
        
        # Username field
        username_frame = ttk.Frame(center_frame, style="TFrame")
        username_frame.pack(fill=tk.X, pady=10)
        
        username_label = create_label(username_frame, "Username", font_size=14)
        username_label.pack(anchor=tk.W)
        
        self.username_entry = create_entry(username_frame, font_size=14, placeholder="Enter your username")
        self.username_entry.pack(fill=tk.X, pady=5)
        
        # Password field
        password_frame = ttk.Frame(center_frame, style="TFrame")
        password_frame.pack(fill=tk.X, pady=10)
        
        password_label = create_label(password_frame, "Password", font_size=14)
        password_label.pack(anchor=tk.W)
        
        self.password_entry = create_entry(password_frame, font_size=14, show="•", placeholder="Enter your password")
        self.password_entry.pack(fill=tk.X, pady=5)
        
        # Login button
        login_button = create_button(
            center_frame,
            text="Login",
            command=self.login,
            style="PrimaryButton.TButton",
            icon_name="login_icon.png"
        )
        login_button.pack(fill=tk.X, pady=20)
        
        # Create account button
        create_account_button = create_button(
            center_frame,
            text="Create Account",
            command=self.show_create_account_screen,
            style="SecondaryButton.TButton",
            icon_name="create_account_icon.png"
        )
        create_account_button.pack(fill=tk.X)
        
        # Bind Enter key to login
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda event: self.login())
        
        # Focus username entry
        self.username_entry.focus()
    
    def show_create_account_screen(self):
        """Display the create account screen."""
        self.clear_screen()
        
        # Create a centered frame for account creation content
        center_frame = create_frame(self.root, padding=20, shadow=True)
        center_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450)
        
        # App title
        title_label = create_label(center_frame, "Create Account", font_size=24, weight="bold")
        title_label.pack(pady=(0, 30))
        
        # Username field
        username_frame = ttk.Frame(center_frame, style="TFrame")
        username_frame.pack(fill=tk.X, pady=10)
        
        username_label = create_label(username_frame, "Username", font_size=14)
        username_label.pack(anchor=tk.W)
        
        self.new_username_entry = create_entry(username_frame, font_size=14, placeholder="Choose a username")
        self.new_username_entry.pack(fill=tk.X, pady=5)
        
        # Password field
        password_frame = ttk.Frame(center_frame, style="TFrame")
        password_frame.pack(fill=tk.X, pady=10)
        
        password_label = create_label(password_frame, "Password", font_size=14)
        password_label.pack(anchor=tk.W)
        
        self.new_password_entry = create_entry(password_frame, font_size=14, show="•", placeholder="Choose a password")
        self.new_password_entry.pack(fill=tk.X, pady=5)
        
        # Confirm password field
        confirm_password_frame = ttk.Frame(center_frame, style="TFrame")
        confirm_password_frame.pack(fill=tk.X, pady=10)
        
        confirm_label = create_label(confirm_password_frame, "Confirm Password", font_size=14)
        confirm_label.pack(anchor=tk.W)
        
        self.confirm_password_entry = create_entry(confirm_password_frame, font_size=14, show="•", placeholder="Confirm your password")
        self.confirm_password_entry.pack(fill=tk.X, pady=5)
        
        # Create account button
        create_account_button = create_button(
            center_frame,
            text="Create Account",
            command=self.create_account,
            style="PrimaryButton.TButton",
            icon_name="create_account_icon.png"
        )
        create_account_button.pack(fill=tk.X, pady=20)
        
        # Back button
        back_button = create_button(
            center_frame,
            text="Back to Login",
            command=self.show_login_screen,
            style="SecondaryButton.TButton"
        )
        back_button.pack(fill=tk.X)
        
        # Focus username entry
        self.new_username_entry.focus()
    
    def login(self):
        """Log in the user."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        success = self.user_manager.login(username, password)
        if success:
            self.current_user = username
            self.show_welcome_screen()
            self.sounds_manager.play_achievement()
    
    def create_account(self):
        """Create a new user account."""
        username = self.new_username_entry.get().strip()
        password = self.new_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        
        success = self.user_manager.create_account(username, password, confirm_password)
        if success:
            self.show_login_screen()
            self.sounds_manager.play_achievement()
    
    def show_welcome_screen(self):
        """Display the welcome screen."""
        self.clear_screen()
        
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
            command=self.show_settings,
            style="SecondaryButton.TButton",
            icon_name="settings_icon.png"
        )
        settings_button.pack(side=tk.RIGHT, padx=5)
        
        dashboard_button = create_button(
            top_bar,
            text="Dashboard",
            command=self.show_dashboard,
            style="SecondaryButton.TButton",
            icon_name="dashboard_icon.png"
        )
        dashboard_button.pack(side=tk.RIGHT, padx=5)
        
        logout_button = create_button(
            top_bar,
            text="Logout",
            command=self.logout,
            style="SecondaryButton.TButton",
            icon_name="logout_icon.png"
        )
        logout_button.pack(side=tk.RIGHT, padx=5)
        
        # Center content
        center_frame = create_frame(main_frame, padding=30, shadow=True)
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
            command=self.start_typing_test,
            style="PrimaryButton.TButton",
            icon_name="start_icon.png",
            icon_size=(24, 24),
        )
        start_button.pack(pady=30, ipady=10, ipadx=20)
        
        # Recent stats if available
        user_stats = self.user_manager.get_user_stats(self.current_user)
        if user_stats and user_stats.get("total_tests", 0) > 0:
            stats_frame = create_frame(center_frame, padding=15, shadow=False, border=True)
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
    
    def start_typing_test(self):
        """Start the typing test."""
        self.clear_screen()
        self.typing_logic.start_test()
        
        # Main container
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Top bar
        top_bar = ttk.Frame(main_frame, style="TFrame")
        top_bar.pack(fill=tk.X, pady=(0, 20))
        
        back_button = create_button(
            top_bar,
            text="Back",
            command=self.show_welcome_screen,
            style="SecondaryButton.TButton"
        )
        back_button.pack(side=tk.LEFT)
        
        # Typing test difficulty and time display
        info_label = create_label(top_bar, f"Difficulty: {self.typing_logic.current_difficulty}", font_size=14)
        info_label.pack(side=tk.RIGHT)
        
        # Get user settings
        user_settings = self.user_manager.get_user_settings(self.current_user) or {}
        show_timer = user_settings.get("show_timer", True)
        show_realtime_wpm = user_settings.get("show_realtime_wpm", True)
        
        # Timer display
        if show_timer:
            self.timer_label = create_label(top_bar, "Time: 0:00", font_size=14)
            self.timer_label.pack(side=tk.RIGHT, padx=20)
            self.timer_running = False
            self.timer_seconds = 0
            
        # Main content area
        content_frame = create_frame(main_frame, padding=30, shadow=True)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sample text display
        sample_label = create_label(content_frame, "Sample Text:", font_size=14)
        sample_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.sample_display = create_text_area(
            content_frame,
            height=5, 
            wrap="word",
            state=tk.DISABLED,
            font_family="SF Mono",
            font_size=user_settings.get("font_size", 14),
            background=COLORS["card_background"],
            foreground=COLORS["text"]
        )
        self.sample_display.pack(fill=tk.X, pady=(0, 20))
        
        # Typing area
        typing_label = create_label(content_frame, "Type here:", font_size=14)
        typing_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.typing_entry = create_text_area(
            content_frame,
            height=8,
            wrap="word",
            font_family="SF Mono",
            font_size=user_settings.get("font_size", 14),
            placeholder="Start typing to begin the test...",
            background=COLORS["input_bg"],
            foreground=COLORS["text"]
        )
        self.typing_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Progress bar
        progress_frame = ttk.Frame(content_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_bar = create_progressbar(progress_frame, orient=tk.HORIZONTAL, mode='determinate', animated=True)
        self.progress_bar.pack(fill=tk.X)
        
        # Stats display
        stats_frame = ttk.Frame(content_frame)
        stats_frame.pack(fill=tk.X, pady=10)
        
        if show_realtime_wpm:
            self.wpm_label = create_label(stats_frame, "WPM: 0", font_size=14)
            self.wpm_label.pack(side=tk.LEFT, padx=(0, 20))
            
        self.accuracy_label = create_label(stats_frame, "Accuracy: 100.0%", font_size=14)
        self.accuracy_label.pack(side=tk.LEFT)
        
        # Action buttons at bottom
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        reset_button = create_button(
            button_frame,
            text="Reset",
            command=self.reset_test,
            style="SecondaryButton.TButton",
            icon_name="reset_icon.png"
        )
        reset_button.pack(side=tk.LEFT)
        
        finish_button = create_button(
            button_frame,
            text="Finish Test",
            command=self.finish_test,
            style="PrimaryButton.TButton"
        )
        finish_button.pack(side=tk.RIGHT)
        
        # Load sample text
        self.sample_display.config(state=tk.NORMAL)
        self.sample_display.delete(1.0, tk.END)
        self.sample_display.insert(tk.END, self.typing_logic.sample_text)
        self.sample_display.config(state=tk.DISABLED)
        
        # Configure the typing area
        self.typing_entry.bind("<KeyRelease>", self.check_typing)
        self.typing_entry.focus_set()
        
        # Set up tag configurations for highlighting
        highlight_style = user_settings.get("error_highlight", "immediate")
        if highlight_style != "none":
            self.sample_display.tag_config("correct", foreground=COLORS["success"])
            self.sample_display.tag_config("incorrect", foreground=COLORS["error"], background="#FFE0E0")
            self.sample_display.tag_config("extra", foreground=COLORS["error"])
            self.sample_display.tag_config("current", background=COLORS["accent"] + "30")
            
        # Start timer when user starts typing
        if show_timer:
            self.typing_entry.bind("<Key>", self.start_timer_on_first_key)
    
    def start_timer_on_first_key(self, event=None):
        """Start the timer when first key is pressed."""
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()
            # Remove this binding after first key
            self.typing_entry.unbind("<Key>")
    
    def update_timer(self):
        """Update the timer display."""
        if self.timer_running:
            self.timer_seconds += 1
            minutes = self.timer_seconds // 60
            seconds = self.timer_seconds % 60
            self.timer_label.config(text=f"Time: {minutes}:{seconds:02d}")
            self.root.after(1000, self.update_timer)
    
    def check_typing(self, event=None):
        """Check the user's typing, update UI and real-time stats."""
        typed_text = self.typing_entry.get(1.0, tk.END).strip()
        
        # Play keypress sound
        if event and event.keysym != "BackSpace":
            self.sounds_manager.play_keypress()
        
        # Update highlighting
        self.highlight_text(typed_text)
        
        # Calculate and update stats
        accuracy = self.typing_logic.calculate_accuracy(typed_text)
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")
        
        # Update WPM if enabled
        user_settings = self.user_manager.get_user_settings(self.current_user) or {}
        if user_settings.get("show_realtime_wpm", True):
            wpm = self.typing_logic.calculate_wpm(typed_text)
            self.wpm_label.config(text=f"WPM: {wpm:.1f}")
        
        # Update progress bar
        progress = min(100, (len(typed_text) / len(self.typing_logic.sample_text)) * 100)
        self.progress_bar['value'] = progress
        
        # Check for test completion
        if len(typed_text) >= len(self.typing_logic.sample_text):
            self.finish_test()
    
    def highlight_text(self, typed_text):
        """Highlight the sample text based on user input and settings."""
        user_settings = self.user_manager.get_user_settings(self.current_user) or {}
        highlight_style = user_settings.get("error_highlight", "immediate")
        
        if highlight_style == "none":
            return
            
        sample_text = self.typing_logic.sample_text
        self.sample_display.config(state=tk.NORMAL)
        self.sample_display.delete(1.0, tk.END)
        
        # Highlight based on error highlighting preference
        if highlight_style == "immediate":
            # Show errors as they are typed
            for i in range(max(len(typed_text), len(sample_text))):
                if i < len(sample_text) and i < len(typed_text):
                    if typed_text[i] == sample_text[i]:
                        self.sample_display.insert(tk.END, sample_text[i], "correct")
                    else:
                        self.sample_display.insert(tk.END, sample_text[i], "incorrect")
                        # Play error sound
                        self.sounds_manager.play_error()
                elif i < len(sample_text):
                    # Remaining sample text
                    if i == len(typed_text):  # Highlight current position
                        self.sample_display.insert(tk.END, sample_text[i], "current")
                    else:
                        self.sample_display.insert(tk.END, sample_text[i])
                else:
                    # Extra typed text
                    self.sample_display.insert(tk.END, typed_text[i], "extra")
        elif highlight_style == "at_end":
            # Just show the sample text with current position highlight
            current_pos = min(len(typed_text), len(sample_text))
            self.sample_display.insert(tk.END, sample_text[:current_pos])
            
            if current_pos < len(sample_text):
                self.sample_display.insert(tk.END, sample_text[current_pos], "current")
                if current_pos + 1 < len(sample_text):
                    self.sample_display.insert(tk.END, sample_text[current_pos+1:])
        
        self.sample_display.config(state=tk.DISABLED)
    
    def reset_test(self):
        """Reset the typing test."""
        self.typing_logic.start_test()  # Generate a new test
        
        # Reset UI elements
        self.sample_display.config(state=tk.NORMAL)
        self.sample_display.delete(1.0, tk.END)
        self.sample_display.insert(tk.END, self.typing_logic.sample_text)
        self.sample_display.config(state=tk.DISABLED)
        
        self.typing_entry.delete(1.0, tk.END)
        
        if hasattr(self, 'wpm_label'):
            self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 100.0%")
        self.progress_bar['value'] = 0
        
        # Reset timer
        if hasattr(self, 'timer_label'):
            self.timer_running = False
            self.timer_seconds = 0
            self.timer_label.config(text="Time: 0:00")
            self.typing_entry.bind("<Key>", self.start_timer_on_first_key)
        
        # Focus on typing entry
        self.typing_entry.focus_set()
        
        # Play achievement sound
        self.sounds_manager.play_achievement()
    
    def finish_test(self):
        """Finish the typing test and show results."""
        # Stop timer
        self.timer_running = False
        
        # Get final text and calculate results
        typed_text = self.typing_entry.get(1.0, tk.END).strip()
        wpm, accuracy = self.typing_logic.calculate_speed_and_accuracy(typed_text)
        
        # Update user statistics
        self.user_manager.update_user_stats(self.current_user, wpm, accuracy)
        
        # Play completion sound
        self.sounds_manager.play_test_complete()
        
        # Show results screen
        self.show_results(wpm, accuracy)
    
    def show_results(self, wpm, accuracy):
        """Show the typing test results."""
        self.clear_screen()
        
        # Main container
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Results header
        header_label = create_label(main_frame, "Test Results", font_size=28, weight="bold")
        header_label.pack(pady=(0, 30))
        
        # Results card
        results_frame = create_frame(main_frame, padding=30, shadow=True)
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
            if info["min_wpm"] <= wpm <= info["max_wpm"]:
                level = lvl
                level_color = info["color"]
                break
        
        wpm_display = ttk.Frame(wpm_frame)
        wpm_display.pack(anchor=tk.W, pady=5)
        
        wpm_value = create_label(wpm_display, f"{wpm:.1f}", font_size=36, weight="bold")
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
        
        accuracy_value = create_label(accuracy_frame, f"{accuracy:.1f}%", font_size=24, weight="bold")
        accuracy_value.pack(anchor=tk.W, pady=5)
        
        # Time taken
        time_frame = ttk.Frame(results_frame)
        time_frame.pack(fill=tk.X, pady=10)
        
        time_label = create_label(time_frame, "Time", font_size=16)
        time_label.pack(anchor=tk.W)
        
        minutes = self.timer_seconds // 60 if hasattr(self, 'timer_seconds') else 0
        seconds = self.timer_seconds % 60 if hasattr(self, 'timer_seconds') else 0
        time_value = create_label(time_frame, f"{minutes}:{seconds:02d}", font_size=24, weight="bold")
        time_value.pack(anchor=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=30)
        
        retry_button = create_button(
            button_frame,
            text="Try Again",
            command=self.start_typing_test,
            style="PrimaryButton.TButton",
            icon_name="reset_icon.png"
        )
        retry_button.pack(side=tk.RIGHT, padx=5)
        
        view_stats_button = create_button(
            button_frame,
            text="View Stats",
            command=self.show_dashboard,
            style="SecondaryButton.TButton",
            icon_name="dashboard_icon.png"
        )
        view_stats_button.pack(side=tk.RIGHT, padx=5)
        
        home_button = create_button(
            button_frame,
            text="Home",
            command=self.show_welcome_screen,
            style="SecondaryButton.TButton"
        )
        home_button.pack(side=tk.RIGHT, padx=5)
    
    def show_settings(self):
        """Show the settings screen."""
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
        
        # Rebuild the current screen to apply new theme
        if hasattr(self, 'current_screen'):
            current_screen = self.current_screen
            if current_screen == "welcome":
                self.show_welcome_screen()
            elif current_screen == "test":
                self.start_typing_test()
    
    def show_dashboard(self):
        """Show the user dashboard."""
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


def main():
    """Run the main program."""
    root = tk.Tk()
    root.title("Typing Speed Test Pro")
    
    # Set icon if available
    icon_path = ICON_PATH / "app_icon.png"
    if icon_path.exists():
        try:
            icon = tk.PhotoImage(file=str(icon_path))
            root.iconphoto(True, icon)
        except Exception:
            pass
    
    # Set minimum window size
    root.minsize(800, 600)
    
    app = TypingSpeedTest(root)
    root.mainloop()


if __name__ == "__main__":
    main()