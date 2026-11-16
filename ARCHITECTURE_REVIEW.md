# ARCHITECTURE REVIEW — Yawm Jadid Academy / Al-Ahd Academy ERP Suite (v1.3.0)

## 1. Original Architecture Assessment

The application follows a clean, offline-first **4-layer local desktop architecture**:

1. **Presentation Layer (`alahd_erp/ui/`):**
   - Vanilla ES Modules (`app.js` + `modules/*.js`) with a shared `finance-engine.js` mirror of the Python financial rules.
   - 100% offline assets: local Cairo WOFF2 fonts, local `xlsx.full.min.js`, `exceljs.min.js`, `html2pdf.bundle.min.js`, and `qrcode.js`.
   - Safe DOM rendering via tagged template `html` / `renderHtml()` in `modules/dom.js` (auto-escaping interpolated values).
2. **API & Security Layer (`alahd_erp/api/`):**
   - FastAPI + Uvicorn bound strictly to loopback (`127.0.0.1`).
   - Per-launch `X-Window-Secret` authentication (header or `httpOnly` cookie), anti-DNS-rebinding `Host` check, `Origin` allowlist, and ASGI-level streaming body size cap (`MaxBodySizeASGIMiddleware`, 25 MB).
   - Optimistic concurrency control (`rev` / `X-Client-Rev` -> HTTP 409).
3. **Domain & Services Layer (`alahd_erp/domain/`, `alahd_erp/services/`, `alahd_erp/tools/`):**
   - Pure-Python `finance_engine.py` using `decimal.Decimal` (`ROUND_HALF_UP`) and integer EGP amounts.
   - `settings_registry.py` managing 55+ validated settings with safe defaults and hard safety clamps.
   - `import_service.py`, `excel_service.py`, `html_export_service.py`, and `excel_converter.py` for preview-bound imports and formula-safe exports.
4. **Infrastructure Layer (`alahd_erp/infrastructure/`):**
   - SQLite 3 in WAL mode (`PRAGMA synchronous=FULL`, `PRAGMA foreign_keys=ON`, schema `user_version = 3`).
   - Startup crash recovery (`recovery.py`), settings-driven `BackupScheduler` (`backup_scheduler.py`), single-instance locking (`instance_probe.py`), and Windows per-user Run-key autostart (`autostart.py`).

## 2. Discovered Architectural Weaknesses & Implemented Improvements

- **Windows Launcher & Build Pipeline Fragility (CRITICAL — FIXED):**
  - `START_ACADEMY.bat` and `build_and_run.bat` had malformed `if (...)` blocks containing `:fail`/`:fail_setup` labels and references to a missing `:unc_fail` label, plus LF-only line endings across all 4 `.bat` files.
  - **Fix:** Repaired control flow and error labels in `START_ACADEMY.bat` and `build_and_run.bat`, converted all `.bat` files to strict ASCII + CRLF, and added automated batch-label & block-nesting validation in `tests/test_build_scripts.py`.
- **Silent Exception Swallowing (MEDIUM — FIXED):**
  - `server.py:306` and `excel_service.py:205` swallowed exceptions silently with `pass`.
  - **Fix:** Replaced with structured `log.warning(...)` calls so failures are captured in `alahd_erp.log` without breaking startup or exports.
- **Monolithic Module Sizes (LOW — DOCUMENTED):**
  - `database.py` (5,619 LOC) and `app.js` (3,279 LOC) combine multiple sub-domains in single files. Because existing tests and build verifiers (`verify_build_artifact.py`) track module layouts directly, we preserved module boundaries to avoid breaking working contracts and recommend incremental repository splitting in v1.4.0.

## 3. Remaining Technical Limitations

- **Single-User Local Locking:** Designed for one operator per SQLite database on one Windows PC; concurrent multi-user network sharing is intentionally unsupported.
- **Financial Parity Pins (`PARITY-1..7`):** 7 intentional `expectedFailure` tests remain pinned pending owner business-rule confirmation (`docs/ISSUES.md` §1).
- **Windows-Only Runtime Features:** `pywebview` native window, `msvcrt`/Win32 mutex locking, `HKCU` Registry autostart, PyInstaller EXE build, and Inno Setup compilation cannot be executed in the Linux container.
