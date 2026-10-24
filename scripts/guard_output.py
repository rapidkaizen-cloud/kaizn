#!/usr/bin/env python3
"""Keep the files a session makes for the user in one folder per repo and per worktree.

A report, a spreadsheet or a PDF written into the repo dirties `git status`, and one left
in a scratchpad is never found again. They go to the output folder instead - `output_dir`
in the plugin's settings, `Downloads/Claude` in the home folder while that is empty - each
session in a folder of its own:
  - a repo's main checkout : `<repo>`
  - a linked worktree      : `<repo>-<worktree>`, beside its repo's folder, never inside it
  - no repo                : `_general`
On one machine the root of that folder had collected some 210 loose files from every repo
before the rule existed, each sorted back by hand from session transcripts.

The session norms print the folder; this hook refuses a tool call naming a folder of the
root that neither exists nor is the session's own, and, from a worktree, a name inside its
repo's folder that does not exist yet. Reading what is already there passes.

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

OPTION = "CLAUDE_PLUGIN_OPTION_OUTPUT_DIR"
NO_REPO = "_general"
# A name ends at a quote, a space, a bracket or a separator. One that opens with `$`, `%`,
# `{`, `<` or `*` is a variable, a placeholder or a glob: unknowable here, so it passes.
NAME = r"""[^\\/"'`\s<>|*?:;,()\[\]{}$%]+"""
DOTS = re.compile(r"\.+")


def base() -> Path:
    """The output folder: the plugin setting, else `Downloads/Claude` in the home folder."""
    value = os.environ.get(OPTION, "").strip()
    return Path(os.path.expandvars(os.path.expanduser(value))) if value else Path.home() / "Downloads" / "Claude"


def checkout(cwd: str) -> tuple[str, str]:
    """The repo's name and, in a linked worktree, the worktree's folder name. Empty outside a repo."""
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--path-format=absolute", "--git-common-dir", "--git-dir", "--show-toplevel"],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return "", ""
    lines = result.stdout.splitlines()
    if result.returncode or len(lines) < 3:
        return "", ""
    common, git_dir, top = (Path(line) for line in lines[:3])
    if os.path.normcase(git_dir) == os.path.normcase(common):
        return top.name, ""
    # A linked worktree has a git dir of its own; the shared one sits in the main checkout.
    return common.parent.name, top.name


def own(repo: str, worktree: str) -> str:
    if not repo:
        return NO_REPO
    if not worktree:
        return repo
    return worktree if worktree.lower().startswith(repo.lower() + "-") else f"{repo}-{worktree}"


def folder(cwd: str) -> Path:
    """The folder this session's output files go to."""
    return base() / own(*checkout(cwd))


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


def named(tool_input, root: Path) -> list[tuple[str, str]]:
    """Each (folder, name inside it) a tool call names under the output folder.

    The folder is matched by its last two names, so `C:\\Users\\me\\Downloads\\Claude`,
    `/c/Users/me/Downloads/Claude`, `~/Downloads/Claude` and `$HOME/Downloads/Claude` are
    one place. Residual ceiling: a path built at runtime - `Path(out) / "x.xlsx"`,
    `Join-Path $root $name` - is not seen."""
    names = list(root.parts[1:] if root.anchor else root.parts)[-2:]
    if not names:
        return []
    pattern = re.compile(
        r"(?<![\w.-])" + r"[\\/]+".join(map(re.escape, names)) + rf"[\\/]+({NAME})(?:[\\/]+({NAME}))?",
        re.I,
    )
    return [
        (m.group(1), m.group(2) or "")
        for text in strings(tool_input, [])
        for m in pattern.finditer(text)
        if not DOTS.fullmatch(m.group(1))
    ]


def entries(path: Path, dirs_only: bool = False) -> set[str]:
    try:
        return {p.name.lower() for p in path.iterdir() if not dirs_only or p.is_dir()}
    except OSError:
        return set()


def refused(tool_input, cwd: str) -> list[str]:
    root = base()
    found = named(tool_input, root)
    if not found:
        return []
    repo, worktree = checkout(cwd)
    allowed = entries(root, dirs_only=True) | {NO_REPO, own(repo, worktree).lower()}
    bad = []
    for name, inside in found:
        if name.lower() not in allowed:
            bad.append(name)
        elif worktree and name.lower() == repo.lower() and inside and not DOTS.fullmatch(inside):
            # shortcut: a name is cut at its first space or bracket, so it is matched by prefix -
            # a new file sharing its opening with an old one passes; tighten if that happens.
            if not any(e.startswith(inside.lower()) for e in entries(root / name)):
                bad.append(f"{name}/{inside}")
    return bad


def main() -> None:
    payload = host.read_payload()
    if switches.mode("guard_output") == switches.OFF:
        sys.exit(0)
    cwd = payload.get("cwd") or os.getcwd()
    bad = refused(payload.get("tool_input"), cwd)
    if not bad:
        sys.exit(0)
    root = base()
    there = sorted(entries(root, dirs_only=True))
    switches.refuse(
        "guard_output",
        f"REFUSED: `{'`, `'.join(dict.fromkeys(bad))}` in `{root}` is not this session's output folder.\n\n"
        f"Write the file to `{folder(cwd)}`. A worktree has its own folder beside its repo's, never\n"
        f"one inside it; a session outside a repo writes to `{NO_REPO}`.\n"
        f"Folders already there: {', '.join(there) or '(none yet)'}.\n"
        "Send it again with that path. A path built at runtime to get past this is the same\n"
        "mistake, unseen.\n",
        payload,
    )


if __name__ == "__main__":
    main()
