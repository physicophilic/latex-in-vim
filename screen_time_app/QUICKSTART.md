# Quick Start Guide

Get up and running with Take Time Back in 5 minutes!

## Installation (One-Time Setup)

### 🐧 Linux
```bash
cd screen_time_app
pip3 install -r requirements.txt
sudo apt-get install xdotool  # Ubuntu/Debian
./run.sh
```

### 🪟 Windows
```cmd
cd screen_time_app
pip install -r requirements.txt
run.bat
```

### 🍎 macOS
```bash
cd screen_time_app
pip3 install -r requirements.txt
pip3 install pyobjc-framework-Cocoa
python3 main.py
```

## First Steps

### 1. Let it Track (Day 1-3)
- Just open the app and minimize it
- Let it track for a few days to understand your habits
- Check the Dashboard to see which apps you use most

### 2. Set a Goal (Day 4)
- Go to **Settings** tab
- Set your daily screen time goal
- Start with your current average (check Statistics)
- Aim to reduce by 15-30 minutes per week

### 3. Block Distractions (Day 5+)
- Go to **Blocker** tab
- Click "+ Add Blocked App"
- Enter apps you want to avoid (e.g., "Instagram.exe", "facebook.com")
- OR set time limits (e.g., 1 hour for social media)

## Common Use Cases

### "I spend too much time on social media"
1. Track for 3 days to see your baseline
2. Set time limits:
   - Facebook: 30 minutes
   - Instagram: 30 minutes
   - Twitter: 20 minutes
3. Monitor your progress in Statistics

### "I get distracted while working"
1. Block social media apps during work hours
   - Add to blocked list before starting work
   - Remove from list during breaks
2. Set limits on chat apps (Discord, Slack)
3. Check Dashboard to stay aware

### "I want better digital habits"
1. Set a daily goal (start with 5 hours)
2. Review weekly statistics every Sunday
3. Reduce goal by 15 minutes each week
4. Celebrate when you hit your targets!

## Pro Tips

- **Finding app names**: Run the app for 5 minutes, open various apps, then check the Dashboard to see their exact names
- **Emergency override**: Close the tracker app if you need unrestricted access
- **Backup data**: Your data is in `~/.screen_time_tracker/` - backup this folder
- **Start small**: Don't block everything at once, focus on your worst habits first

## Keyboard Shortcuts

- **Alt+Tab**: Switch between tabs (after clicking in window)
- **F5**: Refresh current tab
- **Ctrl+Q**: Quit (Linux/Mac)
- **Alt+F4**: Quit (Windows)

## What Gets Tracked?

✅ **Tracked:**
- Active application name
- Time spent in each app
- Window titles
- Daily/weekly totals

❌ **NOT Tracked:**
- Keyboard input
- Mouse movements
- Screenshots
- Web browsing history
- File contents
- Passwords

## Need Help?

Check the full README.md for:
- Detailed feature explanations
- Troubleshooting guide
- Privacy information
- Configuration options

---

**Remember**: The goal isn't to eliminate screen time, but to use it intentionally. Take time back for what matters most to you! 🎯
