# Take Time Back - Screen Time Tracker

A powerful desktop application to track, monitor, and control your screen time. Inspired by apps like Stayfree and Freedom, Take Time Back helps you develop healthier digital habits.

## Features

### 📊 Real-Time Tracking
- Automatically tracks active application usage
- Records time spent in each application
- Works seamlessly in the background

### 📈 Detailed Statistics
- Daily, weekly, and all-time usage reports
- Visual breakdowns of app usage
- Identify time-consuming applications
- Track your progress over time

### 🚫 App Blocking & Limits
- Completely block distracting applications
- Set daily time limits for specific apps
- Automatic warnings at 90% of limit
- Force-close apps when limits are reached

### 🎯 Goals & Productivity
- Set daily screen time goals
- Track goal achievement
- Visual progress indicators
- Stay accountable to your targets

### 🔔 Smart Notifications
- Time limit warnings
- Goal achievement notifications
- App blocking alerts

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Windows

```bash
# Clone or download this repository
cd screen_time_app

# Install dependencies
pip install -r requirements.txt

# Additional Windows dependencies
pip install pywin32 win10toast

# Run the application
python main.py
```

### Linux

```bash
# Clone or download this repository
cd screen_time_app

# Install dependencies
pip install -r requirements.txt

# Install xdotool (required for window tracking)
sudo apt-get install xdotool  # Ubuntu/Debian
# OR
sudo dnf install xdotool      # Fedora
# OR
sudo pacman -S xdotool        # Arch

# Run the application
python main.py
```

### macOS

```bash
# Clone or download this repository
cd screen_time_app

# Install dependencies
pip install -r requirements.txt

# Install additional macOS dependencies
pip install pyobjc-framework-Cocoa

# Run the application
python main.py
```

## Usage

### Starting the App

Simply run:
```bash
python main.py
```

The app will start tracking immediately and display a window with multiple tabs.

### Dashboard Tab
- View today's total screen time
- See progress toward your daily goal
- Browse top applications by usage
- Real-time updates every 5 seconds

### Statistics Tab
- View reports for 7 days, 30 days, or all time
- See daily breakdowns
- Identify usage patterns
- Export data for analysis

### Blocker Tab
- **Block Apps**: Add applications to completely block
  - Click "+ Add Blocked App"
  - Enter the application name (e.g., "chrome.exe", "firefox", "Instagram")
  - The app will be force-closed when detected

- **Time Limits**: Set daily time limits for apps
  - Click "+ Add Time Limit"
  - Enter application name and time limit
  - Receive warnings at 90% usage
  - App automatically blocked when limit reached

### Settings Tab
- **Daily Goal**: Set your target screen time
  - Enter hours and minutes
  - Default is 4 hours (240 minutes)

- **Notifications**: Enable/disable system notifications

- **Data Management**: Clean up old tracking data

## Application Names

To block or limit apps, you need to know their process names:

### Common Application Names

**Windows:**
- Chrome: `chrome.exe`
- Firefox: `firefox.exe`
- Edge: `msedge.exe`
- Instagram (app): `Instagram.exe`
- Facebook: `Facebook.exe`
- Discord: `Discord.exe`
- Slack: `Slack.exe`

**Linux:**
- Chrome: `chrome`
- Firefox: `firefox`
- VS Code: `code`

**macOS:**
- Chrome: `Google Chrome`
- Firefox: `Firefox`
- Safari: `Safari`

**Tip**: Run the app for a few minutes and check the Dashboard to see the exact names of applications being tracked.

## Data Storage

All data is stored locally in your home directory:
- **Location**: `~/.screen_time_tracker/`
- **Files**:
  - `usage_data.json` - All usage tracking data
  - `config.json` - Application settings
  - `blocker_rules.json` - Blocking and limit rules

Your data never leaves your computer.

## Features in Detail

### Time Tracking
The app tracks your active window every 5 seconds. If you switch between applications, the time is accurately recorded for each app. Idle time (no activity for 60+ seconds) is not counted.

### App Blocking
When an app is blocked or reaches its limit:
1. The application is minimized (Windows)
2. The process is terminated
3. You receive a notification
4. The app will be blocked again if you try to restart it

### Goals
Set realistic daily goals to develop healthier habits:
- Start with your current average usage
- Gradually reduce by 15-30 minutes per week
- Track your progress over time
- Celebrate milestones

## Troubleshooting

### App not tracking on Linux
- Ensure `xdotool` is installed
- Check X11 permissions
- Try running with `sudo` (not recommended for regular use)

### App not blocking on Windows
- Run as Administrator for full blocking capabilities
- Some system processes cannot be blocked

### High CPU usage
- Normal usage is <1% CPU
- Check if tracking interval is too frequent
- Restart the application

## Privacy

Take Time Back is completely private:
- All data stored locally
- No internet connection required
- No analytics or tracking
- Open source code for transparency

## Contributing

This is a self-contained application. Feel free to modify and extend:
- `main.py` - Application entry point
- `tracker.py` - Time tracking logic
- `blocker.py` - App blocking functionality
- `data_manager.py` - Data storage and retrieval
- `ui_components.py` - User interface

## License

MIT License - Free to use and modify

## Tips for Success

1. **Start with tracking only** - Use the app for a week to understand your habits
2. **Set realistic goals** - Don't try to cut screen time in half immediately
3. **Block strategically** - Focus on your most distracting apps
4. **Review weekly** - Check statistics every Sunday to plan improvements
5. **Be consistent** - Use the app daily for best results
6. **Adjust limits** - Fine-tune time limits based on your needs
7. **Take breaks** - Remember to step away from the screen regularly

## Support

For issues or questions:
- Check the troubleshooting section above
- Review your data files in `~/.screen_time_tracker/`
- Restart the application

---

Take control of your digital life. Take time back.
