# TEST_REPORT.md — YawmJadidAcademy (v1.3.0)

**Execution Date:** 2026-11-16
**Environment:** Linux (`Python 3.11.2`, `Node.js v18.20.4`)

---

## 1. Automated Test Suite Summary

Command executed:
```bash
python3 -m unittest discover -s tests -t . -q
```

- **Total Tests Discovered & Executed:** 464
- **Passed:** 456 (464 total minus 1 skipped and 7 expected failures)
- **Failures:** 0 (2 initial failures in `test_build_scripts.py` and `test_heavy_ui_certificates_and_stress.py` due to LF-only `.bat` line endings were fixed and verified passing)
- **Errors:** 0
- **Skipped:** 1 (`tests/test_http_api.py::OriginAndHost::test_non_loopback_client_blocked` — `TestClient(client=...)` unsupported on Starlette 0.26.1)
- **Expected Failures (`@unittest.expectedFailure`):** 7 (`tests/test_finance_parity.py`: 6 documented JS/Python edge-case divergences + 1 `test_DEFECT_store_stats_should_follow_settings`)

---

## 2. Test Coverage by Category

| Category | Status | Notes |
|---|---|---|
| **Unit Tests** (`finance_engine`, `models`, `security_utils`, `settings_registry`) | **PASS** | Executed in Python + Node.js (`parity_runner.js`) |
| **Database & Recovery Tests** (`test_store`, `test_backup_wal`, `test_restore_safety`, `test_phase3_data_migration_and_restore`, `test_destructive_and_portable_paths`) | **PASS** | SQLite WAL, migrations, corruption quarantine, rollback verified |
| **HTTP API & Contract Tests** (`test_http_api`, `test_http_integrity`, `test_ui_api_contract`) | **PASS** (1 skipped) | `TestClient` loopback/secret/concurrency/limits verified |
| **Import/Export & Excel Tests** (`test_excel`, `test_import`, `test_import_excel_limits`, `test_html_export`) | **PASS** | XXE/zip-bomb limits, formula escaping, HTML scopes verified |
| **UI & JS E2E Tests** (`test_ui_integration_and_e2e`, `test_heavy_ui_certificates_and_stress`) | **PASS** | Node.js module & E2E harnesses verified |
| **Packaging & Build Script Static Tests** (`test_build_scripts`, `test_branding`, `test_build_artifact_verifier`, `test_docs_in_sync`) | **PASS** | CRLF/ASCII, `ALLOW_PROVISIONAL_BUILD`, version sync, 112-route doc sync verified |
| **Native Windows EXE & Installer Smoke Tests** (`scripts/smoke_exe.ps1`, `iscc`, `pywebview` GUI) | **NOT EXECUTED** | Requires Windows 10/11 runner; automated in `.github/workflows/windows-build.yml` |
