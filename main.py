"""Main entry point for the typing test application."""

import sys
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from app import TypingSpeedTestApp
from simplified_ui import setup_styles
from config import COLORS, FONTS

def check_requirements():
    """Check if all required packages are installed."""
    try:
        import reportlab
    except ImportError:
        print("Required package 'reportlab' is not installed.")
        print("Please install it using: pip install reportlab")
        return False
    
    return True

def setup_app_resources():
    """Set up application resources and directories."""
    # Create base resource directories
    from config import RESOURCES_DIR, ICON_PATH
    
    RESOURCES_DIR.mkdir(exist_ok=True)
    ICON_PATH.mkdir(exist_ok=True)
    
    # Create themes directory
    THEMES_DIR = RESOURCES_DIR / "themes"
    THEMES_DIR.mkdir(exist_ok=True)
    
    # Create an empty user_data.json file if it doesn't exist
    user_data_file = RESOURCES_DIR / "user_data.json"
    if not user_data_file.exists():
        with open(user_data_file, 'w') as f:
            f.write('{"users": {}, "settings": {"theme": "light", "font_scale": 1.0}}')

def setup_fonts():
    """Set up custom fonts."""
    # Try to find available fonts on the system that match our preferences
    available_fonts = []
    try:
        from tkinter import font
        available_fonts = list(font.families())
    except:
        pass
    
    # Define preferred fonts with fallbacks
    preferred_primary = ["Segoe UI", "Roboto", "San Francisco", "Helvetica Neue", "Helvetica", "Arial"]
    preferred_monospace = ["Consolas", "SF Mono", "Menlo", "Monaco", "Cascadia Code", "Courier New", "Courier"]
    
    # Find the first available preferred font
    for font_name in preferred_primary:
        if font_name in available_fonts:
            FONTS["primary"] = font_name
            break
    
    for font_name in preferred_monospace:
        if font_name in available_fonts:
            FONTS["monospace"] = font_name
            break

def save_window_state(root):
    """Save window position and size for restoration."""
    from config import RESOURCES_DIR
    import json
    
    window_state = {
        'width': root.winfo_width(),
        'height': root.winfo_height(),
        'x': root.winfo_x(),
        'y': root.winfo_y(),
        'state': str(root.state())
    }
    
    try:
        config_file = RESOURCES_DIR / "window_config.json"
        with open(config_file, 'w') as f:
            json.dump(window_state, f)
    except:
        pass  # Non-critical if saving fails

def restore_window_state(root):
    """Restore previous window position and size."""
    from config import RESOURCES_DIR
    import json
    
    try:
        config_file = RESOURCES_DIR / "window_config.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                window_state = json.load(f)
            
            # Get screen dimensions
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            
            # Ensure window is visible on screen
            x = min(max(0, window_state.get('x', 0)), screen_width - 800)
            y = min(max(0, window_state.get('y', 0)), screen_height - 600)
            
            # Set window geometry
            width = window_state.get('width', 800)
            height = window_state.get('height', 600)
            root.geometry(f"{width}x{height}+{x}+{y}")
            
            # Restore maximized state if needed
            if window_state.get('state') == 'zoomed':
                root.state('zoomed')
    except:
        # Default positioning at center of screen
        center_window(root, 800, 600)

def center_window(root, width, height):
    """Center window on screen."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def setup_keyboard_shortcuts(root, app):
    """Configure application keyboard shortcuts."""
    root.bind("<Control-q>", lambda e: root.quit())
    root.bind("<F11>", lambda e: toggle_fullscreen(root))
    root.bind("<Escape>", lambda e: exit_fullscreen(root) if root.attributes('-fullscreen') else None)
    # Add more shortcuts as needed for your app features

def toggle_fullscreen(root):
    """Toggle fullscreen mode."""
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))

def exit_fullscreen(root):
    """Exit fullscreen mode."""
    root.attributes('-fullscreen', False)

def show_splash_screen(root):
    """Display a splash screen while loading resources."""
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    
    # Make splash window size appropriate
    width, height = 400, 200
    center_window(splash, width, height)
    
    # Add content to splash screen
    splash.configure(bg=COLORS.get("bg_primary", COLORS.get("background", "#f0f0f0")))
    
    # App title
    title_label = tk.Label(splash, text="Typing Speed Test Pro", 
                          font=(FONTS["primary"], 18, "bold"),
                          bg=COLORS["bg_primary"], fg=COLORS.get("text", "#1D1D1F"))
    title_label.pack(pady=(50, 10))
    
    # Loading indicator
    progress = ttk.Progressbar(splash, mode="indeterminate", length=300)
    progress.pack(pady=20)
    progress.start()
    
    # Version info
    version_label = tk.Label(splash, text="Version 1.0", 
                            font=(FONTS["primary"], 10),
                            bg=COLORS["bg_primary"], fg=COLORS.get("muted_text", "#86868B"))
    version_label.pack(pady=10)
    
    # Force update to show splash immediately
    splash.update()
    
    return splash

def main():
    """Main entry point for the application."""
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Set up resources
    setup_app_resources()
    
    # Create the main window but hide it initially
    root = tk.Tk()
    root.withdraw()
    root.title("Typing Speed Test Pro")
    
    # Set minimum window size
    root.minsize(800, 600)
    
    # Show splash screen while loading
    splash = show_splash_screen(root)
    
    # Configure app theme
    setup_fonts()
    setup_styles()
    
    # Create and run the app
    app = TypingSpeedTestApp(root)
    
    # Set icon if available
    try:
        icon_path = Path(__file__).parent / "resources" / "icons" / "app_icon.png"
        if icon_path.exists():
            img = tk.PhotoImage(file=str(icon_path))
            root.iconphoto(True, img)
    except:
        pass  # Icon setting is not critical
    
    # Set up keyboard shortcuts
    setup_keyboard_shortcuts(root, app)
    
    # Restore previous window state
    restore_window_state(root)
    
    # Close splash and show main window
    root.after(1500, lambda: (splash.destroy(), root.deiconify()))
    
    # Set up window state saving on exit
    root.protocol("WM_DELETE_WINDOW", lambda: (save_window_state(root), root.destroy()))
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()