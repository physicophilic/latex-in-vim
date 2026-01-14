package com.taketimeback.screentime.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.taketimeback.screentime.data.AppUsageDatabase
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import java.util.*

@Composable
fun StatisticsScreen() {
    val context = LocalContext.current
    val database = remember { AppUsageDatabase.getDatabase(context) }
    val scope = rememberCoroutineScope()

    var selectedPeriod by remember { mutableStateOf(Period.WEEK) }
    var weeklyTotal by remember { mutableLongStateOf(0L) }
    var dailyAverage by remember { mutableLongStateOf(0L) }
    var isLoading by remember { mutableStateOf(true) }

    LaunchedEffect(selectedPeriod) {
        scope.launch {
            isLoading = true
            val days = when (selectedPeriod) {
                Period.WEEK -> 7
                Period.MONTH -> 30
            }

            val calendar = Calendar.getInstance()
            val endTime = calendar.timeInMillis
            calendar.add(Calendar.DAY_OF_YEAR, -days)
            calendar.set(Calendar.HOUR_OF_DAY, 0)
            calendar.set(Calendar.MINUTE, 0)
            calendar.set(Calendar.SECOND, 0)
            val startTime = calendar.timeInMillis

            val usageData = database.appUsageDao()
                .getUsageForDateRange(startTime, endTime)
                .first()

            weeklyTotal = usageData.sumOf { it.totalTimeMillis }
            dailyAverage = if (days > 0) weeklyTotal / days else 0L
            isLoading = false
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
                text = "Statistics",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
        }

        item {
            PeriodSelector(
                selectedPeriod = selectedPeriod,
                onPeriodSelected = { selectedPeriod = it }
            )
        }

        if (isLoading) {
            item {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(200.dp),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }
        } else {
            item {
                StatsSummaryCard(
                    total = weeklyTotal,
                    average = dailyAverage,
                    period = selectedPeriod
                )
            }
        }

        item {
            Text(
                text = "Feature Coming Soon",
                style = MaterialTheme.typography.bodyLarge,
                modifier = Modifier.padding(vertical = 32.dp)
            )
            Text(
                text = "Charts and detailed statistics will be added in a future update.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
fun PeriodSelector(
    selectedPeriod: Period,
    onPeriodSelected: (Period) -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Period.values().forEach { period ->
            FilterChip(
                selected = selectedPeriod == period,
                onClick = { onPeriodSelected(period) },
                label = { Text(period.label) },
                modifier = Modifier.weight(1f)
            )
        }
    }
}

@Composable
fun StatsSummaryCard(
    total: Long,
    average: Long,
    period: Period
) {
    val totalHours = total / (1000 * 60 * 60)
    val totalMinutes = (total % (1000 * 60 * 60)) / (1000 * 60)
    val avgHours = average / (1000 * 60 * 60)
    val avgMinutes = (average % (1000 * 60 * 60)) / (1000 * 60)

    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text(
                text = "${period.label} Summary",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold
            )

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceAround
            ) {
                StatItem(
                    label = "Total Time",
                    value = "${totalHours}h ${totalMinutes}m"
                )
                StatItem(
                    label = "Daily Average",
                    value = "${avgHours}h ${avgMinutes}m"
                )
            }
        }
    }
}

@Composable
fun StatItem(label: String, value: String) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = value,
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.primary
        )
        Text(
            text = label,
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

enum class Period(val label: String) {
    WEEK("Last 7 Days"),
    MONTH("Last 30 Days")
}
