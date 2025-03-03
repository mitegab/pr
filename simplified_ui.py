"""Simplified UI components for Typing Speed Test application."""

import tkinter as tk
from tkinter import ttk
from config import COLORS, FONTS

def create_label(parent, text, font_size=12, weight="normal", foreground=None, background=None, anchor="center"):
    """Create a styled label."""
    font_family = FONTS.get("primary", "Helvetica")
    font_spec = (font_family, font_size, weight)
    
    label = ttk.Label(
        parent, 
        text=text, 
        font=font_spec,
        anchor=anchor
    )
    
    # Apply foreground color if provided
    if foreground:
        label.configure(foreground=foreground)
    
    # Apply background color if provided and support exists
    if background:
        try:
            label.configure(background=background)
        except:
            pass
    
    return label

def create_button(parent, text, command=None, width=None, style=None):
    """Create a styled button."""
    if not style:
        style = "PrimaryButton.TButton"
        
    button = ttk.Button(
        parent,
        text=text,
        command=command,
        style=style,
        width=width
    )
    return button

def create_frame(parent, padding=10, bg_color=None, shadow=False, border=False):
    """Create a styled frame."""
    frame = ttk.Frame(parent, padding=padding)
    
    # Apply background color if provided
    if bg_color:
        # Some themes don't allow changing background color for ttk frames
        # In that case, we fallback to tk frames
        try:
            style = ttk.Style()
            temp_style_name = f"Custom{bg_color.replace('#', '')}.TFrame"
            style.configure(temp_style_name, background=bg_color)
            frame.configure(style=temp_style_name)
        except:
            # Create a tk frame instead
            frame = tk.Frame(parent, bg=bg_color, padx=padding, pady=padding)
    
    # Apply shadow effect if requested
    if shadow:
        # In a real application, we'd implement a proper shadow effect
        # For now, we'll just add a border
        if isinstance(frame, ttk.Frame):
            frame.configure(style="Card.TFrame")
        else:
            frame.configure(highlightbackground=COLORS["shadow"], highlightthickness=2)
    
    # Apply border if requested
    if border:
        if isinstance(frame, ttk.Frame):
            frame.configure(style="CardBorder.TFrame")
        else:
            frame.configure(highlightbackground=COLORS["border"], highlightthickness=1)
    
    return frame

def create_entry(parent, textvariable=None, font_size=12, width=None):
    """Create a styled entry widget."""
    font_family = FONTS.get("primary", "Helvetica")
    font_spec = (font_family, font_size)
    
    entry = ttk.Entry(
        parent,
        textvariable=textvariable,
        font=font_spec,
        width=width
    )
    
    return entry

def create_text_area(parent, height=5, width=None, wrap="word", state="normal", 
                  font_family=None, font_size=12, background=None, foreground=None):
    """Create a styled text area."""
    if not font_family:
        font_family = FONTS.get("monospace", "Courier")
    
    font_spec = (font_family, font_size)
    
    text_area = tk.Text(
        parent,
        height=height,
        width=width,
        font=font_spec,
        wrap=wrap
    )
    
    # Set background color
    if background:
        text_area.configure(bg=background)
    else:
        text_area.configure(bg=COLORS.get("input_bg", "#FFFFFF"))
    
    # Set foreground color
    if foreground:
        text_area.configure(fg=foreground)
    else:
        text_area.configure(fg=COLORS.get("text", "#000000"))
    
    # Set state
    text_area.configure(state=state)
    
    return text_area

def create_progressbar(parent, orient=tk.HORIZONTAL, mode='determinate', length=None):
    """Create a styled progressbar."""
    progressbar = ttk.Progressbar(
        parent,
        orient=orient,
        mode=mode,
        length=length
    )
    
    return progressbar

def setup_styles():
    """Set up custom ttk styles."""
    style = ttk.Style()
    
    # Configure TFrame styles
    style.configure("TFrame", background=COLORS["background"])
    style.configure("Card.TFrame", background=COLORS["card_background"])
    style.configure("HoverCard.TFrame", background=COLORS["accent"] + "10")  # 10% opacity accent
    style.configure("CardBorder.TFrame", background=COLORS["card_background"])
    
    # Configure TButton styles
    style.configure(
        "PrimaryButton.TButton",
        background=COLORS["primary_button"],
        foreground="#FFFFFF",
        padding=(10, 5),
        font=(FONTS["primary"], 12)
    )
    
    style.configure(
        "SecondaryButton.TButton", 
        background=COLORS["secondary_button"],
        foreground=COLORS["text"],
        padding=(10, 5),
        font=(FONTS["primary"], 12)
    )
    
    # Configure TLabel style
    style.configure(
        "TLabel",
        background=COLORS["background"],
        foreground=COLORS["text"],
        font=(FONTS["primary"], 12)
    )
    
    # Configure TCheckbutton style
    style.configure(
        "Switch.TCheckbutton",
        background=COLORS["background"],
        foreground=COLORS["text"],
        font=(FONTS["primary"], 12)
    )
    
    # Configure TProgressbar style
    style.configure(
        "Horizontal.TProgressbar",
        troughcolor=COLORS["progress_bg"],
        background=COLORS["accent"]
    )
