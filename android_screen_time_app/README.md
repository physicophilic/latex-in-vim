# Take Time Back - Android Screen Time Tracker

A native Android app to track, monitor, and control your screen time. Built with modern Android development practices using Kotlin, Jetpack Compose, and Material Design 3.

## Features

### 📊 Real-Time Usage Tracking
- Automatically tracks time spent in each app
- Uses Android's UsageStatsManager for accurate tracking
- Updates every 30 seconds in the background
- Persists data locally with Room database

### 🚫 App Blocking
- Completely block distracting apps
- Full-screen blocker overlay when blocked apps are launched
- Automatic redirection to home screen
- Persistent monitoring every 2 seconds

### ⏰ Time Limits
- Set daily time limits for specific apps
- Automatic blocking when limit is reached
- Warning notification at 90% of limit
- Per-app limit configuration

### 📈 Statistics & Reports
- View usage for last 7 days or 30 days
- Total screen time and daily averages
- Per-app breakdowns
- Material Design 3 charts (coming soon)

### 🎨 Modern UI
- Built with Jetpack Compose
- Material Design 3 theming
- Dark mode support
- Dynamic color (Android 12+)
- Clean, intuitive navigation

## Technical Stack

- **Language**: Kotlin
- **UI**: Jetpack Compose + Material Design 3
- **Architecture**: MVVM with Repository pattern
- **Database**: Room (SQLite)
- **Async**: Kotlin Coroutines + Flow
- **Services**: Foreground services for tracking
- **Min SDK**: 26 (Android 8.0)
- **Target SDK**: 34 (Android 14)

## Project Structure

```
app/
├── src/main/java/com/taketimeback/screentime/
│   ├── ScreenTimeApp.kt              # Application class
│   ├── data/
│   │   └── AppUsageDatabase.kt       # Room database, DAOs, entities
│   ├── service/
│   │   ├── UsageTrackingService.kt   # Foreground service for tracking
│   │   └── AppBlockerService.kt      # Foreground service for blocking
│   ├── receiver/
│   │   └── BootReceiver.kt           # Start services on boot
│   └── ui/
│       ├── MainActivity.kt            # Main entry point
│       ├── BlockerOverlayActivity.kt  # Blocking screen
│       ├── screens/
│       │   ├── DashboardScreen.kt     # Dashboard UI
│       │   ├── StatisticsScreen.kt    # Statistics UI
│       │   ├── BlockerScreen.kt       # Blocker config UI
│       │   └── SettingsScreen.kt      # Settings UI
│       └── theme/
│           ├── Theme.kt               # Material theme
│           └── Type.kt                # Typography
```

## Installation

### Prerequisites
- Android Studio Hedgehog (2023.1.1) or later
- Android SDK 34
- Gradle 8.2+

### Build & Install

1. **Clone the repository**
```bash
cd android_screen_time_app
```

2. **Open in Android Studio**
```bash
studio .
# Or: File > Open > Select android_screen_time_app folder
```

3. **Sync Gradle**
   - Android Studio will automatically sync
   - Or: File > Sync Project with Gradle Files

4. **Build the app**
```bash
./gradlew assembleDebug
```

5. **Install on device/emulator**
```bash
./gradlew installDebug
```

Or simply click the "Run" button in Android Studio.

## First Run Setup

### 1. Grant Usage Access Permission
On first launch, the app will request Usage Access permission:

1. Tap "Grant Permission"
2. Find "Take Time Back" in the list
3. Toggle the permission ON
4. Return to the app

**Important**: This permission is required for tracking app usage. Without it, the app cannot function.

### 2. Grant Display Over Other Apps (Optional)
For the blocker feature to work properly:

1. Go to Android Settings > Apps > Take Time Back
2. Navigate to "Display over other apps"
3. Enable the permission

## Usage Guide

### Dashboard Tab
- View today's total screen time
- See list of apps used today with time spent
- Real-time updates every 30 seconds

### Statistics Tab
- Switch between 7-day and 30-day views
- See total time and daily averages
- Charts and detailed breakdowns (coming soon)

### Blocker Tab

**Block Apps Completely:**
1. Tap the "+" icon in Blocked Apps section
2. Enter the app name (e.g., "Instagram")
3. Enter the package name (e.g., "com.instagram.android")
4. Tap "Block"

**Set Time Limits:**
1. Tap the "+" icon in Time Limits section
2. Enter the app name and package name
3. Set hours and minutes
4. Tap "Set Limit"

**Finding Package Names:**
- Check the Dashboard tab - package names are shown below app names
- Or use apps like "App Inspector" from Play Store
- Or use ADB: `adb shell pm list packages | grep <app>`

### Settings Tab
- View app information
- Check permissions
- Privacy policy

## Common Package Names

### Social Media
- Instagram: `com.instagram.android`
- Facebook: `com.facebook.katana`
- Twitter/X: `com.twitter.android`
- TikTok: `com.zhiliaoapp.musically`
- Snapchat: `com.snapchat.android`
- Reddit: `com.reddit.frontpage`

### Messaging
- WhatsApp: `com.whatsapp`
- Telegram: `org.telegram.messenger`
- Discord: `com.discord`

### Video
- YouTube: `com.google.android.youtube`
- Netflix: `com.netflix.mediaclient`
- Prime Video: `com.amazon.avod.thirdpartyclient`

### Games
- Check the Dashboard after opening the game

## Architecture Details

### Services

**UsageTrackingService (Foreground)**
- Queries UsageStatsManager every 30 seconds
- Aggregates daily usage per app
- Stores in Room database
- Shows persistent notification

**AppBlockerService (Foreground)**
- Monitors foreground app every 2 seconds
- Checks against blocked apps list
- Enforces time limits
- Launches blocker overlay when needed

### Database Schema

**app_usage**
- packageName (String)
- appName (String)
- date (Long) - midnight timestamp
- totalTimeMillis (Long)
- lastUsedTimestamp (Long)
- launchCount (Int)

**app_limits**
- packageName (String, Primary Key)
- appName (String)
- dailyLimitMillis (Long)
- enabled (Boolean)

**blocked_apps**
- packageName (String, Primary Key)
- appName (String)
- enabled (Boolean)
- addedTimestamp (Long)

## Permissions Explained

### Required Permissions

**PACKAGE_USAGE_STATS**
- Purpose: Track app usage time
- When: Granted manually in Settings
- Why: Core functionality of the app

**FOREGROUND_SERVICE**
- Purpose: Run tracking in background
- When: Granted automatically
- Why: Continuous monitoring

### Optional Permissions

**POST_NOTIFICATIONS** (Android 13+)
- Purpose: Show time limit warnings
- When: Requested on first use
- Why: Alert users about limits

**RECEIVE_BOOT_COMPLETED**
- Purpose: Start tracking after reboot
- When: Granted automatically
- Why: Automatic startup

**SYSTEM_ALERT_WINDOW**
- Purpose: Show blocker overlay
- When: Granted manually in Settings
- Why: Block apps effectively

## Privacy & Data

### What We Track
- App package names and display names
- Time spent in each app (foreground only)
- Launch counts
- Your configured blocks and limits

### What We DON'T Track
- App content or data
- Notifications
- Keyboard input
- Screenshots or screen content
- Location
- Personal files
- Web browsing history (except browser usage time)

### Data Storage
- All data stored locally on device
- Uses Android Room database (SQLite)
- No cloud sync or backups
- No internet connection required
- No third-party analytics

### Data Location
```
/data/data/com.taketimeback.screentime/databases/screen_time_database
```

## Building for Release

1. **Create keystore**
```bash
keytool -genkey -v -keystore release.keystore -alias release -keyalg RSA -keysize 2048 -validity 10000
```

2. **Configure signing in app/build.gradle.kts**
```kotlin
signingConfigs {
    create("release") {
        storeFile = file("release.keystore")
        storePassword = "your-password"
        keyAlias = "release"
        keyPassword = "your-password"
    }
}
```

3. **Build release APK**
```bash
./gradlew assembleRelease
```

Output: `app/build/outputs/apk/release/app-release.apk`

## Testing

### Manual Testing Checklist
- [ ] Permission request flow
- [ ] Usage tracking after 30 seconds
- [ ] Dashboard displays correct data
- [ ] Statistics calculations accurate
- [ ] Add blocked app
- [ ] Blocked app triggers overlay
- [ ] Add time limit
- [ ] Time limit warning at 90%
- [ ] Time limit blocks at 100%
- [ ] Services restart after device reboot
- [ ] Dark mode switches correctly

### Test Device Requirements
- Android 8.0 (API 26) or higher
- At least 100 MB free storage
- Internet not required

## Troubleshooting

### App not tracking usage
1. Ensure Usage Access permission is granted
2. Check Settings > Apps > Special App Access > Usage Access
3. Restart the app
4. Check if services are running: Settings > Apps > Take Time Back > Running Services

### Blocker not working
1. Grant "Display over other apps" permission
2. Ensure AppBlockerService is running
3. Check if blocked app is in the list
4. Verify package name is correct

### Services stop after phone sleeps
1. Disable battery optimization:
   - Settings > Apps > Take Time Back > Battery
   - Select "Unrestricted"
2. Some OEMs (Xiaomi, Huawei) have aggressive battery management
   - Check dontkillmyapp.com for device-specific instructions

### Database errors
1. Clear app data: Settings > Apps > Take Time Back > Storage > Clear Data
2. Uninstall and reinstall
3. Check logcat for detailed errors

## Known Limitations

1. **Accuracy**: Usage stats update every 30 seconds, not real-time
2. **System Apps**: Cannot block system apps or launcher
3. **Root**: Does not require root, but cannot block without overlay permission
4. **Battery**: Foreground services consume battery (optimized for minimal impact)
5. **Android 14+**: Additional restrictions may apply

## Roadmap

- [ ] Charts and visualizations
- [ ] Export usage data (CSV, JSON)
- [ ] Weekly/monthly reports
- [ ] Focus mode (bulk blocking)
- [ ] Schedule-based blocking
- [ ] App categories
- [ ] Notifications for goal achievement
- [ ] Widget support
- [ ] Tasker/automation integration

## Contributing

This is a standalone project. Feel free to fork and modify for your needs.

## License

MIT License - Free to use and modify

## Support

For issues or questions:
- Check the Troubleshooting section
- Review Android documentation on UsageStatsManager
- Check device-specific battery optimization settings

---

**Take control of your digital life. Take time back.** ⏱️
