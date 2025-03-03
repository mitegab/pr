"""Login screen for the typing test application."""

import tkinter as tk
from tkinter import ttk, messagebox
from config import COLORS, FONTS
from simplified_ui import (
    create_label, create_button, create_frame, create_entry
)

class LoginScreen:
    """Login screen for user authentication."""
    
    def __init__(self, root, user_manager, mode="login", on_login=None, on_create_account=None, on_back=None):
        """Initialize the login screen."""
        self.root = root
        self.user_manager = user_manager
        self.mode = mode  # 'login' or 'create'
        self.on_login = on_login
        self.on_create_account = on_create_account
        self.on_back = on_back
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main container taking full width and height
        main_frame = create_frame(self.root, padding=0)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # App title at the top
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, padx=20, pady=(30, 0))
        
        app_title = create_label(title_frame, "Typing Speed Test Pro", font_size=28, weight="bold")
        app_title.pack()
        
        app_subtitle = create_label(title_frame, "Improve your typing skills with structured practice", font_size=14)
        app_subtitle.pack(pady=5)
        
        # Central login card
        login_card = create_frame(main_frame, padding=30, bg_color=COLORS["card_background"], shadow=True)
        login_card.pack(expand=True, padx=250, pady=50)
        
        # Card title
        if self.mode == "login":
            card_title = create_label(login_card, "Login to Your Account", font_size=20, weight="bold")
        else:
            card_title = create_label(login_card, "Create a New Account", font_size=20, weight="bold")
        
        card_title.pack(pady=(0, 20))
        
        # Username field
        username_label = create_label(login_card, "Username", font_size=14)
        username_label.pack(anchor="w", pady=(0, 5))
        
        self.username_var = tk.StringVar()
        username_entry = create_entry(login_card, textvariable=self.username_var, font_size=16, width=30)
        username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Password field
        password_label = create_label(login_card, "Password", font_size=14)
        password_label.pack(anchor="w", pady=(0, 5))
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(
            login_card, 
            textvariable=self.password_var, 
            font=(FONTS["primary"], 16),
            show="•",
            width=30
        )
        password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Confirm Password field (for create account mode)
        if self.mode == "create":
            confirm_password_label = create_label(login_card, "Confirm Password", font_size=14)
            confirm_password_label.pack(anchor="w", pady=(0, 5))
            
            self.confirm_password_var = tk.StringVar()
            confirm_password_entry = ttk.Entry(
                login_card, 
                textvariable=self.confirm_password_var, 
                font=(FONTS["primary"], 16),
                show="•",
                width=30
            )
            confirm_password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Action buttons
        button_frame = ttk.Frame(login_card)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        login_button = None
        create_button_widget = None
        back_button = None
        
        if self.mode == "login":
            login_button = create_button(
                button_frame,
                text="Login",
                command=self.login_click,
                style="PrimaryButton.TButton"
            )
            login_button.pack(side=tk.RIGHT)
            
            create_button_widget = create_button(
                button_frame,
                text="Create Account",
                command=self.create_account_click,
                style="SecondaryButton.TButton"
            )
            create_button_widget.pack(side=tk.LEFT)
        else:
            create_button_widget = create_button(
                button_frame,
                text="Create Account",
                command=self.create_account_click,
                style="PrimaryButton.TButton"
            )
            create_button_widget.pack(side=tk.RIGHT)
            
            back_button = create_button(
                button_frame,
                text="Back to Login",
                command=self.back_click,
                style="SecondaryButton.TButton"
            )
            back_button.pack(side=tk.LEFT)
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=20)
        
        version_label = create_label(footer_frame, "v1.0", font_size=10, foreground=COLORS["muted_text"])
        version_label.pack(side=tk.RIGHT, padx=20)
    
    def login_click(self):
        """Handle login button click."""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        success, message = self.user_manager.login(username, password)
        
        if success:
            if self.on_login:
                self.on_login(username)
        else:
            messagebox.showerror("Login Error", message)
    
    def create_account_click(self):
        """Handle create account button click."""
        if self.mode == "login":
            # Switch to create account mode
            if self.on_create_account:
                self.on_create_account()
        else:
            # Actually create the account
            username = self.username_var.get().strip()
            password = self.password_var.get()
            confirm_password = self.confirm_password_var.get()
            
            # Validate password match
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
                return
                
            # Create the user
            success, message = self.user_manager.create_user(username, password)
            
            if success:
                messagebox.showinfo("Success", "Account created successfully")
                # Log the user in
                self.user_manager.login(username, password)
                if self.on_login:
                    self.on_login(username)
            else:
                messagebox.showerror("Error", message)
    
    def back_click(self):
        """Handle back button click."""
        if self.on_back:
            self.on_back()
