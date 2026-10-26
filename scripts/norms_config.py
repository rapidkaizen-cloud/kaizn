#!/usr/bin/env python3
"""Show and set the user's switches for the norms and hooks of kaizn, and the output folder.

The `norms-config` skill runs this. The switches sit in `switches.json` in the plugin's
data folder, one file for every repo on the machine, with the output folder under
`output_dir`. A shell command gets no `CLAUDE_PLUGIN_DATA`, so the skill passes the folder
Claude Code wrote into its text. `set` writes every rule's mode and the output folder, the
ones named changed, and creates the folder where it is missing. `output_dir=none` unsets
the output folder.

Usage: python3 norms_config.py --data DIR show
       python3 norms_config.py --data DIR set KEY=MODE [KEY=MODE ...] [output_dir=PATH]
Exit 0 = done, exit 2 = refused and nothing written.
"""
import json
import os
import sys
from pathlib import Path

import guard_output
import switches


def refuse(message: str) -> None:
    sys.stderr.write(f"REFUSED: {message}\n")
    sys.exit(2)


def show(folder: Path, modes: dict, place: str) -> str:
    width = max(map(len, switches.RULES))
    lines = [f"switches in {folder / switches.FILE}", "rule, mode now, modes it takes, what it does:", ""]
    for key, (allowed, what) in switches.RULES.items():
        lines.append(f"{key:<{width}}  {modes[key]:<6}  {'|'.join(allowed):<13}  {what}")
    lines += [
        "",
        f"{switches.OUTPUT_DIR}: {place or 'not set - files go where Claude Code puts them without the plugin'}",
        "  where sessions write the files they make for the user, one folder per repo and per worktree;",
        f"  set with {switches.OUTPUT_DIR}=<full path>, unset with {switches.OUTPUT_DIR}=none",
    ]
    return "\n".join(lines) + "\n"


def parse(pairs: list) -> dict:
    """KEY=MODE pairs, every one checked before anything is written."""
    wanted, wrong = {}, []
    for pair in pairs:
        key, sep, value = pair.partition("=")
        key = key.strip()
        if sep and key == switches.OUTPUT_DIR:
            # A path keeps its case, and is stored expanded so the file alone names the folder.
            value = "" if value.strip().lower() == "none" else value.strip()
            if value and not guard_output.base(value).is_absolute():
                wrong.append(f"`{key}` takes a full path or `none`, not `{value}`")
            else:
                wanted[key] = str(guard_output.base(value)) if value else ""
            continue
        value = switches.read(value)
        if not sep or key not in switches.RULES:
            wrong.append(f"`{pair}` names no switch")
        elif value not in switches.RULES[key][0]:
            wrong.append(f"`{key}` takes {', '.join(switches.RULES[key][0])}, not `{value}`")
        else:
            wanted[key] = value
    if wrong or not wanted:
        refuse("; ".join(wrong or ["no KEY=MODE given"]) + f". The switches: {', '.join(switches.RULES)}, and {switches.OUTPUT_DIR}.")
    return wanted


def write(folder: Path, modes: dict, place: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    # Written beside the file and moved over it, so a failed write never leaves half a file.
    temp = folder / (switches.FILE + ".tmp")
    held = {**modes, switches.OUTPUT_DIR: place} if place else modes
    temp.write_text(json.dumps(held, indent=2) + "\n", encoding="utf-8")
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
    modes, place = switches.stored(folder), switches.place(folder)
    if wanted:
        place = wanted.pop(switches.OUTPUT_DIR, place)
        modes.update(wanted)
        try:
            write(folder, modes, place)
        except OSError as error:
            refuse(f"cannot write `{folder / switches.FILE}`: {error}")
    sys.stdout.write(show(folder, modes, place))


if __name__ == "__main__":
    main()
