"""Typing test screen for the typing test application."""

import tkinter as tk
from tkinter import ttk
from config import COLORS
from simplified_ui import (
    create_label, create_button, create_frame, create_text_area, create_progressbar
)

class TestScreen:
    """Screen for the actual typing test."""
    
    def __init__(self, root, user_manager, typing_logic, sounds_manager, current_user, 
                 on_back=None, on_finish=None):
        """Initialize test screen."""
        self.root = root
        self.user_manager = user_manager
        self.typing_logic = typing_logic
        self.sounds_manager = sounds_manager
        self.current_user = current_user
        
        self.on_back = on_back
        self.on_finish = on_finish
        
        self.timer_running = False
        self.timer_seconds = 0
        
        # Start test
        self.typing_logic.start_test()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Top bar
        top_bar = ttk.Frame(main_frame, style="TFrame")
        top_bar.pack(fill=tk.X, pady=(0, 20))
        
        back_button = create_button(
            top_bar,
            text="Back",
            command=self.back_click,
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
            
        # Main content area
        content_frame = create_frame(main_frame, padding=30, bg_color=COLORS["card_background"])
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
            background=COLORS["input_bg"],
            foreground=COLORS["text"]
        )
        self.typing_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Progress bar
        progress_frame = ttk.Frame(content_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_bar = create_progressbar(progress_frame, orient=tk.HORIZONTAL, mode='determinate')
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
                        # Play error sound if this is the last character typed
                        if i == len(typed_text) - 1:
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
        if self.on_finish:
            self.on_finish(wpm, accuracy, self.timer_seconds)
    
    def back_click(self):
        """Handle back button click."""
        # Stop timer if running
        self.timer_running = False
        
        if self.on_back:
            self.on_back()