#!/usr/bin/env python3
"""
Screen Time Tracker - Take Time Back
A desktop application to track, limit, and control screen time usage.
Inspired by Stayfree and Freedom apps.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys
from datetime import datetime, timedelta
from pathlib import Path

from tracker import TimeTracker
from blocker import AppBlocker
from data_manager import DataManager
from ui_components import DashboardFrame, StatisticsFrame, BlockerFrame, SettingsFrame


class ScreenTimeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Take Time Back - Screen Time Tracker")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)

        # Initialize components
        self.data_manager = DataManager()
        self.tracker = TimeTracker(self.data_manager)
        self.blocker = AppBlocker(self.data_manager)

        # Set up UI
        self.setup_ui()

        # Start tracking
        self.tracking_thread = None
        self.is_tracking = True
        self.start_tracking()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        """Set up the main UI components"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')

        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="⏱ Take Time Back",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)

        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create frames for each tab
        self.dashboard_frame = DashboardFrame(self.notebook, self.data_manager, self.tracker)
        self.statistics_frame = StatisticsFrame(self.notebook, self.data_manager)
        self.blocker_frame = BlockerFrame(self.notebook, self.blocker, self.data_manager)
        self.settings_frame = SettingsFrame(self.notebook, self.data_manager)

        # Add tabs
        self.notebook.add(self.dashboard_frame, text="  Dashboard  ")
        self.notebook.add(self.statistics_frame, text="  Statistics  ")
        self.notebook.add(self.blocker_frame, text="  Blocker  ")
        self.notebook.add(self.settings_frame, text="  Settings  ")

        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Tracking active",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#ecf0f1"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def start_tracking(self):
        """Start the tracking thread"""
        def track():
            while self.is_tracking:
                try:
                    self.tracker.update()
                    self.blocker.check_and_block()

                    # Update UI every 5 seconds
                    if hasattr(self, 'dashboard_frame'):
                        self.root.after(0, self.dashboard_frame.update_display)

                except Exception as e:
                    print(f"Tracking error: {e}")

                # Wait 5 seconds before next update
                for _ in range(50):  # 50 * 0.1 = 5 seconds
                    if not self.is_tracking:
                        break
                    threading.Event().wait(0.1)

        self.tracking_thread = threading.Thread(target=track, daemon=True)
        self.tracking_thread.start()

    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit? Tracking will stop."):
            self.is_tracking = False
            self.tracker.save_data()
            self.root.destroy()


def main():
    root = tk.Tk()
    app = ScreenTimeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
