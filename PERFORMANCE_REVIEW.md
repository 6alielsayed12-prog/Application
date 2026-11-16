# PERFORMANCE REVIEW — Yawm Jadid Academy / Al-Ahd Academy ERP Suite (v1.3.0)

## 1. Database & Query Performance

- **SQLite Configuration:** WAL mode enabled (`PRAGMA journal_mode=WAL`), `PRAGMA synchronous=FULL`, `PRAGMA foreign_keys=ON`, and thread-safe `threading.RLock` synchronization.
- **Indexing Audit:** Verified 16 indexes covering all hot query paths:
  - `students`: `ix_students_teacher`, `ix_students_phone`, `ix_students_name_phone`, `ix_students_code`, `ix_students_pos`
  - `months`: `PRIMARY KEY(student_id, month_key)`, `ix_months_month_key`
  - `installments`: `ix_installments_stu_month`, `ix_installments_month`, `ix_installments_pay_date`
  - `transactions`: `ix_transactions_month`
  - `salaries`: `ix_salaries_teacher_month`
  - `sessions`: `ix_sessions_student`, `ix_sessions_date`, `ix_sessions_teacher_date`
  - `memorization_logs`: `ix_memorization_student`
  - `audit`: `ix_audit_action`
- **Bulk Deletion Efficiency:** `_delete_unkept_rows` uses a temporary `_keep_ids` table to avoid SQLite's `SQLITE_MAX_VARIABLE_NUMBER` limit on large datasets.

## 2. API, Background Tasks & Resource Disposal

- **Off-Event-Loop Execution:** Synchronous SQLite operations run off the async event loop (`def` route handlers / `run_in_threadpool`), keeping health/status checks responsive.
- **Backup Scheduler:** `BackupScheduler` reads settings dynamically, skips unchanged DBs via hash/mtime checks, isolates mirror-folder failures, and enforces retention floors without blocking UI requests.
- **Clean Shutdown:** `Store.close()` runs `PRAGMA wal_checkpoint(TRUNCATE)` and closes the SQLite connection cleanly so `.sqlite3-wal` and `.sqlite3-shm` files are released.
- **Import Safety Bounds:** Hard clamps (200 MB file size, 200,000 rows) protect against memory exhaustion and ZIP-bomb Excel files.

## 3. Observed Bottlenecks & Benchmark

- **Full Test Suite Runtime:** 463 unit/integration/API/stress tests complete in ~81s (including destructive/adversarial recovery and multi-student stress tests).
- **Pre-Populated DB Size:** 110 students / 131 months / 99 installments executes `PRAGMA integrity_check` and `/api/system/health-report` in sub-second time.
