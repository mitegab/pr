from tkinter import ttk, PhotoImage, Text
import os
import tkinter as tk  # Import tkinter directly

from config import COLORS, ICON_PATH

def create_label(parent, text, font_size=12, style="TLabel", **kwargs):
    return ttk.Label(parent, text=text, font=("Helvetica", font_size), style=style, **kwargs)

def create_entry(parent, font_size=14, style="TEntry", show=None, **kwargs):
    return ttk.Entry(parent, font=("Helvetica", font_size), style=style, show=show, **kwargs)

def create_button(parent, text, command, style, icon_name=None, compound="left", **kwargs):
    image = load_icon(icon_name) if icon_name else None
    return ttk.Button(parent, text=text, command=command, style=style, image=image, compound=compound, **kwargs)

def create_combobox(parent, values, font_size=14, style="TCombobox", state="readonly", **kwargs):
    return ttk.Combobox(parent, values=values, font=("Helvetica", font_size), style=style, state=state, **kwargs)

def create_text_area(parent, height, font_size=14, wrap="word", state=tk.DISABLED, bd=0, highlightthickness=0, **kwargs):
    return Text(parent, height=height, wrap=wrap, state=state, font=("Courier New", font_size), bd=bd, highlightthickness=highlightthickness, **kwargs)

def create_progressbar(parent, **kwargs):
    return ttk.Progressbar(parent, style="TProgressbar", **kwargs)

def create_frame(parent, style="CenterFrame.TFrame", **kwargs):
    return ttk.Frame(parent, style=style, **kwargs)

def load_icon(icon_name):
    """Load icons for the UI."""
    try:
        icon_file = os.path.join(ICON_PATH, icon_name)
        if os.path.exists(icon_file):
            return PhotoImage(file=icon_file).subsample(2, 2)
        else:
            print(f"Icon file not found: {icon_file}")
            return None
    except Exception as e:
        print(f"Error loading icon {icon_name}: {e}")
        return None