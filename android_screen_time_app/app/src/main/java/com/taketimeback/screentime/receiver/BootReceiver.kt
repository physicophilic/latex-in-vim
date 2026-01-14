package com.taketimeback.screentime.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.taketimeback.screentime.service.AppBlockerService
import com.taketimeback.screentime.service.UsageTrackingService

/**
 * Receiver to start services on device boot
 */
class BootReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            // Start tracking and blocker services
            UsageTrackingService.start(context)
            AppBlockerService.start(context)
        }
    }
}
