"""Visualize typing statistics for the dashboard."""

import tkinter as tk
from tkinter import ttk
from config import COLORS, USER_LEVELS, FONTS
from datetime import datetime, timedelta
import math

class StatsVisualizer:
    """Creates visual representations of typing statistics."""
    
    def __init__(self, root):
        """Initialize with root window."""
        self.root = root
        
    def create_stats_dashboard(self, parent, user_data):
        """Create a comprehensive dashboard with charts for all stats."""
        dashboard_frame = ttk.Frame(parent)
        
        # Progress over time chart
        progress_frame = ttk.LabelFrame(dashboard_frame, text="Progress Over Time")
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_progress_chart(progress_frame, user_data["history"])
        
        # Accuracy vs. Speed chart
        accuracy_frame = ttk.LabelFrame(dashboard_frame, text="Accuracy vs. Speed")
        accuracy_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_accuracy_vs_speed_chart(accuracy_frame, user_data["history"])
        
        # Most recent tests
        recent_frame = ttk.LabelFrame(dashboard_frame, text="Recent Typing Tests")
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_recent_tests_table(recent_frame, user_data["history"][-10:] if len(user_data["history"]) > 10 else user_data["history"])
        
        return dashboard_frame
    
    def create_progress_chart(self, parent, history):
        """Create a chart showing WPM progress over time."""
        chart_frame = ttk.Frame(parent)
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas for the chart
        canvas = tk.Canvas(chart_frame, bg=COLORS["card_background"], height=200)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        if not history:
            canvas.create_text(
                canvas.winfo_reqwidth() / 2, 
                canvas.winfo_reqheight() / 2,
                text="No data available",
                fill=COLORS["muted_text"]
            )
            return
        
        # Extract WPM and dates
        wpm_data = [(datetime.fromisoformat(entry["timestamp"]), entry["wpm"]) for entry in history]
        
        # Sort by date
        wpm_data.sort(key=lambda x: x[0])
        
        # Get min/max values for scaling
        min_wpm = min(entry[1] for entry in wpm_data) if wpm_data else 0
        max_wpm = max(entry[1] for entry in wpm_data) if wpm_data else 0
        min_wpm = max(0, min_wpm - 5)  # Add some padding
        max_wpm = max_wpm + 5  # Add some padding
        
        # Get date range
        if len(wpm_data) > 1:
            min_date = wpm_data[0][0]
            max_date = wpm_data[-1][0]
            date_range = (max_date - min_date).days + 1
        else:
            min_date = wpm_data[0][0] - timedelta(days=7) if wpm_data else datetime.now() - timedelta(days=7)
            max_date = wpm_data[0][0] + timedelta(days=7) if wpm_data else datetime.now()
            date_range = 14
        
        # Draw axes and grid
        def draw_chart():
            canvas.delete("all")
            
            # Get canvas dimensions
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            # Set margins
            margin_left = 50
            margin_right = 20
            margin_top = 20
            margin_bottom = 40
            
            # Calculate chart area
            chart_width = width - margin_left - margin_right
            chart_height = height - margin_top - margin_bottom
            
            # Draw axes
            canvas.create_line(margin_left, height - margin_bottom, width - margin_right, height - margin_bottom, fill=COLORS["muted_text"])  # X-axis
            canvas.create_line(margin_left, margin_top, margin_left, height - margin_bottom, fill=COLORS["muted_text"])  # Y-axis
            
            # Draw Y-axis labels and grid lines
            y_step = max(1, math.ceil((max_wpm - min_wpm) / 5))
            for i in range(0, int(max_wpm) + y_step, y_step):
                if i < min_wpm:
                    continue
                    
                y = height - margin_bottom - ((i - min_wpm) / (max_wpm - min_wpm) * chart_height if max_wpm > min_wpm else 0)
                canvas.create_line(margin_left - 5, y, margin_left, y, fill=COLORS["muted_text"])
                canvas.create_text(margin_left - 10, y, text=str(i), fill=COLORS["muted_text"], anchor="e")
                canvas.create_line(margin_left + 1, y, width - margin_right, y, fill=COLORS["muted_text"], dash=(1, 3))
            
            # Draw X-axis labels and grid lines
            date_step = max(1, math.ceil(date_range / 5))
            for i in range(date_range + 1):
                if i % date_step != 0:
                    continue
                    
                date = min_date + timedelta(days=i)
                x = margin_left + (i / date_range * chart_width if date_range > 0 else 0)
                canvas.create_line(x, height - margin_bottom, x, height - margin_bottom + 5, fill=COLORS["muted_text"])
                canvas.create_text(x, height - margin_bottom + 20, text=date.strftime("%m/%d"), fill=COLORS["muted_text"], anchor="n")
                if i > 0:  # Don't draw grid line over Y-axis
                    canvas.create_line(x, margin_top, x, height - margin_bottom - 1, fill=COLORS["muted_text"], dash=(1, 3))
            
            # Draw data points and connecting lines
            points = []
            for date, wpm in wpm_data:
                days_from_start = (date - min_date).days
                x = margin_left + (days_from_start / date_range * chart_width if date_range > 0 else chart_width / 2)
                y = height - margin_bottom - ((wpm - min_wpm) / (max_wpm - min_wpm) * chart_height if max_wpm > min_wpm else chart_height / 2)
                points.append((x, y))
            
            # Draw trend line
            if len(points) > 1:
                canvas.create_line(points, fill=COLORS["graph_1"], width=2, smooth=True)
            
            # Draw data points
            for x, y in points:
                canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill=COLORS["graph_1"], outline="")
            
            # Draw chart title
            canvas.create_text(width / 2, margin_top - 5, text="WPM Progress Over Time", fill=COLORS["text"], anchor="n")
        
        # Call the draw function once
        draw_chart()
        
        # Redraw on canvas resize
        canvas.bind("<Configure>", lambda e: draw_chart())
    
    def create_accuracy_vs_speed_chart(self, parent, history):
        """Create a scatter chart showing accuracy vs speed."""
        chart_frame = ttk.Frame(parent)
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas for the chart
        canvas = tk.Canvas(chart_frame, bg=COLORS["card_background"], height=200)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        if not history:
            canvas.create_text(
                canvas.winfo_reqwidth() / 2, 
                canvas.winfo_reqheight() / 2,
                text="No data available",
                fill=COLORS["muted_text"]
            )
            return
        
        # Extract WPM and accuracy
        data_points = [(entry["wpm"], entry["accuracy"]) for entry in history]
        
        # Get min/max values for scaling
        min_wpm = min(point[0] for point in data_points) if data_points else 0
        max_wpm = max(point[0] for point in data_points) if data_points else 0
        min_acc = min(point[1] for point in data_points) if data_points else 0
        max_acc = max(point[1] for point in data_points) if data_points else 0
        
        # Add padding
        min_wpm = max(0, min_wpm - 5)
        max_wpm = max_wpm + 5
        min_acc = max(0, min_acc - 5)
        max_acc = min(100, max_acc + 5)
        
        # Draw axes and scatter points
        def draw_chart():
            canvas.delete("all")
            
            # Get canvas dimensions
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            # Set margins
            margin_left = 50
            margin_right = 20
            margin_top = 20
            margin_bottom = 40
            
            # Calculate chart area
            chart_width = width - margin_left - margin_right
            chart_height = height - margin_top - margin_bottom
            
            # Draw axes
            canvas.create_line(margin_left, height - margin_bottom, width - margin_right, height - margin_bottom, fill=COLORS["muted_text"])  # X-axis
            canvas.create_line(margin_left, margin_top, margin_left, height - margin_bottom, fill=COLORS["muted_text"])  # Y-axis
            
            # Draw axis labels
            canvas.create_text(width / 2, height - 5, text="WPM", fill=COLORS["text"])
            canvas.create_text(15, height / 2, text="Accuracy (%)", fill=COLORS["text"], angle=90)
            
            # Draw X-axis labels and grid lines
            x_step = max(1, math.ceil((max_wpm - min_wpm) / 5))
            for i in range(0, int(max_wpm) + x_step, x_step):
                if i < min_wpm:
                    continue
                    
                x = margin_left + ((i - min_wpm) / (max_wpm - min_wpm) * chart_width if max_wpm > min_wpm else 0)
                canvas.create_line(x, height - margin_bottom, x, height - margin_bottom + 5, fill=COLORS["muted_text"])
                canvas.create_text(x, height - margin_bottom + 20, text=str(i), fill=COLORS["muted_text"])
                canvas.create_line(x, margin_top, x, height - margin_bottom - 1, fill=COLORS["muted_text"], dash=(1, 3))
            
            # Draw Y-axis labels and grid lines
            y_step = max(1, math.ceil((max_acc - min_acc) / 5))
            for i in range(0, int(max_acc) + y_step, y_step):
                if i < min_acc:
                    continue
                    
                y = height - margin_bottom - ((i - min_acc) / (max_acc - min_acc) * chart_height if max_acc > min_acc else 0)
                canvas.create_line(margin_left - 5, y, margin_left, y, fill=COLORS["muted_text"])
                canvas.create_text(margin_left - 10, y, text=str(i), fill=COLORS["muted_text"], anchor="e")
                canvas.create_line(margin_left + 1, y, width - margin_right, y, fill=COLORS["muted_text"], dash=(1, 3))
            
            # Draw data points
            for wpm, acc in data_points:
                if wpm < min_wpm or acc < min_acc:
                    continue
                    
                x = margin_left + ((wpm - min_wpm) / (max_wpm - min_wpm) * chart_width if max_wpm > min_wpm else chart_width / 2)
                y = height - margin_bottom - ((acc - min_acc) / (max_acc - min_acc) * chart_height if max_acc > min_acc else chart_height / 2)
                
                # Choose point color based on accuracy
                if acc >= 95:
                    color = COLORS["success"]
                elif acc >= 85:
                    color = COLORS["accent"]
                else:
                    color = COLORS["error"]
                    
                canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill=color, outline="")
            
            # Draw chart title
            canvas.create_text(width / 2, margin_top - 5, text="Accuracy vs. Speed", fill=COLORS["text"], anchor="n")
        
        # Call the draw function once
        draw_chart()
        
        # Redraw on canvas resize
        canvas.bind("<Configure>", lambda e: draw_chart())
    
    def create_recent_tests_table(self, parent, recent_tests):
        """Create a table of recent test results."""
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Define columns
        columns = ("date", "wpm", "accuracy", "mode", "time")
        
        # Create treeview
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Set column headings
        tree.heading("date", text="Date")
        tree.heading("wpm", text="WPM")
        tree.heading("accuracy", text="Accuracy")
        tree.heading("mode", text="Mode")
        tree.heading("time", text="Time")
        
        # Set column widths
        tree.column("date", width=120)
        tree.column("wpm", width=80)
        tree.column("accuracy", width=80)
        tree.column("mode", width=100)
        tree.column("time", width=80)
        
        # Populate with data
        if recent_tests:
            for i, test in enumerate(reversed(recent_tests)):
                # Format timestamp
                try:
                    test_date = datetime.fromisoformat(test["timestamp"])
                    date_str = test_date.strftime("%Y-%m-%d %H:%M")
                except:
                    date_str = "Unknown"
                
                # Format time
                elapsed = test.get("elapsed_time", 0)
                minutes = int(elapsed // 60)
                seconds = int(elapsed % 60)
                time_str = f"{minutes}:{seconds:02d}"
                
                # Insert row
                tree.insert("", "end", values=(
                    date_str,
                    f"{test.get('wpm', 0):.1f}",
                    f"{test.get('accuracy', 0):.1f}%",
                    test.get("test_type", "Standard").capitalize(),
                    time_str
                ))
        else:
            tree.insert("", "end", values=("No data", "-", "-", "-", "-"))
    
    def create_level_progress_chart(self, parent, user_stats, width=860, height=60):
        """Create a progress chart showing advancement to the next typing level."""
        canvas = tk.Canvas(parent, width=width, height=height, bg=COLORS["card_background"], highlightthickness=0)
        canvas.pack(fill=tk.X)
        
        # Get current level and WPM
        current_wpm = user_stats.get("best_wpm", 0)
        current_level = user_stats.get("level", "Novice")
        
        # Find current level info
        current_level_data = USER_LEVELS.get(current_level, {"min_wpm": 0, "max_wpm": 30, "color": COLORS["muted_text"]})
        
        # Find next level
        level_ranks = list(USER_LEVELS.keys())
        current_index = level_ranks.index(current_level)
        
        if current_index < len(level_ranks) - 1:
            next_level = level_ranks[current_index + 1]
            next_level_data = USER_LEVELS[next_level]
            next_level_min_wpm = next_level_data["min_wpm"]
            
            # Calculate progress to next level
            level_min_wpm = current_level_data["min_wpm"]
            level_max_wpm = current_level_data["max_wpm"]
            level_range = next_level_min_wpm - level_min_wpm
            
            if level_range > 0:
                progress = min(100, max(0, (current_wpm - level_min_wpm) / level_range * 100))
            else:
                progress = 100
            
            # Draw progress bar
            def draw_progress():
                canvas.delete("all")
                
                # Get dimensions
                width = canvas.winfo_width()
                height = canvas.winfo_height()
                
                # Background bar
                canvas.create_rectangle(0, 0, width, height, fill=COLORS["progress_bg"], outline="")
                
                # Progress fill
                fill_width = (progress / 100) * width
                canvas.create_rectangle(0, 0, fill_width, height, fill=current_level_data["color"], outline="")
                
                # Current level label
                canvas.create_text(10, height / 2, text=current_level, fill="#ffffff", anchor="w")
                
                # Next level label
                canvas.create_text(width - 10, height / 2, text=next_level, fill=COLORS["text"], anchor="e")
                
                # WPM indicators
                canvas.create_text(10, height - 5, text=f"{level_min_wpm} WPM", fill=COLORS["muted_text"], anchor="sw", font=(FONTS["primary"], 8))
                canvas.create_text(width - 10, height - 5, text=f"{next_level_min_wpm} WPM", fill=COLORS["muted_text"], anchor="se", font=(FONTS["primary"], 8))
                
                # Current WPM indicator
                if progress > 0 and progress < 100:
                    marker_x = fill_width
                    canvas.create_line(marker_x, 0, marker_x, height, fill=COLORS["warning"], width=2)
                    canvas.create_text(marker_x, height / 2, text=f"{current_wpm:.1f}", fill=COLORS["text"], anchor="e", font=(FONTS["primary"], 10, "bold"))
            
            # Draw initially
            draw_progress()
            
            # Redraw on resize
            canvas.bind("<Configure>", lambda e: draw_progress())
        else:
            # Already at max level
            canvas.create_rectangle(0, 0, width, height, fill=current_level_data["color"], outline="")
            canvas.create_text(width/2, height/2, text=f"Congratulations! You've reached the highest level: {current_level}", fill="#ffffff")
