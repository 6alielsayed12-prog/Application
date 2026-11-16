# DEPENDENCY_AUDIT.md — YawmJadidAcademy (v1.3.0)

**Audit Date:** 2026-11-16

---

## 1. Dependency Manifests Inspected

- `pyproject.toml`: `requires-python = ">=3.12"`, core dependencies `fastapi`, `uvicorn`, `pydantic`, `pywebview`, `openpyxl`; optional `dev = ["ruff", "mypy", "httpx"]`, `build = ["pyinstaller"]`.
- `requirements-core.txt`: `fastapi>=0.110`, `uvicorn>=0.29`, `pydantic>=2.6`, `openpyxl>=3.1` (`pywebview` intentionally optional so headless/CI or browser-fallback environments still work, enforced by `test_pywebview_is_optional_in_requirements`).
- `requirements-build.txt`: `-r requirements-core.txt`, `pyinstaller>=6.5`, `httpx>=0.27`.
- `requirements.txt`: Lower bounds including `pywebview>=5.0`.

---

## 2. Findings & Compatibility

1. **No Missing Runtime Dependencies**: All third-party imports in `alahd_erp/` (`fastapi`, `uvicorn`, `pydantic`, `openpyxl`, optional `webview`) are declared.
2. **Pydantic v1 / v2 Compatibility**: `alahd_erp/api/server.py` uses `BaseModel` and `Field` without v2-only decorators, working cleanly on both `pydantic 1.10.4` (Linux sandbox) and `pydantic>=2.6` (Windows 3.12).
3. **Lockfile Procedure (`requirements.lock`)**:
   - No `requirements.lock` is committed yet because Windows-specific wheels (`pywebview`, `pythonnet`, `clr_loader`) must be frozen on Windows Python 3.12 x64 via `scripts\make_lock.bat`.
   - **Improvement Applied**: Updated `build_and_run.bat` to honor `requirements.lock` when present (matching `build_windows.bat` and `.github/workflows/windows-build.yml`).
