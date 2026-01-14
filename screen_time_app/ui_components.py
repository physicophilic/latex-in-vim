"""
UI Components Module
Contains all UI frames and widgets
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog
from datetime import datetime, timedelta
import math


class DashboardFrame(ttk.Frame):
    """Main dashboard showing today's usage"""

    def __init__(self, parent, data_manager, tracker):
        super().__init__(parent)
        self.data_manager = data_manager
        self.tracker = tracker

        self.setup_ui()
        self.update_display()

    def setup_ui(self):
        """Set up dashboard UI"""
        # Title
        title = tk.Label(self, text="Today's Screen Time", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Total time display
        self.total_frame = tk.Frame(self, bg="#3498db", height=120)
        self.total_frame.pack(fill=tk.X, padx=20, pady=10)
        self.total_frame.pack_propagate(False)

        self.total_label = tk.Label(
            self.total_frame,
            text="0h 0m",
            font=("Arial", 36, "bold"),
            bg="#3498db",
            fg="white"
        )
        self.total_label.pack(expand=True)

        total_text = tk.Label(
            self.total_frame,
            text="Total Screen Time Today",
            font=("Arial", 10),
            bg="#3498db",
            fg="white"
        )
        total_text.pack()

        # Goal progress
        goal_frame = tk.Frame(self)
        goal_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(goal_frame, text="Daily Goal Progress:", font=("Arial", 11, "bold")).pack(anchor=tk.W)

        self.progress_bar = ttk.Progressbar(goal_frame, length=400, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=5)

        self.progress_label = tk.Label(goal_frame, text="0% of daily goal", font=("Arial", 9))
        self.progress_label.pack(anchor=tk.W)

        # Top apps today
        apps_frame = tk.Frame(self)
        apps_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(apps_frame, text="Top Apps Today:", font=("Arial", 11, "bold")).pack(anchor=tk.W)

        # Create treeview for apps
        columns = ("App", "Time", "Percentage")
        self.apps_tree = ttk.Treeview(apps_frame, columns=columns, show="headings", height=10)

        self.apps_tree.heading("App", text="Application")
        self.apps_tree.heading("Time", text="Time Used")
        self.apps_tree.heading("Percentage", text="% of Total")

        self.apps_tree.column("App", width=300)
        self.apps_tree.column("Time", width=150)
        self.apps_tree.column("Percentage", width=100)

        scrollbar = ttk.Scrollbar(apps_frame, orient=tk.VERTICAL, command=self.apps_tree.yview)
        self.apps_tree.configure(yscroll=scrollbar.set)

        self.apps_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update_display(self):
        """Update dashboard display with current data"""
        try:
            # Get today's total
            total_seconds = self.tracker.get_total_today()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)

            self.total_label.config(text=f"{hours}h {minutes}m")

            # Update goal progress
            goal_seconds = self.data_manager.config.get('daily_goal_seconds', 14400)
            progress_pct = min((total_seconds / goal_seconds) * 100, 100)
            self.progress_bar['value'] = progress_pct

            if total_seconds > goal_seconds:
                self.progress_label.config(
                    text=f"Goal exceeded by {self._format_time(total_seconds - goal_seconds)}",
                    fg="red"
                )
            else:
                remaining = goal_seconds - total_seconds
                self.progress_label.config(
                    text=f"{int(progress_pct)}% of daily goal | {self._format_time(remaining)} remaining",
                    fg="green"
                )

            # Update top apps
            today = datetime.now().strftime("%Y-%m-%d")
            top_apps = self.data_manager.get_top_apps(today, 20)

            # Clear existing items
            for item in self.apps_tree.get_children():
                self.apps_tree.delete(item)

            # Add apps
            for app_name, seconds in top_apps:
                if seconds > 0:
                    time_str = self._format_time(seconds)
                    pct = (seconds / total_seconds * 100) if total_seconds > 0 else 0
                    self.apps_tree.insert("", tk.END, values=(app_name, time_str, f"{pct:.1f}%"))

        except Exception as e:
            print(f"Dashboard update error: {e}")

    def _format_time(self, seconds):
        """Format seconds to readable time"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"


class StatisticsFrame(ttk.Frame):
    """Statistics and reports frame"""

    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager

        self.setup_ui()

    def setup_ui(self):
        """Set up statistics UI"""
        # Title
        title = tk.Label(self, text="Statistics & Reports", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Time period selector
        period_frame = tk.Frame(self)
        period_frame.pack(pady=10)

        tk.Label(period_frame, text="Time Period:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

        self.period_var = tk.StringVar(value="7")
        periods = [("Last 7 days", "7"), ("Last 30 days", "30"), ("All time", "all")]

        for text, value in periods:
            tk.Radiobutton(
                period_frame,
                text=text,
                variable=self.period_var,
                value=value,
                command=self.update_stats
            ).pack(side=tk.LEFT, padx=5)

        # Stats display
        stats_frame = tk.Frame(self, bg="#ecf0f1")
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.stats_text = scrolledtext.ScrolledText(
            stats_frame,
            wrap=tk.WORD,
            font=("Courier", 10),
            bg="#ecf0f1",
            relief=tk.FLAT
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Refresh button
        tk.Button(
            self,
            text="Refresh Statistics",
            command=self.update_stats,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(pady=10)

        self.update_stats()

    def update_stats(self):
        """Update statistics display"""
        self.stats_text.delete(1.0, tk.END)

        period = self.period_var.get()

        # Get weekly summary
        if period == "7":
            summary = self.data_manager.get_weekly_summary()
            self._display_summary(summary, "7 Days")
        elif period == "30":
            summary = self._get_period_summary(30)
            self._display_summary(summary, "30 Days")
        else:
            summary = self._get_all_time_summary()
            self._display_summary(summary, "All Time")

    def _get_period_summary(self, days):
        """Get summary for a specific number of days"""
        from collections import defaultdict

        summary = {
            'total_seconds': 0,
            'daily_average': 0,
            'top_apps': defaultdict(int),
            'days': []
        }

        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            daily_data = self.data_manager.get_daily_data(date)

            daily_total = sum(app.get('total_seconds', 0) for app in daily_data.values())
            summary['days'].append({
                'date': date,
                'total_seconds': daily_total
            })

            for app_name, app_data in daily_data.items():
                summary['top_apps'][app_name] += app_data.get('total_seconds', 0)

            summary['total_seconds'] += daily_total

        summary['daily_average'] = summary['total_seconds'] / days if days > 0 else 0
        summary['top_apps'] = sorted(summary['top_apps'].items(), key=lambda x: x[1], reverse=True)[:10]

        return summary

    def _get_all_time_summary(self):
        """Get all-time summary"""
        from collections import defaultdict

        summary = {
            'total_seconds': 0,
            'daily_average': 0,
            'top_apps': defaultdict(int),
            'days': []
        }

        for date, daily_data in self.data_manager.data.items():
            daily_total = sum(app.get('total_seconds', 0) for app in daily_data.values())
            summary['days'].append({
                'date': date,
                'total_seconds': daily_total
            })

            for app_name, app_data in daily_data.items():
                summary['top_apps'][app_name] += app_data.get('total_seconds', 0)

            summary['total_seconds'] += daily_total

        num_days = len(summary['days']) if summary['days'] else 1
        summary['daily_average'] = summary['total_seconds'] / num_days
        summary['top_apps'] = sorted(summary['top_apps'].items(), key=lambda x: x[1], reverse=True)[:10]

        return summary

    def _display_summary(self, summary, period_name):
        """Display summary in text widget"""
        text = f"\n{'='*60}\n"
        text += f"  SCREEN TIME REPORT - {period_name}\n"
        text += f"{'='*60}\n\n"

        # Total time
        text += f"Total Screen Time: {self._format_time(summary['total_seconds'])}\n"
        text += f"Daily Average: {self._format_time(summary['daily_average'])}\n\n"

        # Top apps
        text += f"{'='*60}\n"
        text += f"Top Applications:\n"
        text += f"{'='*60}\n\n"

        for i, (app_name, seconds) in enumerate(summary['top_apps'], 1):
            pct = (seconds / summary['total_seconds'] * 100) if summary['total_seconds'] > 0 else 0
            text += f"{i:2d}. {app_name:30s} {self._format_time(seconds):>12s}  ({pct:5.1f}%)\n"

        # Daily breakdown
        text += f"\n{'='*60}\n"
        text += f"Daily Breakdown:\n"
        text += f"{'='*60}\n\n"

        for day in summary['days'][:14]:  # Show last 14 days max
            date_obj = datetime.strptime(day['date'], "%Y-%m-%d")
            date_str = date_obj.strftime("%a, %b %d, %Y")
            time_str = self._format_time(day['total_seconds'])
            text += f"{date_str:25s} {time_str:>12s}\n"

        self.stats_text.insert(1.0, text)

    def _format_time(self, seconds):
        """Format seconds to readable time"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


class BlockerFrame(ttk.Frame):
    """App blocker configuration frame"""

    def __init__(self, parent, blocker, data_manager):
        super().__init__(parent)
        self.blocker = blocker
        self.data_manager = data_manager

        self.setup_ui()
        self.update_display()

    def setup_ui(self):
        """Set up blocker UI"""
        # Title
        title = tk.Label(self, text="App Blocker & Limits", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Description
        desc = tk.Label(
            self,
            text="Block distracting apps or set time limits",
            font=("Arial", 9),
            fg="gray"
        )
        desc.pack()

        # Blocked apps section
        blocked_frame = tk.LabelFrame(self, text="Blocked Apps", font=("Arial", 11, "bold"), padx=10, pady=10)
        blocked_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.blocked_listbox = tk.Listbox(blocked_frame, height=6)
        self.blocked_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        blocked_btn_frame = tk.Frame(blocked_frame)
        blocked_btn_frame.pack(fill=tk.X)

        tk.Button(
            blocked_btn_frame,
            text="+ Add Blocked App",
            command=self.add_blocked_app,
            bg="#e74c3c",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            blocked_btn_frame,
            text="- Remove",
            command=self.remove_blocked_app
        ).pack(side=tk.LEFT)

        # Limited apps section
        limited_frame = tk.LabelFrame(self, text="Time Limits", font=("Arial", 11, "bold"), padx=10, pady=10)
        limited_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("App", "Limit", "Used Today", "Status")
        self.limited_tree = ttk.Treeview(limited_frame, columns=columns, show="headings", height=6)

        self.limited_tree.heading("App", text="Application")
        self.limited_tree.heading("Limit", text="Time Limit")
        self.limited_tree.heading("Used Today", text="Used Today")
        self.limited_tree.heading("Status", text="Status")

        self.limited_tree.column("App", width=200)
        self.limited_tree.column("Limit", width=100)
        self.limited_tree.column("Used Today", width=100)
        self.limited_tree.column("Status", width=100)

        self.limited_tree.pack(fill=tk.BOTH, expand=True, pady=5)

        limited_btn_frame = tk.Frame(limited_frame)
        limited_btn_frame.pack(fill=tk.X)

        tk.Button(
            limited_btn_frame,
            text="+ Add Time Limit",
            command=self.add_limited_app,
            bg="#f39c12",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            limited_btn_frame,
            text="- Remove",
            command=self.remove_limited_app
        ).pack(side=tk.LEFT)

        # Refresh button
        tk.Button(
            self,
            text="Refresh",
            command=self.update_display,
            bg="#3498db",
            fg="white"
        ).pack(pady=10)

    def update_display(self):
        """Update blocker display"""
        # Update blocked apps
        self.blocked_listbox.delete(0, tk.END)
        for app in sorted(self.blocker.blocked_apps):
            self.blocked_listbox.insert(tk.END, app)

        # Update limited apps
        for item in self.limited_tree.get_children():
            self.limited_tree.delete(item)

        today = datetime.now().strftime("%Y-%m-%d")
        for app_name, limit_seconds in self.blocker.limited_apps.items():
            app_data = self.data_manager.get_app_data(today, app_name)
            used_seconds = app_data.get('total_seconds', 0)

            limit_str = self._format_time(limit_seconds)
            used_str = self._format_time(used_seconds)

            if used_seconds >= limit_seconds:
                status = "⛔ Blocked"
            elif used_seconds >= limit_seconds * 0.9:
                status = "⚠️ Warning"
            else:
                status = "✓ OK"

            self.limited_tree.insert("", tk.END, values=(app_name, limit_str, used_str, status))

    def add_blocked_app(self):
        """Add an app to block list"""
        app_name = simpledialog.askstring("Block App", "Enter application name to block:")
        if app_name:
            self.blocker.add_blocked_app(app_name)
            self.update_display()

    def remove_blocked_app(self):
        """Remove app from block list"""
        selection = self.blocked_listbox.curselection()
        if selection:
            app_name = self.blocked_listbox.get(selection[0])
            self.blocker.remove_blocked_app(app_name)
            self.update_display()

    def add_limited_app(self):
        """Add time limit for an app"""
        app_name = simpledialog.askstring("Time Limit", "Enter application name:")
        if app_name:
            hours = simpledialog.askinteger("Time Limit", "Enter time limit (hours):", minvalue=0, maxvalue=24)
            if hours is not None:
                minutes = simpledialog.askinteger("Time Limit", "Enter additional minutes:", minvalue=0, maxvalue=59)
                if minutes is not None:
                    total_seconds = (hours * 3600) + (minutes * 60)
                    self.blocker.add_limited_app(app_name, total_seconds)
                    self.update_display()

    def remove_limited_app(self):
        """Remove time limit"""
        selection = self.limited_tree.selection()
        if selection:
            item = self.limited_tree.item(selection[0])
            app_name = item['values'][0]
            self.blocker.remove_limited_app(app_name)
            self.update_display()

    def _format_time(self, seconds):
        """Format seconds to readable time"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


class SettingsFrame(ttk.Frame):
    """Settings configuration frame"""

    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.data_manager = data_manager

        self.setup_ui()

    def setup_ui(self):
        """Set up settings UI"""
        # Title
        title = tk.Label(self, text="Settings", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Settings container
        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        # Daily goal
        goal_frame = tk.LabelFrame(container, text="Daily Screen Time Goal", font=("Arial", 11, "bold"), padx=20, pady=15)
        goal_frame.pack(fill=tk.X, pady=10)

        goal_input_frame = tk.Frame(goal_frame)
        goal_input_frame.pack()

        tk.Label(goal_input_frame, text="Hours:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.goal_hours = tk.Spinbox(goal_input_frame, from_=0, to=24, width=5)
        self.goal_hours.pack(side=tk.LEFT, padx=5)

        tk.Label(goal_input_frame, text="Minutes:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.goal_minutes = tk.Spinbox(goal_input_frame, from_=0, to=59, width=5)
        self.goal_minutes.pack(side=tk.LEFT, padx=5)

        # Load current goal
        goal_seconds = self.data_manager.config.get('daily_goal_seconds', 14400)
        self.goal_hours.delete(0, tk.END)
        self.goal_hours.insert(0, str(int(goal_seconds // 3600)))
        self.goal_minutes.delete(0, tk.END)
        self.goal_minutes.insert(0, str(int((goal_seconds % 3600) // 60)))

        # Notifications
        notif_frame = tk.LabelFrame(container, text="Notifications", font=("Arial", 11, "bold"), padx=20, pady=15)
        notif_frame.pack(fill=tk.X, pady=10)

        self.notif_var = tk.BooleanVar(value=self.data_manager.config.get('notifications_enabled', True))
        tk.Checkbutton(
            notif_frame,
            text="Enable notifications",
            variable=self.notif_var,
            font=("Arial", 10)
        ).pack(anchor=tk.W)

        # Data management
        data_frame = tk.LabelFrame(container, text="Data Management", font=("Arial", 11, "bold"), padx=20, pady=15)
        data_frame.pack(fill=tk.X, pady=10)

        tk.Button(
            data_frame,
            text="Clean Old Data (30+ days)",
            command=self.cleanup_data,
            bg="#95a5a6",
            fg="white"
        ).pack(pady=5)

        # Save button
        tk.Button(
            container,
            text="Save Settings",
            command=self.save_settings,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2"
        ).pack(pady=20)

    def save_settings(self):
        """Save settings"""
        try:
            hours = int(self.goal_hours.get())
            minutes = int(self.goal_minutes.get())
            goal_seconds = (hours * 3600) + (minutes * 60)

            self.data_manager.config['daily_goal_seconds'] = goal_seconds
            self.data_manager.config['notifications_enabled'] = self.notif_var.get()

            self.data_manager.save_config()

            tk.messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to save settings: {e}")

    def cleanup_data(self):
        """Clean up old data"""
        if tk.messagebox.askyesno("Confirm", "Delete data older than 30 days?"):
            self.data_manager.cleanup_old_data(30)
            tk.messagebox.showinfo("Success", "Old data cleaned up successfully!")
