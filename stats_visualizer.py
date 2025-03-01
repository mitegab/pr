"""Visualization components for typing statistics."""

import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime, timedelta
from config import COLORS, USER_LEVELS

# Try to import matplotlib with graceful fallback
MATPLOTLIB_AVAILABLE = False
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    print("Warning: matplotlib not available. Install with: pip install matplotlib")

class StatsVisualizer:
    """Class for creating data visualizations for typing statistics."""
    
    def __init__(self, root, theme="light"):
        """Initialize with root window and theme."""
        self.root = root
        self.theme = theme
        if MATPLOTLIB_AVAILABLE:
            self.configure_matplotlib_style()
    
    def configure_matplotlib_style(self):
        """Configure matplotlib style based on the theme."""
        if not MATPLOTLIB_AVAILABLE:
            return
            
        if self.theme == "dark":
            plt_bg = COLORS["background"]
            plt_fg = COLORS["text"]
            plt_grid = COLORS["border"]
        else:
            plt_bg = COLORS["background"]
            plt_fg = COLORS["text"]
            plt_grid = COLORS["border"]
        
        matplotlib.rcParams.update({
            "font.family": "SF Pro Display, Helvetica Neue, Arial",
            "font.size": 10,
            "axes.facecolor": plt_bg,
            "axes.edgecolor": plt_fg,
            "axes.labelcolor": plt_fg,
            "figure.facecolor": plt_bg,
            "text.color": plt_fg,
            "xtick.color": plt_fg,
            "ytick.color": plt_fg,
            "grid.color": plt_grid,
            "grid.linestyle": "--",
            "grid.linewidth": 0.5,
            "grid.alpha": 0.5,
        })
    
    def create_wpm_progress_chart(self, container, history, width=600, height=300):
        """Create a chart showing WPM progress over time."""
        if not MATPLOTLIB_AVAILABLE:
            return self._create_fallback_chart(container, "WPM Progress Chart", history)
            
        # Rest of the matplotlib implementation
        figure = Figure(figsize=(width/100, height/100), dpi=100)
        ax = figure.add_subplot(111)
        
        # Extract data
        if not history:
            dates = [datetime.now() - timedelta(days=1), datetime.now()]
            wpms = [0, 0]
        else:
            dates = [datetime.fromisoformat(item["timestamp"]) for item in history]
            wpms = [item["wpm"] for item in history]
        
        # Plot
        ax.plot(dates, wpms, marker='o', linestyle='-', color=COLORS["graph_1"], 
                linewidth=2, markersize=6)
        ax.set_title("Typing Speed Progress", fontweight="bold")
        ax.set_xlabel("Date")
        ax.set_ylabel("WPM")
        ax.grid(True)
        
        # Add trend line if enough data points
        if len(wpms) > 2:
            z = np.polyfit(range(len(wpms)), wpms, 1)
            p = np.poly1d(z)
            ax.plot(dates, p(range(len(wpms))), linestyle='--', color=COLORS["accent"], linewidth=1.5)
        
        figure.tight_layout()
        
        # Create canvas
        canvas = FigureCanvasTkAgg(figure, master=container)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        return canvas_widget
    
    def _create_fallback_chart(self, container, title, data=None):
        """Create a fallback UI when matplotlib is not available."""
        frame = ttk.Frame(container)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Show a message that matplotlib is needed
        message = f"{title}\n\nInstall matplotlib for visualization:\npip install matplotlib"
        label = ttk.Label(frame, text=message, font=("Helvetica", 14), 
                          foreground=COLORS["text"], background=COLORS["card_background"],
                          anchor="center")
        label.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        return frame
    
    # Include fallbacks for all other chart methods
    def create_accuracy_chart(self, container, history, width=600, height=300):
        if not MATPLOTLIB_AVAILABLE:
            return self._create_fallback_chart(container, "Accuracy Progress Chart", history)
        # Original implementation...
        
    def create_letter_accuracy_chart(self, container, letter_stats, width=600, height=300):
        if not MATPLOTLIB_AVAILABLE:
            return self._create_fallback_chart(container, "Letter Accuracy Chart", letter_stats)
        # Original implementation...
        
    def create_wpm_distribution_chart(self, container, history, width=600, height=300):
        if not MATPLOTLIB_AVAILABLE:
            return self._create_fallback_chart(container, "WPM Distribution Chart", history)
        # Original implementation...
        
    def create_heat_calendar(self, container, history, width=600, height=200):
        if not MATPLOTLIB_AVAILABLE:
            return self._create_fallback_chart(container, "Activity Heat Calendar", history)
        # Original implementation...
    
    def create_level_progress_chart(self, container, user_stats, width=600, height=100):
        """Create a chart showing progress toward next level."""
        if not MATPLOTLIB_AVAILABLE:
            # Create a simple progress bar for the fallback
            frame = ttk.Frame(container)
            frame.pack(fill=tk.BOTH, expand=True)
            
            # Get user's current level and best WPM
            current_level = user_stats.get("level", "Novice")
            best_wpm = user_stats.get("best_wpm", 0)
            
            # Set up level thresholds
            levels = list(USER_LEVELS.keys())
            current_idx = levels.index(current_level)
            
            label = ttk.Label(frame, text=f"Current Level: {current_level} ({best_wpm} WPM)", 
                            font=("Helvetica", 12))
            label.pack(pady=5)
            
            if current_idx < len(levels) - 1:
                next_level = levels[current_idx + 1]
                min_wpm = USER_LEVELS[current_level]["min_wpm"]
                next_min = USER_LEVELS[next_level]["min_wpm"]
                
                # Calculate progress percentage
                progress = (best_wpm - min_wpm) / (next_min - min_wpm) * 100
                progress = min(max(progress, 0), 100)
                
                progress_bar = ttk.Progressbar(frame, length=width-40, mode="determinate")
                progress_bar["value"] = progress
                progress_bar.pack(pady=5)
                
                next_label = ttk.Label(frame, text=f"Next Level: {next_level} ({next_min} WPM)",
                                    font=("Helvetica", 12))
                next_label.pack(pady=5)
            else:
                max_label = ttk.Label(frame, text="Maximum Level Achieved!", 
                                   font=("Helvetica", 12, "bold"))
                max_label.pack(pady=10)
            
            return frame
            
        # Original matplotlib implementation...
    
    def create_stats_dashboard(self, container, user_data):
        """Create a comprehensive stats dashboard."""
        dashboard_frame = ttk.Frame(container)
        
        # Summary stats
        summary_frame = ttk.LabelFrame(dashboard_frame, text="Summary")
        summary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        stats = user_data.get("stats", {})
        history = user_data.get("history", [])
        letter_stats = {}
        if history:
            letter_stats = history[-1].get("letter_stats", {})
        
        # Create summary grid
        for i, (label, value) in enumerate([
            ("Tests Completed", stats.get("total_tests", 0)),
            ("Best WPM", f"{stats.get('best_wpm', 0):.1f}"),
            ("Best Accuracy", f"{stats.get('best_accuracy', 0):.1f}%"),
            ("Average WPM", f"{stats.get('average_wpm', 0):.1f}"),
            ("Average Accuracy", f"{stats.get('average_accuracy', 0):.1f}%"),
            ("Current Level", stats.get("level", "Novice"))
        ]):
            ttk.Label(summary_frame, text=label + ":", font=("SF Pro Display", 12, "bold")).grid(row=i//3, column=(i%3)*2, sticky="e", padx=10, pady=5)
            ttk.Label(summary_frame, text=str(value), font=("SF Pro Display", 12)).grid(row=i//3, column=(i%3)*2+1, sticky="w", padx=10, pady=5)
        
        # Level progress
        level_frame = ttk.Frame(dashboard_frame)
        level_frame.pack(fill=tk.X, padx=10, pady=5)
        self.create_level_progress_chart(level_frame, stats)
        
        # Only add chart tabs if matplotlib is available
        if MATPLOTLIB_AVAILABLE:
            # Charts in tabs
            charts_notebook = ttk.Notebook(dashboard_frame)
            charts_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # Progress chart
            progress_tab = ttk.Frame(charts_notebook)
            charts_notebook.add(progress_tab, text="Speed Progress")
            self.create_wpm_progress_chart(progress_tab, history)
            
            # Accuracy chart
            accuracy_tab = ttk.Frame(charts_notebook)
            charts_notebook.add(accuracy_tab, text="Accuracy Progress")
            self.create_accuracy_chart(accuracy_tab, history)
            
            # Letter accuracy chart
            letter_tab = ttk.Frame(charts_notebook)
            charts_notebook.add(letter_tab, text="Letter Analysis")
            self.create_letter_accuracy_chart(letter_tab, letter_stats)
            
            # Distribution chart
            dist_tab = ttk.Frame(charts_notebook)
            charts_notebook.add(dist_tab, text="WPM Distribution")
            self.create_wpm_distribution_chart(dist_tab, history)
            
            # Activity calendar
            calendar_tab = ttk.Frame(charts_notebook)
            charts_notebook.add(calendar_tab, text="Activity")
            self.create_heat_calendar(calendar_tab, history)
        else:
            # Fallback message when matplotlib is unavailable
            msg_frame = ttk.Frame(dashboard_frame)
            msg_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=20)
            
            msg = "Charts unavailable. Install matplotlib for full statistics:\n\npip install matplotlib"
            ttk.Label(msg_frame, text=msg, font=("Helvetica", 14)).pack(expand=True)
        
        return dashboard_frame
