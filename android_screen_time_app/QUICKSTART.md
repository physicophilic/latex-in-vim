# Quick Start - Android Screen Time Tracker

Get the app running in 5 minutes!

## 🚀 Install & Run

### Option 1: Android Studio (Recommended)

```bash
1. Open Android Studio
2. File > Open > Select "android_screen_time_app" folder
3. Wait for Gradle sync
4. Click the "Run" button (green triangle)
5. Select your device/emulator
```

### Option 2: Command Line

```bash
cd android_screen_time_app

# Build and install
./gradlew installDebug

# Run on device
adb shell am start -n com.taketimeback.screentime/.ui.MainActivity
```

## ⚙️ First Time Setup (2 minutes)

### Step 1: Grant Usage Permission
When you open the app:
1. Tap **"Grant Permission"** button
2. Find **"Take Time Back"** in the settings list
3. Toggle it **ON**
4. Press back button to return to app

**Why needed**: Android requires explicit permission to access app usage statistics.

### Step 2: Start Using
That's it! The app will immediately start tracking your app usage.

## 📱 How to Use

### View Your Usage
- Open the **Dashboard** tab
- See today's total screen time
- View list of apps with time spent

### Block an App
1. Go to **Blocker** tab
2. Tap **"+"** in "Blocked Apps" section
3. Enter:
   - **App Name**: "Instagram" (or any name you want)
   - **Package Name**: "com.instagram.android" (see below)
4. Tap **"Block"**

**Finding Package Names:**
- Look at the Dashboard - package names show below each app
- Or google: "facebook android package name"

### Set a Time Limit
1. Go to **Blocker** tab
2. Tap **"+"** in "Time Limits" section
3. Enter app details and time (e.g., 1 hour 30 minutes)
4. Tap **"Set Limit"**

At 90%: You get a warning notification
At 100%: App is automatically blocked

## 🎯 Quick Blocking Examples

### Block Social Media
```
Instagram
└─ com.instagram.android

Facebook
└─ com.facebook.katana

TikTok
└─ com.zhiliaoapp.musically

Twitter/X
└─ com.twitter.android
```

### Limit YouTube
```
App: YouTube
Package: com.google.android.youtube
Limit: 1 hour 0 minutes
```

## 🔧 Troubleshooting

### "Not tracking any apps"
→ Grant usage access permission (see Step 1)

### "Blocked app still opens"
→ Grant "Display over other apps" permission:
  1. Settings > Apps > Take Time Back
  2. Display over other apps > Allow

### "Services stop after screen off"
→ Disable battery optimization:
  1. Settings > Apps > Take Time Back > Battery
  2. Select "Unrestricted"

## 📦 Building APK

Want to share with friends?

```bash
cd android_screen_time_app
./gradlew assembleDebug

# APK location:
# app/build/outputs/apk/debug/app-debug.apk
```

Install on other devices:
```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```

## 🎨 Features Overview

| Feature | What it does |
|---------|--------------|
| **Dashboard** | Shows today's usage in real-time |
| **Statistics** | View 7-day or 30-day summaries |
| **Blocked Apps** | Completely prevent app from opening |
| **Time Limits** | Block app after X hours/minutes |
| **Auto-start** | Continues tracking after reboot |

## 💡 Pro Tips

1. **Start with tracking only**: Use the app for 2-3 days to understand your habits before blocking anything

2. **Be realistic with limits**: Don't cut from 5 hours to 1 hour immediately - reduce gradually

3. **Find package names easily**: Open an app, wait 30 seconds, check Dashboard

4. **Block strategically**: Focus on your top 3 time-wasting apps first

5. **Check Statistics weekly**: Review your progress every Sunday

## 🔒 Privacy Note

- Everything stays on your device
- No internet connection needed
- No data collection or analytics
- Open source - you can verify!

## ⚡ Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check logcat for debugging: `adb logcat | grep TakeTimeBack`
- Customize the UI in `ui/theme/` folder
- Add features in `service/` or `ui/screens/`

---

**That's it! Start taking your time back today.** ⏱️
