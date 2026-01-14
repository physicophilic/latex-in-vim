# How to Build the APK

Building Android APKs requires the Android SDK. Here are your options:

## Option 1: Build on Your Computer (Recommended) ⭐

### Prerequisites:
- **Android Studio** (recommended): [Download here](https://developer.android.com/studio)
- **OR Command Line Tools**: Java 17 + Android SDK

### Method A: Using Android Studio (Easiest)

1. **Install Android Studio**
   - Download from https://developer.android.com/studio
   - Install and complete the setup wizard

2. **Clone & Open Project**
   ```bash
   git clone <your-repo-url>
   cd android_screen_time_app
   ```
   - Open Android Studio
   - File > Open > Select `android_screen_time_app` folder
   - Wait for Gradle sync (may take 2-5 minutes first time)

3. **Build APK**
   - Build > Build Bundle(s) / APK(s) > Build APK(s)
   - Wait for build to complete
   - Click "locate" in the notification
   - APK is at: `app/build/outputs/apk/debug/app-debug.apk`

4. **Install on Phone**
   - Connect phone via USB (enable USB debugging)
   - Run > Run 'app'
   - OR copy APK to phone and install manually

### Method B: Using Command Line

1. **Install Requirements**
   ```bash
   # Install Java 17 (if not installed)
   # Ubuntu/Debian:
   sudo apt install openjdk-17-jdk

   # Mac:
   brew install openjdk@17

   # Windows: Download from Oracle or Adoptium
   ```

2. **Install Android SDK Command Line Tools**
   - Download from: https://developer.android.com/studio#command-tools
   - Extract and set ANDROID_HOME environment variable

   ```bash
   # Linux/Mac:
   export ANDROID_HOME=$HOME/Android/Sdk
   export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
   export PATH=$PATH:$ANDROID_HOME/platform-tools

   # Windows (PowerShell):
   $env:ANDROID_HOME = "C:\Users\YourName\AppData\Local\Android\Sdk"
   $env:PATH += ";$env:ANDROID_HOME\cmdline-tools\latest\bin"
   ```

3. **Install Android SDK Components**
   ```bash
   sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"
   sdkmanager --licenses  # Accept all licenses
   ```

4. **Build APK**
   ```bash
   cd android_screen_time_app
   ./gradlew assembleDebug

   # APK will be at:
   # app/build/outputs/apk/debug/app-debug.apk
   ```

## Option 2: Use GitHub Actions (Automated) 🤖

I've created a GitHub Actions workflow that automatically builds the APK when you push code!

### How to Use:

1. **Push code to GitHub**
   ```bash
   git push origin claude/screen-time-app-W7v68
   ```

2. **Wait for build** (2-5 minutes)
   - Go to your repository on GitHub
   - Click "Actions" tab
   - Click on the latest workflow run
   - Wait for green checkmark ✅

3. **Download APK**
   - Scroll to "Artifacts" section at bottom
   - Click "TakeTimeBack-debug" to download ZIP
   - Extract the APK from the ZIP file

### Manual Trigger:
- Go to Actions > "Build Android APK" workflow
- Click "Run workflow" button
- Select branch and click "Run workflow"

## Option 3: Use Online Build Services

### Appetize.io (Test without installing):
- Upload project to Appetize.io
- Test in browser on virtual device

### GitHub Codespaces:
- Open repository in Codespaces
- Install Android SDK in the container
- Build APK remotely

## Installing the APK on Your Phone

### Method 1: Direct USB Install
```bash
# With phone connected:
adb install app/build/outputs/apk/debug/app-debug.apk
```

### Method 2: Manual Install
1. Copy APK to phone (email, Google Drive, USB transfer)
2. On phone: Settings > Security > Enable "Install from Unknown Sources"
3. Open file manager, tap APK file
4. Tap "Install"
5. Open "Take Time Back" app

### Method 3: Via Android Studio
- Connect phone with USB debugging enabled
- Click Run button in Android Studio
- Select your device
- App installs and launches automatically

## Troubleshooting

### "Gradle sync failed"
- Ensure you have Java 17 installed
- Check your internet connection (downloads dependencies)
- Try: File > Invalidate Caches and Restart

### "Android SDK not found"
- Set ANDROID_HOME environment variable
- Install Android SDK via Android Studio or command line tools

### "Build failed: compileSdkVersion"
- Open SDK Manager in Android Studio
- Install Android API 34

### "gradlew: Permission denied"
```bash
chmod +x gradlew
./gradlew assembleDebug
```

### Build takes forever
- First build downloads ~500MB of dependencies
- Subsequent builds are much faster (30-60 seconds)

## APK Size & Info

- **Debug APK**: ~15-25 MB
- **Release APK** (optimized): ~8-12 MB
- **Min Android**: 8.0 (API 26)
- **Target Android**: 14 (API 34)

## Building Release APK (Optional)

For a smaller, optimized APK:

1. **Create keystore**
   ```bash
   keytool -genkey -v -keystore release.keystore -alias release \
           -keyalg RSA -keysize 2048 -validity 10000
   ```

2. **Configure signing** (add to `app/build.gradle.kts`):
   ```kotlin
   android {
       signingConfigs {
           create("release") {
               storeFile = file("../release.keystore")
               storePassword = "your-password"
               keyAlias = "release"
               keyPassword = "your-password"
           }
       }
       buildTypes {
           release {
               signingConfig = signingConfigs.getByName("release")
           }
       }
   }
   ```

3. **Build**
   ```bash
   ./gradlew assembleRelease
   # Output: app/build/outputs/apk/release/app-release.apk
   ```

## Quick Summary

**Fastest way**: Install Android Studio, open project, click Build > Build APK

**No installation**: Use GitHub Actions workflow (already set up!)

**Command line**: Install Android SDK + Java 17, run `./gradlew assembleDebug`

---

Need help? Check the [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md)
