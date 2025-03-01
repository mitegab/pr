"""
Launcher script for Typing Speed Test Pro

This script provides a convenient way to run the application:
1. First checks the required dependencies
2. Allows the user to install missing dependencies if needed
3. Launches the main application
"""

import sys
import os
from pathlib import Path

if __name__ == "__main__":
    # Ensure we're running from the correct directory
    script_path = Path(__file__).resolve()
    project_root = script_path.parent
    
    # Add project directory to path if needed
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        # Run the startup script to check dependencies
        from startup import check_dependencies, show_gui
        
        missing_deps = check_dependencies()
        
        # If no command-line args, show GUI for dependency management
        if len(sys.argv) == 1:
            show_gui(missing_deps)
        # Terminal mode with --terminal flag
        elif "--terminal" in sys.argv:
            from startup import launch_app
            if missing_deps:
                print("Warning: Missing some dependencies. Limited functionality will be available.")
            launch_app()
    except Exception as e:
        print(f"Error launching application: {e}")
        input("Press Enter to exit...")
