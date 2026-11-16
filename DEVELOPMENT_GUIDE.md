# DEVELOPMENT_GUIDE.md — Yawm Jadid Academy (v1.3.0)

## Local Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements-build.txt
```

Run the application from source:
```bash
python -m alahd_erp.main
```
Environment variables for development:
- `ALAHD_ERP_HOME=/path/to/dev_data` — isolate dev database from production data
- `ALAHD_ERP_PORT=8895` — custom loopback port (default `8890`, `0` for ephemeral)
- `ALAHD_ERP_NO_UI=1` — run headless API server without opening a window

---

## Codebase Structure
- `alahd_erp/main.py` — desktop entry point, single-instance guard, recovery, scheduler, window launch
- `alahd_erp/config.py` — runtime paths, synced-folder detection, rotating logging
- `alahd_erp/api/server.py` — FastAPI app, security middleware, 112 API routes
- `alahd_erp/domain/` — pure-Python business logic (`finance_engine.py`, `models.py`, `attendance_engine.py`, `statistics_engine.py`, `alerts_engine.py`, `automation_engine.py`, `settings_registry.py`)
- `alahd_erp/infrastructure/` — `database.py` (`Store`), `backup_scheduler.py`, `recovery.py`, `autostart.py`, `instance_probe.py`
- `alahd_erp/services/` — `excel_service.py`, `import_service.py`, `html_export_service.py`
- `alahd_erp/ui/` — Arabic RTL Vanilla ES Modules + vendored offline assets

## Coding Standards
- **Money Arithmetic:** Always use `int` EGP and `decimal.Decimal` (`ROUND_HALF_UP`) in `finance_engine.py`; never use `float`.
- **Batch/PowerShell Scripts:** Keep `*.bat` ASCII-only with CRLF line endings (enforced by `.gitattributes` and `tests/test_build_scripts.py`).
- **Route Inventory Sync:** When adding/removing API routes, run `python scripts/route_inventory.py` and keep `docs/ARCHITECTURE.md` in sync (`tests/test_docs_in_sync.py`).
