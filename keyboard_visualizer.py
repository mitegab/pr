"""Virtual keyboard visualizer for touch typing lessons."""

import tkinter as tk
from config import COLORS, FONTS

class KeyboardVisualizer:
    """Displays a virtual keyboard with highlighted keys and finger indications."""
    
    def __init__(self, parent, width=800, height=260):
        """Initialize the keyboard visualizer."""
        self.parent = parent
        self.width = width
        self.height = height
        
        self.canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg=COLORS["background"],
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Standard keyboard layout
        self.layout = [
            # Row 1: Numbers
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
            # Row 2: QWERTY
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]"],
            # Row 3: Home row
            ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"],
            # Row 4: Bottom row
            ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]
        ]
        
        # Finger mapping (0=pinky, 1=ring, 2=middle, 3=index, 4=thumb)
        # Negative numbers indicate left hand, positive indicate right hand
        self.finger_map = {
            # Left hand
            "1": -0, "2": -1, "3": -2, "4": -3, "5": -3,
            "q": -0, "w": -1, "e": -2, "r": -3, "t": -3,
            "a": -0, "s": -1, "d": -2, "f": -3, "g": -3,
            "z": -0, "x": -1, "c": -2, "v": -3, "b": -3,
            
            # Right hand
            "6": 3, "7": 3, "8": 2, "9": 1, "0": 0, "-": 0, "=": 0,
            "y": 3, "u": 3, "i": 2, "o": 1, "p": 0, "[": 0, "]": 0,
            "h": 3, "j": 3, "k": 2, "l": 1, ";": 0, "'": 0,
            "n": 3, "m": 3, ",": 2, ".": 1, "/": 0,
            
            # Space bar
            " ": 4  # Thumb
        }
        
        # Finger colors
        self.finger_colors = {
            -0: "#FFB3BA",  # Left pinky
            -1: "#FFDFBA",  # Left ring
            -2: "#FFFFBA",  # Left middle
            -3: "#BAFFC9",  # Left index
            0: "#FFB3BA",   # Right pinky
            1: "#FFDFBA",   # Right ring
            2: "#FFFFBA",   # Right middle
            3: "#BAFFC9",   # Right index
            4: "#BAE1FF"    # Thumbs
        }
        
        self.keys = {}  # Dictionary to store key rectangles
        self.draw_keyboard()
    
    def draw_keyboard(self):
        """Draw the keyboard layout."""
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw keyboard background
        self.canvas.create_rectangle(
            10, 10, self.width-10, self.height-10,
            fill=COLORS["card_background"],
            outline=COLORS["border"],
            width=2,
            tags="keyboard_bg"
        )
        
        # Calculate key sizes
        key_width = 50
        key_height = 50
        key_spacing = 5
        
        # Starting position
        start_x = 30
        start_y = 30
        
        # Draw keys row by row
        for row_index, row in enumerate(self.layout):
            # Calculate offset for this row
            row_offset = row_index * 15
            
            for key_index, key in enumerate(row):
                # Calculate position
                x1 = start_x + (key_index * (key_width + key_spacing)) + row_offset
                y1 = start_y + (row_index * (key_height + key_spacing))
                x2 = x1 + key_width
                y2 = y1 + key_height
                
                # Get finger color
                finger = self.finger_map.get(key.lower(), 0)
                key_color = self.finger_colors.get(finger, COLORS["card_background"])
                
                # Draw key background
                key_rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=key_color,
                    outline=COLORS["border"],
                    width=1,
                    tags=f"key_{key}"
                )
                
                # Draw key label
                key_label = self.canvas.create_text(
                    (x1 + x2) / 2, (y1 + y2) / 2,
                    text=key.upper(),
                    font=(FONTS["primary"], 14, "bold"),
                    fill=COLORS["text"],
                    tags=f"label_{key}"
                )
                
                # Store key references
                self.keys[key.lower()] = {
                    "rect": key_rect,
                    "label": key_label,
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2
                }
        
        # Draw space bar
        space_y1 = start_y + (4 * (key_height + key_spacing))
        space_x1 = start_x + (2 * (key_width + key_spacing)) + (4 * 15)
        space_x2 = space_x1 + (key_width * 6)
        space_y2 = space_y1 + key_height
        
        space_rect = self.canvas.create_rectangle(
            space_x1, space_y1, space_x2, space_y2,
            fill=self.finger_colors[4],
            outline=COLORS["border"],
            width=1,
            tags="key_space"
        )
        
        space_label = self.canvas.create_text(
            (space_x1 + space_x2) / 2, (space_y1 + space_y2) / 2,
            text="SPACE",
            font=(FONTS["primary"], 14, "bold"),
            fill=COLORS["text"],
            tags="label_space"
        )
        
        # Store space bar reference
        self.keys[" "] = {
            "rect": space_rect,
            "label": space_label,
            "x1": space_x1, "y1": space_y1, "x2": space_x2, "y2": space_y2
        }
        
        # Draw hand and finger labels
        self.draw_finger_guide()
    
    def draw_finger_guide(self):
        """Draw a guide showing which finger to use for which key."""
        # Draw left hand
        left_x = 20
        left_y = self.height - 70
        
        self.canvas.create_text(
            left_x, left_y - 20,
            text="Left Hand",
            font=(FONTS["primary"], 12),
            fill=COLORS["text"],
            anchor="w"
        )
        
        for i, finger in enumerate(["Pinky", "Ring", "Middle", "Index", "Thumb"]):
            color = self.finger_colors[-(i if i < 4 else 4)]
            
            self.canvas.create_rectangle(
                left_x, left_y + (i * 20),
                left_x + 15, left_y + (i * 20) + 15,
                fill=color,
                outline=COLORS["border"]
            )
            
            self.canvas.create_text(
                left_x + 25, left_y + (i * 20) + 7,
                text=finger,
                font=(FONTS["primary"], 10),
                fill=COLORS["text"],
                anchor="w"
            )
        
        # Draw right hand
        right_x = self.width - 100
        right_y = self.height - 70
        
        self.canvas.create_text(
            right_x, right_y - 20,
            text="Right Hand",
            font=(FONTS["primary"], 12),
            fill=COLORS["text"],
            anchor="w"
        )
        
        for i, finger in enumerate(["Pinky", "Ring", "Middle", "Index", "Thumb"]):
            color = self.finger_colors[i if i < 4 else 4]
            
            self.canvas.create_rectangle(
                right_x, right_y + (i * 20),
                right_x + 15, right_y + (i * 20) + 15,
                fill=color,
                outline=COLORS["border"]
            )
            
            self.canvas.create_text(
                right_x + 25, right_y + (i * 20) + 7,
                text=finger,
                font=(FONTS["primary"], 10),
                fill=COLORS["text"],
                anchor="w"
            )
        
    def highlight_key(self, key):
        """Highlight a specific key on the keyboard."""
        key = key.lower()
        if key not in self.keys:
            return
            
        # Reset all keys to their original colors
        for k, key_info in self.keys.items():
            finger = self.finger_map.get(k, 0)
            key_color = self.finger_colors.get(finger, COLORS["card_background"])
            self.canvas.itemconfig(key_info["rect"], fill=key_color)
        
        # Highlight the pressed key
        self.canvas.itemconfig(self.keys[key]["rect"], fill=COLORS["highlight"])
        
        # Use after to schedule resetting the key
        self.canvas.after(200, lambda: self._reset_key(key))
    
    def _reset_key(self, key):
        """Reset key highlight after delay."""
        if key not in self.keys:
            return
            
        finger = self.finger_map.get(key, 0)
        key_color = self.finger_colors.get(finger, COLORS["card_background"])
        self.canvas.itemconfig(self.keys[key]["rect"], fill=key_color)
    
    def highlight_next_keys(self, keys):
        """Highlight the next keys the user should press."""
        # Reset all keys first
        for k, key_info in self.keys.items():
            finger = self.finger_map.get(k, 0)
            key_color = self.finger_colors.get(finger, COLORS["card_background"])
            self.canvas.itemconfig(key_info["rect"], fill=key_color)
        
        # Highlight the specified keys
        for key in keys:
            key = key.lower()
            if key in self.keys:
                self.canvas.itemconfig(self.keys[key]["rect"], fill=COLORS["success"] + "40")  # 40 = 25% opacity
