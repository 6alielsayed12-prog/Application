# INSTALLATION.md — Yawm Jadid Academy (v1.3.0)

## System Requirements
- **OS:** Windows 10 or Windows 11 (64-bit)
- **WebView2:** Microsoft Edge WebView2 Runtime (preinstalled on Windows 11 and modern Windows 10; falls back to default browser if absent)
- **Running from Source Only:** Python 3.12+ (64-bit) from [python.org](https://www.python.org/downloads/windows/) with `Add python.exe to PATH` enabled

---

## Installation Options

### Option 1: Windows Installer (Recommended)
1. Run `YawmJadidAcademy-Setup-1.3.0.exe` (per-user install, no administrator privileges required).
2. Launch **Yawm Jadid Academy** from the Start Menu or Desktop shortcut.

### Option 2: Portable ZIP Distribution
1. Extract `YawmJadidAcademy-1.3.0-portable.zip` to a local drive folder (e.g., `C:\YawmJadidAcademy\`).
   - **Important:** Do not run from a network UNC path (`\\server\share`) or an actively synced OneDrive/Dropbox folder.
2. Run `YawmJadidAcademy.exe`.

### Option 3: Run from Source
1. Extract the repository to a local folder.
2. Double-click `START_ACADEMY.bat` (creates `.venv`, installs `requirements-core.txt` + optional `pywebview`, and launches `pythonw -m alahd_erp.main`).

---

## Data Storage & Upgrades
All user data is stored **outside** the application folder at:
```text
%LOCALAPPDATA%\AlAhdAcademySuite\
├── alahd_erp_v1.sqlite3      # Primary SQLite WAL database
├── backups\                  # Automatic, daily, and exit backups
└── logs\alahd_erp.log        # Rotating application log
```
Override the data directory with `ALAHD_ERP_HOME` if needed. Upgrading or uninstalling never deletes `%LOCALAPPDATA%\AlAhdAcademySuite\`.
