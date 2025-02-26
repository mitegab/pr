import tkinter as tk
import json
import os
import time
from tkinter import PhotoImage, ttk
from ui_screens import LoginScreen, CreateAccountScreen, WelcomeScreen, TypingTestScreen


class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test Pro")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))

        self.COLORS = {
            "background": "#3B4252",
            "text": "#ECEFF4",
            "primary_button": "#8FBCBB",
            "secondary_button": "#5E81AC",
            "highlight": "#A3BE8C",
            "error": "#BF616A",
            "success": "#A3BE8C",
            "accent": "#D08770"
        }
        self.root.config(bg=self.COLORS["background"])

        self.USER_DATA_FILE = "user_data.json"
        self.users = self.load_user_data()
        self.load_icons()

        self.sample_texts = {
            "Beginner": "The quick brown fox jumps over the lazy dog.",
            "Intermediate": "Programming is a rewarding skill that allows you to create innovative solutions to complex problems.",
            "Advanced": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
        }
        self.current_difficulty = "Beginner"
        self.current_user = None

        self.configure_styles()
        self.show_login_screen()

    def load_icons(self):
        try:
            icon_path = "icons"
            self.login_icon = PhotoImage(file=os.path.join(icon_path, "login_icon.png")).subsample(2, 2)
            self.create_account_icon = PhotoImage(file=os.path.join(icon_path, "create_account_icon.png")).subsample(2,
                                                                                                                     2)
            self.start_icon = PhotoImage(file=os.path.join(icon_path, "start_icon.png")).subsample(2, 2)
            self.reset_icon = PhotoImage(file=os.path.join(icon_path, "reset_icon.png")).subsample(2, 2)
        except Exception as e:
            print(f"Error loading icons: {e}. Using text-only buttons.")
            self.login_icon = None
            self.create_account_icon = None
            self.start_icon = None
            self.reset_icon = None

    def load_user_data(self):
        if os.path.exists(self.USER_DATA_FILE):
            with open(self.USER_DATA_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_user_data(self):
        with open(self.USER_DATA_FILE, "w") as file:
            json.dump(self.users, file)

    def configure_styles(self):
        style = ttk.Style(self.root)
        style.configure("TLabel",
                        background=self.COLORS["background"],
                        foreground=self.COLORS["text"],
                        font=("Helvetica", 12))
        style.configure("TEntry",
                        background=self.COLORS["background"],
                        foreground=self.COLORS["text"],
                        insertcolor=self.COLORS["text"],
                        font=("Helvetica", 14))
        style.configure("TCombobox",
                        background=self.COLORS["background"],
                        foreground=self.COLORS["text"],
                        fieldbackground=self.COLORS["background"],
                        arrowcolor=self.COLORS["text"],
                        font=("Helvetica", 14))
        style.map("TCombobox",
                  background=[("active", self.COLORS["secondary_button"]), ("!disabled", self.COLORS["background"])],
                  foreground=[("!disabled", self.COLORS["text"])])
        style.configure("PrimaryButton.TButton",
                        background=self.COLORS["primary_button"],
                        foreground=self.COLORS["background"],
                        font=("Helvetica", 12, "bold"),
                        padding=10,
                        relief="flat",
                        borderwidth=0,
                        focuscolor=self.COLORS["accent"])
        style.map("PrimaryButton.TButton",
                  background=[("active", self.COLORS["highlight"]), ("!disabled", self.COLORS["primary_button"])],
                  foreground=[("active", self.COLORS["background"]), ("!disabled", self.COLORS["background"])])
        style.configure("SecondaryButton.TButton",
                        background=self.COLORS["secondary_button"],
                        foreground=self.COLORS["text"],
                        font=("Helvetica", 12),
                        padding=8,
                        relief="flat",
                        borderwidth=0,
                        focuscolor=self.COLORS["accent"])
        style.map("SecondaryButton.TButton",
                  background=[("active", self.COLORS["highlight"]), ("!disabled", self.COLORS["secondary_button"])],
                  foreground=[("active", self.COLORS["text"]), ("!disabled", self.COLORS["text"])])
        style.configure("CenterFrame.TFrame", background=self.COLORS["background"])
        style.configure("TProgressbar",
                        background=self.COLORS["primary_button"],
                        troughcolor=self.COLORS["background"],
                        borderwidth=0)
        style.layout("TProgressbar",
                     [('Horizontal.Progressbar.trough',
                       {'children': [('Horizontal.Progressbar.pbar',
                                      {'side': 'left', 'sticky': 'ns'})],
                        'sticky': 'nsew'})])

    def show_login_screen(self):
        LoginScreen(self).show()

    def show_create_account_screen(self):
        CreateAccountScreen(self).show()

    def show_welcome_screen(self):
        WelcomeScreen(self).show()

    def start_test(self):
        TypingTestScreen(self).show()