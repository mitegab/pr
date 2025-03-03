"""Configuration settings for Typing Speed Test application."""

import os
import json
from pathlib import Path

# Base directory for the project
BASE_DIR = Path(__file__).parent

# Resources directory
RESOURCES_DIR = BASE_DIR / "resources"
ICON_PATH = RESOURCES_DIR / "icons"

# Create directories if they don't exist
RESOURCES_DIR.mkdir(exist_ok=True)
ICON_PATH.mkdir(exist_ok=True)

# User data file
USER_DATA_FILE = RESOURCES_DIR / "user_data.json"

# Color themes
THEMES = {
    "light": {
        "background": "#FFFFFF",
        "card_background": "#F5F5F7",
        "text": "#1D1D1F",
        "primary_button": "#0071E3",
        "secondary_button": "#E3E3E8",
        "highlight": "#42A5F5",
        "accent": "#31A8FF",
        "success": "#34C759",
        "error": "#FF3B30",
        "warning": "#FF9500",
        "border": "#D1D1D6",
        "input_bg": "#F5F5F7",
        "shadow": "#00000015",
        "muted_text": "#86868B",
        "progress_bg": "#E3E3E8",
        "graph_1": "#0071E3",
        "graph_2": "#5E5CE6",
        "graph_3": "#FF9500",
        "light_accent": "#A0CFFF"
    },
    "dark": {
        "background": "#1D1D1F",
        "card_background": "#2C2C2E",
        "text": "#F5F5F7",
        "primary_button": "#0A84FF",
        "secondary_button": "#3A3A3C",
        "highlight": "#42A5F5",
        "accent": "#0A84FF",
        "success": "#32D74B",
        "error": "#FF453A",
        "warning": "#FF9F0A",
        "border": "#3A3A3C",
        "input_bg": "#2C2C2E",
        "shadow": "#00000050",
        "muted_text": "#98989D",
        "progress_bg": "#3A3A3C",
        "graph_1": "#0A84FF",
        "graph_2": "#5E5CE6",
        "graph_3": "#FF9F0A",
        "light_accent": "#7ABBFF"
    }
}

# Default theme
DEFAULT_THEME = "light"
COLORS = THEMES[DEFAULT_THEME]

# Add this to your COLORS dictionary in config.py
COLORS["bg_primary"] = "#f0f0f0"  # Or whatever color you prefer

# Font settings
FONTS = {
    "primary": "SF Pro Display",  # Modern font used by many Silicon Valley companies
    "monospace": "SF Mono",       # For typing test text
    "fallback": "Helvetica Neue"  # Fallback font
}

# UI Settings
UI_SETTINGS = {
    "animation_speed": 0.3,  # seconds
    "border_radius": 12,     # pixels
    "padding": 20,           # pixels
    "shadow_depth": 4        # pixels
}

# Sample texts for different difficulty levels
SAMPLE_TEXTS = {
    "Beginner": "The quick brown fox jumps over the lazy dog. Simple sentences like this one are perfect for beginners who are just getting started with typing practice.",
    "Intermediate": "Programming is the process of creating a set of instructions that tell a computer how to perform a task. Programming can be done using many programming languages, such as Python, Java, and C++.",
    "Advanced": "The efficiency of algorithms and data structures is essential in computational theory. When developing software, one must consider both time complexity and space complexity to ensure optimal performance across various operational scenarios.",
    "Expert": "In quantum computing, qubits can exist in a superposition of states, enabling quantum algorithms to perform certain computations exponentially faster than classical algorithms. This advantage is especially notable in areas such as integer factorization using Shor's algorithm and database searching using Grover's algorithm."
}

# User achievement levels
USER_LEVELS = {
    "Novice": {"min_wpm": 0, "max_wpm": 30, "color": "#6C757D"},
    "Intermediate": {"min_wpm": 31, "max_wpm": 60, "color": "#17A2B8"},
    "Advanced": {"min_wpm": 61, "max_wpm": 90, "color": "#28A745"},
    "Expert": {"min_wpm": 91, "max_wpm": 120, "color": "#FFC107"},
    "Master": {"min_wpm": 121, "max_wpm": float('inf'), "color": "#DC3545"}
}

# Add this definition wherever your other path constants are defined
THEMES_DIR = RESOURCES_DIR / "themes"

def save_user_settings(username, settings):
    """Save user-specific settings to file."""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            data = json.load(f)
    else:
        data = {"users": {}}
    
    if username not in data["users"]:
        data["users"][username] = {}
    
    data["users"][username]["settings"] = settings
    
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_user_settings(username):
    """Load user-specific settings from file."""
    if not os.path.exists(USER_DATA_FILE):
        return {}
        
    with open(USER_DATA_FILE, 'r') as f:
        data = json.load(f)
    
    if username in data.get("users", {}) and "settings" in data["users"][username]:
        return data["users"][username]["settings"]
    return {}