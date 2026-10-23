#!/usr/bin/env python3
"""Show and set the user's switches for the norms and hooks of raizen-norms.

The `norms-config` skill runs this. A shell command gets no `CLAUDE_PLUGIN_OPTION_*`, so
the switches are read where Claude Code keeps them: `pluginConfigs` in the user's
`settings.json`, under the plugin's id `raizen-norms@<marketplace>` - read from the file,
never assumed. `set` writes the switches it is given and nothing else: every other key
stays, in its order, and the file keeps its indent and its line endings.

Usage: python3 norms_config.py [--settings PATH] show
       python3 norms_config.py [--settings PATH] set KEY=MODE [KEY=MODE ...]
Exit 0 = done, exit 2 = refused and nothing written.
"""
import json
import os
import re
import sys
from pathlib import Path

import switches

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
NAME = MANIFEST["name"]
OPTIONS = MANIFEST.get("userConfig") or {}


def refuse(message: str) -> None:
    sys.stderr.write(f"REFUSED: {message}\n")
    sys.exit(2)


def settings_file(arg: str) -> Path:
    if arg:
        return Path(arg)
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "settings.json"


def load(path: Path) -> tuple:
    """The file's text and its JSON. Refused when it cannot be read as an object."""
    try:
        text = path.read_bytes().decode("utf-8-sig")
        data = json.loads(text)
    except (OSError, ValueError) as error:
        refuse(f"cannot read `{path}` as JSON: {error}")
    if not isinstance(data, dict):
        refuse(f"`{path}` holds no JSON object")
    return text, data


def ids(data: dict) -> list:
    """The plugin's ids in this file: the enabled ones, else any it holds options for."""
    mine = lambda pid: isinstance(pid, str) and pid.partition("@")[0] == NAME and "@" in pid
    enabled = data.get("enabledPlugins") if isinstance(data.get("enabledPlugins"), dict) else {}
    configs = data.get("pluginConfigs") if isinstance(data.get("pluginConfigs"), dict) else {}
    return [p for p, on in enabled.items() if mine(p) and on is True] or [p for p in configs if mine(p)]


def stored(data: dict, pid: str) -> dict:
    """Each switch's mode as the file holds it for `pid`; missing or unknown is `on`."""
    configs = data.get("pluginConfigs")
    entry = configs.get(pid) if isinstance(configs, dict) else None
    options = entry.get("options") if isinstance(entry, dict) else None
    options = options if isinstance(options, dict) else {}
    found = {key: switches.read(options.get(key)) for key in switches.RULES}
    return {key: value if value in switches.RULES[key] else switches.ON for key, value in found.items()}


def show(path: Path, data: dict, pid: str) -> str:
    modes = stored(data, pid)
    width = max(map(len, switches.RULES))
    lines = [f"{pid} in {path}", "rule, mode now, modes it takes, what it does:", ""]
    for key, allowed in switches.RULES.items():
        option = OPTIONS.get(key) or {}
        lines.append(f"{key:<{width}}  {modes[key]:<6}  {'|'.join(allowed):<13}  {option.get('title', '')}: {option.get('description', '')}")
    return "\n".join(lines) + "\n"


def parse(pairs: list) -> dict:
    """KEY=MODE pairs, every one checked before anything is written."""
    wanted, wrong = {}, []
    for pair in pairs:
        key, sep, value = pair.partition("=")
        key, value = key.strip(), switches.read(value)
        if not sep or key not in switches.RULES:
            wrong.append(f"`{pair}` names no switch")
        elif value not in switches.RULES[key]:
            wrong.append(f"`{key}` takes {', '.join(switches.RULES[key])}, not `{value}`")
        else:
            wanted[key] = value
    if wrong or not wanted:
        refuse(
            "; ".join(wrong or ["no KEY=MODE given"])
            + f". The switches: {', '.join(switches.RULES)}."
        )
    return wanted


def write(path: Path, before: str, data: dict) -> None:
    indent = re.search(r'^([ \t]+)"', before, re.M)
    newline = "\r\n" if "\r\n" in before else "\n"
    text = json.dumps(data, indent=indent.group(1) if indent else 2, ensure_ascii=False)
    text = (text + ("\n" if before.endswith("\n") else "")).replace("\n", newline)
    # Written beside the file and moved over it, so a failed write never leaves half a file.
    temp = path.with_name(path.name + ".norms-config.tmp")
    temp.write_bytes(text.encode("utf-8"))
    os.replace(temp, path)


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = sys.argv[1:]
    given = ""
    if args[:1] == ["--settings"] and len(args) > 1:
        given, args = args[1], args[2:]
    if not args or args[0] not in ("show", "set"):
        refuse("usage: norms_config.py [--settings PATH] show | set KEY=MODE ...")
    wanted = parse(args[1:]) if args[0] == "set" else {}
    path = settings_file(given)
    before, data = load(path)
    found = ids(data)
    if not found:
        refuse(f"{NAME} is not enabled in `{path}`: enable the plugin at user scope first")
    if wanted:
        configs = data.setdefault("pluginConfigs", {})
        for pid in found:
            entry = configs.setdefault(pid, {}) if isinstance(configs, dict) else None
            options = entry.setdefault("options", {}) if isinstance(entry, dict) else None
            if not isinstance(options, dict):
                refuse(f"`pluginConfigs` in `{path}` is not in the shape Claude Code writes")
            options.update(wanted)
        write(path, before, data)
    sys.stdout.write(show(path, data, found[0]))


if __name__ == "__main__":
    main()
