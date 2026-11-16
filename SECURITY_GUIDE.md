# SECURITY_GUIDE.md — Yawm Jadid Academy (v1.3.0)

## Security Architecture
- **Loopback-Only Binding:** Server binds exclusively to `127.0.0.1` (default port `8890`). Non-loopback clients, invalid `Host` headers, and cross-origin `Origin` headers are rejected with HTTP `403`.
- **Per-Launch `X-Window-Secret`:** Generated per launch via `secrets.token_urlsafe(24)`. Planted as an `httponly; samesite=strict` cookie on bootstrap (`?wsec=`) and verified with `secrets.compare_digest` on every `/api/*` request.
- **Optional Single-User PIN Lock:** Stored as salted `hashlib.scrypt` (`n=16384, r=8, p=1`), verified via `hmac.compare_digest`, protected by thread-safe exponential backoff after 5 consecutive failures.
- **Upload & Import Hardening:** `MaxBodySizeASGIMiddleware` enforces a 25 MB limit; `sanitize_upload_filename` strips path traversal and control characters; `import_service.py` enforces XXE/zip-bomb and row limits; `excel_service.py` neutralizes formula injection.
- **XSS & Error Sanitization:** `dom.js` (`renderHtml`) auto-escapes interpolated values; `unhandled_error` returns generic 500 messages without stack traces.
- **Secrets Policy:** Never commit `.env`, API keys, certificates, or user `.sqlite3` databases (`scripts/verify_build_artifact.py` enforces forbidden payload checks).
