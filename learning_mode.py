"""Learning mode with structured typing lessons."""

import tkinter as tk
from tkinter import ttk
import time
from config import COLORS, FONTS
from simplified_ui import (
    create_label, create_button, create_frame, create_text_area, create_progressbar
)

class LearningMode:
    """Learning mode with structured typing lessons."""
    
    def __init__(self, root, user_manager, lesson_manager, sounds_manager, current_user,
                 on_back=None, on_complete=None):
        """Initialize learning mode."""
        self.root = root
        self.user_manager = user_manager
        self.lesson_manager = lesson_manager
        self.sounds_manager = sounds_manager
        self.current_user = current_user
        
        self.on_back = on_back
        self.on_complete = on_complete
        
        # State variables
        self.current_difficulty = None
        self.current_lesson = None
        self.current_exercise_index = 0
        self.start_time = None
        self.elapsed_time = 0
        self.timer_running = False
        self.errors = 0
        
        # Load lesson data and show selection screen
        self.setup_lesson_selection_ui()
    
    def setup_lesson_selection_ui(self):
        """Set up the lesson selection UI."""
        self.clear_screen()
        
        # Main container
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = create_label(header_frame, "Learning Mode", font_size=24, weight="bold")
        title_label.pack(side=tk.LEFT)
        
        back_button = create_button(
            header_frame,
            text="Back to Menu",
            command=self.back_click,
            style="SecondaryButton.TButton"
        )
        back_button.pack(side=tk.RIGHT)
        
        # Create two columns: lesson categories and lessons
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Get all lessons and user progress
        all_lessons = self.lesson_manager.get_lessons()
        user_progress = self.lesson_manager.get_user_progress(self.current_user)
        
        # Check if suggested lesson exists
        suggested_difficulty, suggested_lesson = self.lesson_manager.get_next_lesson(self.current_user)
        
        # Left column - Difficulty/categories
        left_frame = create_frame(content_frame, padding=15, bg_color=COLORS["card_background"])
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), expand=False, ipadx=10)
        
        category_label = create_label(left_frame, "Lesson Categories", font_size=18, weight="bold")
        category_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Difficulty buttons
        self.difficulty_buttons = {}
        
        for difficulty in all_lessons.keys():
            # Count completed lessons in this difficulty
            completed = 0
            total = len(all_lessons.get(difficulty, []))
            
            if difficulty in user_progress:
                for lesson_id, progress in user_progress[difficulty].items():
                    if progress.get("completed", False):
                        completed += 1
            
            # Create button with progress info
            btn_text = f"{difficulty.capitalize()} ({completed}/{total})"
            
            button = create_button(
                left_frame,
                text=btn_text,
                command=lambda d=difficulty: self.select_difficulty(d),
                style="SecondaryButton.TButton",
                width=20
            )
            button.pack(fill=tk.X, pady=5)
            self.difficulty_buttons[difficulty] = button
        
        # Create "fast track" button to go straight to suggested lesson
        if suggested_difficulty and suggested_lesson:
            spacer = ttk.Frame(left_frame, height=20)
            spacer.pack()
            
            suggested_button = create_button(
                left_frame,
                text=f"Continue Learning ►",
                command=lambda: self.start_lesson(suggested_difficulty, suggested_lesson["id"]),
                style="PrimaryButton.TButton"
            )
            suggested_button.pack(fill=tk.X, pady=10)
            
            suggestion_label = create_label(
                left_frame, 
                f"Next lesson: {suggested_lesson['title']}",
                font_size=10
            )
            suggestion_label.pack()
        
        # Right column - lesson list (initially empty)
        self.right_frame = create_frame(content_frame, padding=15, bg_color=COLORS["card_background"])
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        welcome_label = create_label(
            self.right_frame, 
            "Select a category to view available lessons", 
            font_size=16
        )
        welcome_label.pack(expand=True)
        
        # Select the suggested difficulty by default, if any
        if suggested_difficulty:
            self.select_difficulty(suggested_difficulty)
    
    def select_difficulty(self, difficulty):
        """Handle difficulty selection."""
        self.current_difficulty = difficulty
        
        # Update button styles
        for d, btn in self.difficulty_buttons.items():
            if d == difficulty:
                btn.configure(style="PrimaryButton.TButton")
            else:
                btn.configure(style="SecondaryButton.TButton")
        
        # Clear and repopulate the right frame with lessons
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        
        # Get lessons and user progress
        lessons = self.lesson_manager.get_lessons(difficulty)
        user_progress = self.lesson_manager.get_user_progress(self.current_user)
        
        # Add title
        title_label = create_label(
            self.right_frame, 
            f"{difficulty.capitalize()} Lessons", 
            font_size=18, 
            weight="bold"
        )
        title_label.pack(anchor=tk.W, pady=(0, 15))
        
        if not lessons.get(difficulty, []):
            empty_label = create_label(
                self.right_frame, 
                "No lessons available for this difficulty", 
                font_size=14
            )
            empty_label.pack(expand=True)
            return
        
        # Create a scrollable container for lessons
        canvas = tk.Canvas(
            self.right_frame,
            bg=COLORS["card_background"],
            highlightthickness=0
        )
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        lessons_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=lessons_frame, anchor="nw")
        
        # Sort lessons by order (if they have an order key)
        sorted_lessons = sorted(lessons.get(difficulty, []), key=lambda l: l.get("order", 0))
        
        # Add lesson cards
        for i, lesson in enumerate(sorted_lessons):
            lesson_id = lesson["id"]
            lesson_title = lesson["title"]
            lesson_desc = lesson.get("description", "")
            
            lesson_frame = create_frame(lessons_frame, padding=10, bg_color=COLORS["card_background"])
            lesson_frame.pack(fill=tk.X, pady=5)
            
            title_label = create_label(lesson_frame, lesson_title, font_size=16, weight="bold")
            title_label.pack(anchor=tk.W)
            
            desc_label = create_label(lesson_frame, lesson_desc, font_size=14)
            desc_label.pack(anchor=tk.W, pady=(5, 0))
            
            start_button = create_button(
                lesson_frame,
                text="Start Lesson",
                command=lambda d=difficulty, l=lesson_id: self.start_lesson(d, l),
                style="PrimaryButton.TButton"
            )
            start_button.pack(anchor=tk.E, pady=(10, 0))
    
    def start_lesson(self, difficulty, lesson_id):
        """Start a lesson."""
        self.current_difficulty = difficulty
        self.current_lesson = self.lesson_manager.get_lesson(difficulty, lesson_id)
        self.current_exercise_index = 0
        self.setup_lesson_ui()
    
    def setup_lesson_ui(self):
        """Set up the lesson UI."""
        self.clear_screen()
        
        # Main container
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = create_label(header_frame, self.current_lesson["title"], font_size=24, weight="bold")
        title_label.pack(side=tk.LEFT)
        
        back_button = create_button(
            header_frame,
            text="Back to Lessons",
            command=self.setup_lesson_selection_ui,
            style="SecondaryButton.TButton"
        )
        back_button.pack(side=tk.RIGHT)
        
        # Exercise area
        exercise_frame = create_frame(main_frame, padding=15, bg_color=COLORS["card_background"])
        exercise_frame.pack(fill=tk.BOTH, expand=True)
        
        # Exercise title
        exercise_title = create_label(
            exercise_frame,
            f"Exercise {self.current_exercise_index + 1}/{len(self.current_lesson['exercises'])}",
            font_size=18,
            weight="bold"
        )
        exercise_title.pack(anchor=tk.W, pady=(0, 15))
        
        # Sample text display
        self.sample_display = create_text_area(
            exercise_frame,
            height=3,
            wrap="word",
            state=tk.DISABLED,
            font_family=FONTS["monospace"],
            font_size=18,
            background=COLORS["card_background"],
            foreground=COLORS["text"]
        )
        self.sample_display.pack(fill=tk.X, pady=(0, 15))
        
        # Typing area
        typing_label = create_label(exercise_frame, "Your typing:", font_size=14)
        typing_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.typing_entry = create_text_area(
            exercise_frame,
            height=3,
            wrap="word",
            font_family=FONTS["monospace"],
            font_size=18,
            background=COLORS["input_bg"],
            foreground=COLORS["text"]
        )
        self.typing_entry.pack(fill=tk.X)
        
        # Progress bar
        progress_frame = ttk.Frame(exercise_frame)
        progress_frame.pack(fill=tk.X, pady=(15, 5))
        
        self.progress_label = create_label(progress_frame, "Exercise Progress", font_size=12)
        self.progress_label.pack(anchor=tk.W)
        
        self.progress_bar = create_progressbar(progress_frame)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Navigation buttons
        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.prev_button = create_button(
            nav_frame,
            text="Previous Exercise",
            command=self.prev_exercise,
            style="SecondaryButton.TButton"
        )
        self.prev_button.pack(side=tk.LEFT)
        
        self.next_button = create_button(
            nav_frame,
            text="Next Exercise",
            command=self.next_exercise,
            style="PrimaryButton.TButton"
        )
        self.next_button.pack(side=tk.RIGHT)
        
        # Bind events
        self.typing_entry.bind("<KeyRelease>", self.check_typing)
        self.typing_entry.bind("<Key>", self.on_key_press)
        
        # Load the first exercise
        self.load_current_exercise()
        
        # Set focus on typing entry
        self.typing_entry.focus_set()
    
    def load_current_exercise(self):
        """Load the current exercise text and reset stats."""
        if not self.current_lesson or not self.current_lesson['exercises']:
            return
        
        # Get current exercise text
        exercise_text = self.current_lesson['exercises'][self.current_exercise_index]
        
        # Reset stats
        self.start_time = None
        self.elapsed_time = 0
        self.timer_running = False
        self.errors = 0
        
        # Update exercise counter
        self.progress_label.config(
            text=f"Exercise {self.current_exercise_index + 1}/{len(self.current_lesson['exercises'])}"
        )
        
        # Update sample text
        self.sample_display.config(state=tk.NORMAL)
        self.sample_display.delete(1.0, tk.END)
        self.sample_display.insert(tk.END, exercise_text)
        self.sample_display.config(state=tk.DISABLED)
        
        # Clear typing entry
        self.typing_entry.delete(1.0, tk.END)
        
        # Reset progress bar
        self.progress_bar['value'] = 0
        
        # Update button states
        self.prev_button['state'] = 'disabled' if self.current_exercise_index == 0 else 'normal'
        self.next_button['state'] = 'disabled'
    
    def on_key_press(self, event):
        """Handle key press events."""
        if not self.timer_running and event.keysym != "BackSpace":
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()
    
    def check_typing(self, event=None):
        """Check the user's typing, update the UI."""
        typed_text = self.typing_entry.get(1.0, tk.END).strip()
        exercise_text = self.current_lesson['exercises'][self.current_exercise_index]
        
        # Highlight text
        self.highlight_text(typed_text, exercise_text)
        
        # Calculate progress
        progress = min(100, (len(typed_text) / len(exercise_text)) * 100)
        self.progress_bar['value'] = progress
        
        # Calculate accuracy and WPM
        current_accuracy = self.calculate_accuracy(typed_text, exercise_text)
        
        if self.timer_running and time.time() - self.start_time > 0:
            minutes = (time.time() - self.start_time) / 60
            words = len(typed_text) / 5  # Standard: 5 characters = 1 word
            wpm = words / minutes if minutes > 0 else 0
        
        # Check if exercise is complete
        if len(typed_text) >= len(exercise_text):
            self.exercise_complete()
    
    def highlight_text(self, typed_text, exercise_text):
        """Highlight the current position and mark correct/incorrect characters."""
        # Clear previous tags
        self.sample_display.tag_remove("current", "1.0", "end")
        self.sample_display.tag_remove("correct", "1.0", "end")
        self.sample_display.tag_remove("incorrect", "1.0", "end")
        
        # Use a hardcoded lighter version of the accent color
        light_accent = "#A0CFFF"  # A lighter version of the blue accent
        self.sample_display.tag_config("current", background=COLORS.get("light_accent", "#a0cfff"))
        
        # Configure other tags
        self.sample_display.tag_config("correct", foreground=COLORS["success"])
        self.sample_display.tag_config("incorrect", foreground=COLORS["error"])
        
        # Continue with the rest of your method...
    
    def calculate_accuracy(self, typed_text, exercise_text):
        """Calculate typing accuracy percentage."""
        if not typed_text:
            return 100.0
            
        compare_len = min(len(typed_text), len(exercise_text))
        total_chars = max(len(typed_text), len(exercise_text))
        
        if total_chars == 0:
            return 100.0
            
        # Count matching characters
        correct_chars = sum(1 for i in range(compare_len) if typed_text[i] == exercise_text[i])
        
        # Calculate accuracy percentage
        accuracy = (correct_chars / total_chars) * 100
        return accuracy
    
    def update_timer(self):
        """Update the timer display."""
        if self.timer_running:
            self.elapsed_time = int(time.time() - self.start_time)
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            self.root.after(1000, self.update_timer)
    
    def exercise_complete(self):
        """Handle completion of the current exercise."""
        self.timer_running = False
        
        # Enable the next button
        self.next_button['state'] = 'normal'
        
        # Calculate final stats
        typed_text = self.typing_entry.get(1.0, tk.END).strip()
        exercise_text = self.current_lesson['exercises'][self.current_exercise_index]
        accuracy = self.calculate_accuracy(typed_text, exercise_text)
        
        minutes = self.elapsed_time / 60
        words = len(exercise_text) / 5  # Standard: 5 characters = 1 word
        wpm = words / minutes if minutes > 0 else 0
        
        # Save progress for this exercise
        stats = {
            "wpm": wpm,
            "accuracy": accuracy,
            "elapsed_time": self.elapsed_time
        }
        self.lesson_manager.update_lesson_progress(
            self.current_user, 
            self.current_difficulty, 
            self.current_lesson['id'], 
            stats
        )
    
    def prev_exercise(self):
        """Navigate to the previous exercise."""
        if self.current_exercise_index > 0:
            self.current_exercise_index -= 1
            self.load_current_exercise()
    
    def next_exercise(self):
        """Navigate to the next exercise."""
        if self.current_exercise_index < len(self.current_lesson['exercises']) - 1:
            self.current_exercise_index += 1
            self.load_current_exercise()
        else:
            # Completed all exercises in this lesson
            self.show_lesson_complete()
    
    def show_lesson_complete(self):
        """Show the lesson completion screen."""
        self.clear_screen()
        
        # Main frame
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Success icon or animation could be added here
        
        # Completion message
        title_label = create_label(
            main_frame,
            "Lesson Complete!",
            font_size=28,
            weight="bold"
        )
        title_label.pack(pady=(50, 20))
        
        message_label = create_label(
            main_frame,
            f"Congratulations! You've completed the {self.current_lesson['title']} lesson.",
            font_size=16
        )
        message_label.pack(pady=10)
        
        # Get user progress for this lesson
        progress = self.lesson_manager.get_user_progress(self.current_user)
        lesson_data = progress.get(self.current_difficulty, {}).get(self.current_lesson['id'], {})
        
        # Create stats frame
        stats_frame = create_frame(main_frame, padding=15, bg_color=COLORS["card_background"])
        stats_frame.pack(fill=tk.X, pady=20, padx=50)
        
        stats_title = create_label(stats_frame, "Your Performance", font_size=18, weight="bold")
        stats_title.pack(pady=(0, 20))
        
        # Stats grid
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X)
        
        stats = [
            ("Best WPM", f"{lesson_data.get('best_wpm', 0):.1f}"),
            ("Best Accuracy", f"{lesson_data.get('best_accuracy', 0):.1f}%"),
            ("Attempts", str(lesson_data.get('attempts', 0)))
        ]
        
        for i, (label, value) in enumerate(stats):
            stat_label = create_label(stats_grid, label, font_size=14)
            stat_label.grid(row=i, column=0, sticky="e", padx=10, pady=5)
            
            value_label = create_label(stats_grid, value, font_size=14, weight="bold")
            value_label.grid(row=i, column=1, sticky="w", padx=10, pady=5)
        
        # Center the grid columns
        stats_grid.columnconfigure(0, weight=1)
        stats_grid.columnconfigure(1, weight=1)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(30, 0))
        
        next_lesson_button = create_button(
            button_frame,
            text="Next Lesson",
            command=self.load_next_lesson,
            style="PrimaryButton.TButton"
        )
        next_lesson_button.pack(side=tk.RIGHT, padx=5)
        
        retry_button = create_button(
            button_frame,
            text="Retry Lesson",
            command=self.retry_lesson,
            style="SecondaryButton.TButton"
        )
        retry_button.pack(side=tk.RIGHT, padx=5)
        
        menu_button = create_button(
            button_frame,
            text="Back to Menu",
            command=self.back_click,
            style="SecondaryButton.TButton"
        )
        menu_button.pack(side=tk.LEFT)
    
    def load_next_lesson(self):
        """Load the next available lesson."""
        level, lesson = self.lesson_manager.get_next_lesson(self.current_user)
        if level and lesson:
            self.current_difficulty = level
            self.current_lesson = lesson
            self.current_exercise_index = 0
            self.setup_lesson_ui()
        else:
            # All lessons completed
            self.show_all_complete_screen()
    
    def retry_lesson(self):
        """Retry the current lesson."""
        self.current_exercise_index = 0
        self.setup_lesson_ui()
    
    def show_all_complete_screen(self):
        """Show the screen when all lessons are completed."""
        self.clear_screen()
        
        # Main frame
        main_frame = create_frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Completion message
        title_label = create_label(
            main_frame,
            "All Lessons Complete!",
            font_size=28,
            weight="bold"
        )
        title_label.pack(pady=(50, 20))
        
        message_label = create_label(
            main_frame,
            "Congratulations! You've completed all available typing lessons.",
            font_size=16
        )
        message_label.pack(pady=10)
        
        # Suggestion for next steps
        suggestions_frame = create_frame(main_frame, padding=15, bg_color=COLORS["card_background"])
        suggestions_frame.pack(fill=tk.X, pady=20, padx=50)
        
        suggestions_title = create_label(suggestions_frame, "Next Steps", font_size=18, weight="bold")
        suggestions_title.pack(pady=(0, 20))
        
        suggestions = [
            "Continue practicing with the speed typing mode",
            "Challenge yourself with accuracy-focused tests",
            "Try typing real-world content to apply your skills",
            "Work on improving your personal best WPM score"
        ]
        
        for suggestion in suggestions:
            suggestion_label = create_label(suggestions_frame, "• " + suggestion, font_size=14)
            suggestion_label.pack(anchor=tk.W, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(30, 0))
        
        speed_test_button = create_button(
            button_frame,
            text="Speed Typing Mode",
            command=self.go_to_speed_typing,
            style="PrimaryButton.TButton"
        )
        speed_test_button.pack(side=tk.RIGHT, padx=5)
        
        menu_button = create_button(
            button_frame,
            text="Back to Menu",
            command=self.back_click,
            style="SecondaryButton.TButton"
        )
        menu_button.pack(side=tk.LEFT)
    
    def go_to_speed_typing(self):
        """Navigate to the speed typing mode."""
        if self.on_complete:
            self.on_complete("speed")
    
    def back_click(self):
        """Handle back button click."""
        if self.on_back:
            self.on_back()
    
    def clear_screen(self):
        """Clear all widgets from the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()