import tkinter as tk
from tkinter import messagebox, ttk
import time
import json
import os
from tkinter import PhotoImage

# config.py
COLORS = {
    "background": "#3B4252",
    "text": "#ECEFF4",
    "primary_button": "#8FBCBB",
    "secondary_button": "#5E81AC",
    "highlight": "#A3BE8C",
    "error": "#BF616A",
    "success": "#A3BE8C",
    "accent": "#D08770"
}
USER_DATA_FILE = "user_data.json"
SAMPLE_TEXTS = {
    "Beginner": "The quick brown fox jumps over the lazy dog.",
    "Intermediate": "Programming is a rewarding skill that allows you to create innovative solutions to complex problems.",
    "Advanced": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
}
ICON_PATH = "icons"