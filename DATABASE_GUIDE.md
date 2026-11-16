# DATABASE_GUIDE.md — Yawm Jadid Academy (v1.3.0)

## Storage Location
- Default: `%LOCALAPPDATA%\AlAhdAcademySuite\alahd_erp_v1.sqlite3`
- Override: `ALAHD_ERP_HOME` environment variable

## SQLite Configuration
- `PRAGMA journal_mode=WAL`
- `PRAGMA synchronous=FULL`
- `PRAGMA foreign_keys=ON`
- `PRAGMA busy_timeout=5000`
- `PRAGMA user_version = 3` (`SCHEMA_VERSION = 3`)

## Schema Overview (17 Tables)
`teachers`, `students`, `months`, `transactions`, `installments`, `salaries`, `study_groups`, `attendance_plans`, `sessions`, `memorization_logs`, `madrasa_batches`, `madrasa_enrollments`, `madrasa_logs`, `certificates`, `closed_months`, `import_batches`, `kv`, `audit`.

## Backups & Recovery
- **Automatic Backups (`BackupScheduler`):** Driven by settings (`autoBackupEnabled`, `autoBackupIntervalMinutes`, `autoBackupKeep`, `dailyBackupKeep`, `backupOnExit`, `mirrorBackupsToExtraFolder`, `extraBackupFolder`).
- **Integrity Verification:** Every backup is verified with `PRAGMA integrity_check` before replacing the target file.
- **Startup Crash Recovery (`recovery.py`):** Detects unclean shutdowns, runs `PRAGMA quick_check`, attempts WAL repair, and if unrecoverable, quarantines the corrupt DB and restores the newest verified backup.
- **Restore Safety:** `Store.restore_from` takes a pre-restore snapshot, runs migrations + `PRAGMA integrity_check` + `PRAGMA foreign_key_check`, and rolls back on any error.
