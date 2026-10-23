#!/usr/bin/env python3
"""Self-check norms_config.py, and that the manifest and `switches.RULES` list one set.

Every case writes a settings file of its own in a temporary folder and passes it with
`--settings`: the user's real settings are never read or written here.
Run directly: python3 test_norms_config.py
"""
import json
import subprocess
import tempfile
from pathlib import Path

import switches

SCRIPT = Path(__file__).parent / "norms_config.py"
MANIFEST = SCRIPT.parent.parent / ".claude-plugin" / "plugin.json"

# `python3`, not sys.executable: the name the skill tells a session to run.
PYTHON = "python3"


def modes(out: str) -> dict:
    """The mode column of `show`, by switch."""
    return {line.split()[0]: line.split()[1] for line in out.splitlines() if line.split()[:1] and line.split()[0] in switches.RULES}


def run(settings: Path, *args: str) -> tuple:
    result = subprocess.run(
        [PYTHON, str(SCRIPT), "--settings", str(settings), *args], capture_output=True, text=True, encoding="utf-8"
    )
    assert result.returncode in (0, 2), result.stderr
    return result.returncode, result.stdout, result.stderr


def demo() -> None:
    # the manifest offers exactly the switches the scripts read, each defaulting to `on`
    options = json.loads(MANIFEST.read_text(encoding="utf-8"))["userConfig"]
    offered = {key: tuple(o["options"]) for key, o in options.items() if "options" in o}
    assert offered == switches.RULES, offered
    for key in switches.RULES:
        assert options[key]["type"] == "string" and options[key]["default"] == "on", key
        assert options[key]["title"] and options[key]["description"], key
    assert "output_dir" in options

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        def settings(data, name: str = "settings.json", indent=2, newline: str = "\n") -> Path:
            path = tmp / name
            path.write_bytes((json.dumps(data, indent=indent) + "\n").replace("\n", newline).encode("utf-8"))
            return path

        real = {
            "model": "opus",
            "enabledPlugins": {"other@x": True, "raizen-norms@some-market": True},
            "pluginConfigs": {
                "other@x": {"options": {"guard_git": "off"}},
                "raizen-norms@some-market": {"options": {"output_dir": "D:\\Out", "norm_scope": "bogus"}},
            },
            "hooks": {"PreToolUse": []},
        }
        path = settings(real)

        # show: every switch, its mode, read from the file; an unknown stored value reads as on
        code, out, _ = run(path, "show")
        assert code == 0 and out.startswith(f"raizen-norms@some-market in {path}")
        assert modes(out) == {key: "on" for key in switches.RULES}
        assert "on|advice|off" in out and "on|off " in out
        assert "Guard: git:" in out

        # set: the switches named, under the plugin's own id, and nothing else
        code, out, _ = run(path, "set", "guard_git=advice", "norm_git=OFF", "remind_docs=off")
        assert code == 0, out
        data = json.loads(path.read_text(encoding="utf-8"))
        mine = data["pluginConfigs"]["raizen-norms@some-market"]["options"]
        assert mine == {"output_dir": "D:\\Out", "norm_scope": "bogus", "guard_git": "advice", "norm_git": "off", "remind_docs": "off"}
        assert data["pluginConfigs"]["other@x"] == {"options": {"guard_git": "off"}}
        assert list(data) == ["model", "enabledPlugins", "pluginConfigs", "hooks"]
        assert path.read_bytes().decode("utf-8").startswith('{\n  "model"') and path.read_bytes().endswith(b"}\n")
        assert modes(out) == {**{key: "on" for key in switches.RULES}, "guard_git": "advice", "norm_git": "off", "remind_docs": "off"}

        # refused, and the file left byte for byte: an unknown switch, a mode it does not take, no pair
        before = path.read_bytes()
        for bad in (["set", "guard_gti=off"], ["set", "remind_docs=advice"], ["set", "norm_git=maybe"],
                    ["set", "norm_git"], ["set"], ["show-all"], ["set", "guard_git=off", "nope=off"]):
            code, _, err = run(path, *bad)
            assert code == 2 and err.startswith("REFUSED:"), (bad, err)
            assert path.read_bytes() == before, bad

        # the plugin's id is read from the file: an enabled copy wins over a disabled one, and
        # a file with no pluginConfigs yet gets one
        path = settings({"enabledPlugins": {"raizen-norms@old": False, "raizen-norms@new": True}}, "two.json")
        assert run(path, "set", "guard_output=off")[0] == 0
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["pluginConfigs"] == {"raizen-norms@new": {"options": {"guard_output": "off"}}}

        # the indent and the line endings the file had are kept
        path = settings({"enabledPlugins": {"raizen-norms@m": True}}, "crlf.json", indent=4, newline="\r\n")
        assert run(path, "set", "norm_output=advice")[0] == 0
        raw = path.read_bytes().decode("utf-8")
        assert raw.startswith('{\r\n    "enabledPlugins"') and "\n" not in raw.replace("\r\n", "")

        # refused: the plugin not enabled, a file that is not JSON, a file that is not there
        for name, content in (("none.json", {"enabledPlugins": {"raizen-norms-x@m": True}}), ("bad.json", None)):
            path = tmp / name
            path.write_text(json.dumps(content) if content else "{ not json", encoding="utf-8")
            before = path.read_bytes()
            code, _, err = run(path, "set", "guard_git=off")
            assert code == 2 and err.startswith("REFUSED:") and path.read_bytes() == before, err
        assert run(tmp / "missing.json", "show")[0] == 2 and not (tmp / "missing.json").exists()

    print("ok")


if __name__ == "__main__":
    demo()
