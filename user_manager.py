# user_manager.py
import json
import os
from tkinter import messagebox

class UserManager:
    def __init__(self, user_data_file):
        self.USER_DATA_FILE = user_data_file
        self.users = self.load_user_data()

    def load_user_data(self):
        """Load user data from a JSON file."""
        if os.path.exists(self.USER_DATA_FILE):
            with open(self.USER_DATA_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_user_data(self):
        """Save user data to a JSON file."""
        with open(self.USER_DATA_FILE, "w") as file:
            json.dump(self.users, file)

    def create_account(self, username, password, confirm_password, show_login_screen):
        """Create a new account."""
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if username in self.users:
            messagebox.showerror("Error", "Username already exists!")
            return

        self.users[username] = password
        self.save_user_data()
        messagebox.showinfo("Success", "Account created successfully!")
        show_login_screen()

    def login(self, username, password, show_welcome_screen):
        """Log in the user."""
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required!")
            return

        if username not in self.users or self.users[username] != password:
            messagebox.showerror("Error", "Invalid username or password!")
            return

        return username