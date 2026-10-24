#!/usr/bin/env python3
"""Print the help card of this copy of kaizn: version, commands, pages, last change.

The `norms-help` skill runs this from the plugin folder it was read from, so the card is
about the copy the session runs: a machine keeps one folder per installed version, and
the newest of them is not always the one a session loaded.

Nothing is written for the card alone. The commands are `docs/reference/commands.md`, the
pages are `docs/README.md`, and the last change is the top entry of `CHANGELOG.md` - each
printed as its file holds it, so the card cannot disagree with them.

Usage: python3 norms_help.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ".claude-plugin/plugin.json"


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def page(path: Path) -> str:
    """A docs page without its title line. Empty when the file is gone."""
    return re.sub(r"\A#[^\n]*\n", "", read(path)).strip()


def last_change(changelog: str) -> str:
    """The top entry, heading included, and nothing below it."""
    found = re.search(r"^## \[.*?(?=^## \[|\Z)", changelog, re.S | re.M)
    return found[0].strip() if found else ""


def card(root: Path) -> str:
    version = json.loads((root / MANIFEST).read_text(encoding="utf-8"))["version"]
    blocks = [
        ("COMMANDS", page(root / "docs" / "reference" / "commands.md")),
        ("PAGES - under docs/ of the plugin folder", page(root / "docs" / "README.md")),
        ("LAST CHANGE", last_change(read(root / "CHANGELOG.md"))),
    ]
    out = [f"kaizn {version}"]
    for title, body in blocks:
        if body:
            out += ["", title, "", body]
    return "\n".join(out) + "\n"


def main() -> None:
    # On Windows stdout defaults to the ANSI codepage, which mangles the dashes these files use.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.stdout.write(card(ROOT))


if __name__ == "__main__":
    main()
