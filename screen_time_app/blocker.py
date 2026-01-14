"""
App Blocker Module
Blocks or limits access to specific applications
"""

import psutil
import platform
import subprocess
from datetime import datetime
from tkinter import messagebox


class AppBlocker:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.system = platform.system()
        self.blocked_apps = set()
        self.limited_apps = {}  # {app_name: limit_seconds}
        self.warning_shown = {}  # Track if warning already shown
        self.load_rules()

    def load_rules(self):
        """Load blocking and limiting rules"""
        rules = self.data_manager.get_blocker_rules()
        self.blocked_apps = set(rules.get('blocked', []))
        self.limited_apps = rules.get('limited', {})

    def save_rules(self):
        """Save blocking and limiting rules"""
        rules = {
            'blocked': list(self.blocked_apps),
            'limited': self.limited_apps
        }
        self.data_manager.save_blocker_rules(rules)

    def add_blocked_app(self, app_name):
        """Add an app to the block list"""
        self.blocked_apps.add(app_name)
        self.save_rules()

    def remove_blocked_app(self, app_name):
        """Remove an app from the block list"""
        self.blocked_apps.discard(app_name)
        self.save_rules()

    def add_limited_app(self, app_name, limit_seconds):
        """Add an app time limit"""
        self.limited_apps[app_name] = limit_seconds
        self.save_rules()

    def remove_limited_app(self, app_name):
        """Remove an app time limit"""
        self.limited_apps.pop(app_name, None)
        self.save_rules()

    def check_and_block(self):
        """Check for blocked/limited apps and take action"""
        today = datetime.now().strftime("%Y-%m-%d")

        # Check blocked apps
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                app_name = proc.info['name']

                # Block completely blocked apps
                if app_name in self.blocked_apps:
                    self._block_process(proc, app_name, "This app is blocked")

                # Check limited apps
                elif app_name in self.limited_apps:
                    app_data = self.data_manager.get_app_data(today, app_name)
                    used_seconds = app_data.get('total_seconds', 0)
                    limit_seconds = self.limited_apps[app_name]

                    if used_seconds >= limit_seconds:
                        self._block_process(proc, app_name, f"Time limit reached ({self._format_time(limit_seconds)})")
                    elif used_seconds >= limit_seconds * 0.9:  # 90% of limit
                        # Show warning at 90%
                        if app_name not in self.warning_shown:
                            remaining = limit_seconds - used_seconds
                            self._show_warning(app_name, remaining)
                            self.warning_shown[app_name] = True

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def _block_process(self, process, app_name, reason):
        """Block/kill a process"""
        try:
            # Show notification
            if self.system == "Windows":
                # On Windows, minimize or close the window
                try:
                    import win32gui
                    import win32con

                    def enum_windows_callback(hwnd, results):
                        if win32gui.IsWindowVisible(hwnd):
                            _, pid = win32process.GetWindowThreadProcessId(hwnd)
                            if pid == process.info['pid']:
                                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                        return True

                    win32gui.EnumWindows(enum_windows_callback, None)
                except:
                    pass

            # Try to terminate the process
            process.terminate()

            # Show system notification
            self._show_notification(f"{app_name} blocked", reason)

        except Exception as e:
            print(f"Could not block {app_name}: {e}")

    def _show_notification(self, title, message):
        """Show a system notification"""
        try:
            if self.system == "Windows":
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=5, threaded=True)
            elif self.system == "Linux":
                subprocess.run(['notify-send', title, message])
            elif self.system == "Darwin":
                subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'])
        except Exception as e:
            print(f"Notification error: {e}")

    def _show_warning(self, app_name, remaining_seconds):
        """Show warning when approaching time limit"""
        message = f"You have {self._format_time(remaining_seconds)} remaining for {app_name}"
        self._show_notification("Time Limit Warning", message)

    def _format_time(self, seconds):
        """Format seconds to readable time"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"

    def is_blocked(self, app_name):
        """Check if an app is blocked"""
        return app_name in self.blocked_apps

    def get_limit(self, app_name):
        """Get time limit for an app"""
        return self.limited_apps.get(app_name)

    def get_all_rules(self):
        """Get all blocking rules"""
        return {
            'blocked': list(self.blocked_apps),
            'limited': self.limited_apps
        }
