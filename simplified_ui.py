"""Simplified UI components for the Typing Speed Test application."""

import tkinter as tk
from tkinter import ttk
from config import COLORS, FONTS, UI_SETTINGS

def create_label(parent, text, font_size=12, **kwargs):
    """Create a styled label."""
    font_family = kwargs.pop("font_family", FONTS["primary"])
    weight = kwargs.pop("weight", "normal")
    foreground = kwargs.pop("foreground", COLORS["text"])
    
    label = tk.Label(
        parent,
        text=text,
        font=(font_family, font_size, weight),
        foreground=foreground,
        background=COLORS["background"],
        **kwargs
    )
    return label

def create_button(parent, text=None, command=None, **kwargs):
    """Create a styled button."""
    font_family = kwargs.pop("font_family", FONTS["primary"])
    font_size = kwargs.pop("font_size", 12)
    
    button = ttk.Button(
        parent,
        text=text,
        command=command,
        **kwargs
    )
    return button

def create_entry(parent, **kwargs):
    """Create a styled entry field."""
    font_family = kwargs.pop("font_family", FONTS["primary"])
    font_size = kwargs.pop("font_size", 12)
    show = kwargs.pop("show", None)
    
    entry = ttk.Entry(
        parent,
        font=(font_family, font_size),
        show=show,
        **kwargs
    )
    return entry

def create_text_area(parent, height=5, width=40, **kwargs):
    """Create a styled text area."""
    font_family = kwargs.pop("font_family", FONTS["monospace"])
    font_size = kwargs.pop("font_size", 14)
    
    text_area = tk.Text(
        parent,
        height=height,
        width=width,
        font=(font_family, font_size),
        padx=10,
        pady=10,
        wrap=kwargs.pop("wrap", "word"),
        **kwargs
    )
    return text_area

def create_frame(parent, **kwargs):
    """Create a styled frame."""
    padding = kwargs.pop("padding", 0)
    bg_color = kwargs.pop("bg_color", COLORS["card_background"])
    
    frame = ttk.Frame(
        parent,
        padding=padding,
        style="Card.TFrame",
        **kwargs
    )
    return frame

def create_progressbar(parent, **kwargs):
    """Create a styled progress bar."""
    length = kwargs.pop("length", 100)
    mode = kwargs.pop("mode", "determinate")
    orient = kwargs.pop("orient", tk.HORIZONTAL)
    
    progressbar = ttk.Progressbar(
        parent,
        orient=orient,
        length=length,
        mode=mode,
        **kwargs
    )
    return progressbar

def create_combobox(parent, values=None, **kwargs):
    """Create a styled combobox."""
    font_size = kwargs.pop("font_size", 12)
    
    combobox = ttk.Combobox(
        parent,
        values=values,
        font=(FONTS["primary"], font_size),
        **kwargs
    )
    return combobox

def configure_styles(root):
    """Configure application styles."""
    style = ttk.Style(root)
    
    # Configure basic styles
    style.configure("TLabel", background=COLORS["background"], foreground=COLORS["text"])
    style.configure("TButton", font=(FONTS["primary"], 12))
    style.configure("TEntry", fieldbackground=COLORS["input_bg"])
    style.configure("TCombobox", fieldbackground=COLORS["input_bg"])
    style.configure("TFrame", background=COLORS["background"])
    style.configure("Card.TFrame", background=COLORS["card_background"])
    style.configure("TProgressbar", background=COLORS["primary_button"], 
                   troughcolor=COLORS["progress_bg"])
                   
    # Define button styles
    style.configure("PrimaryButton.TButton", background=COLORS["primary_button"], 
                   foreground="white", font=(FONTS["primary"], 12, "bold"))
    style.map("PrimaryButton.TButton", 
             background=[("active", COLORS["highlight"]), ("disabled", COLORS["border"])])
    
    style.configure("SecondaryButton.TButton", background=COLORS["secondary_button"], 
                   foreground=COLORS["text"], font=(FONTS["primary"], 12))
    style.map("SecondaryButton.TButton", 
             background=[("active", COLORS["border"]), ("disabled", COLORS["border"])])
    
    return style
