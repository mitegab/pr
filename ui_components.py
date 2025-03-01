"""UI components for the Typing Speed Test application."""

import tkinter as tk
from tkinter import ttk, font
import os
from pathlib import Path
import time
import threading

# Handle PIL/Pillow imports with error handling
try:
    from PIL import Image, ImageFilter, ImageEnhance
    # Try different ways to import ImageTk
    try:
        from PIL import ImageTk
    except ImportError:
        # Alternative import path sometimes needed
        import PIL._tkinter_finder
        from PIL import ImageTk
except ImportError:
    # Provide a fallback if PIL is not fully available
    Image = None
    ImageTk = None
    print("Warning: PIL image processing features are limited. Install pillow with: pip install pillow")

from config import COLORS, FONTS, UI_SETTINGS, ICON_PATH

# Cache for loaded icons
ICON_CACHE = {}

# Add rounded rectangle method to Canvas
tk.Canvas.create_rounded_rect = lambda self, x1, y1, x2, y2, radius, **kwargs: self.create_polygon(
    x1+radius, y1,
    x2-radius, y1,
    x2, y1,
    x2, y1+radius,
    x2, y2-radius,
    x2, y2,
    x2-radius, y2,
    x1+radius, y2,
    x1, y2,
    x1, y2-radius,
    x1, y1+radius,
    x1, y1,
    smooth=True,
    **kwargs
)

class AnimatedButton(ttk.Button):
    """Button with hover and click animations."""
    
    def __init__(self, parent, **kwargs):
        self.animated = kwargs.pop("animated", True)
        self.hover_color = kwargs.pop("hover_color", None)
        self.normal_bg = kwargs.get("style", "").split(".")[0]
        
        super().__init__(parent, **kwargs)
        
        if self.animated:
            self.bind("<Enter>", self._on_enter)
            self.bind("<Leave>", self._on_leave)
            self.bind("<ButtonPress-1>", self._on_press)
            self.bind("<ButtonRelease-1>", self._on_release)
    
    def _on_enter(self, event):
        """Mouse hover effect."""
        self.state(["hover"])
        self._animate_scale(1.05)
    
    def _on_leave(self, event):
        """Mouse leave effect."""
        self.state(["!hover"])
        self._animate_scale(1.0)
    
    def _on_press(self, event):
        """Mouse press effect."""
        self._animate_scale(0.95)
    
    def _on_release(self, event):
        """Mouse release effect."""
        self._animate_scale(1.05)
        
    def _animate_scale(self, target_scale):
        """Animate button scale."""
        self.config(scale=target_scale)

class ModernEntry(ttk.Entry):
    """Modern entry with placeholder and animations."""
    
    def __init__(self, parent, **kwargs):
        self.placeholder = kwargs.pop("placeholder", "")
        self.placeholder_color = kwargs.pop("placeholder_color", COLORS["muted_text"])
        self.normal_fg = kwargs.pop("foreground", COLORS["text"])
        
        super().__init__(parent, **kwargs)
        
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        
        self._is_placeholder = False
        self._show_placeholder()
    
    def _show_placeholder(self):
        """Show placeholder text if entry is empty."""
        if not self.get() and not self._is_placeholder:
            self._is_placeholder = True
            self.configure(foreground=self.placeholder_color)
            self.insert(0, self.placeholder)
    
    def _on_focus_in(self, event):
        """Handle focus in event."""
        if self._is_placeholder:
            self.delete(0, tk.END)
            self.configure(foreground=self.normal_fg)
            self._is_placeholder = False
    
    def _on_focus_out(self, event):
        """Handle focus out event."""
        self._show_placeholder()

class ModernTextArea(tk.Text):
    """Enhanced text area with modern styling."""
    
    def __init__(self, parent, **kwargs):
        self.placeholder = kwargs.pop("placeholder", "")
        self.placeholder_color = kwargs.pop("placeholder_color", COLORS["muted_text"])
        self.normal_fg = kwargs.pop("foreground", COLORS["text"])
        
        super().__init__(parent, **kwargs)
        
        # Make corners rounded
        self.configure(bd=0, highlightthickness=0)
        
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        
        self._is_placeholder = False
        self._show_placeholder()
        
        # Enable automatic scrolling
        self.bind("<KeyPress>", self._auto_scroll)
    
    def _show_placeholder(self):
        """Show placeholder text if text area is empty."""
        if not self.get("1.0", "end-1c") and not self._is_placeholder:
            self._is_placeholder = True
            self.configure(foreground=self.placeholder_color)
            self.insert("1.0", self.placeholder)
    
    def _on_focus_in(self, event):
        """Handle focus in event."""
        if self._is_placeholder:
            self.delete("1.0", tk.END)
            self.configure(foreground=self.normal_fg)
            self._is_placeholder = False
    
    def _on_focus_out(self, event):
        """Handle focus out event."""
        self._show_placeholder()
    
    def _auto_scroll(self, event):
        """Automatically scroll to keep cursor visible."""
        self.see(tk.INSERT)

class ModernProgressBar(ttk.Progressbar):
    """Enhanced progress bar with smooth animations."""
    
    def __init__(self, parent, **kwargs):
        self.animated = kwargs.pop("animated", True)
        self.animation_speed = kwargs.pop("animation_speed", UI_SETTINGS["animation_speed"])
        
        super().__init__(parent, **kwargs)
        
        self._target_value = 0
        self._animation_thread = None
    
    def set_value(self, value):
        """Set progress bar value with animation."""
        self._target_value = value
        
        if self.animated:
            if self._animation_thread and self._animation_thread.is_alive():
                return
            
            self._animation_thread = threading.Thread(target=self._animate_value)
            self._animation_thread.daemon = True
            self._animation_thread.start()
        else:
            self['value'] = value
    
    def _animate_value(self):
        """Animate progress bar value change."""
        current = self['value']
        target = self._target_value
        
        # Calculate number of steps for smooth animation
        steps = max(int(abs(target - current) / 2), 10)
        step_size = (target - current) / steps
        
        for i in range(steps):
            new_value = current + step_size * (i + 1)
            self['value'] = new_value
            time.sleep(self.animation_speed / steps)
        
        # Ensure final value is exact
        self['value'] = target

def load_icon(icon_name, size=(24, 24), color=None):
    """Load an icon with caching and color adjustment."""
    if not Image or not ImageTk or not icon_name or not isinstance(icon_name, str):
        return None
    
    # Check cache first
    cache_key = f"{icon_name}_{size[0]}x{size[1]}_{color}"
    if cache_key in ICON_CACHE:
        return ICON_CACHE[cache_key]
    
    icon_path = ICON_PATH / icon_name
    
    # Return None if icon doesn't exist
    if not icon_path.exists():
        return None
    
    try:
        with Image.open(icon_path) as img:
            # Resize image
            img = img.resize(size, Image.Resampling.LANCZOS)
            
            # Apply color if specified and image has alpha channel
            if color and img.mode == 'RGBA':
                # Create color mask while preserving transparency
                r, g, b = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
                data = img.getdata()
                new_data = []
                
                for pixel in data:
                    # Keep transparency but change color
                    if pixel[3] > 0:  # If not completely transparent
                        new_data.append((r, g, b, pixel[3]))
                    else:
                        new_data.append(pixel)
                
                img.putdata(new_data)
            
            # Convert to PhotoImage
            tk_image = ImageTk.PhotoImage(img)
            ICON_CACHE[cache_key] = tk_image
            return tk_image
    except Exception as e:
        print(f"Error loading icon {icon_name}: {e}")
        return None

# Helper functions for creating UI components
def create_label(parent, text, font_size=12, style="TLabel", **kwargs):
    """Create a professionally styled label."""
    font_family = kwargs.pop("font_family", FONTS["primary"])
    weight = kwargs.pop("weight", "normal")
    
    custom_font = (font_family, font_size, weight)
    label = ttk.Label(parent, text=text, style=style, font=custom_font, **kwargs)
    return label

def create_entry(parent, font_size=14, style="TEntry", **kwargs):
    """Create a professionally styled entry."""
    placeholder = kwargs.pop("placeholder", "")
    
    try:
        entry = ModernEntry(
            parent, 
            style=style,
            font=(FONTS["primary"], font_size),
            placeholder=placeholder,
            **kwargs
        )
    except:
        # Fallback to standard entry if ModernEntry fails
        entry = ttk.Entry(parent, style=style, font=(FONTS["primary"], font_size), **kwargs)
    
    return entry

def create_button(parent, text=None, command=None, style="PrimaryButton.TButton", **kwargs):
    """Create a professionally styled button."""
    icon_name = kwargs.pop("icon_name", None)
    icon_size = kwargs.pop("icon_size", (20, 20))
    icon_color = kwargs.pop("icon_color", None)
    compound = kwargs.pop("compound", "left")
    animated = kwargs.pop("animated", True)
    
    icon = None
    if icon_name:
        icon = load_icon(icon_name, size=icon_size, color=icon_color)
    
    try:
        button = AnimatedButton(
            parent, 
            text=text, 
            command=command, 
            style=style,
            image=icon if icon else None,
            compound=compound if icon else "center",
            animated=animated,
            **kwargs
        )
    except:
        # Fallback to standard button
        button = ttk.Button(
            parent,
            text=text,
            command=command,
            style=style,
            image=icon if icon else None,
            compound=compound if icon else "center",
            **kwargs
        )
    
    # Store icon reference to prevent garbage collection
    if icon:
        button._icon = icon
    
    return button

def create_combobox(parent, values=None, textvariable=None, **kwargs):
    """Create a professionally styled combobox."""
    font_family = kwargs.pop("font_family", FONTS["primary"])
    font_size = kwargs.pop("font_size", 14)
    
    combobox = ttk.Combobox(
        parent,
        values=values,
        textvariable=textvariable,
        font=(font_family, font_size),
        **kwargs
    )
    return combobox

def create_text_area(parent, height=5, width=40, **kwargs):
    """Create a professionally styled text area."""
    placeholder = kwargs.pop("placeholder", "")
    font_family = kwargs.pop("font_family", FONTS["monospace"])
    font_size = kwargs.pop("font_size", 14)
    
    text_area = ModernTextArea(
        parent,
        height=height,
        width=width,
        font=(font_family, font_size),
        padx=10,
        pady=10,
        wrap=kwargs.pop("wrap", "word"),
        placeholder=placeholder,
        **kwargs
    )
    return text_area

def create_progressbar(parent, orient=tk.HORIZONTAL, length=100, mode='determinate', **kwargs):
    """Create a professionally styled progress bar."""
    animated = kwargs.pop("animated", True)
    
    progressbar = ModernProgressBar(
        parent,
        orient=orient,
        length=length,
        mode=mode,
        animated=animated,
        **kwargs
    )
    return progressbar

def create_frame(parent, padding=None, **kwargs):
    """Create a professionally styled frame."""
    bg_color = kwargs.pop("bg_color", COLORS["card_background"])
    corner_radius = kwargs.pop("corner_radius", UI_SETTINGS["border_radius"])
    shadow = kwargs.pop("shadow", True)
    border = kwargs.pop("border", False)
    
    try:
        frame = ModernFrame(
            parent,
            padding=padding,
            bg_color=bg_color,
            corner_radius=corner_radius,
            shadow=shadow,
            border=border,
            **kwargs
        )
    except:
        # Fallback to standard frame
        frame = ttk.Frame(parent, padding=padding, **kwargs)
    
    return frame