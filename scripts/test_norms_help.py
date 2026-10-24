#!/usr/bin/env python3
"""Self-check norms_help.py: the card holds the version, the commands, the pages and one entry.

The last case reads this repo's own docs. `docs/README.md` is the index on GitHub, the
site's sidebar and the card's page list at once, so a page it does not list is in none of
them, and a link it holds to a page that is gone breaks all three. Both fail here.
Run directly: python3 test_norms_help.py
"""
import importlib.util
import json
import re
import subprocess
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent / "norms_help.py"
DOCS = SCRIPT.parent.parent / "docs"

# `python3`, not sys.executable: the name the skill tells a session to run.
PYTHON = "python3"

spec = importlib.util.spec_from_file_location("norms_help", SCRIPT)
norms_help = importlib.util.module_from_spec(spec)
spec.loader.exec_module(norms_help)

COMMANDS = """\
# Commands

| Situation | Run |
|---|---|
| New app | `/x:settle` |
"""
PAGES = """\
# docs

| Page | Holds |
|---|---|
| [Gates](concepts/gates.md) | The stops |
"""
CHANGELOG = """\
# Changelog

Intro.

## [kaizn 0.3.0] - 2026-02-01

- third

To act on:

- rename the thing

## [kaizn 0.2.0] - 2026-01-10

- second
"""


def demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / ".claude-plugin").mkdir()
        (root / ".claude-plugin" / "plugin.json").write_text(json.dumps({"version": "0.3.0"}), encoding="utf-8")

        # a copy holding nothing but its manifest still names its version, and adds no empty block
        assert norms_help.card(root) == "kaizn 0.3.0\n"

        (root / "docs" / "reference").mkdir(parents=True)
        (root / "docs" / "reference" / "commands.md").write_text(COMMANDS, encoding="utf-8")
        (root / "docs" / "README.md").write_text(PAGES, encoding="utf-8")
        (root / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
        out = norms_help.card(root)

        assert out.startswith("kaizn 0.3.0\n")
        # the commands and the pages: each file whole, without its title
        assert "`/x:settle`" in out and "# Commands" not in out
        assert "concepts/gates.md" in out and "# docs" not in out
        # the version's change: the top entry whole, and no older one
        assert "## [kaizn 0.3.0] - 2026-02-01" in out and "- rename the thing" in out
        assert "0.2.0" not in out and "- second" not in out
        assert out.index("COMMANDS") < out.index("PAGES") < out.index("LAST CHANGE")

    # as the skill runs it, on this repo: the real files must fill every block
    result = subprocess.run([PYTHON, str(SCRIPT)], capture_output=True)
    assert result.returncode == 0, result.stderr
    out = result.stdout.decode("utf-8")
    assert out.startswith("kaizn ")
    assert "COMMANDS" in out and "PAGES" in out and "LAST CHANGE" in out
    assert "/kaizn:norms-help" in out
    assert out.count("\n## [") == 1

    # this repo's index lists every page, and every page it lists exists
    index = (DOCS / "README.md").read_text(encoding="utf-8")
    listed = set(re.findall(r"\]\((?!https?:)([^)]+\.md)\)", index))
    pages = {
        path.relative_to(DOCS).as_posix()
        for path in DOCS.rglob("*.md")
        if "node_modules" not in path.parts and path.name != "README.md"
    } - {"queue.md"}
    assert listed == pages, f"unlisted: {sorted(pages - listed)} - missing: {sorted(listed - pages)}"

    print("ok")


if __name__ == "__main__":
    demo()
