"""Simple version of the Typing Speed Test application."""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from pathlib import Path

# Create necessary directories
BASE_DIR = Path(__file__).parent
RESOURCES_DIR = BASE_DIR / "resources"
RESOURCES_DIR.mkdir(exist_ok=True)

# Define basic colors
COLORS = {
    "background": "#FFFFFF",
    "card_background": "#F5F5F7",
    "text": "#1D1D1F",
    "primary_button": "#0071E3",
    "secondary_button": "#E3E3E8",
    "highlight": "#42A5F5",
    "accent": "#31A8FF",
    "success": "#34C759",
    "error": "#FF3B30",
    "border": "#D1D1D6",
    "input_bg": "#F5F5F7",
}

# Sample texts
SAMPLE_TEXTS = {
    "Easy": "The quick brown fox jumps over the lazy dog.",
    "Medium": "Programming is the process of creating instructions for computers to follow.",
    "Hard": "The efficiency of algorithms is analyzed in terms of time complexity and space complexity."
}

class SimpleTypingTest:
    """Simple typing test application."""
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("Simple Typing Speed Test")
        self.root.geometry("800x600")
        self.root.config(bg=COLORS["background"])
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background=COLORS["background"])
        self.style.configure("TLabel", background=COLORS["background"], foreground=COLORS["text"])
        self.style.configure("TButton", font=('Helvetica', 12))
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create the main application widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Typing Speed Test", font=('Helvetica', 24, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Difficulty selection
        diff_frame = ttk.Frame(main_frame)
        diff_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(diff_frame, text="Select Difficulty:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.difficulty_var = tk.StringVar(value="Medium")
        difficulty_cb = ttk.Combobox(diff_frame, textvariable=self.difficulty_var, values=list(SAMPLE_TEXTS.keys()))
        difficulty_cb.pack(side=tk.LEFT, fill=tk.X, expand=True)
        difficulty_cb.bind("<<ComboboxSelected>>", self.update_sample_text)
        
        # Sample text
        sample_frame = ttk.Frame(main_frame)
        sample_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(sample_frame, text="Sample Text:").pack(anchor=tk.W)
        
        self.sample_text = tk.Text(sample_frame, height=3, width=50, wrap=tk.WORD, font=('Courier', 12))
        self.sample_text.pack(fill=tk.X, pady=5)
        self.sample_text.insert(tk.END, SAMPLE_TEXTS[self.difficulty_var.get()])
        self.sample_text.config(state=tk.DISABLED)
        
        # Typing area
        typing_frame = ttk.Frame(main_frame)
        typing_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(typing_frame, text="Type Here:").pack(anchor=tk.W)
        
        self.typing_entry = tk.Text(typing_frame, height=5, width=50, wrap=tk.WORD, font=('Courier', 12))
        self.typing_entry.pack(fill=tk.X, pady=5)
        self.typing_entry.bind("<KeyRelease>", self.check_typing)
        
        # Stats frame
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.wpm_label = ttk.Label(stats_frame, text="WPM: 0")
        self.wpm_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.accuracy_label = ttk.Label(stats_frame, text="Accuracy: 0%")
        self.accuracy_label.pack(side=tk.LEFT)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_test)
        self.reset_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.finish_button = ttk.Button(button_frame, text="Finish", command=self.finish_test)
        self.finish_button.pack(side=tk.LEFT)
        
    def update_sample_text(self, event=None):
        """Update the sample text based on selected difficulty."""
        difficulty = self.difficulty_var.get()
        self.sample_text.config(state=tk.NORMAL)
        self.sample_text.delete(1.0, tk.END)
        self.sample_text.insert(tk.END, SAMPLE_TEXTS[difficulty])
        self.sample_text.config(state=tk.DISABLED)
        self.reset_test()
    
    def check_typing(self, event=None):
        """Check the user's typing progress."""
        typed_text = self.typing_entry.get(1.0, tk.END).strip()
        sample_text = SAMPLE_TEXTS[self.difficulty_var.get()]
        
        # Calculate accuracy
        min_len = min(len(typed_text), len(sample_text))
        correct_chars = sum(1 for i in range(min_len) if typed_text[i] == sample_text[i])
        accuracy = (correct_chars / max(1, len(sample_text))) * 100
        
        # Simple WPM calculation (not entirely accurate)
        wpm = len(typed_text) / 5  # Assuming 5 chars per word
        
        # Update stats
        self.wpm_label.config(text=f"WPM: {wpm:.1f}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")
    
    def reset_test(self):
        """Reset the typing test."""
        self.typing_entry.delete(1.0, tk.END)
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 0%")
    
    def finish_test(self):
        """Finish the typing test."""
        typed_text = self.typing_entry.get(1.0, tk.END).strip()
        sample_text = SAMPLE_TEXTS[self.difficulty_var.get()]
        
        # Calculate final stats
        min_len = min(len(typed_text), len(sample_text))
        correct_chars = sum(1 for i in range(min_len) if typed_text[i] == sample_text[i])
        accuracy = (correct_chars / max(1, len(sample_text))) * 100
        wpm = len(typed_text) / 5  # Simple approximation
        
        # Show results
        messagebox.showinfo("Test Results", 
                            f"Words Per Minute: {wpm:.1f}\nAccuracy: {accuracy:.1f}%")
        self.reset_test()

def main():
    """Run the main application."""
    root = tk.Tk()
    app = SimpleTypingTest(root)
    root.mainloop()

if __name__ == "__main__":
    main()
