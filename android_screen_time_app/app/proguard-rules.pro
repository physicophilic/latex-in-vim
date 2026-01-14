# Add project specific ProGuard rules here.
# By default, the flags in this file are appended to flags specified
# in /path/to/sdk/tools/proguard/proguard-android.txt

# Keep Room entities and DAOs
-keep class com.taketimeback.screentime.data.** { *; }

# Keep Compose
-keep class androidx.compose.** { *; }

# Keep Kotlin coroutines
-keepnames class kotlinx.coroutines.internal.MainDispatcherFactory {}
-keepnames class kotlinx.coroutines.CoroutineExceptionHandler {}

# Keep service classes
-keep class com.taketimeback.screentime.service.** { *; }
