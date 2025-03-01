"""Entry point for the Typing Speed Test application."""

import tkinter as tk
import sys
import importlib.util

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

from app import TypingSpeedTestApp

def main():
    """Run the main application."""
    root = tk.Tk()
    root.title("Typing Speed Test Pro")
    
    # Set minimum window size
    root.minsize(800, 600)
    
    app = TypingSpeedTestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()