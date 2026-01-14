package com.taketimeback.screentime.service

import android.app.*
import android.app.usage.UsageStatsManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import com.taketimeback.screentime.R
import com.taketimeback.screentime.ScreenTimeApp
import com.taketimeback.screentime.data.AppUsageDatabase
import com.taketimeback.screentime.data.AppUsageEntity
import com.taketimeback.screentime.ui.MainActivity
import kotlinx.coroutines.*
import java.util.*

/**
 * Foreground service that tracks app usage statistics
 */
class UsageTrackingService : Service() {

    private val serviceScope = CoroutineScope(Dispatchers.Default + SupervisorJob())
    private lateinit var database: AppUsageDatabase
    private lateinit var usageStatsManager: UsageStatsManager
    private lateinit var packageManager: PackageManager

    private var isTracking = false

    override fun onCreate() {
        super.onCreate()
        database = AppUsageDatabase.getDatabase(this)
        usageStatsManager = getSystemService(Context.USAGE_STATS_SERVICE) as UsageStatsManager
        packageManager = this.packageManager
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_START_TRACKING -> startTracking()
            ACTION_STOP_TRACKING -> stopTracking()
        }
        return START_STICKY
    }

    private fun startTracking() {
        if (isTracking) return

        val notification = createNotification()
        startForeground(NOTIFICATION_ID, notification)

        isTracking = true
        startTrackingLoop()
    }

    private fun stopTracking() {
        isTracking = false
        serviceScope.coroutineContext.cancelChildren()
        stopForeground(STOP_FOREGROUND_REMOVE)
        stopSelf()
    }

    private fun startTrackingLoop() {
        serviceScope.launch {
            while (isTracking) {
                try {
                    updateUsageStats()
                    delay(UPDATE_INTERVAL_MS)
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }
    }

    private suspend fun updateUsageStats() = withContext(Dispatchers.IO) {
        val calendar = Calendar.getInstance()
        val endTime = calendar.timeInMillis

        // Get start of today
        calendar.set(Calendar.HOUR_OF_DAY, 0)
        calendar.set(Calendar.MINUTE, 0)
        calendar.set(Calendar.SECOND, 0)
        calendar.set(Calendar.MILLISECOND, 0)
        val startTime = calendar.timeInMillis

        // Query usage stats for today
        val usageStats = usageStatsManager.queryUsageStats(
            UsageStatsManager.INTERVAL_DAILY,
            startTime,
            endTime
        )

        if (usageStats.isNullOrEmpty()) return@withContext

        // Group by package and calculate totals
        val usageMap = usageStats.groupBy { it.packageName }
            .mapValues { (_, stats) ->
                stats.maxByOrNull { it.lastTimeUsed } to stats.sumOf { it.totalTimeInForeground }
            }

        // Save to database
        val usageEntities = usageMap.mapNotNull { (packageName, data) ->
            val (latestStat, totalTime) = data
            if (totalTime > 0 && latestStat != null) {
                try {
                    val appInfo = packageManager.getApplicationInfo(packageName, 0)
                    val appName = packageManager.getApplicationLabel(appInfo).toString()

                    AppUsageEntity(
                        packageName = packageName,
                        appName = appName,
                        date = startTime,
                        totalTimeMillis = totalTime,
                        lastUsedTimestamp = latestStat.lastTimeUsed,
                        launchCount = 0  // Launch count not directly available from UsageStats
                    )
                } catch (e: PackageManager.NameNotFoundException) {
                    null
                }
            } else null
        }

        database.appUsageDao().insertUsages(usageEntities)
    }

    private fun createNotification(): Notification {
        val intent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )

        return NotificationCompat.Builder(this, ScreenTimeApp.CHANNEL_TRACKING)
            .setContentTitle("Take Time Back")
            .setContentText("Tracking your screen time")
            .setSmallIcon(R.drawable.ic_notification)
            .setContentIntent(pendingIntent)
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setCategory(NotificationCompat.CATEGORY_SERVICE)
            .build()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        super.onDestroy()
        isTracking = false
        serviceScope.cancel()
    }

    companion object {
        private const val NOTIFICATION_ID = 1001
        private const val UPDATE_INTERVAL_MS = 30_000L // 30 seconds

        const val ACTION_START_TRACKING = "com.taketimeback.screentime.START_TRACKING"
        const val ACTION_STOP_TRACKING = "com.taketimeback.screentime.STOP_TRACKING"

        fun start(context: Context) {
            val intent = Intent(context, UsageTrackingService::class.java).apply {
                action = ACTION_START_TRACKING
            }
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                context.startForegroundService(intent)
            } else {
                context.startService(intent)
            }
        }

        fun stop(context: Context) {
            val intent = Intent(context, UsageTrackingService::class.java).apply {
                action = ACTION_STOP_TRACKING
            }
            context.startService(intent)
        }
    }
}
