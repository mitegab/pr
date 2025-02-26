# ui_screens.py
import tkinter as tk
from tkinter import ttk

class LoginScreen:
    def __init__(self, controller):
        self.controller = controller

    def show(self):
        self.controller.clear_screen()
        frame = ttk.Frame(self.controller.root)
        frame.pack(expand=True)
        label = ttk.Label(frame, text="Login Screen", font=("Helvetica", 16))
        label.pack(pady=20)
        button = ttk.Button(frame, text="Go to Create Account", style="PrimaryButton.TButton",
                            command=self.controller.show_create_account_screen)
        button.pack(pady=10)

class CreateAccountScreen:
    def __init__(self, controller):
        self.controller = controller

    def show(self):
        self.controller.clear_screen()
        frame = ttk.Frame(self.controller.root)
        frame.pack(expand=True)
        label = ttk.Label(frame, text="Create Account Screen", font=("Helvetica", 16))
        label.pack(pady=20)
        button = ttk.Button(frame, text="Go to Welcome", style="PrimaryButton.TButton",
                            command=self.controller.show_welcome_screen)
        button.pack(pady=10)

class WelcomeScreen:
    def __init__(self, controller):
        self.controller = controller

    def show(self):
        self.controller.clear_screen()
        frame = ttk.Frame(self.controller.root)
        frame.pack(expand=True)
        label = ttk.Label(frame, text="Welcome Screen", font=("Helvetica", 16))
        label.pack(pady=20)
        button = ttk.Button(frame, text="Start Test", style="PrimaryButton.TButton",
                            command=self.controller.start_test)
        button.pack(pady=10)

class TypingTestScreen:
    def __init__(self, controller):
        self.controller = controller

    def show(self):
        self.controller.clear_screen()
        frame = ttk.Frame(self.controller.root)
        frame.pack(expand=True)
        label = ttk.Label(frame, text="Typing Test Screen", font=("Helvetica", 16))
        label.pack(pady=20)
        text_box = tk.Text(frame, height=10, width=50, font=("Helvetica", 14))
        text_box.pack(pady=10)
        button = ttk.Button(frame, text="End Test", style="PrimaryButton.TButton",
                            command=self.controller.show_login_screen)
        button.pack(pady=10)