# BUILD_GUIDE.md — Yawm Jadid Academy (v1.3.0)

## Prerequisites (Windows Build Machine)
1. **Python 3.12 x64** (`py -3.12` launcher available).
2. **Inno Setup 6** (`iscc.exe`) for building `YawmJadidAcademy-Setup-1.3.0.exe` (optional for portable ZIP).
3. Local NTFS drive (UNC paths are rejected by `build_windows.bat` and `build_and_run.bat`).

---

## Automated One-Click Build

### Release Build (Recommended)
```bat
build_windows.bat /strict
```
This script:
1. Verifies Python 3.12 x64.
2. Creates/activates `.venv`, installs `requirements.lock` (if present), `requirements-build.txt`, and `pywebview>=5.0`.
3. Runs `python -m unittest discover -s tests -t .`.
4. Builds `dist\YawmJadidAcademy\YawmJadidAcademy.exe` via `YawmJadidAcademy.spec`.
5. Verifies the EXE (`scripts\verify_build_artifact.py`) and dist payload (`scripts\verify_build.py`).
6. Runs the isolated headless smoke test (`scripts\smoke_exe.ps1`).
7. Saves `build-freeze.txt` and compiles `installer\YawmJadidAcademy.iss` via `iscc`.

### Interactive Build & Launch
```bat
build_and_run.bat /strict
```
Supports `/fast` (skip tests & smoke), `/run` (launch existing EXE), `/dev` (run from source), and `/nopause`. Also packages `release\YawmJadidAcademy-1.3.0-portable.zip`.

---

## Expected Build Outputs
- `dist\YawmJadidAcademy\YawmJadidAcademy.exe`
- `release\YawmJadidAcademy-1.3.0-portable.zip`
- `installer\Output\YawmJadidAcademy-Setup-1.3.0.exe`
- `build_verification_report.json`, `build-freeze.txt`
