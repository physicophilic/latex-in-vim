package com.taketimeback.screentime

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build

class ScreenTimeApp : Application() {

    override fun onCreate() {
        super.onCreate()
        instance = this
        createNotificationChannels()
    }

    private fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val notificationManager = getSystemService(NotificationManager::class.java)

            // Tracking Service Channel
            val trackingChannel = NotificationChannel(
                CHANNEL_TRACKING,
                "Screen Time Tracking",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Persistent notification for screen time tracking"
                setShowBadge(false)
            }

            // Blocker Service Channel
            val blockerChannel = NotificationChannel(
                CHANNEL_BLOCKER,
                "App Blocker",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Notifications for app blocking events"
                setShowBadge(false)
            }

            // Alerts Channel
            val alertsChannel = NotificationChannel(
                CHANNEL_ALERTS,
                "Time Limit Alerts",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Alerts when approaching or exceeding time limits"
                setShowBadge(true)
            }

            notificationManager.createNotificationChannels(
                listOf(trackingChannel, blockerChannel, alertsChannel)
            )
        }
    }

    companion object {
        lateinit var instance: ScreenTimeApp
            private set

        const val CHANNEL_TRACKING = "tracking_channel"
        const val CHANNEL_BLOCKER = "blocker_channel"
        const val CHANNEL_ALERTS = "alerts_channel"
    }
}
