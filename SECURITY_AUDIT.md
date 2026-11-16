# SECURITY_AUDIT.md — YawmJadidAcademy (v1.3.0)

**Audit Date:** 2026-11-16

---

## 1. Security Controls Verified

| Control | Implementation | Verification |
|---|---|---|
| **Localhost & DNS-Rebinding Guard** | `server.py` (`LOOPBACK`, `host_allowed`, `origin_allowed` in `security_utils.py`) | Rejects non-loopback clients, invalid `Host` headers (IPv4/IPv6), and cross-origin requests with HTTP 403. |
| **Per-Launch `X-Window-Secret`** | `server.py` (`secrets.token_urlsafe(24)` + `secrets.compare_digest`) | Required via header or `httponly; samesite=strict` cookie on all `/api/*` routes; `?wsec=` accepted only on `BOOTSTRAP_PATHS`. |
| **PIN Lock Storage & Brute-Force Protection** | `database.py` (`hashlib.scrypt`, n=16384, r=8, p=1, random salt, `hmac.compare_digest`), `server.py` (`pin_guard` + `threading.Lock`) | Salted `scrypt` hash; exponential backoff after 5 consecutive failures (capped at 300s). |
| **Request Size & Upload Hardening** | `MaxBodySizeASGIMiddleware` (25 MB cap on Content-Length & chunked streams), `sanitize_upload_filename`, `parse_multipart_upload` | Strips path traversal & control chars; returns HTTP 413 on oversized bodies. |
| **Excel Import & Export Safety** | `import_service.py` (XXE/zip-bomb bounds), `excel_service.py` (formula injection prefixing) | Tested by `test_import_excel_limits.py` and `test_destructive_and_portable_paths.py`. |
| **XSS & Security Headers** | `dom.js` (`renderHtml` auto-escaping), `server.py` (`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, `Cache-Control: no-store`) | Zero unescaped `innerHTML` sinks; zero external URLs in `index.html`. |
| **Error Disclosure** | `server.py` (`unhandled_error` handler) | Logs tracebacks internally; returns generic Arabic 500 JSON message to clients. |
| **Static Code Hygiene** | AST scan across `alahd_erp/` (29 files) | Zero bare `except:`, `eval()`, `exec()`, `pickle.load()`, `yaml.load()`, `os.system()`, or `subprocess(..., shell=True)`. |

---

## 2. Residual / Accepted Risks

- **Single-User Local Desktop Model (Low)**: Traffic over `127.0.0.1` is unencrypted HTTP (standard for local `pywebview` desktop apps); mitigated by `X-Window-Secret` and loopback-only binding.
- **Unauthenticated Local Bootstrap Option (Info)**: `ALAHD_ALLOW_OPEN_BOOTSTRAP=1` is off by default and only for manual developer debugging.
- **Non-Loopback TestClient Skip (Info)**: `tests/test_http_api.py::OriginAndHost::test_non_loopback_client_blocked` is skipped on older Starlette (`0.26.1`) where `TestClient(client=...)` is unsupported; runs on Windows CI with `fastapi>=0.110`.
