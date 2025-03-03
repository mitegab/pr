"""Accuracy mode for the typing test application."""

import tkinter as tk
from tkinter import ttk
import time
import random
from config import COLORS, FONTS, SAMPLE_TEXTS
from simplified_ui import (
    create_label, create_button, create_frame, create_text_area, create_progressbar
)

class AccuracyMode:
    """Accuracy typing mode focused on precision typing."""
    
    def __init__(self, root, user_manager, typing_logic, sounds_manager, current_user,
                 on_back=None, on_complete=None):
        """Initialize accuracy mode."""
        self.root = root
        self.user_manager = user_manager
        self.typing_logic = typing_logic
        self.sounds_manager = sounds_manager
        self.current_user = current_user
        
        self.on_back = on_back
        self.on_complete = on_complete
        
        # Accuracy mode settings
        self.error_limit_options = [1, 3, 5, 10]
        self.selected_error_limit = 3
        self.strict_mode = False
        
        # Stats
        self.start_time = None
        self.elapsed_time = 0
        self.timer_running = False
        self.current_position = 0
        self.errors = 0
        self.retries = 0
        
        # Setup UI
        self.setup_config_ui()
    
    def setup_config_ui(self):
        """Set up the configuration UI for accuracy typing mode."""
        # Main container
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = create_label(header_frame, "Accuracy Typing Mode", font_size=24, weight="bold")
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
            "In Accuracy Mode, focus on precise typing. The test will reset if you exceed the error limit.",
            font_size=14
        )
        instructions_label.pack(pady=(0, 20))
        
        # Error limit selection
        error_frame = ttk.Frame(config_frame)
        error_frame.pack(fill=tk.X, pady=10)
        
        error_label = create_label(error_frame, "Error Limit:", font_size=16)
        error_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.error_buttons = {}
        error_button_frame = ttk.Frame(error_frame)
        error_button_frame.pack(side=tk.LEFT)
        
        for i, limit in enumerate(self.error_limit_options):
            button = create_button(
                error_button_frame,
                text=str(limit),
                command=lambda l=limit: self.select_error_limit(l),
                style="SecondaryButton.TButton" if limit != self.selected_error_limit else "PrimaryButton.TButton",
                width=10
            )
            button.grid(row=0, column=i, padx=5)
            self.error_buttons[limit] = button
        
        # Strict mode toggle
        strict_frame = ttk.Frame(config_frame)
        strict_frame.pack(fill=tk.X, pady=20)
        
        strict_label = create_label(strict_frame, "Strict Mode:", font_size=16)
        strict_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.strict_var = tk.BooleanVar(value=self.strict_mode)
        strict_check = ttk.Checkbutton(
            strict_frame, 
            text="Reset immediately on error (for maximum precision)", 
            variable=self.strict_var,
            style="Switch.TCheckbutton"
        )
        strict_check.pack(side=tk.LEFT)
        
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
            text="Start Accuracy Test",
            command=self.start_accuracy_test,
            style="PrimaryButton.TButton"
        )
        start_button.pack(pady=20, ipady=10, ipadx=20)
        
        # Show personal best
        user_stats = self.user_manager.get_user_stats(self.current_user)
        if user_stats and "best_accuracy" in user_stats:
            best_frame = create_frame(main_frame, padding=15, bg_color=COLORS["card_background"], shadow=False)
            best_frame.pack(fill=tk.X, pady=20, padx=100)
            
            best_label = create_label(best_frame, "Your Best Accuracy", font_size=16, weight="bold")
            best_label.pack(anchor=tk.W, pady=(0, 10))
            
            stats_grid = ttk.Frame(best_frame)
            stats_grid.pack(fill=tk.X)
            
            stats = [
                ("Best Accuracy", f"{user_stats.get('best_accuracy', 0):.1f}%"),
                ("Best WPM with >95% Accuracy", f"{user_stats.get('best_accurate_wpm', 0):.1f}"),
                ("Typing Level", user_stats.get("level", "Novice"))
            ]
            
            for i, (label, value) in enumerate(stats):
                stat_label = create_label(stats_grid, label, font_size=14)
                stat_label.grid(row=0, column=i*2, sticky="e", padx=10, pady=5)
                
                value_label = create_label(stats_grid, value, font_size=14, weight="bold")
                value_label.grid(row=0, column=i*2+1, sticky="w", padx=10, pady=5)
    
    def select_error_limit(self, limit):
        """Handle error limit selection."""
        self.selected_error_limit = limit
        
        # Update button styles
        for err_limit, button in self.error_buttons.items():
            if err_limit == limit:
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
    
    def start_accuracy_test(self):
        """Start the accuracy typing test."""
        self.clear_screen()
        self.typing_logic.set_difficulty(self.difficulty_var.get())
        self.typing_logic.start_test()
        
        # Update strict mode from checkbox
        self.strict_mode = self.strict_var.get()
        
        # Reset stats
        self.start_time = None
        self.elapsed_time = 0
        self.errors = 0
        self.retries = 0
        self.current_position = 0
        
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
        
        # Accuracy test info
        mode_text = "Strict Mode" if self.strict_mode else f"Error Limit: {self.selected_error_limit}"
        info_label = create_label(
            top_bar, 
            f"Accuracy Test - {self.typing_logic.current_difficulty} - {mode_text}", 
            font_size=16
        )
        info_label.pack(side=tk.LEFT, padx=20)
        
        # Error counter display
        self.error_label = create_label(
            top_bar, 
            f"Errors: 0/{self.selected_error_limit if not self.strict_mode else 0}", 
            font_size=18, 
            weight="bold",
            foreground=COLORS["success"]
        )
        self.error_label.pack(side=tk.RIGHT)
        
        # Main test frame
        test_frame = create_frame(main_frame, padding=20, bg_color=COLORS["card_background"])
        test_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sample text display
        sample_label = create_label(test_frame, "Type exactly:", font_size=14)
        sample_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.sample_display = create_text_area(
            test_frame,
            height=6,
            wrap="word",
            state="disabled",
            font_family=FONTS["monospace"],
            font_size=14,
            background=COLORS["card_background"],
            foreground=COLORS["text"]
        )
        self.sample_display.pack(fill=tk.X, pady=10)
        
        # Typing entry
        typing_label = create_label(test_frame, "Your typing:", font_size=14)
        typing_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.typing_entry = create_text_area(
            test_frame,
            height=6,
            wrap="word",
            font_family=FONTS["monospace"],
            font_size=14,
            background=COLORS["input_bg"],
            foreground=COLORS["text"]
        )
        self.typing_entry.pack(fill=tk.X, pady=10)
        
        # Progress bar
        progress_frame = ttk.Frame(test_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_bar = create_progressbar(progress_frame)
        self.progress_bar.pack(fill=tk.X)
        
        # Stats display
        stats_frame = ttk.Frame(test_frame)
        stats_frame.pack(fill=tk.X, pady=10)
        
        # Timer display
        self.timer_label = create_label(stats_frame, "Time: 0:00", font_size=14)
        self.timer_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # WPM display
        self.wpm_label = create_label(stats_frame, "WPM: 0", font_size=14)
        self.wpm_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Retries counter
        self.retries_label = create_label(stats_frame, "Retries: 0", font_size=14)
        self.retries_label.pack(side=tk.RIGHT)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        restart_button = create_button(
            button_frame,
            text="Restart Test",
            command=self.start_accuracy_test,
            style="SecondaryButton.TButton"
        )
        restart_button.pack(side=tk.LEFT)
        
        finish_button = create_button(
            button_frame,
            text="Finish Test",
            command=self.finish_accuracy_test,
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
        self.typing_entry.bind("<KeyRelease>", self.on_key_release)
        self.typing_entry.bind("<Key>", self.on_key_press)
        
        # Start timer
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        """Update the timer display."""
        if self.timer_running:
            self.elapsed_time = int(time.time() - self.start_time)
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            self.timer_label.config(text=f"Time: {minutes}:{seconds:02d}")
            self.root.after(1000, self.update_timer)
    
    def on_key_press(self, event):
        """Handle key press event."""
        # Don't count function keys, etc.
        if event.char and event.keysym not in ('BackSpace', 'Delete', 'Tab', 'Return'):
            # Play keypress sound
            self.sounds_manager.play_keypress()
            
            # In strict mode, immediately check if this key causes an error
            if self.strict_mode:
                typed_text = self.typing_entry.get("1.0", "end-1c") + event.char
                sample_text = self.typing_logic.sample_text
                pos = len(typed_text) - 1
                
                if pos < len(sample_text) and typed_text[pos] != sample_text[pos]:
                    # Play error sound
                    self.sounds_manager.play_error()
                    
                    # Reset test immediately
                    self.root.after(500, self.reset_test_with_error)
    
    def on_key_release(self, event):
        """Handle key release event."""
        if not self.timer_running:
            return
        
        typed_text = self.typing_entry.get("1.0", "end-1c")
        sample_text = self.typing_logic.sample_text
        
        # Update highlighting
        self.highlight_text(typed_text, sample_text)
        
        # Calculate progress
        progress = min(100, (len(typed_text) / len(sample_text)) * 100)
        self.progress_bar['value'] = progress
        
        # Calculate and update stats
        if time.time() - self.start_time > 0:
            minutes = (time.time() - self.start_time) / 60
            words = len(typed_text) / 5  # Standard: 5 characters = 1 word
            wpm = words / minutes if minutes > 0 else 0
            self.wpm_label.config(text=f"WPM: {wpm:.1f}")
        
        # Check for errors in non-strict mode
        if not self.strict_mode and len(typed_text) > 0:
            current_errors = self.count_errors(typed_text, sample_text[:len(typed_text)])
            if current_errors > self.errors:
                # New errors detected
                self.errors = current_errors
                self.error_label.config(
                    text=f"Errors: {self.errors}/{self.selected_error_limit}",
                    foreground=COLORS["error"] if self.errors > 0 else COLORS["success"]
                )
                
                # Play error sound
                self.sounds_manager.play_error()
                
                # Check if error limit reached
                if self.errors >= self.selected_error_limit:
                    self.root.after(500, self.reset_test_with_error)
        
        # Check for completion
        if len(typed_text) >= len(sample_text):
            self.finish_accuracy_test()
    
    def highlight_text(self, typed_text, sample_text):
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
            elif i < len(sample_text):
                # Untyped characters
                if i == len(typed_text):
                    # Current position
                    self.sample_display.insert("end", sample_text[i], "current")
                else:
                    # Future characters
                    self.sample_display.insert("end", sample_text[i])
        
        self.sample_display.config(state="disabled")
    
    def count_errors(self, typed_text, sample_text):
        """Count the number of errors in the typed text."""
        error_count = 0
        min_len = min(len(typed_text), len(sample_text))
        
        for i in range(min_len):
            if typed_text[i] != sample_text[i]:
                error_count += 1
                
        # Count extra characters as errors
        error_count += abs(len(typed_text) - len(sample_text))
        
        return error_count
    
    def reset_test_with_error(self):
        """Reset the test after an error is made."""
        # Increment retry counter
        self.retries += 1
        self.retries_label.config(text=f"Retries: {self.retries}")
        
        # Save the progress before resetting
        typed_text = self.typing_entry.get("1.0", "end-1c")
        elapsed_minutes = (time.time() - self.start_time) / 60
        progress_pct = min(100, (len(typed_text) / len(self.typing_logic.sample_text)) * 100)
        
        # Reset typing entry
        self.typing_entry.delete("1.0", "end")
        
        # Reset error count
        self.errors = 0
        self.error_label.config(text=f"Errors: 0/{self.selected_error_limit}", foreground=COLORS["success"])
        
        # Reset timer
        self.start_time = time.time()
        
        # Reset progress bar
        self.progress_bar['value'] = 0
        
        # Focus on typing entry
        self.typing_entry.focus_set()
    
    def finish_accuracy_test(self):
        """Finish the accuracy test and show results."""
        # Stop timer
        self.timer_running = False
        
        # Calculate final stats
        if self.start_time is None:
            elapsed_minutes = 0
        else:
            elapsed_minutes = (time.time() - self.start_time) / 60
        
        typed_text = self.typing_entry.get("1.0", "end-1c")
        sample_text = self.typing_logic.sample_text
        total_chars = len(typed_text)
        
        # Calculate WPM
        wpm = (total_chars / 5) / elapsed_minutes if elapsed_minutes > 0 else 0
        
        # Calculate accuracy
        errors = self.count_errors(typed_text, sample_text)
        accuracy = ((total_chars - errors) / total_chars * 100) if total_chars > 0 else 100
        
        # Save stats to user profile
        self.user_manager.update_user_stats(
            self.current_user,
            wpm=wpm,
            accuracy=accuracy,
            test_type="accuracy"
        )
        
        # Show results
        self.show_accuracy_results(wpm, accuracy, errors, self.retries, elapsed_minutes * 60)
    
    def show_accuracy_results(self, wpm, accuracy, errors, retries, elapsed_time):
        """Show the accuracy test results."""
        self.clear_screen()
        
        # Main container
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        header_label = create_label(header_frame, "Accuracy Test Results", font_size=24, weight="bold")
        header_label.pack(side=tk.LEFT)
        
        # Results card
        results_card = create_frame(main_frame, padding=30, bg_color=COLORS["card_background"])
        results_card.pack(fill=tk.X, pady=20, padx=40)
        
        # Accuracy result with badge
        accuracy_frame = ttk.Frame(results_card)
        accuracy_frame.pack(fill=tk.X, pady=10)
        
        acc_label = create_label(accuracy_frame, "Accuracy", font_size=16)
        acc_label.pack(anchor="w")
        
        # Create badge color based on accuracy
        if accuracy >= 98:
            badge_color = COLORS["success"]
            badge_text = "Perfect!"
        elif accuracy >= 95:
            badge_color = COLORS["success"]
            badge_text = "Excellent!"
        elif accuracy >= 90:
            badge_color = COLORS["accent"]
            badge_text = "Good"
        elif accuracy >= 80:
            badge_color = COLORS["warning"]
            badge_text = "Acceptable"
        else:
            badge_color = COLORS["error"]
            badge_text = "Needs Improvement"
        
        acc_value_frame = ttk.Frame(accuracy_frame)
        acc_value_frame.pack(anchor="w", pady=5)
        
        acc_value = create_label(acc_value_frame, f"{accuracy:.1f}%", font_size=36, weight="bold")
        acc_value.pack(side=tk.LEFT)
        
        acc_badge = create_frame(acc_value_frame, padding=8, bg_color=badge_color)
        acc_badge.pack(side=tk.LEFT, padx=20)
        
        badge_text = create_label(acc_badge, badge_text, font_size=14, weight="bold", foreground="#ffffff")
        badge_text.pack()
        
        # Other stats
        stats_grid = ttk.Frame(results_card)
        stats_grid.pack(fill=tk.X, pady=20)
        
        # Define stats to display
        stats = [
            ("WPM", f"{wpm:.1f}"),
            ("Errors", str(errors)),
            ("Retries", str(retries)),
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
        
        # Personalized feedback based on accuracy performance
        if accuracy >= 98:
            feedback = "Exceptional accuracy! Your precision typing skills are impeccable."
        elif accuracy >= 95:
            feedback = "Excellent precision! You're on your way to becoming a perfect typist."
        elif accuracy >= 90:
            feedback = "Good accuracy. Remember, slow down slightly more to maintain better precision."
        elif accuracy >= 80:
            feedback = "Your accuracy is acceptable but needs improvement. Focus on careful placement of fingers."
        else:
            feedback = "Try slowing down significantly to improve accuracy. Speed will follow naturally."
        
        # Add feedback about retries if applicable
        if retries > 5:
            retry_feedback = " Work on maintaining focus and consistency to reduce the number of retries."
            feedback += retry_feedback
        
        summary_label = create_label(summary_frame, feedback, font_size=14, foreground=COLORS["accent"])
        summary_label.pack(pady=10)
        
        # Get user's previous best
        user_stats = self.user_manager.get_user_stats(self.current_user)
        if user_stats:
            best_accuracy = user_stats.get("best_accuracy", 0)
            
            if accuracy > best_accuracy:
                new_record = create_label(
                    summary_frame,
                    "🎉 New Personal Best Accuracy! 🎉",
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
            command=self.start_accuracy_test,
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
        
        # If accuracy is 100% and this is their best, offer a certificate
        if accuracy >= 98 and (not user_stats or accuracy >= user_stats.get("best_accuracy", 0)):
            self.offer_certificate(wpm, accuracy)
    
    def offer_certificate(self, wpm, accuracy):
        """Offer to generate a certificate for excellent performance."""
        # Create a popup dialog to offer a certificate
        popup = tk.Toplevel(self.root)
        popup.title("Achievement Unlocked!")
        popup.geometry("400x300")
        popup.transient(self.root)
        popup.grab_set()
        
        # Center on parent
        x = self.root.winfo_x() + (self.root.winfo_width() - 400) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 300) // 2
        popup.geometry(f"+{x}+{y}")
        
        popup.configure(bg=COLORS["background"])
        
        # Create content
        content_frame = create_frame(popup, padding=20)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Trophy icon or similar
        trophy_label = create_label(content_frame, "🏆", font_size=48)
        trophy_label.pack(pady=(0, 10))
        
        # Congratulatory message
        congrats_label = create_label(
            content_frame,
            "Perfect Accuracy Achievement!",
            font_size=18,
            weight="bold"
        )
        congrats_label.pack(pady=(0, 10))
        
        message_label = create_label(
            content_frame,
            f"Congratulations on achieving {accuracy:.1f}% accuracy at {wpm:.1f} WPM!\nWould you like to generate a certificate for this achievement?",
            font_size=12
        )
        message_label.pack(pady=(0, 20))
        
        # Button frame
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill=tk.X)
        
        # No button
        no_button = create_button(
            button_frame,
            text="No Thanks",
            command=popup.destroy,
            style="SecondaryButton.TButton"
        )
        no_button.pack(side=tk.LEFT, padx=5)
        
        # Yes button
        yes_button = create_button(
            button_frame,
            text="Generate Certificate",
            command=lambda: [popup.destroy(), self.generate_certificate(wpm, accuracy)],
            style="PrimaryButton.TButton"
        )
        yes_button.pack(side=tk.RIGHT, padx=5)
    
    def generate_certificate(self, wpm, accuracy):
        """Generate a certificate for the user's achievement."""
        from certificate_generator import CertificateGenerator
        from tkinter import simpledialog, messagebox
        import os
        import platform
        import subprocess
        
        # Ask for full name
        name_dialog = tk.Toplevel(self.root)
        name_dialog.title("Enter Your Name")
        name_dialog.geometry("400x200")
        name_dialog.transient(self.root)
        name_dialog.grab_set()
        name_dialog.configure(bg=COLORS["background"])
        
        # Center on parent
        x = self.root.winfo_x() + (self.root.winfo_width() - 400) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 200) // 2
        name_dialog.geometry(f"+{x}+{y}")
        
        # Create dialog content
        dialog_frame = create_frame(name_dialog, padding=20)
        dialog_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        prompt_label = create_label(
            dialog_frame, 
            "Please enter your full name for the certificate:",
            font_size=14
        )
        prompt_label.pack(pady=(0, 20))
        
        from simplified_ui import create_entry
        name_var = tk.StringVar(value=self.current_user)
        name_entry = create_entry(
            dialog_frame,
            textvariable=name_var,
            font_size=16
        )
        name_entry.pack(fill=tk.X, pady=10)
        name_entry.select_range(0, tk.END)  # Select all text
        name_entry.focus_set()
        
        # Buttons
        button_frame = ttk.Frame(dialog_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        cancel_btn = create_button(
            button_frame,
            text="Cancel",
            command=name_dialog.destroy,
            style="SecondaryButton.TButton"
        )
        cancel_btn.pack(side=tk.LEFT)
        
        generate_btn = create_button(
            button_frame,
            text="Generate Certificate",
            command=lambda: self._create_certificate(name_var.get(), wpm, accuracy, name_dialog),
            style="PrimaryButton.TButton"
        )
        generate_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key
        name_entry.bind("<Return>", lambda event: generate_btn.invoke())
    
    def _create_certificate(self, full_name, wpm, accuracy, dialog=None):
        """Create and save the certificate."""
        if dialog:
            dialog.destroy()
            
        from certificate_generator import CertificateGenerator
        from tkinter import messagebox
        import os
        import platform
        import subprocess
        from datetime import datetime
        
        # Certificate data
        certificate_data = {
            "full_name": full_name,
            "wpm": f"{wpm:.1f}",
            "accuracy": f"{accuracy:.1f}%",
            "text_title": "Accuracy Challenge",
            "text_genre": self.typing_logic.current_difficulty,
            "date": datetime.now().strftime("%B %d, %Y"),
            "level": self._get_level_for_wpm(wpm)
        }
        
        try:
            # Generate the certificate
            certificate_generator = CertificateGenerator()
            pdf_path = certificate_generator.generate_certificate(certificate_data)
            
            # Show success message and ask to open
            response = messagebox.askyesno(
                "Certificate Generated",
                f"Your certificate has been saved to:\n{pdf_path}\n\nWould you like to open it now?"
            )
            
            if response:
                # Open the PDF with the default PDF viewer
                if platform.system() == 'Darwin':  # macOS
                    subprocess.run(['open', pdf_path])
                elif platform.system() == 'Windows':
                    os.startfile(pdf_path)
                else:  # Linux
                    subprocess.run(['xdg-open', pdf_path])
                    
        except Exception as e:
            messagebox.showerror(
                "Certificate Error",
                f"There was an error generating the certificate:\n{str(e)}"
            )
    
    def _get_level_for_wpm(self, wpm):
        """Get the skill level based on WPM."""
        from config import USER_LEVELS
        
        for level, info in USER_LEVELS.items():
            if info["min_wpm"] <= wpm <= info["max_wpm"]:
                return level
        
        return "Novice"  # Default level
    
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