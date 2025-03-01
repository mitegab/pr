"""Login and account creation screens for the typing test application."""

import tkinter as tk
from tkinter import ttk, messagebox
from config import COLORS
from simplified_ui import (
    create_label, create_entry, create_button, create_frame
)

class LoginScreen:
    """Login screen with username and password fields."""
    
    def __init__(self, root, user_manager, on_login=None, on_create_account=None, 
                 on_back=None, mode="login"):
        """Initialize login screen."""
        self.root = root
        self.user_manager = user_manager
        self.on_login = on_login
        self.on_create_account = on_create_account
        self.on_back = on_back
        self.mode = mode  # "login" or "create"
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        if self.mode == "login":
            self.setup_login_ui()
        else:
            self.setup_create_account_ui()
    
    def setup_login_ui(self):
        """Set up login user interface."""
        # Create a centered frame for login content
        center_frame = create_frame(self.root, padding=20, bg_color=COLORS["card_background"])
        center_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=380)
        
        # App title
        title_label = create_label(center_frame, "Typing Speed Test Pro", font_size=24, weight="bold")
        title_label.pack(pady=(0, 30))
        
        # Username field
        username_frame = ttk.Frame(center_frame, style="TFrame")
        username_frame.pack(fill=tk.X, pady=10)
        
        username_label = create_label(username_frame, "Username", font_size=14)
        username_label.pack(anchor=tk.W)
        
        self.username_entry = create_entry(username_frame, font_size=14)
        self.username_entry.pack(fill=tk.X, pady=5)
        
        # Password field
        password_frame = ttk.Frame(center_frame, style="TFrame")
        password_frame.pack(fill=tk.X, pady=10)
        
        password_label = create_label(password_frame, "Password", font_size=14)
        password_label.pack(anchor=tk.W)
        
        self.password_entry = create_entry(password_frame, font_size=14, show="•")
        self.password_entry.pack(fill=tk.X, pady=5)
        
        # Login button
        login_button = create_button(
            center_frame,
            text="Login",
            command=self.login,
            style="PrimaryButton.TButton",
        )
        login_button.pack(fill=tk.X, pady=20)
        
        # Create account button
        create_account_button = create_button(
            center_frame,
            text="Create Account",
            command=self.create_account_click,
            style="SecondaryButton.TButton",
        )
        create_account_button.pack(fill=tk.X)
        
        # Bind Enter key to login
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda event: self.login())
        
        # Focus username entry
        self.username_entry.focus()
    
    def setup_create_account_ui(self):
        """Set up account creation user interface."""
        # Create a centered frame for account creation content
        center_frame = create_frame(self.root, padding=20, bg_color=COLORS["card_background"])
        center_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450)
        
        # App title
        title_label = create_label(center_frame, "Create Account", font_size=24, weight="bold")
        title_label.pack(pady=(0, 30))
        
        # Username field
        username_frame = ttk.Frame(center_frame, style="TFrame")
        username_frame.pack(fill=tk.X, pady=10)
        
        username_label = create_label(username_frame, "Username", font_size=14)
        username_label.pack(anchor=tk.W)
        
        self.new_username_entry = create_entry(username_frame, font_size=14)
        self.new_username_entry.pack(fill=tk.X, pady=5)
        
        # Password field
        password_frame = ttk.Frame(center_frame, style="TFrame")
        password_frame.pack(fill=tk.X, pady=10)
        
        password_label = create_label(password_frame, "Password", font_size=14)
        password_label.pack(anchor=tk.W)
        
        self.new_password_entry = create_entry(password_frame, font_size=14, show="•")
        self.new_password_entry.pack(fill=tk.X, pady=5)
        
        # Confirm password field
        confirm_password_frame = ttk.Frame(center_frame, style="TFrame")
        confirm_password_frame.pack(fill=tk.X, pady=10)
        
        confirm_label = create_label(confirm_password_frame, "Confirm Password", font_size=14)
        confirm_label.pack(anchor=tk.W)
        
        self.confirm_password_entry = create_entry(confirm_password_frame, font_size=14, show="•")
        self.confirm_password_entry.pack(fill=tk.X, pady=5)
        
        # Create account button
        create_account_button = create_button(
            center_frame,
            text="Create Account",
            command=self.create_account,
            style="PrimaryButton.TButton",
        )
        create_account_button.pack(fill=tk.X, pady=20)
        
        # Back button
        back_button = create_button(
            center_frame,
            text="Back to Login",
            command=self.back_to_login,
            style="SecondaryButton.TButton"
        )
        back_button.pack(fill=tk.X)
        
        # Focus username entry
        self.new_username_entry.focus()
    
    def login(self):
        """Handle login button click."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        success = self.user_manager.login(username, password)
        if success and self.on_login:
            self.on_login(username)
    
    def create_account_click(self):
        """Handle create account button click."""
        if self.on_create_account:
            self.on_create_account()
    
    def create_account(self):
        """Handle account creation."""
        username = self.new_username_entry.get().strip()
        password = self.new_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        
        success = self.user_manager.create_account(username, password, confirm_password)
        if success and self.on_back:
            self.on_back()
    
    def back_to_login(self):
        """Return to login screen."""
        if self.on_back:
            self.on_back()
