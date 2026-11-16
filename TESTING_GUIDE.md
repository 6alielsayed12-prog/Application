# TESTING_GUIDE.md — Yawm Jadid Academy (v1.3.0)

## Running the Automated Suite
Run all Python & Node.js tests from the repository root:
```bash
python -m unittest discover -s tests -t . -v
```

### Key Test Categories
- **Finance & Parity:** `tests/test_finance_engine.py`, `tests/test_finance_golden.py`, `tests/test_finance_parity.py` (uses `node` + `tests/js/parity_runner.js`).
- **Database & Recovery:** `tests/test_store.py`, `tests/test_backup_wal.py`, `tests/test_restore_safety.py`, `tests/test_resilience.py`, `tests/test_destructive_and_portable_paths.py`.
- **API & Security:** `tests/test_http_api.py`, `tests/test_http_integrity.py`, `tests/test_security_utils.py`, `tests/test_frontend_security.py`.
- **Import / Export:** `tests/test_import.py`, `tests/test_import_excel_limits.py`, `tests/test_excel.py`, `tests/test_html_export.py`.
- **UI & E2E:** `tests/test_ui_api_contract.py`, `tests/test_ui_integration_and_e2e.py`, `tests/test_heavy_ui_certificates_and_stress.py`.
- **Build & Docs Sync:** `tests/test_build_scripts.py`, `tests/test_branding.py`, `tests/test_build_artifact_verifier.py`, `tests/test_docs_in_sync.py`.

## Windows Executable Smoke Test (Windows Only)
After building `dist\YawmJadidAcademy\YawmJadidAcademy.exe`:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\smoke_exe.ps1 -ExePath dist\YawmJadidAcademy\YawmJadidAcademy.exe
```
This launches the EXE against an isolated temporary `ALAHD_ERP_HOME`, verifies `/api/health`, `/`, and SQLite DB creation, then terminates cleanly.
