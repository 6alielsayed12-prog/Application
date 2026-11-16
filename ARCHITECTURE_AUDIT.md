# ARCHITECTURE_AUDIT.md — YawmJadidAcademy (v1.3.0)

**Audit Date:** 2026-11-16

---

## 1. Architectural Overview

The application follows a clean, pragmatic **4-layer modular architecture** tailored for an offline-first single-user Windows desktop application:

1. **Entry & Lifecycle Layer (`alahd_erp/main.py`, `config.py`)**:
   - Handles portable path resolution (`%LOCALAPPDATA%\AlAhdAcademySuite` or `ALAHD_ERP_HOME`), rotating file logging, `SingleInstanceGuard`, `BootGuard`, startup crash recovery, background `BackupScheduler`, Uvicorn thread lifecycle, `pywebview` native window (with browser fallback), and clean shutdown (`scheduler.stop(run_exit_backup=True)`, `store.close()`).
2. **API Layer (`alahd_erp/api/server.py`, `security_utils.py`)**:
   - FastAPI app with 112 registered routes, pure-ASGI `MaxBodySizeASGIMiddleware` (25 MB), loopback/Host/Origin/`X-Window-Secret` middleware, optimistic concurrency (`rev` / `X-Client-Rev` -> HTTP 409), centralized `_handle_domain_or_store_error`, and generic 500 error sanitization.
3. **Domain & Service Layer (`alahd_erp/domain/*`, `alahd_erp/services/*`)**:
   - Pure-Python domain engines (`finance_engine.py`, `attendance_engine.py`, `statistics_engine.py`, `alerts_engine.py`, `automation_engine.py`, `models.py`, `settings_registry.py`) decoupled from FastAPI.
   - Service layer for Excel export (`excel_service.py`), Excel/CSV/JSON import (`import_service.py`), and HTML/receipt export (`html_export_service.py`).
4. **Infrastructure Layer (`alahd_erp/infrastructure/*`)**:
   - `database.py` (`Store`): SQLite WAL persistence, schema migrations (`user_version = 3`), backups/restore, audit log.
   - `recovery.py`, `backup_scheduler.py`, `autostart.py`, `instance_probe.py`.
5. **Frontend (`alahd_erp/ui/`)**:
   - Vanilla ES Modules (`app.js`, `finance-engine.js`, `modules/*`), zero external CDNs, local Cairo WOFF2 fonts, tagged-template `dom.js` (`html` / `renderHtml`) preventing XSS.

---

## 2. Strengths Verified

- **Separation of Concerns**: Domain logic (`finance_engine.py`, `models.py`, `statistics_engine.py`) has zero FastAPI/HTTP dependencies and is directly unit-tested.
- **No Circular Imports**: Clean downward dependency flow (`main` -> `api` -> `services`/`domain` -> `infrastructure`).
- **Concurrency & Lifecycle**: Synchronous SQLite handlers run via FastAPI threadpool (`def` routes), protected by `Store` locking and optimistic `rev` checks; `store.close()` runs `PRAGMA wal_checkpoint(TRUNCATE)` on shutdown.
- **Offline-First**: Zero external URLs in `index.html`; all fonts and JS vendor libraries are bundled locally.

---

## 3. Architectural Weaknesses & Findings

1. **Monolithic Files (Maintainability Debt — Medium)**:
   - `alahd_erp/infrastructure/database.py` (5,619 LOC), `alahd_erp/services/import_service.py` (2,855 LOC), and `alahd_erp/api/server.py` (2,289 LOC) are large single files. While internally organized with section comments, splitting `server.py` into `APIRouter` modules and `database.py` into repositories would improve long-term maintainability. *Decision: Avoid speculative large-scale rewrite now to preserve stability and 112-route parity; document as recommended next-phase refactoring.*
2. **Batch Script Line-Ending & Lock Drift (Fixed)**:
   - `.gitattributes` had `* text=auto` without `eol=crlf` for `*.bat`, `*.ps1`, `*.iss`, causing Linux/Git checkouts to convert Windows scripts to LF-only (breaking `cmd.exe` labels and failing 2 tests).
   - `build_and_run.bat` lacked `if exist requirements.lock` pinning support that `build_windows.bat` had.
   - **Action Taken**: Updated `.gitattributes`, converted all `.bat`/`.ps1`/`.iss` files to CRLF, and added `requirements.lock` support to `build_and_run.bat`.
3. **Missing Native Windows CI/CD Pipeline (Fixed)**:
   - No `.github/workflows/windows-build.yml` existed to validate Python 3.12 x64 builds, PyInstaller packaging, smoke tests, and Inno Setup compilation on a real Windows runner.
   - **Action Taken**: Created `.github/workflows/windows-build.yml` (Phase 9).
4. **Empty Root `README.md` (Fixed)**:
   - Root `README.md` contained only `# project` (11 bytes).
   - **Action Taken**: Replaced with comprehensive project documentation and guides.
