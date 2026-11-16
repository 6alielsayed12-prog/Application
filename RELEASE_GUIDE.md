# RELEASE_GUIDE.md — Yawm Jadid Academy (v1.3.0)

## Release Qualification Rules
- Release builds **must** use **Python 3.12 x64** (`TIER 1 - RELEASE-QUALIFYING BUILD`).
- Version strings must stay synchronized across `alahd_erp/__init__.py`, `pyproject.toml`, `installer/version_info.txt`, `installer/YawmJadidAcademy.iss`, and `build_and_run.bat` (`tests/test_branding.py` enforces this).

---

## Reproducible Release Process

### Via GitHub Actions (Recommended)
1. Push changes to `main`/`master` or trigger **Windows Production Build & Verification** (`.github/workflows/windows-build.yml`) via `workflow_dispatch`.
2. Download the workflow artifacts:
   - `YawmJadidAcademy-1.3.0-windows-x64` (`YawmJadidAcademy-1.3.0-portable.zip` + `YawmJadidAcademy-Setup-1.3.0.exe`)
   - `build-diagnostics-<run_number>` (`build_logs/`, `build-freeze.txt`, `build_verification_report.json`, `release/release-metadata.json`)

### Via Local Windows 10/11 Build Machine
1. Run `build_windows.bat /strict` (or `build_and_run.bat /strict` to also pack the portable ZIP).
2. On the first clean Python 3.12 x64 build, generate and commit the dependency lockfile:
   ```bat
   scripts\make_lock.bat
   ```
3. Verify `dist\YawmJadidAcademy\YawmJadidAcademy.exe`, `release\YawmJadidAcademy-1.3.0-portable.zip`, and `installer\Output\YawmJadidAcademy-Setup-1.3.0.exe`.
4. Complete the manual checks in `docs\RELEASE_CHECKLIST.md`.
