"""Startup script for Typing Speed Test - checks dependencies and helps install them."""

import sys
import os
import subprocess
import importlib.util
import tkinter as tk
from tkinter import ttk, messagebox

def check_dependencies():
    """Check if all required dependencies are installed."""
    dependencies = {
        'tkinter': 'Usually comes with Python. On Linux: sudo apt-get install python3-tk',
        'PIL': 'pip install pillow',
        'matplotlib': 'pip install matplotlib',
        'numpy': 'pip install numpy',
        'pygame': 'pip install pygame',
    }
    
    missing = {}
    for module, install_cmd in dependencies.items():
        try:
            if module == 'tkinter':
                import tkinter
            else:
                importlib.import_module(module)
            print(f"✅ {module} is installed")
        except ImportError:
            missing[module] = install_cmd
            print(f"❌ {module} is missing")
    
    return missing

def install_dependencies(dependencies):
    """Install missing dependencies using pip."""
    for module, install_cmd in dependencies.items():
        if 'pip install' in install_cmd:
            package = install_cmd.split(' ')[-1]
            try:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ {package} installed successfully")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                return False
    return True

def show_gui(missing_deps):
    """Show a GUI to help install missing dependencies."""
    root = tk.Tk()
    root.title("Typing Speed Test - Setup")
    root.geometry("600x450")
    
    # Set a clean style
    style = ttk.Style(root)
    style.configure("TFrame", background="#f5f5f7")
    style.configure("TLabel", background="#f5f5f7", font=("Helvetica", 10))
    style.configure("TButton", font=("Helvetica", 10))
    style.configure("Header.TLabel", background="#f5f5f7", font=("Helvetica", 16, "bold"))
    style.configure("Subheader.TLabel", background="#f5f5f7", font=("Helvetica", 12))
    
    main_frame = ttk.Frame(root, padding=20, style="TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # App header
    ttk.Label(
        main_frame, 
        text="Typing Speed Test Pro - Setup", 
        style="Header.TLabel"
    ).pack(pady=(0, 20))
    
    if missing_deps:
        ttk.Label(
            main_frame,
            text="The following dependencies are missing:",
            style="Subheader.TLabel"
        ).pack(anchor="w", pady=(10, 5))
        
        # Create frame for dependencies list
        deps_frame = ttk.Frame(main_frame, style="TFrame")
        deps_frame.pack(fill=tk.X, pady=10, padx=10)
        
        for i, (module, cmd) in enumerate(missing_deps.items()):
            ttk.Label(
                deps_frame, text=f"{i+1}. {module}", 
                font=("Helvetica", 11, "bold"),
                style="TLabel"
            ).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            
            ttk.Label(
                deps_frame, text=f"Install with: {cmd}",
                style="TLabel"
            ).grid(row=i, column=1, sticky="w", padx=5, pady=5)
        
        # Status message area
        status_frame = ttk.Frame(main_frame, style="TFrame")
        status_frame.pack(fill=tk.X, pady=15)
        
        status_message = ttk.Label(
            status_frame, 
            text="Choose an option below:",
            style="TLabel"
        )
        status_message.pack(anchor="w", pady=5)
        
        def update_status(message, is_error=False):
            """Update the status message."""
            status_message.config(
                text=message,
                foreground="red" if is_error else "black"
            )
            root.update()
        
        # Install buttons
        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.pack(fill=tk.X, pady=10)
        
        def auto_install():
            """Automatically install missing dependencies."""
            update_status("Installing dependencies... Please wait.")
            
            success = install_dependencies(missing_deps)
            
            if success:
                update_status("Dependencies installed successfully!")
                messagebox.showinfo(
                    "Installation Complete", 
                    "All dependencies were installed successfully.\nYou can now launch the application."
                )
                root.destroy()
                launch_app()
            else:
                update_status("Failed to install some dependencies. Try manual installation.", True)
        
        def skip_installation():
            """Skip installation and continue with limited functionality."""
            if messagebox.askyesno(
                "Limited Functionality", 
                "Running without all dependencies will disable some features. Continue anyway?"
            ):
                root.destroy()
                launch_app()
        
        install_button = ttk.Button(
            button_frame,
            text="Install Dependencies Automatically",
            command=auto_install
        )
        install_button.pack(side=tk.LEFT, padx=10)
        
        skip_button = ttk.Button(
            button_frame,
            text="Continue with Limited Features",
            command=skip_installation
        )
        skip_button.pack(side=tk.LEFT)
        
        # Help text
        help_frame = ttk.Frame(main_frame, style="TFrame")
        help_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(
            help_frame, 
            text="Manual Installation Instructions:",
            font=("Helvetica", 11, "bold"),
            style="TLabel"
        ).pack(anchor="w")
        
        # Create a text widget for scrollable instructions
        help_text = tk.Text(
            help_frame, 
            height=6, 
            width=70, 
            wrap="word",
            font=("Helvetica", 10),
            background="#ffffff"
        )
        help_text.pack(fill=tk.X, pady=5)
        
        # Add instructions
        help_text.insert("1.0", "To manually install the dependencies:\n\n")
        help_text.insert("end", "1. Open a terminal or command prompt\n")
        help_text.insert("end", "2. Run the following commands:\n\n")
        
        for module, cmd in missing_deps.items():
            help_text.insert("end", f"   {cmd}\n")
        
        help_text.insert("end", "\n3. After installation, restart the application.")
        help_text.config(state="disabled")  # Make read-only
    else:
        # All dependencies are met
        ttk.Label(
            main_frame,
            text="All dependencies are installed! You're good to go.",
            style="Subheader.TLabel"
        ).pack(pady=20)
        
        continue_button = ttk.Button(
            main_frame,
            text="Launch Application",
            command=lambda: [root.destroy(), launch_app()]
        )
        continue_button.pack(pady=10)
    
    # Always include a quit button
    quit_button = ttk.Button(
        main_frame,
        text="Exit",
        command=root.destroy
    )
    quit_button.pack(side=tk.BOTTOM, pady=20)
    
    root.mainloop()

def launch_app():
    """Launch the main application."""
    try:
        from main import main
        main()
    except Exception as e:
        print(f"Error launching application: {e}")
        messagebox.showerror(
            "Launch Error", 
            f"Failed to launch the application: {e}\n\nPlease ensure all dependencies are correctly installed."
        )

if __name__ == "__main__":
    # Check if all dependencies are installed
    missing_dependencies = check_dependencies()
    
    # If running in terminal (non-GUI mode)
    if len(sys.argv) > 1 and sys.argv[1] == "--terminal":
        if missing_dependencies:
            print("\nMissing dependencies detected. Install them? (y/n)")
            choice = input("> ")
            if choice.lower().startswith("y"):
                install_dependencies(missing_dependencies)
            else:
                print("Continuing with limited functionality...")
        launch_app()
    else:
        # Show GUI for dependency installation
        show_gui(missing_dependencies)