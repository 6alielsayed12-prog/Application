# DATABASE_AUDIT.md — YawmJadidAcademy (v1.3.0)

**Audit Date:** 2026-11-16

---

## 1. Database Engine & Configuration

- **Engine**: SQLite 3 (`alahd_erp/infrastructure/database.py`, 5,619 LOC).
- **Journal & Durability**: `PRAGMA journal_mode=WAL`, `PRAGMA synchronous=FULL`, `PRAGMA busy_timeout=5000`, `PRAGMA foreign_keys=ON`.
- **Schema Version**: `SCHEMA_VERSION = 3` (`PRAGMA user_version = 3`), with ordered versioned migrations (`_mig_v1_to_v2`, `_mig_v2_to_v3`).
- **Tables (17)**: `teachers`, `students`, `months`, `transactions`, `installments`, `salaries`, `study_groups`, `attendance_plans`, `sessions`, `memorization_logs`, `madrasa_batches`, `madrasa_enrollments`, `madrasa_logs`, `certificates`, `closed_months`, `import_batches`, `kv`, `audit`.
- **Indexes (12)**: `ix_students_teacher`, `ix_students_phone`, `ix_students_name_phone`, `ix_students_code`, `ix_students_pos`, `ix_months_month_key`, `ix_transactions_month`, `ix_installments_stu_month`, `ix_installments_month`, `ix_installments_pay_date`, `ix_salaries_teacher_month`, `ix_sessions_student`, `ix_sessions_date`, `ix_sessions_teacher_date`, `ix_memorization_student`, `ix_audit_action`.

---

## 2. Integrity, Security & Lifecycle Verification

- **Bundled Prepopulated DB Check (`data/alahd_erp_v1_prepopulated.sqlite3`)**:
  - `PRAGMA integrity_check`: `ok`
  - `PRAGMA foreign_key_check`: `[]` (0 violations)
  - `PRAGMA user_version`: `3`
- **SQL Injection Audit**:
  - Static AST/regex scan found zero user-controlled string interpolation in SQL queries. The 14 f-string `execute(...)` calls in `database.py` and `demo_cleaner.py` use only internal table/column constants, `SCHEMA_VERSION` integers, or `?` placeholder lists (`IN ({marks})`).
- **Transactions, Backups & Recovery**:
  - `Store.backup_to` writes to a temporary file, runs `PRAGMA integrity_check` via `verify_sqlite_backup_file`, and atomically replaces the target.
  - `Store.restore_from` creates a pre-restore snapshot, runs migrations + `PRAGMA integrity_check` + `PRAGMA foreign_key_check`, and rolls back automatically on any failure (verified by `test_restore_safety.py`).
  - `Store.close()` executes `PRAGMA wal_checkpoint(TRUNCATE)` before closing, preventing stale `-wal`/`-shm` locks on Windows.
- **Cloud-Sync Protection**: `config.is_onedrive_or_synced_path` warns if `APP_HOME` resides inside OneDrive, Dropbox, Google Drive, or iCloud.
