package com.taketimeback.screentime.service

import android.app.*
import android.app.usage.UsageStatsManager
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import com.taketimeback.screentime.R
import com.taketimeback.screentime.ScreenTimeApp
import com.taketimeback.screentime.data.AppUsageDatabase
import com.taketimeback.screentime.ui.BlockerOverlayActivity
import com.taketimeback.screentime.ui.MainActivity
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.first
import java.util.*

/**
 * Service that monitors running apps and blocks them when limits are exceeded
 */
class AppBlockerService : Service() {

    private val serviceScope = CoroutineScope(Dispatchers.Default + SupervisorJob())
    private lateinit var database: AppUsageDatabase
    private lateinit var usageStatsManager: UsageStatsManager

    private var isMonitoring = false
    private val warningShown = mutableSetOf<String>()

    override fun onCreate() {
        super.onCreate()
        database = AppUsageDatabase.getDatabase(this)
        usageStatsManager = getSystemService(Context.USAGE_STATS_SERVICE) as UsageStatsManager
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_START_MONITORING -> startMonitoring()
            ACTION_STOP_MONITORING -> stopMonitoring()
        }
        return START_STICKY
    }

    private fun startMonitoring() {
        if (isMonitoring) return

        val notification = createNotification()
        startForeground(NOTIFICATION_ID, notification)

        isMonitoring = true
        startMonitoringLoop()
    }

    private fun stopMonitoring() {
        isMonitoring = false
        serviceScope.coroutineContext.cancelChildren()
        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    private fun startMonitoringLoop() {
        serviceScope.launch {
            while (isMonitoring) {
                try {
                    checkAndBlockApps()
                    delay(CHECK_INTERVAL_MS)
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }
    }

    private suspend fun checkAndBlockApps() = withContext(Dispatchers.IO) {
        val currentApp = getCurrentForegroundApp() ?: return@withContext

        // Check if app is in blocked list
        val blockedApps = database.blockedAppDao().getAllBlockedApps().first()
        val isBlocked = blockedApps.any { it.packageName == currentApp && it.enabled }

        if (isBlocked) {
            blockApp(currentApp, "This app is blocked")
            return@withContext
        }

        // Check time limits
        val limits = database.appLimitDao().getAllLimits().first()
        val limitForApp = limits.find { it.packageName == currentApp && it.enabled }

        if (limitForApp != null) {
            val calendar = Calendar.getInstance()
            calendar.set(Calendar.HOUR_OF_DAY, 0)
            calendar.set(Calendar.MINUTE, 0)
            calendar.set(Calendar.SECOND, 0)
            calendar.set(Calendar.MILLISECOND, 0)
            val todayStart = calendar.timeInMillis

            val usageToday = database.appUsageDao()
                .getUsageForApp(currentApp, todayStart)
                .first()
                .sumOf { it.totalTimeMillis }

            when {
                usageToday >= limitForApp.dailyLimitMillis -> {
                    blockApp(currentApp, "Daily time limit reached")
                }
                usageToday >= limitForApp.dailyLimitMillis * 0.9 -> {
                    if (currentApp !in warningShown) {
                        showWarning(currentApp, limitForApp.dailyLimitMillis - usageToday)
                        warningShown.add(currentApp)
                    }
                }
            }
        }
    }

    private fun getCurrentForegroundApp(): String? {
        val endTime = System.currentTimeMillis()
        val startTime = endTime - 1000 // Last 1 second

        val usageStats = usageStatsManager.queryUsageStats(
            UsageStatsManager.INTERVAL_BEST,
            startTime,
            endTime
        )

        return usageStats?.maxByOrNull { it.lastTimeUsed }?.packageName
    }

    private fun blockApp(packageName: String, reason: String) {
        // Launch blocker overlay
        val intent = Intent(this, BlockerOverlayActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            putExtra(EXTRA_PACKAGE_NAME, packageName)
            putExtra(EXTRA_REASON, reason)
        }
        startActivity(intent)

        // Send to home screen
        val homeIntent = Intent(Intent.ACTION_MAIN).apply {
            addCategory(Intent.CATEGORY_HOME)
            flags = Intent.FLAG_ACTIVITY_NEW_TASK
        }
        startActivity(homeIntent)
    }

    private fun showWarning(packageName: String, remainingTimeMillis: Long) {
        val minutes = (remainingTimeMillis / 60000).toInt()

        val notification = NotificationCompat.Builder(this, ScreenTimeApp.CHANNEL_ALERTS)
            .setContentTitle("Time Limit Warning")
            .setContentText("$minutes minutes remaining for this app")
            .setSmallIcon(R.drawable.ic_warning)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .build()

        val notificationManager = getSystemService(NotificationManager::class.java)
        notificationManager.notify(packageName.hashCode(), notification)
    }

    private fun createNotification(): Notification {
        val intent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )

        return NotificationCompat.Builder(this, ScreenTimeApp.CHANNEL_BLOCKER)
            .setContentTitle("App Blocker Active")
            .setContentText("Monitoring for blocked apps")
            .setSmallIcon(R.drawable.ic_notification)
            .setContentIntent(pendingIntent)
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        super.onDestroy()
        isMonitoring = false
        serviceScope.cancel()
    }

    companion object {
        private const val NOTIFICATION_ID = 1002
        private const val CHECK_INTERVAL_MS = 2000L // 2 seconds

        const val ACTION_START_MONITORING = "com.taketimeback.screentime.START_MONITORING"
        const val ACTION_STOP_MONITORING = "com.taketimeback.screentime.STOP_MONITORING"
        const val EXTRA_PACKAGE_NAME = "package_name"
        const val EXTRA_REASON = "reason"

        fun start(context: Context) {
            val intent = Intent(context, AppBlockerService::class.java).apply {
                action = ACTION_START_MONITORING
            }
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                context.startForegroundService(intent)
            } else {
                context.startService(intent)
            }
        }

        fun stop(context: Context) {
            val intent = Intent(context, AppBlockerService::class.java).apply {
                action = ACTION_STOP_MONITORING
            }
            context.startService(intent)
        }
    }
}
