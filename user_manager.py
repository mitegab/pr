"""User management functionality."""

import os
import json
import hashlib
import uuid
from datetime import datetime
import tkinter.messagebox as messagebox

class UserManager:
    """Manages user accounts and data."""
    
    def __init__(self, user_data_file):
        """Initialize with the path to the user data file."""
        self.user_data_file = user_data_file
        self.current_user = None
        self.ensure_data_file_exists()
    
    def ensure_data_file_exists(self):
        """Create the user data file if it doesn't exist."""
        if not os.path.exists(self.user_data_file):
            os.makedirs(os.path.dirname(self.user_data_file), exist_ok=True)
            with open(self.user_data_file, 'w') as f:
                json.dump({
                    "users": {},
                    "version": "1.0"
                }, f, indent=4)
    
    def hash_password(self, password, salt=None):
        """Hash the password with a salt using SHA-256."""
        if not salt:
            salt = uuid.uuid4().hex
        
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return hashed, salt
    
    def create_account(self, username, password, confirm_password, on_success=None):
        """Create a new user account."""
        # Validate inputs
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return False
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return False
        
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters.")
            return False
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters.")
            return False
        
        # Check if the username already exists
        with open(self.user_data_file, 'r') as f:
            data = json.load(f)
        
        if username in data["users"]:
            messagebox.showerror("Error", "Username already exists.")
            return False
        
        # Hash the password with a salt
        hashed_password, salt = self.hash_password(password)
        
        # Create user account
        data["users"][username] = {
            "password_hash": hashed_password,
            "salt": salt,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "stats": {
                "total_tests": 0,
                "best_wpm": 0,
                "best_accuracy": 0,
                "average_wpm": 0,
                "average_accuracy": 0,
                "level": "Novice",
            },
            "settings": {
                "theme": "light",
                "font_size": 14,
                "show_timer": True,
                "sound_effects": True,
                "keyboard_layout": "QWERTY",
            }
        }
        
        # Save to file
        with open(self.user_data_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        messagebox.showinfo("Success", f"Account created for {username}!")
        
        if on_success:
            on_success()
        
        return True
    
    def login(self, username, password, on_success=None):
        """Log in a user."""
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return None
        
        # Check if the user exists
        if not os.path.exists(self.user_data_file):
            messagebox.showerror("Error", "No users found.")
            return None
        
        with open(self.user_data_file, 'r') as f:
            data = json.load(f)
        
        if username not in data["users"]:
            messagebox.showerror("Error", "Username not found.")
            return None
        
        # Verify password
        user_data = data["users"][username]
        hashed_password, _ = self.hash_password(password, user_data["salt"])
        
        if hashed_password != user_data["password_hash"]:
            messagebox.showerror("Error", "Incorrect password.")
            return None
        
        # Update last login
        data["users"][username]["last_login"] = datetime.now().isoformat()
        
        with open(self.user_data_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        self.current_user = username
        
        if on_success:
            on_success()
        
        return username
    
    def update_user_stats(self, username, wpm, accuracy):
        """Update user statistics with new test results."""
        if not username:
            return False
        
        with open(self.user_data_file, 'r') as f:
            data = json.load(f)
        
        if username not in data["users"]:
            return False
        
        user_stats = data["users"][username]["stats"]
        
        # Update total tests
        user_stats["total_tests"] += 1
        
        # Update best scores
        if wpm > user_stats["best_wpm"]:
            user_stats["best_wpm"] = wpm
        
        if accuracy > user_stats["best_accuracy"]:
            user_stats["best_accuracy"] = accuracy
        
        # Update averages
        user_stats["average_wpm"] = ((user_stats["average_wpm"] * (user_stats["total_tests"] - 1)) + wpm) / user_stats["total_tests"]
        user_stats["average_accuracy"] = ((user_stats["average_accuracy"] * (user_stats["total_tests"] - 1)) + accuracy) / user_stats["total_tests"]
        
        # Update level based on best WPM
        best_wpm = user_stats["best_wpm"]
        from config import USER_LEVELS
        for level, info in USER_LEVELS.items():
            if info["min_wpm"] <= best_wpm <= info["max_wpm"]:
                user_stats["level"] = level
                break
        
        # Save to file
        with open(self.user_data_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        return True
    
    def get_user_stats(self, username):
        """Get user statistics."""
        if not username:
            return None
        
        if not os.path.exists(self.user_data_file):
            return None
        
        with open(self.user_data_file, 'r') as f:
            data = json.load(f)
        
        if username not in data["users"]:
            return None
        
        return data["users"][username]["stats"]
    
    def get_user_settings(self, username):
        """Get user settings."""
        if not username:
            return None
        
        if not os.path.exists(self.user_data_file):
            return None
        
        with open(self.user_data_file, 'r') as f:
            data = json.load(f)
        
        if username not in data["users"]:
            return None
        
        return data["users"][username]["settings"]
    
    def update_user_settings(self, username, settings):
        """Update user settings."""
        if not username or not settings:
            return False
        
        with open(self.user_data_file, 'r') as f:
            data = json.load(f)
        
        if username not in data["users"]:
            return False
        
        # Update settings
        data["users"][username]["settings"].update(settings)
        
        # Save to file
        with open(self.user_data_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        return True
    
    def get_user_ranking(self, username):
        """Get the user's ranking among all users based on WPM."""
        if not username:
            return None
        
        if not os.path.exists(self.user_data_file):
            return None
        
        with open(self.user_data_file, 'r') as f:
            data = json.load(f)
        
        if username not in data["users"]:
            return None
        
        # Get all users' WPM
        users_wpm = []
        for user, user_data in data["users"].items():
            users_wpm.append((user, user_data["stats"]["best_wpm"]))
        
        # Sort by WPM (descending)
        users_wpm.sort(key=lambda x: x[1], reverse=True)
        
        # Find user's position
        for i, (user, _) in enumerate(users_wpm):
            if user == username:
                return {
                    "rank": i + 1,
                    "total_users": len(users_wpm),
                    "percentile": 100 - (i / len(users_wpm) * 100) if len(users_wpm) > 1 else 100
                }
        
        return None
    
    def logout(self):
        """Log out the current user."""
        self.current_user = None

    def load_user_settings(self, username):
        """Load user-specific settings from file."""
        try:
            if not os.path.exists(self.user_data_file):
                return {}
                
            with open(self.user_data_file, 'r') as f:
                data = json.load(f)
            
            if username in data.get("users", {}) and "settings" in data["users"][username]:
                return data["users"][username]["settings"]
            return {}
        except Exception as e:
            print(f"Error loading user settings: {e}")
            return {}