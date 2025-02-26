# typing_test_logic.py
import time
from tkinter import messagebox

class TypingTestLogic:
    def __init__(self, sample_texts):
        self.sample_texts = sample_texts
        self.current_difficulty = "Beginner"
        self.sample_text = self.sample_texts[self.current_difficulty]
        self.start_time = 0
        self.end_time = None

    def set_difficulty(self, difficulty):
        self.current_difficulty = difficulty
        self.sample_text = self.sample_texts[self.current_difficulty]

    def start_test(self):
        self.start_time = time.time()
        self.end_time = None

    def calculate_wpm(self, typed_text):
        """Calculate words per minute."""
        elapsed_time = time.time() - self.start_time
        if elapsed_time == 0:
            return 0
        words = len(typed_text.split()) / 5
        wpm = (words / elapsed_time) * 60
        return max(0, wpm)

    def calculate_accuracy(self, typed_text):
        """Calculate typing accuracy."""
        correct_chars = 0
        for i in range(min(len(typed_text), len(self.sample_text))):
            if typed_text[i] == self.sample_text[i]:
                correct_chars += 1
        total_chars = len(self.sample_text)
        if total_chars == 0:
            return 100.00
        accuracy = (correct_chars / total_chars) * 100
        return max(0.00, accuracy)

    def calculate_speed_and_accuracy(self, typed_text):
        """Final calculation and display of typing speed and accuracy after test completion."""
        time_taken = time.time() - self.start_time
        words = len(self.sample_text.split())
        wpm = (words / time_taken) * 60
        accuracy = self.calculate_accuracy(typed_text)
        return wpm, accuracy
