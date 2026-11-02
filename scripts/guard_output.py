#!/usr/bin/env python3
"""Keep the files a session makes for the user in one folder per repo.

A report, a spreadsheet or a PDF written into the repo dirties `git status`, and one left
in a scratchpad is never found again. They go to the output folder instead - `output_dir`
in the switches file (`switches.py`), set with `norms-config` - each repo in a folder of
its own:
  - a repo's main checkout or a linked worktree : `<repo>`
  - no repo                                     : `_general`
A worktree shares its repo's folder because one is made per task, and a folder per
worktree left one more folder behind for every task.
On one machine the root of that folder had collected some 210 loose files from every repo
before the rule existed, each sorted back by hand from session transcripts.

Until the user sets a folder there is none: the norms print no `OUTPUT` block, this hook
passes every call, and files go where Claude Code puts them without the plugin.

The session norms print the folder; this hook refuses a tool call naming a folder of the
root that neither exists nor is the session's own. Reading what is already there passes.

Exit 0 = pass, exit 2 = block. The user's `guard_output` switch (`switches.py`) can make
it warn instead of refusing, or do nothing; every refusal names it.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

import host
import switches

NO_REPO = "_general"
# A name ends at a quote, a space, a bracket or a separator. One that opens with `$`, `%`,
# `{`, `<` or `*` is a variable, a placeholder or a glob: unknowable here, so it passes.
NAME = r"""[^\\/"'`\s<>|*?:;,()\[\]{}$%]+"""
DOTS = re.compile(r"\.+")


def base(value=None):
    """The output folder: `value`, else the one the user set; None while there is none."""
    value = switches.output_dir() if value is None else value.strip()
    return Path(os.path.expandvars(os.path.expanduser(value))) if value else None


def checkout(cwd: str) -> str:
    """The repo's name, its main checkout's from a linked worktree. Empty outside a repo."""
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--path-format=absolute", "--git-common-dir", "--git-dir", "--show-toplevel"],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    lines = result.stdout.splitlines()
    if result.returncode or len(lines) < 3:
        return ""
    common, git_dir, top = (Path(line) for line in lines[:3])
    if os.path.normcase(git_dir) == os.path.normcase(common):
        return top.name
    # A linked worktree has a git dir of its own; the shared one sits in the main checkout.
    return common.parent.name


def own(cwd: str) -> str:
    return checkout(cwd) or NO_REPO


def folder(cwd: str):
    """The folder this session's output files go to; None while no output folder is set."""
    root = base()
    return root / own(cwd) if root else None


def strings(value, out: list) -> list:
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, dict):
        for item in value.values():
            strings(item, out)
    elif isinstance(value, list):
        for item in value:
            strings(item, out)
    return out


def named(tool_input, root: Path) -> list[str]:
    """Each folder a tool call names under the output folder.

    The folder is matched by its last two names, so `C:\\Users\\me\\Downloads\\Claude`,
    `/c/Users/me/Downloads/Claude`, `~/Downloads/Claude` and `$HOME/Downloads/Claude` are
    one place. Residual ceiling: a path built at runtime - `Path(out) / "x.xlsx"`,
    `Join-Path $root $name` - is not seen."""
    names = list(root.parts[1:] if root.anchor else root.parts)[-2:]
    if not names:
        return []
    pattern = re.compile(
        r"(?<![\w.-])" + r"[\\/]+".join(map(re.escape, names)) + rf"[\\/]+({NAME})",
        re.I,
    )
    return [
        m.group(1)
        for text in strings(tool_input, [])
        for m in pattern.finditer(text)
        if not DOTS.fullmatch(m.group(1))
    ]


def folders(path: Path) -> set[str]:
    try:
        return {p.name.lower() for p in path.iterdir() if p.is_dir()}
    except OSError:
        return set()


def refused(tool_input, cwd: str) -> list[str]:
    root = base()
    found = named(tool_input, root) if root else []
    if not found:
        return []
    allowed = folders(root) | {NO_REPO, own(cwd).lower()}
    return [name for name in found if name.lower() not in allowed]


def main() -> None:
    payload = host.read_payload()
    if switches.mode("guard_output") == switches.OFF:
        sys.exit(0)
    cwd = payload.get("cwd") or os.getcwd()
    bad = refused(payload.get("tool_input"), cwd)
    if not bad:
        sys.exit(0)
    root = base()
    there = sorted(folders(root))
    switches.refuse(
        "guard_output",
        f"REFUSED: `{'`, `'.join(dict.fromkeys(bad))}` in `{root}` is not this session's output folder.\n\n"
        f"Write the file to `{folder(cwd)}`. A worktree writes to its repo's folder; a session\n"
        f"outside a repo writes to `{NO_REPO}`.\n"
        f"Folders already there: {', '.join(there) or '(none yet)'}.\n"
        "Send it again with that path. A path built at runtime to get past this is the same\n"
        "mistake, unseen.\n",
        payload,
    )


if __name__ == "__main__":
    main()
