#!/usr/bin/env python3
"""Show and set the user's switches for the norms and hooks of kaizn.

The `norms-config` skill runs this. The switches sit in `switches.json` in the plugin's
data folder, one file for every repo on the machine. A shell command gets no
`CLAUDE_PLUGIN_DATA`, so the skill passes the folder Claude Code wrote into its text. `set`
writes every rule's mode, the ones named changed, and creates the folder where it is
missing.

Usage: python3 norms_config.py --data DIR show
       python3 norms_config.py --data DIR set KEY=MODE [KEY=MODE ...]
Exit 0 = done, exit 2 = refused and nothing written.
"""
import json
import os
import sys
from pathlib import Path

import switches


def refuse(message: str) -> None:
    sys.stderr.write(f"REFUSED: {message}\n")
    sys.exit(2)


def show(folder: Path, modes: dict) -> str:
    width = max(map(len, switches.RULES))
    lines = [f"switches in {folder / switches.FILE}", "rule, mode now, modes it takes, what it does:", ""]
    for key, (allowed, what) in switches.RULES.items():
        lines.append(f"{key:<{width}}  {modes[key]:<6}  {'|'.join(allowed):<13}  {what}")
    return "\n".join(lines) + "\n"


def parse(pairs: list) -> dict:
    """KEY=MODE pairs, every one checked before anything is written."""
    wanted, wrong = {}, []
    for pair in pairs:
        key, sep, value = pair.partition("=")
        key, value = key.strip(), switches.read(value)
        if not sep or key not in switches.RULES:
            wrong.append(f"`{pair}` names no switch")
        elif value not in switches.RULES[key][0]:
            wrong.append(f"`{key}` takes {', '.join(switches.RULES[key][0])}, not `{value}`")
        else:
            wanted[key] = value
    if wrong or not wanted:
        refuse("; ".join(wrong or ["no KEY=MODE given"]) + f". The switches: {', '.join(switches.RULES)}.")
    return wanted


def write(folder: Path, modes: dict) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    # Written beside the file and moved over it, so a failed write never leaves half a file.
    temp = folder / (switches.FILE + ".tmp")
    temp.write_text(json.dumps(modes, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, folder / switches.FILE)


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = sys.argv[1:]
    if args[:1] != ["--data"] or len(args) < 3 or args[2] not in ("show", "set"):
        refuse("usage: norms_config.py --data DIR show | set KEY=MODE ...")
    # The skill's text left unsubstituted reaches here empty or as `${...}`: never a folder.
    folder = Path(args[1].strip())
    if not args[1].strip() or "$" in args[1] or not folder.is_absolute():
        refuse(f"no plugin data folder was given (`{args[1]}`): switches are not available on this host")
    wanted = parse(args[3:]) if args[2] == "set" else {}
    modes = switches.stored(folder)
    if wanted:
        modes.update(wanted)
        try:
            write(folder, modes)
        except OSError as error:
            refuse(f"cannot write `{folder / switches.FILE}`: {error}")
    sys.stdout.write(show(folder, modes))


if __name__ == "__main__":
    main()
