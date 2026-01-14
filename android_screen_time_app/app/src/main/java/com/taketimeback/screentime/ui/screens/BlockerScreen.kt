package com.taketimeback.screentime.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.taketimeback.screentime.data.*
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

@Composable
fun BlockerScreen() {
    val context = LocalContext.current
    val database = remember { AppUsageDatabase.getDatabase(context) }
    val scope = rememberCoroutineScope()

    var blockedApps by remember { mutableStateOf<List<BlockedAppEntity>>(emptyList()) }
    var limitedApps by remember { mutableStateOf<List<AppLimitEntity>>(emptyList()) }
    var showAddBlockDialog by remember { mutableStateOf(false) }
    var showAddLimitDialog by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        scope.launch {
            blockedApps = database.blockedAppDao().getAllBlockedApps().first()
            limitedApps = database.appLimitDao().getAllLimits().first()
        }
    }

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Text(
                text = "App Blocker & Limits",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
        }

        // Blocked Apps Section
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Blocked Apps",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.SemiBold
                )
                IconButton(onClick = { showAddBlockDialog = true }) {
                    Icon(Icons.Default.Add, "Add blocked app")
                }
            }
        }

        if (blockedApps.isEmpty()) {
            item {
                Card(modifier = Modifier.fillMaxWidth()) {
                    Text(
                        text = "No blocked apps yet",
                        modifier = Modifier.padding(16.dp)
                    )
                }
            }
        } else {
            items(blockedApps) { app ->
                BlockedAppCard(
                    app = app,
                    onDelete = {
                        scope.launch {
                            database.blockedAppDao().deleteBlockedApp(app)
                            blockedApps = database.blockedAppDao().getAllBlockedApps().first()
                        }
                    }
                )
            }
        }

        // Time Limits Section
        item {
            Spacer(modifier = Modifier.height(16.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Time Limits",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.SemiBold
                )
                IconButton(onClick = { showAddLimitDialog = true }) {
                    Icon(Icons.Default.Add, "Add time limit")
                }
            }
        }

        if (limitedApps.isEmpty()) {
            item {
                Card(modifier = Modifier.fillMaxWidth()) {
                    Text(
                        text = "No time limits set",
                        modifier = Modifier.padding(16.dp)
                    )
                }
            }
        } else {
            items(limitedApps) { limit ->
                LimitedAppCard(
                    limit = limit,
                    onDelete = {
                        scope.launch {
                            database.appLimitDao().deleteLimit(limit)
                            limitedApps = database.appLimitDao().getAllLimits().first()
                        }
                    }
                )
            }
        }
    }

    if (showAddBlockDialog) {
        AddBlockedAppDialog(
            onDismiss = { showAddBlockDialog = false },
            onConfirm = { packageName, appName ->
                scope.launch {
                    database.blockedAppDao().insertBlockedApp(
                        BlockedAppEntity(packageName, appName, true)
                    )
                    blockedApps = database.blockedAppDao().getAllBlockedApps().first()
                    showAddBlockDialog = false
                }
            }
        )
    }

    if (showAddLimitDialog) {
        AddLimitDialog(
            onDismiss = { showAddLimitDialog = false },
            onConfirm = { packageName, appName, hours, minutes ->
                scope.launch {
                    val limitMillis = (hours * 60L + minutes) * 60L * 1000L
                    database.appLimitDao().insertLimit(
                        AppLimitEntity(packageName, appName, limitMillis, true)
                    )
                    limitedApps = database.appLimitDao().getAllLimits().first()
                    showAddLimitDialog = false
                }
            }
        )
    }
}

@Composable
fun BlockedAppCard(
    app: BlockedAppEntity,
    onDelete: () -> Unit
) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = app.appName,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold
                )
                Text(
                    text = app.packageName,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            IconButton(onClick = onDelete) {
                Icon(Icons.Default.Delete, "Delete")
            }
        }
    }
}

@Composable
fun LimitedAppCard(
    limit: AppLimitEntity,
    onDelete: () -> Unit
) {
    val hours = limit.dailyLimitMillis / (1000 * 60 * 60)
    val minutes = (limit.dailyLimitMillis % (1000 * 60 * 60)) / (1000 * 60)
    val timeText = if (hours > 0) "${hours}h ${minutes}m" else "${minutes}m"

    Card(modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = limit.appName,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold
                )
                Text(
                    text = "Limit: $timeText",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.primary
                )
            }
            IconButton(onClick = onDelete) {
                Icon(Icons.Default.Delete, "Delete")
            }
        }
    }
}

@Composable
fun AddBlockedAppDialog(
    onDismiss: () -> Unit,
    onConfirm: (String, String) -> Unit
) {
    var packageName by remember { mutableStateOf("") }
    var appName by remember { mutableStateOf("") }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Block App") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedTextField(
                    value = appName,
                    onValueChange = { appName = it },
                    label = { Text("App Name") },
                    singleLine = true
                )
                OutlinedTextField(
                    value = packageName,
                    onValueChange = { packageName = it },
                    label = { Text("Package Name") },
                    placeholder = { Text("com.example.app") },
                    singleLine = true
                )
            }
        },
        confirmButton = {
            Button(
                onClick = { onConfirm(packageName, appName) },
                enabled = packageName.isNotBlank() && appName.isNotBlank()
            ) {
                Text("Block")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}

@Composable
fun AddLimitDialog(
    onDismiss: () -> Unit,
    onConfirm: (String, String, Int, Int) -> Unit
) {
    var packageName by remember { mutableStateOf("") }
    var appName by remember { mutableStateOf("") }
    var hours by remember { mutableStateOf("1") }
    var minutes by remember { mutableStateOf("0") }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Set Time Limit") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedTextField(
                    value = appName,
                    onValueChange = { appName = it },
                    label = { Text("App Name") },
                    singleLine = true
                )
                OutlinedTextField(
                    value = packageName,
                    onValueChange = { packageName = it },
                    label = { Text("Package Name") },
                    placeholder = { Text("com.example.app") },
                    singleLine = true
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        value = hours,
                        onValueChange = { hours = it.filter { c -> c.isDigit() } },
                        label = { Text("Hours") },
                        modifier = Modifier.weight(1f),
                        singleLine = true
                    )
                    OutlinedTextField(
                        value = minutes,
                        onValueChange = { minutes = it.filter { c -> c.isDigit() } },
                        label = { Text("Minutes") },
                        modifier = Modifier.weight(1f),
                        singleLine = true
                    )
                }
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    val h = hours.toIntOrNull() ?: 0
                    val m = minutes.toIntOrNull() ?: 0
                    onConfirm(packageName, appName, h, m)
                },
                enabled = packageName.isNotBlank() && appName.isNotBlank()
            ) {
                Text("Set Limit")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}
