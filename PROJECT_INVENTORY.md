# PROJECT_INVENTORY.md — YawmJadidAcademy (v1.3.0)

**Audit Date:** 2026-11-16
**Repository / Archive:** `6alielsayed12-prog/my-project` (`alahd-erp` v1.3.0)
**Primary Target Environment:** Windows 10 / Windows 11 (x64), Python 3.12 x64
**Current Inspection Environment:** Linux (`Python 3.11.2`, `Node.js v18.20.4`)

---

## 1. Technology Stack (Verified from Source)

| Layer | Technology | Evidence / Source |
|---|---|---|
| **Language (Backend)** | Python 3.12+ (target 3.12 x64) | `pyproject.toml`, `alahd_erp/*.py` (29 files, 22,284 LOC) |
| **Web / API Framework** | FastAPI + Uvicorn + Pydantic | `alahd_erp/api/server.py`, `requirements-core.txt` |
| **Desktop Shell** | `pywebview` (optional; WebView2 on Windows, browser fallback) | `alahd_erp/main.py`, `YawmJadidAcademy.spec` |
| **Database** | SQLite 3 (WAL mode, `synchronous=FULL`, `foreign_keys=ON`, `user_version=3`) | `alahd_erp/infrastructure/database.py` (5,619 LOC) |
| **Excel Processing** | `openpyxl` (`>=3.1`) | `alahd_erp/services/excel_service.py`, `import_service.py` |
| **Frontend UI** | Vanilla ES Modules + HTML5 + CSS3 (100% offline, Arabic RTL) | `alahd_erp/ui/` (12 JS files 8,407 LOC; 1 CSS 1,769 LOC; 1 HTML 2,132 LOC) |
| **Vendored Assets** | Cairo WOFF2 fonts (Arabic/Latin), `xlsx.full.min.js`, `exceljs.min.js`, `html2pdf.bundle.min.js`, `qrcode.js` | `alahd_erp/ui/vendor/` (zero external CDN URLs) |
| **Packaging & Installer** | PyInstaller 6 (`YawmJadidAcademy.spec`) + Inno Setup 6 (`installer/YawmJadidAcademy.iss`) | Root & `installer/` |
| **Testing** | `unittest` (36 test files, 10,194 LOC) + Node.js JS parity/E2E harnesses | `tests/`, `tests/js/` |

---

## 2. Directory & Module Inventory

### 2.1 Application Package (`alahd_erp/`)
- `alahd_erp/__init__.py`: App metadata (`__version__ = "1.3.0"`, `APP_NAME`, `EXECUTABLE_NAME = "YawmJadidAcademy"`, `DATA_DIR_NAME = "AlAhdAcademySuite"`, `DEFAULT_PORT = 8890`, `DB_FILENAME = "alahd_erp_v1.sqlite3"`).
- `alahd_erp/config.py` (162 LOC): Path resolution (`resolve_app_home`, `resolve_ui_dir`, `resolve_db_path`, `resolve_port`), OneDrive/synced-folder detection (`is_onedrive_or_synced_path`), rotating file logging (`configure_logging`).
- `alahd_erp/main.py` (362 LOC): Desktop entry point, `SingleInstanceGuard`, `BootGuard`, startup crash recovery, uvicorn thread launch, bundled Excel auto-loader, auto-start sync, `BackupScheduler`, `pywebview` window / browser fallback, graceful shutdown.

#### `alahd_erp/api/`
- `server.py` (2,289 LOC): FastAPI app factory (`create_app`), ASGI `MaxBodySizeASGIMiddleware` (25 MB cap), loopback + Host + Origin + `X-Window-Secret` middleware, `unhandled_error` 500 sanitizer, 112 API route registrations covering health, PIN lock, state/revisions, students, teachers, packages, months/receipts, installments, salaries, groups, attendance, memorization, madrasa, certificates, alerts, statistics, automation, Excel import/export, HTML export, backups/restore, settings, and autostart.
- `security_utils.py` (107 LOC): `host_allowed`, `origin_allowed`, `sanitize_upload_filename`, `parse_multipart_upload`.

#### `alahd_erp/domain/`
- `models.py` (836 LOC): Domain validation, duplicate student/teacher detection, teacher name normalization.
- `finance_engine.py` (815 LOC): Integer EGP `Decimal` (`ROUND_HALF_UP`) financial calculations, teacher percentages, installments, monthly summaries.
- `attendance_engine.py` (361 LOC): Study period calculation, smart attendance date projection.
- `statistics_engine.py` (658 LOC): General academy statistics and aggregations.
- `alerts_engine.py` (800 LOC): Rule-based alerts (unpaid, expiring, attendance, data quality).
- `automation_engine.py` (1,336 LOC): Scheduling conflict detection, bulk operation previews, salary preparation reports, entity search, data quality audit.
- `settings_registry.py` (946 LOC): Central 55-setting registry, defaults, types, and validation.
- `academy_data_loader.py` (173 LOC, 184 KB): Bundled dataset loader for September (`قواعد شهر 9.xlsx`) and Oct/Nov (`Academy_Management_Dashboard_2026-11-11.xlsx`).
- `demo_data.py` (306 LOC) & `demo_cleaner.py` (390 LOC): Demo seed definitions and cleanup utilities (disabled on desktop startup).

#### `alahd_erp/infrastructure/`
- `database.py` (5,619 LOC): `Store` class, SQLite WAL schema (17 tables + indexes), versioned migrations (`SCHEMA_VERSION = 3`), optimistic concurrency (`rev`), backup/snapshot/restore with `PRAGMA integrity_check` & `foreign_key_check`, PIN hashing/verification, audit log.
- `backup_scheduler.py` (212 LOC): Settings-driven periodic, daily, and exit backups + optional `extraBackupFolder` mirroring.
- `recovery.py` (317 LOC): Startup crash detection, WAL repair, quarantine, and automatic restore from verified backup.
- `autostart.py` (748 LOC): Windows `HKCU\...\Run` registry management, `SingleInstanceGuard` (OS mutex/lockfile), `BootGuard` loop protection.
- `instance_probe.py`: Local instance health probing.

#### `alahd_erp/services/` & `alahd_erp/tools/`
- `excel_service.py` (1,325 LOC): Excel workbook generation/export.
- `import_service.py` (2,855 LOC): Excel/CSV/JSON preview, column mapping, XXE/zip-bomb limits, transactional commit with post-commit verification and undo.
- `html_export_service.py` (1,089 LOC): Read-only public/financial HTML reports and printable receipts.
- `excel_converter.py` (522 LOC): Standalone Excel conversion helper.

### 2.2 Build, Packaging, Scripts & Data
- Build & Launchers: `build_and_run.bat`, `build_windows.bat`, `START_ACADEMY.bat`, `YawmJadidAcademy.spec`, `pyproject.toml`, `requirements.txt`, `requirements-core.txt`, `requirements-build.txt`, `.gitattributes`.
- Installer: `installer/YawmJadidAcademy.iss`, `installer/version_info.txt`.
- Scripts: `scripts/make_lock.bat`, `scripts/verify_build_artifact.py`, `scripts/verify_build.py`, `scripts/smoke_exe.ps1`, `scripts/create_shortcut.ps1`, `scripts/route_inventory.py`, `scripts/make_checkpoint.sh`, `scripts/qa/*`.
- Data (`data/`): `Academy_Management_Dashboard_2026-11-11.xlsx`, `قواعد شهر 9.xlsx`, `YawmJadid_Complete_ERP_Export.xlsx`, `YawmJadid_Full_Backup_With_Sep_Oct_Nov.json`, `alahd_erp_v1_prepopulated.sqlite3`.
- Tests (`tests/`): 36 Python test modules + `tests/js/` (`f03_harness.mjs`, `parity_runner.js`).
- Docs (`docs/` + root): `docs/*.md` (11 files), root audit/changelog markdowns, `README.md` (was empty placeholder, now updated).
