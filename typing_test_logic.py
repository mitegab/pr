"""Core typing test logic for the application."""

import random
import time

class TypingTestLogic:
    """Handles the core logic for typing tests."""
    
    def __init__(self, sample_texts):
        """Initialize with sample texts dictionary."""
        self.sample_texts = sample_texts
        self.current_difficulty = "Intermediate"  # Default difficulty
        self.sample_text = ""
        self.start_time = None
        self.end_time = None
        self.typed_text = ""
        self.reset()
        
    def reset(self):
        """Reset the typing test state."""
        self.start_time = None
        self.end_time = None
        self.typed_text = ""
        
    def start_test(self):
        """Start a new typing test."""
        self.reset()
        self.sample_text = self.get_sample_text()
        self.start_time = time.time()
        return self.sample_text
        
    def end_test(self):
        """End the typing test and return results."""
        self.end_time = time.time()
        elapsed_time = self.end_time - self.start_time
        
        results = self.calculate_results(self.typed_text, self.sample_text, elapsed_time)
        return results
        
    def update_typed_text(self, text):
        """Update the current typed text."""
        self.typed_text = text
        
        # If this is the first character typed, start the timer
        if len(text) == 1 and self.start_time is None:
            self.start_time = time.time()
            
        return self.calculate_current_results()
        
    def calculate_current_results(self):
        """Calculate current results based on typed text so far."""
        if not self.start_time:
            return {"wpm": 0, "accuracy": 0, "elapsed_time": 0}
            
        elapsed_time = time.time() - self.start_time
        
        return self.calculate_results(self.typed_text, self.sample_text, elapsed_time)
        
    def calculate_results(self, typed_text, sample_text, elapsed_time):
        """Calculate WPM, accuracy and other metrics."""
        # Calculate WPM
        minutes = elapsed_time / 60
        char_count = len(typed_text)
        wpm = (char_count / 5) / minutes if minutes > 0 else 0
        
        # Calculate accuracy
        accuracy = self.calculate_accuracy(typed_text, sample_text)
        
        # Collect detailed results
        results = {
            "wpm": wpm,
            "accuracy": accuracy,
            "elapsed_time": elapsed_time,
            "char_count": char_count,
            "error_count": self.count_errors(typed_text, sample_text)
        }
        
        return results
        
    def calculate_accuracy(self, typed_text, sample_text):
        """Calculate the accuracy percentage."""
        if not typed_text:
            return 100.0
            
        compare_len = min(len(typed_text), len(sample_text))
        total_chars = max(len(typed_text), len(sample_text))
        
        errors = sum(1 for i in range(compare_len) if typed_text[i] != sample_text[i])
        errors += abs(len(typed_text) - len(sample_text))  # Count extra or missing chars
        
        correct_chars = total_chars - errors
        accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 100
        
        return accuracy
        
    def count_errors(self, typed_text, sample_text):
        """Count the number of errors in the typed text."""
        if not typed_text:
            return 0
            
        compare_len = min(len(typed_text), len(sample_text))
        
        errors = sum(1 for i in range(compare_len) if typed_text[i] != sample_text[i])
        errors += abs(len(typed_text) - len(sample_text))  # Count extra or missing chars
        
        return errors
        
    def get_sample_text(self):
        """Get a sample text for the current difficulty."""
        if self.current_difficulty in self.sample_texts:
            return self.sample_texts[self.current_difficulty]
        else:
            # Fallback to a default text
            return "The quick brown fox jumps over the lazy dog."
            
    def set_difficulty(self, difficulty):
        """Set the difficulty level."""
        if difficulty in self.sample_texts:
            self.current_difficulty = difficulty
            
    def get_difficulties(self):
        """Get available difficulty levels."""
        return list(self.sample_texts.keys())
        
    def is_completed(self):
        """Check if the typing test is completed."""
        if not self.sample_text:
            return False
            
        return len(self.typed_text) >= len(self.sample_text)
