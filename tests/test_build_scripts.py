"""F9 - release builds must use Python 3.12 only; the 3.14 fallback must be opt-in and never release-qualifying."""
from __future__ import annotations

import re
import unittest

from tests import _helpers  # noqa: F401  (sets sys.path)
from tests._helpers import ROOT

SCRIPTS = ["build_windows.bat", "build_and_run.bat"]
LAUNCHERS = SCRIPTS + ["START_ACADEMY.bat", "scripts/make_lock.bat"]


class BuildScriptTests(unittest.TestCase):
    def test_python_314_fallback_is_opt_in(self):
        for name in SCRIPTS:
            text = (ROOT / name).read_text(encoding="utf-8")
            for m in re.finditer(r"py -3\.14", text):
                head = text[: m.start()]
                guard = head.rfind('if not defined PY if "%ALLOW_PROVISIONAL_BUILD%"=="1" (')
                self.assertGreater(guard, -1, f"{name}: py -3.14 reachable without ALLOW_PROVISIONAL_BUILD=1")
                self.assertLess(m.start() - guard, 400, f"{name}: guard too far from the 3.14 probe")

    def test_provisional_is_labelled_not_for_release(self):
        for name in SCRIPTS:
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("NOT FOR RELEASE", text, name)

    def test_build_does_not_overwrite_committed_lock(self):
        text = (ROOT / "build_windows.bat").read_text(encoding="utf-8")
        self.assertNotRegex(text, r"freeze\s*>\s*requirements\.lock")
        self.assertTrue((ROOT / "scripts" / "make_lock.bat").is_file())

    def test_launchers_are_ascii_with_crlf(self):
        """cmd.exe mis-parses LF-only batch files (goto/labels) and non-ASCII text without a matching code page."""
        for name in LAUNCHERS:
            raw = (ROOT / name).read_bytes()
            self.assertTrue(all(b < 128 for b in raw), f"{name}: contains non-ASCII bytes")
            self.assertEqual(raw.count(b"\n"), raw.count(b"\r\n"), f"{name}: has LF-only line endings")

    def test_pywebview_is_optional_in_requirements(self):
        core = (ROOT / "requirements-core.txt").read_text(encoding="utf-8").lower()
        self.assertNotIn("pywebview", [ln.split(">")[0].strip() for ln in core.splitlines() if not ln.startswith("#")])
        build = (ROOT / "requirements-build.txt").read_text(encoding="utf-8")
        self.assertIn("requirements-core.txt", build)


    def test_batch_labels_and_blocks_valid(self):
        """Every goto/call :label must resolve to a top-level :label (not nested inside parens)."""
        for name in LAUNCHERS:
            text = (ROOT / name).read_text(encoding="utf-8")
            labels = set(re.findall(r"(?im)^:([A-Za-z0-9_]+)\b", text))
            targets = re.findall(r"(?im)\b(?:goto|call)\s+:([A-Za-z0-9_]+)\b", text)
            missing = [t for t in targets if t.lower() != "eof" and t.lower() not in {l.lower() for l in labels}]
            self.assertEqual(missing, [], f"{name}: missing batch label targets {missing}")
            # Ensure no label definition appears while inside a parenthesized block
            depth = 0
            for idx, line in enumerate(text.splitlines(), 1):
                stripped = line.strip()
                if stripped.upper().startswith("REM ") or stripped.startswith("::"):
                    continue
                if stripped.startswith(":") and depth > 0:
                    self.fail(f"{name}:{idx}: label {stripped} defined inside parenthesized block (depth={depth})")
                # Track unescaped parens outside quotes
                in_q = False
                for ch in stripped:
                    if ch == '"':
                        in_q = not in_q
                    elif not in_q:
                        if ch == "(":
                            depth += 1
                        elif ch == ")" and depth > 0:
                            depth -= 1

if __name__ == "__main__":
    unittest.main()
