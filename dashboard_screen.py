"""Dashboard screen for displaying user statistics and performance."""

import tkinter as tk
from tkinter import ttk
from config import COLORS, USER_LEVELS
from ui_components import (
    create_label, create_button, create_frame, load_icon
)
from stats_visualizer import StatsVisualizer

class DashboardScreen:
    """Dashboard screen for displaying user statistics."""
    
    def __init__(self, root, user_manager, current_user, on_close=None):
        """Initialize with root window."""
        self.root = root
        self.user_manager = user_manager
        self.current_user = current_user
        self.on_close = on_close
        self.stats_visualizer = StatsVisualizer(root)
    
    def show(self):
        """Show the dashboard screen."""
        self.dashboard_window = tk.Toplevel(self.root)
        self.dashboard_window.title(f"{self.current_user}'s Dashboard")
        self.dashboard_window.geometry("900x700")
        self.dashboard_window.resizable(True, True)
        self.dashboard_window.transient(self.root)
        self.dashboard_window.grab_set()
        
        # Center on parent
        x = self.root.winfo_x() + (self.root.winfo_width() - 900) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 700) // 2
        self.dashboard_window.geometry(f"+{x}+{y}")
        
        self.dashboard_window.config(background=COLORS["background"])
        self.create_dashboard_ui()
    
    def create_dashboard_ui(self):
        """Create the dashboard UI."""
        main_frame = create_frame(self.dashboard_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = create_label(header_frame, "Typing Performance Dashboard", font_size=24, weight="bold")
        title_label.pack(side=tk.LEFT)
        
        close_button = create_button(
            header_frame,
            text="Close",
            command=self.close_dashboard,
            style="SecondaryButton.TButton"
        )
        close_button.pack(side=tk.RIGHT)
        
        # Load user data
        user_stats = self.user_manager.get_user_stats(self.current_user)
        if not user_stats:
            no_data_label = create_label(main_frame, "No typing data available. Complete some typing tests first.", font_size=16)
            no_data_label.pack(expand=True)
            return
        
        # Get user ranking
        ranking = self.user_manager.get_user_ranking(self.current_user)
        
        # Create dashboard content
        self.create_dashboard_content(main_frame, user_stats, ranking)
    
    def create_dashboard_content(self, parent, user_stats, ranking):
        """Create the main dashboard content."""
        # Top stats bar
        top_stats_frame = create_frame(parent, padding=15, shadow=True)
        top_stats_frame.pack(fill=tk.X, pady=10)
        
        level = user_stats.get("level", "Novice")
        level_color = USER_LEVELS.get(level, {}).get("color", COLORS["text"])
        
        # Level badge
        level_badge = create_frame(top_stats_frame, padding=10, bg_color=level_color)
        level_badge.grid(row=0, column=0, rowspan=2, padx=(0, 15))
        
        level_label = create_label(level_badge, level, font_size=16, weight="bold", foreground="#ffffff")
        level_label.pack()
        
        # Key stats in the top bar
        stats = [
            ("Best WPM", f"{user_stats.get('best_wpm', 0):.1f}"),
            ("Best Accuracy", f"{user_stats.get('best_accuracy', 0):.1f}%"),
            ("Average WPM", f"{user_stats.get('average_wpm', 0):.1f}"),
            ("Tests Completed", str(user_stats.get('total_tests', 0)))
        ]
        
        for i, (label, value) in enumerate(stats):
            stat_frame = ttk.Frame(top_stats_frame)
            stat_frame.grid(row=0, column=i+1, padx=15)
            
            create_label(stat_frame, value, font_size=24, weight="bold").pack(anchor="center")
            create_label(stat_frame, label, font_size=12).pack(anchor="center")
        
        # Ranking display
        if ranking:
            rank_frame = ttk.Frame(top_stats_frame)
            rank_frame.grid(row=0, column=len(stats)+1, padx=15)
            
            create_label(rank_frame, f"#{ranking['rank']}", font_size=24, weight="bold").pack(anchor="center")
            create_label(rank_frame, f"Top {ranking['percentile']:.1f}%", font_size=12).pack(anchor="center")
        
        top_stats_frame.columnconfigure(tuple(range(len(stats) + 2)), weight=1)
        
        # Progress to next level
        if user_stats:
            progress_frame = create_frame(parent, padding=15)
            progress_frame.pack(fill=tk.X, pady=10)
            progress_label = create_label(progress_frame, "Progress to Next Level", font_size=16, weight="bold")
            progress_label.pack(anchor="w", pady=(0, 10))
            
            self.stats_visualizer.create_level_progress_chart(progress_frame, user_stats, width=860, height=60)
        
        # Main charts area
        charts_frame = ttk.Notebook(parent)
        charts_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Prepare data structure for visualization
        user_data = {
            "stats": user_stats,
            "history": self.get_typing_history()
        }
        
        # Create dashboard with all charts
        dashboard = self.stats_visualizer.create_stats_dashboard(charts_frame, user_data)
        charts_frame.add(dashboard, text="All Stats")
        
        # Recommendations frame
        recommendations_frame = create_frame(parent, padding=15)
        recommendations_frame.pack(fill=tk.X, pady=10)
        
        recommend_label = create_label(recommendations_frame, "Recommendations", font_size=16, weight="bold")
        recommend_label.pack(anchor="w", pady=(0, 10))
        
        recommendations = self.get_recommendations(user_stats, user_data.get("history", []))
        for recommendation in recommendations:
            rec_item = create_frame(recommendations_frame, padding=10, bg_color=COLORS["card_background"], shadow=False, border=True)
            rec_item.pack(fill=tk.X, pady=5)
            create_label(rec_item, recommendation, font_size=14).pack(anchor="w")
    
    def get_typing_history(self):
        """Get typing history from user data file."""
        # This method would access history data from the user's stored data
        # For now, we'll return dummy data
        import random
        from datetime import datetime, timedelta
        
        history = []
        base_date = datetime.now() - timedelta(days=30)
        
        for i in range(30):
            # Generate some random data points with an overall improving trend
            test_date = base_date + timedelta(days=i)
            wpm_base = 40 + (i * 0.5)  # Gradually improving WPM
            wpm = max(10, wpm_base + random.randint(-10, 10))  # Add some randomness
            accuracy = min(100, max(70, 90 + random.randint(-10, 10)))  # Random accuracy between 70-100%
            
            # Create random letter stats
            letter_stats = {}
            for letter in 'abcdefghijklmnopqrstuvwxyz':
                correct = random.randint(1, 10)
                incorrect = random.randint(0, 5)
                letter_stats[letter] = {
                    "correct": correct,
                    "incorrect": incorrect
                }
            
            # Create a test entry
            history.append({
                "timestamp": test_date.isoformat(),
                "difficulty": random.choice(["Beginner", "Intermediate", "Advanced", "Expert"]),
                "wpm": round(wpm, 2),
                "accuracy": round(accuracy, 2),
                "elapsed_time": round(random.uniform(30, 180), 2),
                "letter_stats": letter_stats
            })
        
        # Sort by date
        history.sort(key=lambda x: x["timestamp"])
        return history
    
    def get_recommendations(self, user_stats, history):
        """Generate personalized typing recommendations based on user data."""
        recommendations = []
        
        # Check if user has enough data
        if not history or len(history) < 2:
            recommendations.append("Complete more typing tests to get personalized recommendations.")
            return recommendations
        
        # Get most recent test
        latest_test = history[-1]
        
        # Check accuracy trend
        accuracies = [test["accuracy"] for test in history[-5:]] if len(history) >= 5 else [test["accuracy"] for test in history]
        avg_accuracy = sum(accuracies) / len(accuracies)
        
        # Check WPM trend
        wpms = [test["wpm"] for test in history[-5:]] if len(history) >= 5 else [test["wpm"] for test in history]
        avg_wpm = sum(wpms) / len(wpms)
        
        # Find problem letters
        problem_letters = []
        if "letter_stats" in latest_test:
            for letter, stats in latest_test["letter_stats"].items():
                total = stats["correct"] + stats["incorrect"]
                if total >= 5:  # Only check letters with enough data
                    accuracy = (stats["correct"] / total * 100) if total > 0 else 0
                    if accuracy < 70:
                        problem_letters.append(letter)
        
        # Generate recommendations
        if len(problem_letters) > 0:
            recommendations.append(f"Focus on improving accuracy for these letters: {', '.join(problem_letters)}.")
        
        if avg_accuracy < 90:
            recommendations.append("Try slowing down to improve accuracy. Speed will come naturally with practice.")
        elif avg_wpm < 40:
            recommendations.append("Your accuracy is good! Now try to increase your speed gradually.")
        
        # Level-specific recommendations
        level = user_stats.get("level", "Novice")
        if level == "Novice":
            recommendations.append("Practice the home row keys (asdf jkl;) until you can type them without looking.")
        elif level == "Intermediate":
            recommendations.append("Try practicing with common programming syntax to improve coding speed.")
        elif level == "Advanced":
            recommendations.append("Challenge yourself with advanced texts or try typing without looking at the keyboard at all.")
        
        # General practice recommendations
        if len(history) < 10:
            recommendations.append("Consistency is key! Try to practice daily, even if just for 5 minutes.")
        
        # Default recommendation if none generated
        if not recommendations:
            recommendations.append("Keep practicing regularly to maintain your skills!")
        
        return recommendations[:3]  # Limit to top 3 recommendations
    
    def close_dashboard(self):
        """Close the dashboard window."""
        if self.dashboard_window:
            self.dashboard_window.destroy()
            
        if self.on_close:
            self.on_close()