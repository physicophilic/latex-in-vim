"""
Data Manager Module
Handles all data storage and retrieval
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict


class DataManager:
    def __init__(self):
        self.data_dir = Path.home() / ".screen_time_tracker"
        self.data_dir.mkdir(exist_ok=True)

        self.data_file = self.data_dir / "usage_data.json"
        self.config_file = self.data_dir / "config.json"
        self.blocker_file = self.data_dir / "blocker_rules.json"

        self.data = self.load_data()
        self.config = self.load_config()

    def load_data(self):
        """Load usage data from file"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading data: {e}")
                return {}
        return {}

    def save(self):
        """Save usage data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_config(self):
        """Load configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self._default_config()
        return self._default_config()

    def save_config(self):
        """Save configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def _default_config(self):
        """Default configuration"""
        return {
            'daily_goal_seconds': 14400,  # 4 hours
            'notifications_enabled': True,
            'auto_start': False,
            'theme': 'light',
            'tracking_interval': 5
        }

    def get_app_data(self, date, app_name):
        """Get data for a specific app on a specific date"""
        if date not in self.data:
            self.data[date] = {}
        if app_name not in self.data[date]:
            self.data[date][app_name] = {
                'total_seconds': 0,
                'last_active': None,
                'title': ''
            }
        return self.data[date][app_name]

    def update_app_data(self, date, app_name, app_data):
        """Update data for a specific app"""
        if date not in self.data:
            self.data[date] = {}
        self.data[date][app_name] = app_data

    def get_daily_data(self, date):
        """Get all data for a specific date"""
        return self.data.get(date, {})

    def get_date_range_data(self, start_date, end_date):
        """Get data for a date range"""
        result = {}
        current = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            result[date_str] = self.get_daily_data(date_str)
            current += timedelta(days=1)

        return result

    def get_top_apps(self, date, limit=10):
        """Get top apps by usage for a specific date"""
        daily_data = self.get_daily_data(date)
        apps = [(app, data.get('total_seconds', 0)) for app, data in daily_data.items()]
        apps.sort(key=lambda x: x[1], reverse=True)
        return apps[:limit]

    def get_weekly_summary(self):
        """Get summary for the last 7 days"""
        summary = {
            'total_seconds': 0,
            'daily_average': 0,
            'top_apps': defaultdict(int),
            'days': []
        }

        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            daily_data = self.get_daily_data(date)

            daily_total = sum(app.get('total_seconds', 0) for app in daily_data.values())
            summary['days'].append({
                'date': date,
                'total_seconds': daily_total
            })

            for app_name, app_data in daily_data.items():
                summary['top_apps'][app_name] += app_data.get('total_seconds', 0)

            summary['total_seconds'] += daily_total

        summary['daily_average'] = summary['total_seconds'] / 7
        summary['top_apps'] = sorted(summary['top_apps'].items(), key=lambda x: x[1], reverse=True)[:5]

        return summary

    def get_blocker_rules(self):
        """Load blocker rules"""
        if self.blocker_file.exists():
            try:
                with open(self.blocker_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading blocker rules: {e}")
                return {'blocked': [], 'limited': {}}
        return {'blocked': [], 'limited': {}}

    def save_blocker_rules(self, rules):
        """Save blocker rules"""
        try:
            with open(self.blocker_file, 'w') as f:
                json.dump(rules, f, indent=2)
        except Exception as e:
            print(f"Error saving blocker rules: {e}")

    def cleanup_old_data(self, days=30):
        """Remove data older than N days"""
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        dates_to_remove = [date for date in self.data.keys() if date < cutoff_date]

        for date in dates_to_remove:
            del self.data[date]

        if dates_to_remove:
            self.save()
