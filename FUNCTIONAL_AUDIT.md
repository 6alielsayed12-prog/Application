# FUNCTIONAL_AUDIT.md — YawmJadidAcademy (v1.3.0)

**Audit Date:** 2026-11-16

---

## 1. Core Feature & Workflow Verification

All 112 API routes (`scripts/route_inventory.py`) and corresponding domain/service modules were traced and verified against the test suite (`tests/`):

| Feature Area | Implementation | Validation & Error Handling | Status |
|---|---|---|---|
| **Students & Teachers CRUD** | `server.py`, `models.py`, `database.py` | Duplicate teacher/student checks, rev concurrency (409), SQLite constraints | **VERIFIED** |
| **Financial Engine (EGP)** | `domain/finance_engine.py`, `ui/js/finance-engine.js` | Integer EGP via `Decimal` (`ROUND_HALF_UP`), teacher `pct` sync (`_sync_pct_aliases`) | **VERIFIED** (6 known JS/Py edge-case divergences marked `@expectedFailure` in `test_finance_parity.py`) |
| **Installments & Receipts** | `database.py`, `html_export_service.py` | Month locking (`MonthLockedError`), partial payments, printable HTML receipts | **VERIFIED** |
| **Attendance & Study Periods** | `domain/attendance_engine.py`, `automation_engine.py` | Date projection, scheduling conflict detection (409), auto-compensation | **VERIFIED** |
| **Excel / CSV / JSON Import** | `services/import_service.py` | Preview-first, column mapping, XXE/zip-bomb limits, transactional commit + post-commit verification + undo | **VERIFIED** |
| **Excel & Read-Only HTML Export** | `services/excel_service.py`, `html_export_service.py` | Formula injection escaping, public vs. financial scope filtering | **VERIFIED** |
| **Alerts & General Statistics** | `alerts_engine.py`, `statistics_engine.py` | Rule-based alerts, dismiss/snooze/restore, KPI aggregations | **VERIFIED** |
| **Certificates (6 Templates)** | `ui/js/modules/certificates.js`, `database.py` | Template persistence, QR generation (`qrcode.js`), PDF print via `html2pdf` | **VERIFIED** |
| **Settings (55 Keys) & Auto-Start** | `settings_registry.py`, `autostart.py` | Type/range validation, HKCU Run sync & self-repair, `BootGuard` | **VERIFIED** (Windows registry execution `NOT EXECUTED` on Linux) |
| **Crash Recovery & Backups** | `recovery.py`, `backup_scheduler.py` | Startup WAL repair, quarantine, auto-restore, periodic/daily/exit backups | **VERIFIED** |

---

## 2. Known Divergences & Open Defects

1. **Finance Engine Parity (`tests/test_finance_parity.py`)**: 6 `KNOWN_DIVERGENCE` cases (non-numeric money text, Arabic-Indic digits in JS, `null` vs `undefined` receipts, invalid reference date, student without receipt + `month.paymentDate`, blank student name) and 1 `test_DEFECT_store_stats_should_follow_settings` are intentionally marked `@unittest.expectedFailure` awaiting business-rule sign-off.
2. **Windows Batch Launchers (Fixed)**: `build_windows.bat`, `build_and_run.bat`, `START_ACADEMY.bat`, and `scripts/make_lock.bat` had LF-only line endings, which caused `test_build_scripts.py` and `test_heavy_ui_certificates_and_stress.py` to fail. Fixed by converting to CRLF and enforcing `eol=crlf` in `.gitattributes`.
