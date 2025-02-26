# main.py
import tkinter as tk
from tkinter import ttk, messagebox

from config import COLORS, USER_DATA_FILE, SAMPLE_TEXTS, ICON_PATH
from user_manager import UserManager
from ui_components import (
    create_label, create_entry, create_button, create_combobox,
    create_text_area, create_progressbar, create_frame, load_icon
)
from typing_test_logic import TypingTestLogic


class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test Pro")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))
        self.root.config(bg=COLORS["background"])

        self.user_manager = UserManager(USER_DATA_FILE)
        self.typing_logic = TypingTestLogic(SAMPLE_TEXTS)
        self.current_user = None

        self.login_icon = load_icon("login_icon.png")
        self.create_account_icon = load_icon("create_account_icon.png")
        self.start_icon = load_icon("start_icon.png")
        self.reset_icon = load_icon("reset_icon.png")

        self.configure_styles()
        self.show_login_screen()

    def clear_screen(self):
        """Clear all widgets from the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def configure_styles(self):
        """Configure ttk styles for a modern look."""
        style = ttk.Style(self.root)

        style.configure("TLabel", background=COLORS["background"], foreground=COLORS["text"], font=("Helvetica", 12))
        style.configure("TEntry", background=COLORS["background"], foreground=COLORS["text"], insertcolor=COLORS["text"], font=("Helvetica", 14))
        style.configure("TCombobox", background=COLORS["background"], foreground=COLORS["text"], fieldbackground=COLORS["background"], arrowcolor=COLORS["text"], font=("Helvetica", 14))
        style.map("TCombobox", background=[("active", COLORS["secondary_button"]), ("!disabled", COLORS["background"])], foreground=[("!disabled", COLORS["text"])])
        style.configure("PrimaryButton.TButton", background=COLORS["primary_button"], foreground=COLORS["background"], font=("Helvetica", 12, "bold"), padding=10, relief="flat", borderwidth=0, focuscolor=COLORS["accent"])
        style.map("PrimaryButton.TButton", background=[("active", COLORS["highlight"]), ("!disabled", COLORS["primary_button"])], foreground=[("active", COLORS["background"]), ("!disabled", COLORS["background"])])
        style.configure("SecondaryButton.TButton", background=COLORS["secondary_button"], foreground=COLORS["text"], font=("Helvetica", 12), padding=8, relief="flat", borderwidth=0, focuscolor=COLORS["accent"])
        style.map("SecondaryButton.TButton", background=[("active", COLORS["highlight"]), ("!disabled", COLORS["secondary_button"])], foreground=[("active", COLORS["text"]), ("!disabled", COLORS["text"])])
        style.configure("CenterFrame.TFrame", background=COLORS["background"])
        style.configure("TProgressbar", background=COLORS["primary_button"], troughcolor=COLORS["background"], borderwidth=0)
        style.layout("TProgressbar", [('Horizontal.Progressbar.trough', {'children': [('Horizontal.Progressbar.pbar', {'side': 'left', 'sticky': 'ns'})], 'sticky': 'nsew'})])


    def show_login_screen(self):
        """Display the login screen."""
        self.clear_screen()
        center_frame = create_frame(self.root, padding="30 20")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        create_label(center_frame, "Login", font_size=24, style="TLabel").grid(column=0, row=0, pady=20, columnspan=2)
        create_label(center_frame, "Username:", font_size=14, style="TLabel").grid(column=0, row=1, sticky="w", pady=5)
        self.username_entry = create_entry(center_frame, font_size=14, style="TEntry")
        self.username_entry.grid(column=1, row=1, sticky="ew", padx=10, pady=5)

        create_label(center_frame, "Password:", font_size=14, style="TLabel").grid(column=0, row=2, sticky="w", pady=5)
        self.password_entry = create_entry(center_frame, font_size=14, show="*", style="TEntry")
        self.password_entry.grid(column=1, row=2, sticky="ew", padx=10, pady=5)

        login_button_text = "Login" if not self.login_icon else None
        login_button = create_button(
            center_frame, text=login_button_text, command=self.login, style="PrimaryButton.TButton", icon_name="login_icon.png", compound="left"
        )
        login_button.grid(column=0, row=3, columnspan=2, pady=15, sticky="ew")

        create_account_button_text = "Create Account" if not self.create_account_icon else None
        create_account_button = create_button(
            center_frame, text=create_account_button_text, command=self.show_create_account_screen, style="SecondaryButton.TButton", icon_name="create_account_icon.png", compound="left"
        )
        create_account_button.grid(column=0, row=4, columnspan=2, pady=5, sticky="ew")

        center_frame.columnconfigure(1, weight=1)

    def show_create_account_screen(self):
        """Display the create account screen."""
        self.clear_screen()

        center_frame = create_frame(self.root, padding="30 20")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        create_label(center_frame, "Create Account", font_size=24, style="TLabel").grid(column=0, row=0, pady=20, columnspan=2)

        create_label(center_frame, "Username:", font_size=14, style="TLabel").grid(column=0, row=1, sticky="w", pady=5)
        self.new_username_entry = create_entry(center_frame, font_size=14, style="TEntry")
        self.new_username_entry.grid(column=1, row=1, sticky="ew", padx=10, pady=5)

        create_label(center_frame, "Password:", font_size=14, style="TLabel").grid(column=0, row=2, sticky="w", pady=5)
        self.new_password_entry = create_entry(center_frame, font_size=14, show="*", style="TEntry")
        self.new_password_entry.grid(column=1, row=2, sticky="ew", padx=10, pady=5)

        create_label(center_frame, "Confirm Password:", font_size=14, style="TLabel").grid(column=0, row=3, sticky="w", pady=5)
        self.confirm_password_entry = create_entry(center_frame, font_size=14, show="*", style="TEntry")
        self.confirm_password_entry.grid(column=1, row=3, sticky="ew", padx=10, pady=5)

        create_account_button_text = "Create Account" if not self.create_account_icon else None
        create_account_final_button = create_button(
            center_frame, text=create_account_button_text, command=self.create_account, style="PrimaryButton.TButton", icon_name="create_account_icon.png", compound="left"
        )
        create_account_final_button.grid(column=0, row=4, columnspan=2, pady=15, sticky="ew")

        back_to_login_button = create_button(
            center_frame, text="Back to Login", command=self.show_login_screen, style="SecondaryButton.TButton"
        )
        back_to_login_button.grid(column=0, row=5, columnspan=2, pady=5, sticky="ew")

        center_frame.columnconfigure(1, weight=1)

    def create_account(self):
        """Create a new account using UserManager."""
        username = self.new_username_entry.get().strip()
        password = self.new_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        self.user_manager.create_account(username, password, confirm_password, self.show_login_screen)


    def login(self):
        """Log in the user."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        user = self.user_manager.login(username, password, self.show_welcome_screen)
        if user:
            self.current_user = user
            self.show_welcome_screen()


    def show_welcome_screen(self):
        """Display the welcome screen with the username and difficulty selection."""
        self.clear_screen()

        center_frame = create_frame(self.root, padding="30 20")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        create_label(center_frame, f"Welcome, {self.current_user}!", font_size=24, style="TLabel").grid(row=0, column=0, columnspan=2, pady=30)

        create_label(center_frame, "Select Difficulty:", font_size=14, style="TLabel").grid(row=1, column=0, sticky="w", pady=10)
        self.difficulty_var = tk.StringVar(value=self.typing_logic.current_difficulty)
        difficulty_combobox = create_combobox(
            center_frame, values=list(SAMPLE_TEXTS.keys()), textvariable=self.difficulty_var
        )
        difficulty_combobox.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        difficulty_combobox.bind("<<ComboboxSelected>>", self.update_difficulty)


        start_button_text = "Start Typing Test" if not self.start_icon else None
        start_button = create_button(
            center_frame, text=start_button_text, command=self.start_test, style="PrimaryButton.TButton", icon_name="start_icon.png", compound="left"
        )
        start_button.grid(row=2, column=0, columnspan=2, pady=20, sticky="ew")

        center_frame.columnconfigure(1, weight=1)

    def update_difficulty(self, event):
        """Update the current difficulty based on combobox selection."""
        self.typing_logic.set_difficulty(self.difficulty_var.get())

    def start_test(self):
        """Start the typing test."""
        self.clear_screen()
        self.typing_logic.start_test()

        center_frame = create_frame(self.root, padding="30 20")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        create_label(center_frame, f"Difficulty: {self.typing_logic.current_difficulty}", font_size=14, style="TLabel").grid(row=0, column=0, columnspan=2, pady=5)

        self.sample_display = create_text_area(
            center_frame, height=5, wrap="word", state=tk.DISABLED,
            background=COLORS["background"], foreground=COLORS["text"]
        )
        self.sample_display.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

        self.entry = create_text_area(
            center_frame, height=10, wrap="word", state=tk.NORMAL,
            background=COLORS["background"], foreground=COLORS["text"], insertbackground=COLORS["text"]
        )
        self.entry.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        self.progress_bar = create_progressbar(center_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress_bar.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        self.stats_frame = create_frame(center_frame)
        self.stats_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        self.wpm_label = create_label(self.stats_frame, text="WPM: 0", font_size=12, style="TLabel")
        self.wpm_label.grid(row=0, column=0, padx=20, sticky="w")
        self.accuracy_label = create_label(self.stats_frame, text="Accuracy: 100.00%", font_size=12, style="TLabel")
        self.accuracy_label.grid(row=0, column=1, padx=20, sticky="e")
        self.stats_frame.columnconfigure(1, weight=1)

        reset_button_text = "Reset" if not self.reset_icon else None
        self.reset_button = create_button(
            center_frame, text=reset_button_text, command=self.reset_test, style="SecondaryButton.TButton", icon_name="reset_icon.png", compound="left"
        )
        self.reset_button.grid(row=5, column=0, columnspan=2, pady=15, sticky="ew")


        center_frame.columnconfigure(0, weight=1)
        center_frame.columnconfigure(1, weight=1)

        self.sample_display.config(state=tk.NORMAL)
        self.sample_display.delete(1.0, tk.END)
        self.sample_display.insert(tk.END, self.typing_logic.sample_text)
        self.sample_display.config(state=tk.DISABLED)

        self.entry.delete(1.0, tk.END)
        self.entry.focus()
        self.entry.bind("<KeyRelease>", self.check_typing)
        self.update_stats_display(0, 100.00)
        self.update_progress_bar(0, len(self.typing_logic.sample_text))


    def check_typing(self, event):
        """Check the user's typing, update UI and real-time stats."""
        typed_text = self.entry.get(1.0, tk.END).strip()
        self.highlight_text()
        accuracy = self.typing_logic.calculate_accuracy(typed_text)
        wpm = self.typing_logic.calculate_wpm(typed_text)
        self.update_stats_display(wpm, accuracy)
        self.update_progress_bar(len(typed_text), len(self.typing_logic.sample_text))

        if len(typed_text) >= len(self.typing_logic.sample_text):
            self.end_test(typed_text)

    def end_test(self, typed_text):
        self.entry.unbind("<KeyRelease>")
        wpm, accuracy = self.typing_logic.calculate_speed_and_accuracy(typed_text)
        messagebox.showinfo(
            "Typing Results",
            f"Your typing speed is: {wpm:.2f} WPM\n"
            f"Your accuracy is: {accuracy:.2f}%"
        )


    def update_progress_bar(self, typed_length, total_length):
        """Update the progress bar."""
        if total_length > 0:
            progress_value = (typed_length / total_length) * 100
            self.progress_bar['value'] = progress_value
        else:
            self.progress_bar['value'] = 0

    def update_stats_display(self, wpm, accuracy):
        """Update the WPM and Accuracy labels in real-time."""
        self.wpm_label.config(text=f"WPM: {wpm:.0f}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.2f}%")

    def highlight_text(self):
        """Highlight the sample text based on user input."""
        typed_text = self.entry.get(1.0, tk.END).strip()
        sample_text = self.typing_logic.sample_text
        self.sample_display.config(state=tk.NORMAL)
        self.sample_display.delete(1.0, tk.END)

        for i in range(len(typed_text)):
            if i < len(sample_text):
                if typed_text[i] == sample_text[i]:
                    self.sample_display.insert(tk.END, sample_text[i], "correct")
                else:
                    self.sample_display.insert(tk.END, sample_text[i], "incorrect")
            else:
                self.sample_display.insert(tk.END, typed_text[i], "extra") # Highlight extra typed chars

        if len(typed_text) < len(sample_text):
            self.sample_display.insert(tk.END, sample_text[len(typed_text):])

        self.sample_display.config(state=tk.DISABLED)

        self.sample_display.tag_config("correct", foreground=COLORS["success"])
        self.sample_display.tag_config("incorrect", foreground=COLORS["error"])
        self.sample_display.tag_config("extra", foreground=COLORS["error"])


    def reset_test(self):
        """Reset the typing test."""
        self.entry.config(state=tk.NORMAL)
        self.entry.delete(1.0, tk.END)
        self.progress_bar['value'] = 0
        self.update_stats_display(0, 100.00)
        self.typing_logic.start_test()
        self.highlight_text()
        self.entry.bind("<KeyRelease>", self.check_typing)


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()