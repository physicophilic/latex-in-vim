package com.taketimeback.screentime.data

import android.content.Context
import androidx.room.*
import kotlinx.coroutines.flow.Flow
import java.util.Date

/**
 * Room Database for storing app usage data
 */
@Database(
    entities = [AppUsageEntity::class, AppLimitEntity::class, BlockedAppEntity::class],
    version = 1,
    exportSchema = false
)
@TypeConverters(Converters::class)
abstract class AppUsageDatabase : RoomDatabase() {
    abstract fun appUsageDao(): AppUsageDao
    abstract fun appLimitDao(): AppLimitDao
    abstract fun blockedAppDao(): BlockedAppDao

    companion object {
        @Volatile
        private var INSTANCE: AppUsageDatabase? = null

        fun getDatabase(context: Context): AppUsageDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppUsageDatabase::class.java,
                    "screen_time_database"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}

/**
 * Entity for storing daily app usage
 */
@Entity(
    tableName = "app_usage",
    primaryKeys = ["packageName", "date"]
)
data class AppUsageEntity(
    val packageName: String,
    val appName: String,
    val date: Long, // Timestamp for the day (midnight)
    val totalTimeMillis: Long,
    val lastUsedTimestamp: Long,
    val launchCount: Int = 0
)

/**
 * Entity for app time limits
 */
@Entity(tableName = "app_limits")
data class AppLimitEntity(
    @PrimaryKey val packageName: String,
    val appName: String,
    val dailyLimitMillis: Long,
    val enabled: Boolean = true
)

/**
 * Entity for blocked apps
 */
@Entity(tableName = "blocked_apps")
data class BlockedAppEntity(
    @PrimaryKey val packageName: String,
    val appName: String,
    val enabled: Boolean = true,
    val addedTimestamp: Long = System.currentTimeMillis()
)

/**
 * DAO for app usage data
 */
@Dao
interface AppUsageDao {
    @Query("SELECT * FROM app_usage WHERE date = :date ORDER BY totalTimeMillis DESC")
    fun getUsageForDate(date: Long): Flow<List<AppUsageEntity>>

    @Query("SELECT * FROM app_usage WHERE date >= :startDate AND date <= :endDate")
    fun getUsageForDateRange(startDate: Long, endDate: Long): Flow<List<AppUsageEntity>>

    @Query("SELECT * FROM app_usage WHERE packageName = :packageName AND date >= :startDate ORDER BY date DESC")
    fun getUsageForApp(packageName: String, startDate: Long): Flow<List<AppUsageEntity>>

    @Query("SELECT SUM(totalTimeMillis) FROM app_usage WHERE date = :date")
    suspend fun getTotalUsageForDate(date: Long): Long?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUsage(usage: AppUsageEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUsages(usages: List<AppUsageEntity>)

    @Query("DELETE FROM app_usage WHERE date < :cutoffDate")
    suspend fun deleteOldData(cutoffDate: Long)
}

/**
 * DAO for app limits
 */
@Dao
interface AppLimitDao {
    @Query("SELECT * FROM app_limits WHERE enabled = 1")
    fun getAllLimits(): Flow<List<AppLimitEntity>>

    @Query("SELECT * FROM app_limits WHERE packageName = :packageName")
    suspend fun getLimit(packageName: String): AppLimitEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertLimit(limit: AppLimitEntity)

    @Delete
    suspend fun deleteLimit(limit: AppLimitEntity)

    @Query("UPDATE app_limits SET enabled = :enabled WHERE packageName = :packageName")
    suspend fun setLimitEnabled(packageName: String, enabled: Boolean)
}

/**
 * DAO for blocked apps
 */
@Dao
interface BlockedAppDao {
    @Query("SELECT * FROM blocked_apps WHERE enabled = 1")
    fun getAllBlockedApps(): Flow<List<BlockedAppEntity>>

    @Query("SELECT * FROM blocked_apps WHERE packageName = :packageName")
    suspend fun getBlockedApp(packageName: String): BlockedAppEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertBlockedApp(app: BlockedAppEntity)

    @Delete
    suspend fun deleteBlockedApp(app: BlockedAppEntity)

    @Query("UPDATE blocked_apps SET enabled = :enabled WHERE packageName = :packageName")
    suspend fun setBlockEnabled(packageName: String, enabled: Boolean)
}

/**
 * Type converters for Room
 */
class Converters {
    @TypeConverter
    fun fromTimestamp(value: Long?): Date? {
        return value?.let { Date(it) }
    }

    @TypeConverter
    fun dateToTimestamp(date: Date?): Long? {
        return date?.time
    }
}
