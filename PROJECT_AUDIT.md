# PROJECT AUDIT — Yawm Jadid Academy / Al-Ahd Academy ERP Suite (v1.3.0)

**Audit Date:** 2026-11-16
**Target Project:** `My-Prokject-096cbacd99bc63f2c76233124f62f38d818786b1` (`alahd_erp` v1.3.0)
**Environment:** Linux x86_64 sandbox, Python 3.11.2, FastAPI 0.92.0, Pydantic 1.10.4, Uvicorn 0.17.6, OpenPyXL 3.1.5, Node.js v18.20.4

---

## 1. Technology Stack & Entry Points

| Layer | Technology | Entry Point / Key Files |
|---|---|---|
| Desktop Launcher | Python 3.12+ / PyWebView (optional browser fallback) | `alahd_erp/main.py` |
| Backend API | FastAPI + Uvicorn (loopback `127.0.0.1` / `::1`) | `alahd_erp/api/server.py` (2,288 LOC), `alahd_erp/api/security_utils.py` |
| Domain Engines | Pure Python + `decimal.Decimal` (`ROUND_HALF_UP`) | `alahd_erp/domain/` (`finance_engine.py`, `models.py`, `settings_registry.py`, `alerts_engine.py`, `automation_engine.py`, `statistics_engine.py`, `attendance_engine.py`, `demo_cleaner.py`, `demo_data.py`, `academy_data_loader.py`) |
| Persistence | SQLite 3 (WAL mode, `PRAGMA foreign_keys=ON`, schema v3) | `alahd_erp/infrastructure/database.py` (5,619 LOC), `recovery.py`, `backup_scheduler.py`, `autostart.py`, `instance_probe.py` |
| Services & Tools | Excel/HTML import & export | `alahd_erp/services/` (`import_service.py`, `excel_service.py`, `html_export_service.py`), `alahd_erp/tools/excel_converter.py` |
| Frontend UI | Vanilla JS ES Modules + CSS Design System (Arabic RTL, offline Cairo WOFF2) | `alahd_erp/ui/index.html` (2,132 LOC), `alahd_erp/ui/css/design-system.css` (1,769 LOC), `alahd_erp/ui/js/app.js` (3,279 LOC), `alahd_erp/ui/js/finance-engine.js`, `alahd_erp/ui/js/modules/*.js` |
| Windows Packaging | PyInstaller one-dir spec + Inno Setup 6 + Batch launchers | `YawmJadidAcademy.spec`, `installer/YawmJadidAcademy.iss`, `START_ACADEMY.bat`, `build_windows.bat`, `build_and_run.bat`, `scripts/*.ps1`, `scripts/verify_build*.py` |

**Total Source Volume:** ~36,962 lines across Python, JS, CSS, and HTML.

---

## 2. Baseline Verification Results (Pre-Fix)

1. **Automated Test Suite (`python3 -m unittest discover -s tests -t .`):**
   - **463 tests run** in 81.6s
   - **453 passed**, **2 FAILED**, **1 skipped** (Pillow optional dev dependency), **7 expected failures** (intentional `PARITY-1..7` financial parity pins documented in `docs/ISSUES.md`).
2. **Pre-Populated Database (`data/alahd_erp_v1_prepopulated.sqlite3`):**
   - `PRAGMA integrity_check` = `ok`, `PRAGMA foreign_key_check` = `[]`, `PRAGMA user_version` = `3`.
   - Contains 110 students, 8 teachers, 131 months, 99 installments, 49 study groups, 1 salary, 1 audit entry.
3. **Frontend Syntax & Offline Check:**
   - All 12 JS files parse cleanly as ES modules/scripts in Node v18.20.4.
   - Zero external HTTP/HTTPS CDN URLs in `alahd_erp/ui/`.
4. **Git Repository:**
   - Not initialized as a `.git` repository in the extracted archive (`.git` absent).

---

## 3. Discovered Defects & Prioritization

| ID | Severity | Component | Finding |
|---|---|---|---|
| **BAT-1** | **CRITICAL** | `START_ACADEMY.bat` | Corrupted `if not exist ".venv\Scripts\python.exe" (...)` block: `%PY% -m venv .venv \|\| goto :unc_fail` jumps to a non-existent `:unc_fail` label, and `:fail_setup` + `goto :fail` are nested inside the parenthesized `if (...)` block, breaking `cmd.exe` parsing on Windows. Also LF-only line endings. |
| **BAT-2** | **CRITICAL** | `build_and_run.bat` | Corrupted `if not defined PY (...)` block: `goto :unc_fail` jumps to a non-existent `:unc_fail` label, `:fail` is duplicated inside the `if (...)` block with a stray `)`, and the file uses LF-only line endings (causing `test_bat_scripts_ascii_crlf_and_valid_labels` to FAIL). |
| **BAT-3** | **HIGH** | `build_windows.bat`, `scripts/make_lock.bat` | LF-only line endings instead of CRLF (causing `test_launchers_are_ascii_with_crlf` to FAIL and risking `cmd.exe` label mis-parsing on Windows). |
| **LOG-1** | **MEDIUM** | `server.py:306`, `excel_service.py:205` | Silent `except Exception: pass` on demo data auto-seeding and Excel header logo embedding hides operational diagnostics. |
| **TEST-1** | **MEDIUM** | `tests/test_build_scripts.py` | Missing automated regression check for `.bat` label integrity (`goto`/`call` target existence and no `:label` inside parenthesized `if (...)` blocks). |
| **ARCH-1** | **LOW** | `database.py`, `app.js`, `import_service.py`, `server.py` | Monolithic file sizes (`database.py` 5,619 LOC, `app.js` 3,279 LOC, `import_service.py` 2,855 LOC, `server.py` 2,288 LOC). Well-structured internally, but candidates for future incremental module splitting. |
| **WIN-1** | **INFO** | Windows EXE Build | PyInstaller `.exe` and Inno Setup installer cannot be compiled or executed in the Linux sandbox; Windows 10/11 + Python 3.12 machine required for final binary build and `smoke_exe.ps1` execution. |
