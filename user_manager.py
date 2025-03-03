"""User management system for the typing test application."""

import os
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from config import USER_LEVELS

class UserManager:
    """Manages user accounts, progress, and statistics."""
    
    def __init__(self, data_file):
        """Initialize with path to user data file."""
        self.data_file = data_file
        self.current_user = None
        self.ensure_data_file_exists()
    
    def ensure_data_file_exists(self):
        """Create the data file if it doesn't exist."""
        if not os.path.exists(self.data_file):
            data_dir = os.path.dirname(self.data_file)
            os.makedirs(data_dir, exist_ok=True)
            self._save_data({"users": {}})
    
    def _save_data(self, data):
        """Save data to the JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def _load_data(self):
        """Load data from the JSON file."""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is empty or doesn't exist, return empty data
            return {"users": {}}
    
    def create_user(self, username, password):
        """Create a new user account."""
        if not username or not password:
            return False, "Username and password cannot be empty"
            
        data = self._load_data()
        
        if username in data["users"]:
            return False, "Username already exists"
        
        # Hash the password
        hashed_password = self._hash_password(password)
        
        # Create user
        data["users"][username] = {
            "password": hashed_password,
            "created": datetime.now().isoformat(),
            "settings": {
                "theme": "light",
                "sound_effects": True,
                "keyboard_layout": "QWERTY",
                "default_difficulty": "Intermediate"
            },
            "stats": {
                "best_wpm": 0,
                "best_accuracy": 0,
                "average_wpm": 0,
                "total_tests": 0,
                "total_time": 0,
                "total_characters": 0,
                "level": "Novice"
            },
            "lesson_progress": {}
        }
        
        self._save_data(data)
        return True, "User created successfully"
    
    def login(self, username, password):
        """Log in a user."""
        if not username or not password:
            return False, "Username and password cannot be empty"
            
        data = self._load_data()
        
        if username not in data["users"]:
            return False, "Username not found"
        
        hashed_password = self._hash_password(password)
        
        if data["users"][username]["password"] != hashed_password:
            return False, "Incorrect password"
        
        self.current_user = username
        return True, "Login successful"
    
    def logout(self):
        """Log out the current user."""
        self.current_user = None
    
    def is_logged_in(self):
        """Check if a user is logged in."""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get the current user's username."""
        return self.current_user
    
    def get_user_data(self, username):
        """Get all data for a user."""
        data = self._load_data()
        
        if username not in data["users"]:
            return None
            
        return data["users"][username]
    
    def save_user_data(self, username, user_data):
        """Save the user data."""
        data = self._load_data()
        
        if username not in data["users"]:
            return False
            
        data["users"][username] = user_data
        self._save_data(data)
        return True
    
    def get_user_settings(self, username):
        """Get user settings."""
        user_data = self.get_user_data(username)
        
        if not user_data:
            return {}
            
        return user_data.get("settings", {})
    
    def update_user_settings(self, username, settings):
        """Update user settings."""
        user_data = self.get_user_data(username)
        
        if not user_data:
            return False
            
        user_data["settings"] = settings
        return self.save_user_data(username, user_data)
    
    def get_user_stats(self, username):
        """Get user statistics."""
        user_data = self.get_user_data(username)
        
        if not user_data:
            return {}
            
        return user_data.get("stats", {})
    
    def update_user_stats(self, username, wpm=None, accuracy=None, test_type="standard", practice_type=None, practice_title=None):
        """Update user statistics with new test results."""
        user_data = self.get_user_data(username)
        
        if not user_data:
            return False
            
        # Get current stats
        stats = user_data.get("stats", {})
        
        # Update history
        history = stats.get("history", [])
        practice_history = stats.get("practice_history", {})
        
        # Create test entry
        test_entry = {
            "timestamp": datetime.now().isoformat(),
            "wpm": wpm,
            "accuracy": accuracy,
            "test_type": test_type
        }
        
        # Add to history
        history.append(test_entry)
        
        # Add to practice history if applicable
        if practice_type and practice_title:
            practice_key = f"{practice_type}_{practice_title}"
            if practice_key not in practice_history:
                practice_history[practice_key] = []
            
            practice_history[practice_key].append(test_entry)
        
        # Update best scores
        if wpm:
            stats["best_wpm"] = max(stats.get("best_wpm", 0), wpm)
            
            # Update accurate WPM (high accuracy and WPM)
            if accuracy and accuracy >= 95:
                stats["best_accurate_wpm"] = max(stats.get("best_accurate_wpm", 0), wpm)
        
        if accuracy:
            stats["best_accuracy"] = max(stats.get("best_accuracy", 0), accuracy)
        
        # Calculate average WPM
        if wpm:
            total_tests = stats.get("total_tests", 0) + 1
            current_avg_wpm = stats.get("average_wpm", 0)
            new_avg_wpm = ((current_avg_wpm * (total_tests - 1)) + wpm) / total_tests
            
            stats["average_wpm"] = new_avg_wpm
            stats["total_tests"] = total_tests
        
        # Update user level based on WPM
        if wpm:
            # Find the level based on WPM range
            current_level = stats.get("level", "Novice")
            new_level = current_level
            
            for level, level_data in USER_LEVELS.items():
                if level_data["min_wpm"] <= wpm <= level_data["max_wpm"]:
                    new_level = level
                    break
                    
            # Only update if the new level is better than the current one
            level_ranks = list(USER_LEVELS.keys())
            if level_ranks.index(new_level) > level_ranks.index(current_level):
                stats["level"] = new_level
                
        # Save updated stats
        stats["history"] = history[-100:]  # Keep only last 100 entries
        stats["practice_history"] = practice_history
        user_data["stats"] = stats
        
        return self.save_user_data(username, user_data)
    
    def get_user_ranking(self, username):
        """Get user's ranking among all users."""
        data = self._load_data()
        users = data.get("users", {})
        
        if username not in users:
            return None
            
        # Get all users with stats
        user_stats = []
        for user, user_data in users.items():
            best_wpm = user_data.get("stats", {}).get("best_wpm", 0)
            user_stats.append((user, best_wpm))
        
        # Sort users by WPM (descending)
        user_stats.sort(key=lambda x: x[1], reverse=True)
        
        # Find the current user's position
        user_position = next((i for i, (user, _) in enumerate(user_stats) if user == username), -1)
        
        if user_position == -1:
            return None
            
        # Calculate rank and percentile
        rank = user_position + 1  # 1-based ranking
        percentile = ((len(user_stats) - rank) / len(user_stats)) * 100
        
        return {
            "rank": rank,
            "total_users": len(user_stats),
            "percentile": percentile
        }
    
    def _hash_password(self, password):
        """Hash the password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()