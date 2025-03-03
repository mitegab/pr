"""Practice mode with pre-existing texts from different genres."""

import tkinter as tk
from tkinter import ttk
import os
import json
import random
import time
from pathlib import Path

from config import COLORS, FONTS, RESOURCES_DIR
from simplified_ui import (
    create_label, create_button, create_frame, create_text_area, create_progressbar
)

# Define practice texts directory
PRACTICE_TEXTS_DIR = RESOURCES_DIR / "practice_texts"
PRACTICE_TEXTS_DIR.mkdir(exist_ok=True)

# Sample genres with example texts (these would be loaded from files)
SAMPLE_GENRES = {
    "Literature": {
        "Pride and Prejudice": "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.",
        "The Great Gatsby": "In my younger and more vulnerable years my father gave me some advice that I've been turning over in my mind ever since.",
        "To Kill a Mockingbird": "When he was nearly thirteen, my brother Jem got his arm badly broken at the elbow."
    },
    "Science": {
        "Quantum Physics": "Quantum mechanics is a fundamental theory in physics that provides a description of the physical properties of nature at the scale of atoms and subatomic particles.",
        "Biology": "The cell is the basic structural, functional, and biological unit of all known organisms. A cell is the smallest unit of life.",
        "Astronomy": "A black hole is a region of spacetime where gravity is so strong that nothing—no particles or even electromagnetic radiation such as light—can escape from it."
    },
    "Technology": {
        "Machine Learning": "Machine learning is the study of computer algorithms that improve automatically through experience and by the use of data.",
        "Web Development": "HTML5 is a markup language used for structuring and presenting content on the World Wide Web. It is the fifth and last major version of HTML.",
        "Cybersecurity": "Cryptography is the practice and study of techniques for secure communication in the presence of adversarial behavior."
    },
    "History": {
        "Ancient Rome": "The Roman Empire was the post-Republican period of ancient Rome, including the period of the dictatorship of Julius Caesar.",
        "World War II": "World War II was a global war that lasted from 1939 to 1945, involving many of the world's nations—including all of the great powers.",
        "Renaissance": "The Renaissance was a period in European history marking the transition from the Middle Ages to modernity."
    }
}

class PracticeText:
    """Class to represent a practice text."""
    
    def __init__(self, title, content, genre, author="Unknown", difficulty="Intermediate"):
        """Initialize practice text."""
        self.title = title
        self.content = content
        self.genre = genre
        self.author = author
        self.difficulty = difficulty
        self.word_count = len(content.split())
        
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "title": self.title,
            "content": self.content,
            "genre": self.genre,
            "author": self.author,
            "difficulty": self.difficulty,
            "word_count": self.word_count
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a PracticeText from a dictionary."""
        return cls(
            data["title"],
            data["content"],
            data["genre"],
            data.get("author", "Unknown"),
            data.get("difficulty", "Intermediate")
        )


class PracticeMode:
    """Practice mode with pre-existing texts from different genres."""
    
    def __init__(self, root, user_manager, sounds_manager, current_user, 
                 on_back=None, on_complete=None):
        """Initialize practice mode."""
        self.root = root
        self.user_manager = user_manager
        self.sounds_manager = sounds_manager
        self.current_user = current_user
        
        self.on_back = on_back
        self.on_complete = on_complete
        
        # Initialize variables
        self.genres = {}
        self.selected_genre = None
        self.selected_text = None
        self.practice_texts = {}
        
        # Stats
        self.start_time = None
        self.elapsed_time = 0
        self.timer_running = False
        self.current_position = 0
        self.errors = 0
        
        # Load practice texts
        self.load_practice_texts()
        
        # Setup UI
        self.setup_selection_ui()
    
    def load_practice_texts(self):
        """Load practice texts from files or create them if they don't exist."""
        # Ensure genres directory exists
        if not PRACTICE_TEXTS_DIR.exists():
            PRACTICE_TEXTS_DIR.mkdir(parents=True)
            
        # Check if we need to create sample texts
        if not any(PRACTICE_TEXTS_DIR.glob("*.json")):
            # Create sample texts from our dictionary
            for genre, texts in SAMPLE_GENRES.items():
                genre_dir = PRACTICE_TEXTS_DIR / genre
                genre_dir.mkdir(exist_ok=True)
                
                for title, content in texts.items():
                    text_obj = PracticeText(title, content, genre)
                    file_path = genre_dir / f"{title.replace(' ', '_')}.json"
                    
                    with open(file_path, 'w') as f:
                        json.dump(text_obj.to_dict(), f, indent=4)
        
        # Load texts from directories
        self.practice_texts = {}
        self.genres = {}
        
        for genre_dir in PRACTICE_TEXTS_DIR.glob("*"):
            if genre_dir.is_dir():
                genre_name = genre_dir.name
                self.genres[genre_name] = []
                self.practice_texts[genre_name] = {}
                
                for text_file in genre_dir.glob("*.json"):
                    try:
                        with open(text_file, 'r') as f:
                            text_data = json.load(f)
                            text_obj = PracticeText.from_dict(text_data)
                            self.genres[genre_name].append(text_obj.title)
                            self.practice_texts[genre_name][text_obj.title] = text_obj
                    except Exception as e:
                        print(f"Error loading practice text {text_file}: {e}")
        
        # If no texts were loaded, use our sample dictionary
        if not self.genres:
            for genre, texts in SAMPLE_GENRES.items():
                self.genres[genre] = list(texts.keys())
                self.practice_texts[genre] = {}
                
                for title, content in texts.items():
                    text_obj = PracticeText(title, content, genre)
                    self.practice_texts[genre][title] = text_obj
    
    def setup_selection_ui(self):
        """Set up the text selection UI."""
        self.clear_screen()
        
        # Main frame
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame, style="TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = create_label(header_frame, "Practice Mode", font_size=24, weight="bold")
        title_label.pack(side=tk.LEFT)
        
        # Back button
        back_button = create_button(
            header_frame,
            text="Back to Menu",
            command=self.back_click,
            style="SecondaryButton.TButton"
        )
        back_button.pack(side=tk.RIGHT)
        
        # Create a two-column layout
        content_frame = ttk.Frame(main_frame, style="TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column - genre selection
        left_frame = create_frame(content_frame, padding=15, bg_color=COLORS["card_background"])
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), expand=False)
        
        genre_label = create_label(left_frame, "Select Genre", font_size=18, weight="bold")
        genre_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Create a scrollable frame for genres
        genre_canvas = tk.Canvas(
            left_frame,
            bg=COLORS["card_background"],
            highlightthickness=0,
            width=200
        )
        genre_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        genre_scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=genre_canvas.yview)
        genre_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        genre_canvas.configure(yscrollcommand=genre_scrollbar.set)
        genre_canvas.bind('<Configure>', lambda e: genre_canvas.configure(scrollregion=genre_canvas.bbox("all")))
        
        genre_frame = ttk.Frame(genre_canvas, style="TFrame")
        genre_canvas.create_window((0, 0), window=genre_frame, anchor="nw")
        
        # Genre buttons
        self.genre_buttons = {}
        
        for genre_name in self.genres.keys():
            genre_btn = create_button(
                genre_frame,
                text=genre_name,
                command=lambda g=genre_name: self.select_genre(g),
                style="SecondaryButton.TButton",
                width=18
            )
            genre_btn.pack(fill=tk.X, pady=5)
            self.genre_buttons[genre_name] = genre_btn
        
        # Right column - text selection (initially empty)
        self.right_frame = create_frame(content_frame, padding=15, bg_color=COLORS["card_background"])
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        welcome_label = create_label(
            self.right_frame, 
            "Select a genre to view available texts", 
            font_size=16
        )
        welcome_label.pack(expand=True)
        
        # Select first genre by default if any exist
        if self.genres:
            first_genre = next(iter(self.genres.keys()))
            self.select_genre(first_genre)
    
    def select_genre(self, genre_name):
        """Handle genre selection."""
        # Update selected state
        self.selected_genre = genre_name
        
        # Update button styles
        for g, btn in self.genre_buttons.items():
            if g == genre_name:
                btn.configure(style="PrimaryButton.TButton")
            else:
                btn.configure(style="SecondaryButton.TButton")
        
        # Clear right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        
        # Add title
        title_label = create_label(self.right_frame, f"{genre_name} Texts", font_size=18, weight="bold")
        title_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Check if genre has texts
        if not self.genres.get(genre_name, []):
            empty_label = create_label(self.right_frame, "No texts available for this genre", font_size=14)
            empty_label.pack(expand=True)
            return
        
        # Create scrollable frame for texts
        texts_canvas = tk.Canvas(
            self.right_frame,
            bg=COLORS["card_background"],
            highlightthickness=0
        )
        texts_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        texts_scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=texts_canvas.yview)
        texts_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        texts_canvas.configure(yscrollcommand=texts_scrollbar.set)
        texts_canvas.bind('<Configure>', lambda e: texts_canvas.configure(scrollregion=texts_canvas.bbox("all")))
        
        texts_frame = ttk.Frame(texts_canvas, style="TFrame")
        texts_canvas.create_window((0, 0), window=texts_frame, anchor="nw")
        
        # Add texts
        for title in self.genres[genre_name]:
            text_obj = self.practice_texts[genre_name][title]
            
            # Create a card for each text
            text_card = create_frame(texts_frame, padding=10, bg_color=COLORS["card_background"], shadow=False, border=True)
            text_card.pack(fill=tk.X, pady=5, padx=5)
            
            card_content = ttk.Frame(text_card, style="TFrame")
            card_content.pack(fill=tk.X)
            
            # Title and metadata
            title_label = create_label(card_content, title, font_size=16, weight="bold")
            title_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
            
            difficulty_label = create_label(card_content, f"Difficulty: {text_obj.difficulty}", font_size=12)
            difficulty_label.grid(row=1, column=0, sticky="w")
            
            author_label = create_label(card_content, f"Author: {text_obj.author}", font_size=12)
            author_label.grid(row=2, column=0, sticky="w")
            
            word_count_label = create_label(card_content, f"Words: {text_obj.word_count}", font_size=12)
            word_count_label.grid(row=3, column=0, sticky="w")
            
            # Preview button
            preview_btn = create_button(
                card_content,
                text="Preview",
                command=lambda g=genre_name, t=title: self.preview_text(g, t),
                style="SecondaryButton.TButton"
            )
            preview_btn.grid(row=1, column=1, rowspan=2, padx=10)
            
            # Start button
            start_btn = create_button(
                card_content,
                text="Start",
                command=lambda g=genre_name, t=title: self.start_practice(g, t),
                style="PrimaryButton.TButton"
            )
            start_btn.grid(row=1, column=2, rowspan=2)
            
            # Configure grid layout
            card_content.columnconfigure(0, weight=1)
            card_content.columnconfigure((1, 2), weight=0)
    
    def preview_text(self, genre, title):
        """Show a preview of the selected text."""
        text_obj = self.practice_texts[genre][title]
        
        # Create a preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"Preview: {title}")
        preview_window.geometry("600x400")
        preview_window.transient(self.root)
        preview_window.grab_set()
        preview_window.configure(bg=COLORS["background"])
        
        # Center on parent
        x = self.root.winfo_x() + (self.root.winfo_width() - 600) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 400) // 2
        preview_window.geometry(f"+{x}+{y}")
        
        # Preview content
        main_frame = create_frame(preview_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = create_label(header_frame, title, font_size=18, weight="bold")
        title_label.pack(side=tk.LEFT)
        
        close_btn = create_button(
            header_frame,
            text="Close",
            command=preview_window.destroy,
            style="SecondaryButton.TButton"
        )
        close_btn.pack(side=tk.RIGHT)
        
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        genre_label = create_label(info_frame, f"Genre: {genre}", font_size=12)
        genre_label.pack(side=tk.LEFT, padx=(0, 20))
        
        author_label = create_label(info_frame, f"Author: {text_obj.author}", font_size=12)
        author_label.pack(side=tk.LEFT, padx=(0, 20))
        
        difficulty_label = create_label(info_frame, f"Difficulty: {text_obj.difficulty}", font_size=12)
        difficulty_label.pack(side=tk.LEFT)
        
        # Text preview
        preview_frame = create_frame(main_frame, padding=15, bg_color=COLORS["card_background"])
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        text_area = create_text_area(
            preview_frame,
            wrap="word",
            font_size=14,
            state=tk.NORMAL,
            background=COLORS["card_background"],
            foreground=COLORS["text"]
        )
        text_area.pack(fill=tk.BOTH, expand=True)
        text_area.insert(tk.END, text_obj.content)
        text_area.config(state=tk.DISABLED)
        
        # Start button
        start_btn = create_button(
            main_frame,
            text="Start Practice",
            command=lambda: [preview_window.destroy(), self.start_practice(genre, title)],
            style="PrimaryButton.TButton"
        )
        start_btn.pack(pady=(20, 0))
    
    def start_practice(self, genre, title):
        """Start the typing practice with the selected text."""
        self.selected_genre = genre
        self.selected_text = title
        text_obj = self.practice_texts[genre][title]
        
        # Clear the screen and show practice UI
        self.clear_screen()
        self.setup_practice_ui(text_obj)
    
    def setup_practice_ui(self, text_obj):
        """Set up the practice typing interface."""
        # Main container
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Top bar
        top_bar = ttk.Frame(main_frame, style="TFrame")
        top_bar.pack(fill=tk.X, pady=(0, 20))
        
        back_button = create_button(
            top_bar,
            text="Back to Selection",
            command=self.setup_selection_ui,
            style="SecondaryButton.TButton"
        )
        back_button.pack(side=tk.LEFT)
        
        # Practice info
        info_label = create_label(
            top_bar, 
            f"{text_obj.title} ({text_obj.genre}) - {text_obj.difficulty}", 
            font_size=16, 
            weight="bold"
        )
        info_label.pack(side=tk.LEFT, padx=20)
        
        # Timer display
        self.timer_label = create_label(top_bar, "Time: 0:00", font_size=14)
        self.timer_label.pack(side=tk.RIGHT)
        
        # Text area
        text_frame = create_frame(main_frame, padding=15, bg_color=COLORS["card_background"])
        text_frame.pack(fill=tk.X, pady=10)
        
        # Sample text display
        sample_label = create_label(text_frame, "Text:", font_size=14)
        sample_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.sample_display = create_text_area(
            text_frame,
            height=6, 
            wrap="word",
            state=tk.DISABLED,
            font_family=FONTS["monospace"],
            font_size=14,
            background=COLORS["card_background"],
            foreground=COLORS["text"]
        )
        self.sample_display.pack(fill=tk.X, pady=(0, 20))
        
        # Typing area
        typing_label = create_label(text_frame, "Type here:", font_size=14)
        typing_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.typing_entry = create_text_area(
            text_frame,
            height=6,
            wrap="word",
            font_family=FONTS["monospace"],
            font_size=14,
            background=COLORS["input_bg"],
            foreground=COLORS["text"]
        )
        self.typing_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Progress bar
        progress_frame = ttk.Frame(text_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_bar = create_progressbar(progress_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress_bar.pack(fill=tk.X)
        
        # Stats display
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.wpm_label = create_label(stats_frame, "WPM: 0", font_size=14)
        self.wpm_label.pack(side=tk.LEFT, padx=(0, 20))
            
        self.accuracy_label = create_label(stats_frame, "Accuracy: 100.0%", font_size=14)
        self.accuracy_label.pack(side=tk.LEFT)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        reset_button = create_button(
            button_frame,
            text="Reset",
            command=lambda: self.setup_practice_ui(text_obj),
            style="SecondaryButton.TButton"
        )
        reset_button.pack(side=tk.LEFT)
        
        finish_button = create_button(
            button_frame,
            text="Finish Practice",
            command=self.finish_practice,
            style="PrimaryButton.TButton"
        )
        finish_button.pack(side=tk.RIGHT)
        
        # Load sample text
        self.sample_display.config(state=tk.NORMAL)
        self.sample_display.delete(1.0, tk.END)
        self.sample_display.insert(tk.END, text_obj.content)
        self.sample_display.config(state=tk.DISABLED)
        self.sample_display.tag_config("correct", foreground=COLORS["success"])
        self.sample_display.tag_config("incorrect", foreground=COLORS["error"], background="#FFE0E0")
        self.sample_display.tag_config("current", background=COLORS["accent"] + "40")
        
        # Configure typing entry events
        self.typing_entry.bind("<KeyRelease>", self.check_typing)
        self.typing_entry.bind("<Key>", self.start_timer_on_first_key)
        self.typing_entry.focus_set()
        
        # Reset stats
        self.start_time = None
        self.timer_running = False
        self.elapsed_time = 0
        self.current_position = 0
        self.errors = 0
    
    def start_timer_on_first_key(self, event=None):
        """Start the timer when first key is pressed."""
        if not self.timer_running and event.keysym != "BackSpace":
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()
            # Remove this binding after first key
            self.typing_entry.unbind("<Key>")
    
    def update_timer(self):
        """Update the timer display."""
        if self.timer_running:
            self.elapsed_time = int(time.time() - self.start_time)
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            self.timer_label.config(text=f"Time: {minutes}:{seconds:02d}")
            self.root.after(1000, self.update_timer)
    
    def check_typing(self, event=None):
        """Check the user's typing progress."""
        text_obj = self.practice_texts[self.selected_genre][self.selected_text]
        typed_text = self.typing_entry.get(1.0, tk.END).strip()
        sample_text = text_obj.content
        
        # Play keypress sound if applicable
        if event and event.keysym != "BackSpace":
            self.sounds_manager.play_keypress()
        
        # Update highlighting
        self.highlight_text(typed_text, sample_text)
        
        # Calculate and update stats
        accuracy = self.calculate_accuracy(typed_text, sample_text)
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")
        
        # Calculate WPM
        if self.timer_running and time.time() - self.start_time > 0:
            minutes = (time.time() - self.start_time) / 60
            words = len(typed_text) / 5  # Standard: 5 characters = 1 word
            wpm = words / minutes if minutes > 0 else 0
            self.wpm_label.config(text=f"WPM: {wpm:.1f}")
        
        # Update progress bar
        progress = min(100, (len(typed_text) / len(sample_text)) * 100)
        self.progress_bar['value'] = progress
        
        # Check for completion
        if len(typed_text) >= len(sample_text):
            self.finish_practice()
    
    def highlight_text(self, typed_text, sample_text):
        """Highlight the sample text based on user input."""
        self.sample_display.config(state=tk.NORMAL)
        self.sample_display.delete(1.0, tk.END)
        
        # Count errors for this check
        current_errors = 0
        
        # Process each character
        for i in range(max(len(typed_text), len(sample_text))):
            if i < len(sample_text) and i < len(typed_text):
                # Both typed and sample text have this position
                if typed_text[i] == sample_text[i]:
                    # Correct character
                    self.sample_display.insert(tk.END, sample_text[i], "correct")
                else:
                    # Incorrect character
                    self.sample_display.insert(tk.END, sample_text[i], "incorrect")
                    current_errors += 1
                    # Play error sound if this is a new error
                    if i >= self.current_position:
                        self.sounds_manager.play_error()
            elif i < len(sample_text):
                # Only sample text has this position
                if i == len(typed_text):
                    # Current position - highlight as next character
                    self.sample_display.insert(tk.END, sample_text[i], "current")
                else:
                    # Remaining sample text
                    self.sample_display.insert(tk.END, sample_text[i])
            else:
                # Extra typed text - count as errors
                current_errors += 1
        
        # Update the errors count
        self.errors += max(0, current_errors - self.errors)
        
        # Update the current position
        self.current_position = len(typed_text)
        
        self.sample_display.config(state=tk.DISABLED)
    
    def calculate_accuracy(self, typed_text, sample_text):
        """Calculate typing accuracy percentage."""
        if not typed_text:
            return 100.0
            
        compare_len = min(len(typed_text), len(sample_text))
        total_chars = max(len(typed_text), len(sample_text))
        
        if total_chars == 0:
            return 100.0
            
        # Count matching characters
        correct_chars = sum(1 for i in range(compare_len) if typed_text[i] == sample_text[i])
        
        # Calculate accuracy percentage
        accuracy = (correct_chars / total_chars) * 100
        return accuracy
    
    def finish_practice(self):
        """Finish practice and show results."""
        # Stop timer
        self.timer_running = False
        
        # Get final text and calculate results
        text_obj = self.practice_texts[self.selected_genre][self.selected_text]
        typed_text = self.typing_entry.get(1.0, tk.END).strip()
        sample_text = text_obj.content
        
        accuracy = self.calculate_accuracy(typed_text, sample_text)
        
        # Calculate WPM
        minutes = max(0.01, self.elapsed_time / 60)
        words = len(typed_text) / 5  # Standard: 5 characters = 1 word
        wpm = words / minutes
        
        # Save stats to user data
        self.save_practice_stats(wpm, accuracy)
        
        # Show results screen
        self.show_practice_results(wpm, accuracy, text_obj)
    
    def save_practice_stats(self, wpm, accuracy):
        """Save practice statistics to user data."""
        # This would save the practice stats to the user profile
        # Update stats for the current user
        self.user_manager.update_user_stats(
            self.current_user,
            wpm=wpm,
            accuracy=accuracy,
            practice_type=f"genre_{self.selected_genre}",
            practice_title=self.selected_text
        )
    
    def show_practice_results(self, wpm, accuracy, text_obj):
        """Show practice results screen."""
        self.clear_screen()
        
        # Main container
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Results header
        header_label = create_label(main_frame, "Practice Results", font_size=28, weight="bold")
        header_label.pack(pady=(0, 30))
        
        # Text info
        text_info_frame = create_frame(main_frame, padding=15, bg_color=COLORS["card_background"])
        text_info_frame.pack(fill=tk.X, pady=(0, 20))
        
        text_title = create_label(text_info_frame, text_obj.title, font_size=18, weight="bold")
        text_title.pack(anchor=tk.W)
        
        genre_label = create_label(text_info_frame, f"Genre: {text_obj.genre}", font_size=14)
        genre_label.pack(anchor=tk.W, pady=5)
        
        # Results card
        results_frame = create_frame(main_frame, padding=30, bg_color=COLORS["card_background"])
        results_frame.pack(fill=tk.X, pady=20, padx=40)
        
        # Results grid
        results_grid = ttk.Frame(results_frame)
        results_grid.pack(fill=tk.X)
        
        # WPM display with level indicator
        wpm_frame = ttk.Frame(results_frame)
        wpm_frame.pack(fill=tk.X, pady=10)
        
        wpm_label = create_label(wpm_frame, "Typing Speed", font_size=16)
        wpm_label.pack(anchor=tk.W)
        
        # Get user level based on WPM
        from config import USER_LEVELS
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
        
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        time_value = create_label(time_frame, f"{minutes}:{seconds:02d}", font_size=24, weight="bold")
        time_value.pack(anchor=tk.W, pady=5)
        
        # Get user stats history for this text
        user_stats = self.user_manager.get_user_stats(self.current_user)
        text_history = user_stats.get("practice_history", {}).get(f"{self.selected_genre}_{self.selected_text}", [])
        
        if text_history:
            # Get best performance
            best_wpm = max([entry.get("wpm", 0) for entry in text_history])
            best_accuracy = max([entry.get("accuracy", 0) for entry in text_history])
            
            # Add improvement stats if this isn't the first attempt
            if len(text_history) > 1:
                improvement_frame = create_frame(results_frame, padding=10, bg_color=COLORS["card_background"], shadow=False, border=True)
                improvement_frame.pack(fill=tk.X, pady=10)
                
                previous_wpm = text_history[-2].get("wpm", 0)
                wpm_improvement = wpm - previous_wpm
                wpm_improve_text = f"+ {wpm_improvement:.1f}" if wpm_improvement > 0 else f"- {abs(wpm_improvement):.1f}"
                
                improvement_label = create_label(
                    improvement_frame, 
                    f"From previous attempt: {wpm_improve_text} WPM", 
                    font_size=14,
                    foreground=COLORS["success"] if wpm_improvement > 0 else COLORS["error"]
                )
                improvement_label.pack(anchor=tk.W)
                
                if wpm >= best_wpm:
                    new_record_label = create_label(
                        improvement_frame,
                        "🎉 New Personal Best! 🎉",
                        font_size=14,
                        weight="bold",
                        foreground=COLORS["success"]
                    )
                    new_record_label.pack(anchor=tk.W, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(30, 0))
        
        # Certificate button if they did well
        if wpm >= 40 and accuracy >= 95:
            certificate_button = create_button(
                button_frame,
                text="Generate Certificate",
                command=lambda: self.generate_certificate(text_obj, wpm, accuracy),
                style="PrimaryButton.TButton"
            )
            certificate_button.pack(side=tk.RIGHT, padx=5)
        
        retry_button = create_button(
            button_frame,
            text="Retry Text",
            command=lambda: self.start_practice(self.selected_genre, self.selected_text),
            style="PrimaryButton.TButton" if wpm < 40 or accuracy < 95 else "SecondaryButton.TButton"
        )
        retry_button.pack(side=tk.RIGHT, padx=5)
        
        choose_text_button = create_button(
            button_frame,
            text="Choose Another Text",
            command=self.setup_selection_ui,
            style="SecondaryButton.TButton"
        )
        choose_text_button.pack(side=tk.RIGHT, padx=5)
        
        menu_button = create_button(
            button_frame,
            text="Back to Menu",
            command=self.back_click,
            style="SecondaryButton.TButton"
        )
        menu_button.pack(side=tk.LEFT)
    
    def generate_certificate(self, text_obj, wpm, accuracy):
        """Generate a certificate of achievement."""
        from certificate_generator import CertificateGenerator
        
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
            command=lambda: [
                name_dialog.destroy(),
                self.create_certificate(name_var.get(), text_obj, wpm, accuracy)
            ],
            style="PrimaryButton.TButton"
        )
        generate_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key
        name_entry.bind("<Return>", lambda event: generate_btn.invoke())
    
    def create_certificate(self, full_name, text_obj, wpm, accuracy):
        """Create and save the certificate."""
        # Import here to avoid circular imports
        from certificate_generator import CertificateGenerator
        
        # Get the date
        from datetime import datetime
        today = datetime.now().strftime("%B %d, %Y")
        
        # Certificate data
        certificate_data = {
            "full_name": full_name,
            "wpm": f"{wpm:.1f}",
            "accuracy": f"{accuracy:.1f}%",
            "text_title": text_obj.title,
            "text_genre": text_obj.genre,
            "date": today,
            "level": self.get_level_for_wpm(wpm)
        }
        
        try:
            # Generate the certificate
            certificate_generator = CertificateGenerator()
            pdf_path = certificate_generator.generate_certificate(certificate_data)
            
            # Show success message
            messagebox = tk.messagebox.showinfo(
                "Certificate Generated",
                f"Your certificate has been saved to:\n{pdf_path}\n\nWould you like to open it now?",
                type=tk.messagebox.YESNO
            )
            
            if messagebox == tk.messagebox.YES:
                import os
                import platform
                import subprocess
                
                # Open the PDF with the default PDF viewer
                if platform.system() == 'Darwin':  # macOS
                    subprocess.run(['open', pdf_path])
                elif platform.system() == 'Windows':
                    os.startfile(pdf_path)
                else:  # Linux
                    subprocess.run(['xdg-open', pdf_path])
                    
        except Exception as e:
            tk.messagebox.showerror(
                "Certificate Error",
                f"There was an error generating the certificate:\n{str(e)}"
            )
    
    def get_level_for_wpm(self, wpm):
        """Get the skill level based on WPM."""
        from config import USER_LEVELS
        
        for level, info in USER_LEVELS.items():
            if info["min_wpm"] <= wpm <= info["max_wpm"]:
                return level
        
        return "Novice"  # Default level
    
    def back_click(self):
        """Handle back button click."""
        if self.on_back:
            self.on_back()
    
    def clear_screen(self):
        """Clear all widgets from the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()
