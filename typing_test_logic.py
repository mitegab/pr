"""Logic for the typing test functionality."""

import time
import random
from datetime import datetime

class TypingTestLogic:
    """Logic for the typing test functionality."""
    
    def __init__(self, sample_texts):
        """Initialize with sample texts for different difficulties."""
        self.sample_texts = sample_texts
        self.current_difficulty = "Intermediate"  # Default difficulty
        self.sample_text = self.sample_texts[self.current_difficulty]
        self.start_time = None
        self.end_time = None
        self.elapsed_time = 0
        self.letter_stats = {}
        self.history = []
    
    def set_difficulty(self, difficulty):
        """Set the difficulty level and update sample text."""
        if difficulty in self.sample_texts:
            self.current_difficulty = difficulty
            self.start_test()
    
    def start_test(self):
        """Start a new typing test."""
        # Select a random sample text from the chosen difficulty level
        self.sample_text = self.sample_texts[self.current_difficulty]
        self.start_time = time.time()
        self.end_time = None
        self.elapsed_time = 0
        self.letter_stats = {letter: {"correct": 0, "incorrect": 0} for letter in "abcdefghijklmnopqrstuvwxyz"}
    
    def end_test(self):
        """End the typing test and record final time."""
        if self.start_time:
            self.end_time = time.time()
            self.elapsed_time = self.end_time - self.start_time
    
    def calculate_wpm(self, typed_text):
        """Calculate words per minute based on current typing."""
        if not self.start_time:
            return 0
        
        elapsed = time.time() - self.start_time
        if elapsed < 0.1:  # Avoid division by very small numbers
            elapsed = 0.1
        
        # Standard WPM calculation: 5 characters = 1 word
        word_count = len(typed_text) / 5
        minutes = elapsed / 60
        
        return word_count / minutes if minutes > 0 else 0
    
    def calculate_accuracy(self, typed_text):
        """Calculate accuracy percentage."""
        if not typed_text:
            return 100.0
        
        correct_chars = 0
        total_chars = min(len(typed_text), len(self.sample_text))
        
        for i in range(total_chars):
            if typed_text[i] == self.sample_text[i]:
                correct_chars += 1
                
                # Track letter-specific stats
                char = typed_text[i].lower()
                if char.isalpha():
                    self.letter_stats[char]["correct"] += 1
            else:
                # Track letter-specific stats
                char = self.sample_text[i].lower()
                if char.isalpha():
                    self.letter_stats[char]["incorrect"] += 1
        
        return (correct_chars / total_chars * 100) if total_chars > 0 else 100.0
    
    def calculate_speed_and_accuracy(self, typed_text):
        """Calculate final WPM and accuracy after test completion."""
        self.end_test()
        
        wpm = self.calculate_wpm(typed_text)
        accuracy = self.calculate_accuracy(typed_text)
        
        # Save this test result to history
        self.save_result(wpm, accuracy)
        
        return wpm, accuracy
    
    def save_result(self, wpm, accuracy):
        """Save test result to history."""
        result = {
            "timestamp": datetime.now().isoformat(),
            "difficulty": self.current_difficulty,
            "wpm": round(wpm, 2),
            "accuracy": round(accuracy, 2),
            "elapsed_time": round(self.elapsed_time, 2),
            "letter_stats": self.letter_stats
        }
        self.history.append(result)
        
        # Keep only the last 100 results
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        return result
    
    def get_weak_letters(self, limit=5):
        """Get the letters with lowest accuracy."""
        letter_accuracy = {}
        for letter, stats in self.letter_stats.items():
            total = stats["correct"] + stats["incorrect"]
            if total >= 3:  # Only consider letters with enough data
                accuracy = (stats["correct"] / total * 100) if total > 0 else 0
                letter_accuracy[letter] = accuracy
        
        # Sort by accuracy (ascending) and take the lowest 'limit' letters
        weak_letters = sorted(letter_accuracy.items(), key=lambda x: x[1])
        return weak_letters[:limit]
    
    def get_progress_summary(self):
        """Get a summary of progress over time."""
        if not self.history:
            return {"avg_wpm": 0, "avg_accuracy": 0, "trend": "stable"}
        
        recent = self.history[-min(10, len(self.history)):]
        
        avg_wpm = sum(r["wpm"] for r in recent) / len(recent)
        avg_accuracy = sum(r["accuracy"] for r in recent) / len(recent)
        
        # Calculate trend
        if len(recent) >= 2:
            first_wpm = recent[0]["wpm"]
            last_wpm = recent[-1]["wpm"]
            trend = "improving" if last_wpm > first_wpm else "declining" if last_wpm < first_wpm else "stable"
        else:
            trend = "stable"
        
        return {
            "avg_wpm": round(avg_wpm, 2),
            "avg_accuracy": round(avg_accuracy, 2),
            "trend": trend
        }
