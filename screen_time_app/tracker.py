"""
Time Tracker Module
Tracks active window/application usage time
"""

import psutil
import platform
from datetime import datetime, timedelta
from collections import defaultdict


class TimeTracker:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.current_app = None
        self.last_update = datetime.now()
        self.system = platform.system()

        # Get active window function based on OS
        if self.system == "Windows":
            self.get_active_window = self._get_active_window_windows
        elif self.system == "Linux":
            self.get_active_window = self._get_active_window_linux
        elif self.system == "Darwin":  # macOS
            self.get_active_window = self._get_active_window_macos
        else:
            self.get_active_window = self._get_active_window_fallback

    def _get_active_window_windows(self):
        """Get active window on Windows"""
        try:
            import win32gui
            import win32process

            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)

            return {
                'name': process.name(),
                'title': win32gui.GetWindowText(hwnd),
                'pid': pid
            }
        except Exception as e:
            return None

    def _get_active_window_linux(self):
        """Get active window on Linux"""
        try:
            import subprocess

            # Try using xdotool
            window_id = subprocess.check_output(['xdotool', 'getactivewindow']).decode().strip()
            window_pid = subprocess.check_output(['xdotool', 'getwindowpid', window_id]).decode().strip()
            window_name = subprocess.check_output(['xdotool', 'getwindowname', window_id]).decode().strip()

            process = psutil.Process(int(window_pid))

            return {
                'name': process.name(),
                'title': window_name,
                'pid': int(window_pid)
            }
        except Exception as e:
            return None

    def _get_active_window_macos(self):
        """Get active window on macOS"""
        try:
            from AppKit import NSWorkspace

            active_app = NSWorkspace.sharedWorkspace().activeApplication()

            return {
                'name': active_app['NSApplicationName'],
                'title': active_app.get('NSApplicationBundleIdentifier', ''),
                'pid': active_app['NSApplicationProcessIdentifier']
            }
        except Exception as e:
            return None

    def _get_active_window_fallback(self):
        """Fallback method - track all running processes"""
        try:
            # Just get the process with highest CPU usage as a fallback
            processes = [(p.info['name'], p.info['cpu_percent'])
                        for p in psutil.process_iter(['name', 'cpu_percent'])]
            processes.sort(key=lambda x: x[1], reverse=True)

            if processes:
                return {
                    'name': processes[0][0],
                    'title': 'Unknown',
                    'pid': 0
                }
            return None
        except Exception as e:
            return None

    def update(self):
        """Update tracking data"""
        now = datetime.now()
        time_delta = (now - self.last_update).total_seconds()

        # Get current active window
        active_window = self.get_active_window()

        if active_window and time_delta < 60:  # Only count if less than 60 seconds passed
            app_name = active_window['name']

            # Update today's data
            today = now.strftime("%Y-%m-%d")
            app_data = self.data_manager.get_app_data(today, app_name)

            app_data['total_seconds'] = app_data.get('total_seconds', 0) + time_delta
            app_data['last_active'] = now.isoformat()
            app_data['title'] = active_window.get('title', '')

            self.data_manager.update_app_data(today, app_name, app_data)
            self.current_app = app_name

        self.last_update = now

    def get_today_usage(self):
        """Get today's usage statistics"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.data_manager.get_daily_data(today)

    def get_app_usage(self, app_name, days=7):
        """Get usage for a specific app over last N days"""
        usage = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            app_data = self.data_manager.get_app_data(date, app_name)
            usage.append({
                'date': date,
                'seconds': app_data.get('total_seconds', 0)
            })
        return usage

    def get_total_today(self):
        """Get total screen time today"""
        today_data = self.get_today_usage()
        total = sum(app.get('total_seconds', 0) for app in today_data.values())
        return total

    def save_data(self):
        """Save all data"""
        self.data_manager.save()
