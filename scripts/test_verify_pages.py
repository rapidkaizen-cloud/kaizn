#!/usr/bin/env python3
"""Self-check verify_pages.js: its arguments and its table, then its refusals.

The checks themselves run in a browser this repo has no copy of; the `--selftest` mode is the
part that needs none. Skipped, and said so, on a machine with no `node`.
Run directly: python3 test_verify_pages.py
"""
import shutil
import subprocess
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent / "verify_pages.js"


def run(*args: str, cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["node", str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8", cwd=cwd)


def main() -> None:
    if not shutil.which("node"):
        print("verify_pages: skipped - no node on this machine")
        return
    # What must pass: a well-formed call and a table whose clean rows pass.
    done = run("--selftest")
    assert done.returncode == 0 and done.stdout.strip() == "ok", done.stderr or done.stdout
    # What must be refused: a call missing its widths, and a repo with no Playwright.
    done = run("--url", "http://localhost:5173", "home=/")
    assert done.returncode == 2 and "--widths" in done.stderr, done.stderr
    with tempfile.TemporaryDirectory() as empty:
        done = run("--url", "http://localhost:5173", "--widths", "1440,375", "home=/", cwd=empty)
    assert done.returncode == 3 and "not verified" in done.stderr, done.stderr
    print("verify_pages: ok")


if __name__ == "__main__":
    main()
