"""Speed typing mode for the typing test application."""

import tkinter as tk
from tkinter import ttk
import time
import random
from config import COLORS, FONTS, SAMPLE_TEXTS
from simplified_ui import (
    create_label, create_button, create_frame, create_text_area, create_progressbar
)

class SpeedMode:
    """Speed typing mode focused on maximizing WPM."""
    
    def __init__(self, root, user_manager, typing_logic, sounds_manager, current_user,
                 on_back=None, on_complete=None):
        """Initialize speed mode."""
        self.root = root
        self.user_manager = user_manager
        self.typing_logic = typing_logic
        self.sounds_manager = sounds_manager
        self.current_user = current_user
        
        self.on_back = on_back
        self.on_complete = on_complete
        
        # Speed mode settings
        self.time_options = [30, 60, 120, 300]  # seconds
        self.selected_time = 60
        
        # Stats
        self.start_time = None
        self.elapsed_time = 0
        self.remaining_time = self.selected_time
        self.timer_running = False
        self.current_position = 0
        self.errors = 0
        
        # Setup UI
        self.setup_config_ui()
    
    def setup_config_ui(self):
        """Set up the configuration UI for speed typing mode."""
        # Main container
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = create_label(header_frame, "Speed Typing Mode", font_size=24, weight="bold")
        title_label.pack(side=tk.LEFT)
        
        back_button = create_button(
            header_frame,
            text="Back to Menu",
            command=self.back_click,
            style="SecondaryButton.TButton"
        )
        back_button.pack(side=tk.RIGHT)
        
        # Configuration card
        config_frame = create_frame(main_frame, padding=20, bg_color=COLORS["card_background"])
        config_frame.pack(fill=tk.X, pady=20, padx=100)
        
        instructions_label = create_label(
            config_frame,
            "In Speed Mode, the goal is to type as many words as possible within the time limit.",
            font_size=14
        )
        instructions_label.pack(pady=(0, 20))
        
        # Time selection
        time_frame = ttk.Frame(config_frame)
        time_frame.pack(fill=tk.X, pady=10)
        
        time_label = create_label(time_frame, "Select Time Limit:", font_size=16)
        time_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.time_buttons = {}
        time_button_frame = ttk.Frame(time_frame)
        time_button_frame.pack(side=tk.LEFT)
        
        for i, seconds in enumerate(self.time_options):
            formatted_time = self.format_time(seconds)
            button = create_button(
                time_button_frame,
                text=formatted_time,
                command=lambda s=seconds: self.select_time(s),
                style="SecondaryButton.TButton" if seconds != self.selected_time else "PrimaryButton.TButton",
                width=10
            )
            button.grid(row=0, column=i, padx=5)
            self.time_buttons[seconds] = button
        
        # Selected difficulty
        difficulty_frame = ttk.Frame(config_frame)
        difficulty_frame.pack(fill=tk.X, pady=20)
        
        difficulty_label = create_label(difficulty_frame, "Difficulty:", font_size=16)
        difficulty_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.difficulty_var = tk.StringVar(value=self.typing_logic.current_difficulty)
        
        # Load user's preferred difficulty if available
        user_settings = self.user_manager.get_user_settings(self.current_user)
        if user_settings and "default_difficulty" in user_settings:
            self.difficulty_var.set(user_settings["default_difficulty"])
            self.typing_logic.set_difficulty(user_settings["default_difficulty"])
        
        self.difficulty_buttons = {}
        difficulty_button_frame = ttk.Frame(difficulty_frame)
        difficulty_button_frame.pack(side=tk.LEFT)
        
        for i, difficulty in enumerate(SAMPLE_TEXTS.keys()):
            button = create_button(
                difficulty_button_frame,
                text=difficulty,
                command=lambda d=difficulty: self.select_difficulty(d),
                style="SecondaryButton.TButton" if difficulty != self.difficulty_var.get() else "PrimaryButton.TButton",
                width=12
            )
            button.grid(row=0, column=i, padx=5)
            self.difficulty_buttons[difficulty] = button
        
        # Start button
        start_button = create_button(
            config_frame,
            text="Start Speed Test",
            command=self.start_speed_test,
            style="PrimaryButton.TButton"
        )
        start_button.pack(pady=20, ipady=10, ipadx=20)
        
        # Show personal best
        user_stats = self.user_manager.get_user_stats(self.current_user)
        if user_stats and "best_wpm" in user_stats:
            best_frame = create_frame(main_frame, padding=15, bg_color=COLORS["card_background"], shadow=False)
            best_frame.pack(fill=tk.X, pady=20, padx=100)
            
            best_label = create_label(best_frame, "Your Personal Best", font_size=16, weight="bold")
            best_label.pack(anchor=tk.W, pady=(0, 10))
            
            stats_grid = ttk.Frame(best_frame)
            stats_grid.pack(fill=tk.X)
            
            stats = [
                ("Best WPM", f"{user_stats.get('best_wpm', 0):.1f}"),
                ("Best Accuracy", f"{user_stats.get('best_accuracy', 0):.1f}%"),
                ("Typing Level", user_stats.get("level", "Novice"))
            ]
            
            for i, (label, value) in enumerate(stats):
                stat_label = create_label(stats_grid, label, font_size=14)
                stat_label.grid(row=0, column=i*2, sticky="e", padx=10, pady=5)
                
                value_label = create_label(stats_grid, value, font_size=14, weight="bold")
                value_label.grid(row=0, column=i*2+1, sticky="w", padx=10, pady=5)
        
    def format_time(self, seconds):
        """Format seconds into a readable time string."""
        minutes = seconds // 60
        remainder_seconds = seconds % 60
        if minutes > 0:
            return f"{minutes}:{remainder_seconds:02d}"
        else:
            return f"{seconds} sec"
    
    def select_time(self, seconds):
        """Handle time selection."""
        self.selected_time = seconds
        
        # Update button styles
        for time_val, button in self.time_buttons.items():
            if time_val == seconds:
                button.configure(style="PrimaryButton.TButton")
            else:
                button.configure(style="SecondaryButton.TButton")
    
    def select_difficulty(self, difficulty):
        """Handle difficulty selection."""
        self.typing_logic.set_difficulty(difficulty)
        self.difficulty_var.set(difficulty)
        
        # Update button styles
        for diff, button in self.difficulty_buttons.items():
            if diff == difficulty:
                button.configure(style="PrimaryButton.TButton")
            else:
                button.configure(style="SecondaryButton.TButton")
    
    def start_speed_test(self):
        """Start the speed typing test."""
        self.clear_screen()
        self.typing_logic.set_difficulty(self.difficulty_var.get())
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
            command=self.setup_config_ui,
            style="SecondaryButton.TButton"
        )
        back_button.pack(side=tk.LEFT)
        
        # Speed test info
        info_label = create_label(
            top_bar, 
            f"Speed Test - {self.typing_logic.current_difficulty} - {self.format_time(self.selected_time)}", 
            font_size=16
        )
        info_label.pack(side=tk.LEFT, padx=20)
        
        # Timer display
        self.timer_label = create_label(top_bar, f"Time: {self.format_time(self.selected_time)}", font_size=18, weight="bold")
        self.timer_label.pack(side=tk.RIGHT)
        
        # Main test frame
        test_frame = create_frame(main_frame, padding=20, bg_color=COLORS["card_background"])
        test_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sample text display
        self.sample_display = create_text_area(
            test_frame,
            height=8,
            width=80,
            wrap="word",
            state="disabled",
            font_family=FONTS["monospace"],
            font_size=14,
            background=COLORS["card_background"],
            foreground=COLORS["text"]
        )
        self.sample_display.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Typing entry
        self.typing_entry = create_text_area(
            test_frame,
            height=8,
            width=80,
            wrap="word",
            font_family=FONTS["monospace"],
            font_size=14,
            background=COLORS["input_bg"],
            foreground=COLORS["text"]
        )
        self.typing_entry.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Stats display
        stats_frame = ttk.Frame(test_frame)
        stats_frame.pack(fill=tk.X, pady=10)
        
        # WPM display
        self.wpm_label = create_label(stats_frame, "WPM: 0", font_size=16)
        self.wpm_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Character count
        self.char_count_label = create_label(stats_frame, "Characters: 0", font_size=16)
        self.char_count_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Accuracy display
        self.accuracy_label = create_label(stats_frame, "Accuracy: 100%", font_size=16)
        self.accuracy_label.pack(side=tk.RIGHT)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        restart_button = create_button(
            button_frame,
            text="Restart Test",
            command=self.start_speed_test,
            style="SecondaryButton.TButton"
        )
        restart_button.pack(side=tk.LEFT)
        
        finish_button = create_button(
            button_frame,
            text="Finish Test",
            command=self.finish_speed_test,
            style="PrimaryButton.TButton"
        )
        finish_button.pack(side=tk.RIGHT)
        
        # Set up text and tags
        self.sample_display.config(state="normal")
        self.sample_display.delete(1.0, "end")
        self.sample_display.insert("end", self.typing_logic.sample_text)
        self.sample_display.config(state="disabled")
        
        # Set up text highlighting tags
        self.sample_display.tag_config("correct", foreground=COLORS["success"])
        self.sample_display.tag_config("incorrect", foreground=COLORS["error"], background="#FFE0E0")
        self.sample_display.tag_config("current", background=COLORS.get("light_accent", "#a0cfff"))
        
        # Focus typing entry and bind events
        self.typing_entry.focus_set()
        self.typing_entry.bind("<KeyRelease>", self.check_typing)
        
        # Start timer
        self.remaining_time = self.selected_time
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        """Update the timer display."""
        if not self.timer_running:
            return
            
        elapsed = time.time() - self.start_time
        self.remaining_time = max(0, self.selected_time - int(elapsed))
        
        # Update timer display
        self.timer_label.config(text=f"Time: {self.format_time(self.remaining_time)}")
        
        # Check if time is up
        if self.remaining_time <= 0:
            self.timer_running = False
            self.finish_speed_test()
        else:
            self.root.after(1000, self.update_timer)
    
    def check_typing(self, event=None):
        """Check the user's typing and update stats."""
        if not self.timer_running:
            return
            
        typed_text = self.typing_entry.get("1.0", "end-1c")  # Get text without the final newline
        sample_text = self.typing_logic.sample_text
        
        # Play keypress sound if available
        if event and event.keysym not in ('BackSpace', 'Tab', 'Return', 'Escape'):
            self.sounds_manager.play_keypress()
        
        # Update character count
        self.char_count_label.config(text=f"Characters: {len(typed_text)}")
        
        # Update WPM
        elapsed_minutes = (time.time() - self.start_time) / 60
        if elapsed_minutes > 0:
            # Calculate WPM: (characters / 5) / minutes
            wpm = (len(typed_text) / 5) / elapsed_minutes
            self.wpm_label.config(text=f"WPM: {wpm:.1f}")
        
        # Calculate and update accuracy
        if len(typed_text) > 0:
            accuracy = self.calculate_accuracy(typed_text, sample_text[:len(typed_text)])
            self.accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")
        
        # Highlight text according to correctness
        self.highlight_text(typed_text, sample_text, event)
        
        # If sample text is completed, get new text and continue
        if len(typed_text) >= len(sample_text):
            # Load new sample
            self.typing_logic.start_test()
            sample_text = self.typing_logic.sample_text
            
            # Clear typing entry and update sample display
            self.typing_entry.delete("1.0", "end")
            
            self.sample_display.config(state="normal")
            self.sample_display.delete("1.0", "end")
            self.sample_display.insert("end", sample_text)
            self.sample_display.config(state="disabled")
            
            # Play achievement sound
            self.sounds_manager.play_achievement()
    
    def highlight_text(self, typed_text, sample_text, event=None):
        """Highlight the sample text based on user input."""
        self.sample_display.config(state="normal")
        self.sample_display.delete("1.0", "end")
        
        # Process each character
        for i in range(max(len(typed_text), len(sample_text))):
            if i < len(typed_text) and i < len(sample_text):
                if typed_text[i] == sample_text[i]:
                    # Correct character
                    self.sample_display.insert("end", sample_text[i], "correct")
                else:
                    # Incorrect character
                    self.sample_display.insert("end", sample_text[i], "incorrect")
                    # Play error sound if applicable
                    if event and event.char and i == len(typed_text) - 1:
                        self.sounds_manager.play_error()
            elif i < len(sample_text):
                # Untyped characters
                if i == len(typed_text):
                    # Current position
                    self.sample_display.insert("end", sample_text[i], "current")
                else:
                    # Future characters
                    self.sample_display.insert("end", sample_text[i])
        
        self.sample_display.config(state="disabled")
    
    def calculate_accuracy(self, typed_text, sample_text):
        """Calculate typing accuracy percentage."""
        if not typed_text:
            return 100.0
            
        min_len = min(len(typed_text), len(sample_text))
        correct_chars = sum(1 for i in range(min_len) if typed_text[i] == sample_text[i])
        
        return (correct_chars / len(typed_text)) * 100
    
    def finish_speed_test(self):
        """Finish the speed test and show results."""
        # Stop timer
        self.timer_running = False
        
        # Calculate final stats
        typed_text = self.typing_entry.get("1.0", "end-1c")
        total_chars = len(typed_text)
        if self.start_time is None:
            elapsed_minutes = 0
        else:
            elapsed_minutes = (time.time() - self.start_time) / 60
        
        # Calculate WPM: (characters / 5) / minutes
        wpm = (total_chars / 5) / elapsed_minutes if elapsed_minutes > 0 else 0
        
        # Calculate accuracy
        correct_chars = 0
        for i in range(min(len(typed_text), len(self.typing_logic.sample_text))):
            if typed_text[i] == self.typing_logic.sample_text[i]:
                correct_chars += 1
                
        accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0
        
        # Save stats
        self.user_manager.update_user_stats(
            self.current_user,
            wpm=wpm,
            accuracy=accuracy,
            test_type="speed"
        )
        
        # Show results
        self.show_speed_results(wpm, accuracy, total_chars, elapsed_minutes * 60)
    
    def show_speed_results(self, wpm, accuracy, total_chars, elapsed_time):
        """Show the speed test results."""
        self.clear_screen()
        
        # Main container
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        header_label = create_label(header_frame, "Speed Test Results", font_size=24, weight="bold")
        header_label.pack(side=tk.LEFT)
        
        # Results card
        results_card = create_frame(main_frame, padding=30, bg_color=COLORS["card_background"])
        results_card.pack(fill=tk.X, pady=20, padx=40)
        
        # WPM result with level
        wpm_frame = ttk.Frame(results_card)
        wpm_frame.pack(fill=tk.X, pady=10)
        
        wpm_label = create_label(wpm_frame, "Typing Speed", font_size=16)
        wpm_label.pack(anchor="w")
        
        # Get user level based on WPM
        from config import USER_LEVELS
        level = "Novice"
        level_color = USER_LEVELS["Novice"]["color"]
        for lvl, info in USER_LEVELS.items():
            if info["min_wpm"] <= wpm <= info["max_wpm"]:
                level = lvl
                level_color = info["color"]
                break
        
        wpm_value_frame = ttk.Frame(wpm_frame)
        wpm_value_frame.pack(anchor="w", pady=5)
        
        wpm_value = create_label(wpm_value_frame, f"{wpm:.1f}", font_size=36, weight="bold")
        wpm_value.pack(side=tk.LEFT)
        
        wpm_unit = create_label(wpm_value_frame, "WPM", font_size=20)
        wpm_unit.pack(side=tk.LEFT, padx=10, pady=(8, 0))
        
        level_badge = create_frame(wpm_value_frame, padding=8, bg_color=level_color)
        level_badge.pack(side=tk.LEFT, padx=20)
        
        level_text = create_label(level_badge, level, font_size=14, weight="bold", foreground="#ffffff")
        level_text.pack()
        
        # Other stats
        stats_grid = ttk.Frame(results_card)
        stats_grid.pack(fill=tk.X, pady=20)
        
        # Define stats to display
        stats = [
            ("Accuracy", f"{accuracy:.1f}%"),
            ("Characters Typed", str(total_chars)),
            ("Time", f"{int(elapsed_time // 60)}:{int(elapsed_time % 60):02d}")
        ]
        
        # Create grid of stats
        for i, (label, value) in enumerate(stats):
            stat_label = create_label(stats_grid, label, font_size=14)
            stat_label.grid(row=i, column=0, sticky="e", padx=10, pady=5)
            
            value_label = create_label(stats_grid, value, font_size=14, weight="bold")
            value_label.grid(row=i, column=1, sticky="w", padx=10, pady=5)
        
        # Center the grid columns
        stats_grid.columnconfigure(0, weight=1)
        stats_grid.columnconfigure(1, weight=1)
        
        # Performance summary
        summary_frame = create_frame(results_card, padding=15, bg_color=COLORS["card_background"])
        summary_frame.pack(fill=tk.X, pady=10)
        
        # Personalized feedback based on performance
        if wpm < 30:
            feedback = "Keep practicing! Focus on accuracy first, then gradually increase your speed."
        elif wpm < 60:
            feedback = "Good job! You're making progress. Try to practice regularly to improve your speed further."
        elif wpm < 90:
            feedback = "Excellent! You're typing at a professional level. Keep challenging yourself!"
        else:
            feedback = "Outstanding! You're among the fastest typists. Consider participating in typing competitions!"
        
        summary_label = create_label(summary_frame, feedback, font_size=14, foreground=COLORS["accent"])
        summary_label.pack(pady=10)
        
        # Get user's previous best
        user_stats = self.user_manager.get_user_stats(self.current_user)
        if user_stats:
            best_wpm = user_stats.get("best_wpm", 0)
            
            if wpm > best_wpm:
                new_record = create_label(
                    summary_frame,
                    "🎉 New Personal Best! 🎉",
                    font_size=16,
                    weight="bold",
                    foreground=COLORS["success"]
                )
                new_record.pack(pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        retry_button = create_button(
            button_frame,
            text="Try Again",
            command=self.start_speed_test,
            style="PrimaryButton.TButton"
        )
        retry_button.pack(side=tk.RIGHT, padx=5)
        
        settings_button = create_button(
            button_frame,
            text="Change Settings",
            command=self.setup_config_ui,
            style="SecondaryButton.TButton"
        )
        settings_button.pack(side=tk.RIGHT, padx=5)
        
        home_button = create_button(
            button_frame,
            text="Back to Menu",
            command=self.back_click,
            style="SecondaryButton.TButton"
        )
        home_button.pack(side=tk.LEFT)
        
        # Play completion sound
        self.sounds_manager.play_test_complete()
    
    def back_click(self):
        """Handle back button click."""
        # Stop timer if running
        self.timer_running = False
        
        if self.on_back:
            self.on_back()
    
    def clear_screen(self):
        """Clear all widgets from the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()