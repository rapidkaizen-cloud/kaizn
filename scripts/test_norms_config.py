#!/usr/bin/env python3
"""Self-check norms_config.py, and that the install dialog asks for no switch.

Every case passes a data folder of its own in a temporary folder with `--data`: the
plugin's real data folder is never read or written here.
Run directly: python3 test_norms_config.py
"""
import json
import os
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


def run(*args: str) -> tuple:
    result = subprocess.run([PYTHON, str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8")
    assert result.returncode in (0, 2), result.stderr
    return result.returncode, result.stdout, result.stderr


def demo() -> None:
    # install asks for the output folder alone: a rule is decided when it gets in the way
    assert list(json.loads(MANIFEST.read_text(encoding="utf-8"))["userConfig"]) == ["output_dir"]
    every = {key: "on" for key in switches.RULES}
    for key, (allowed, what) in switches.RULES.items():
        assert allowed in (switches.THREE, switches.TWO) and what.endswith("."), key

    with tempfile.TemporaryDirectory() as tmp:
        data = Path(tmp) / "plugins" / "data" / "kaizn-kaizn"
        file = data / "switches.json"

        # show, before any file or folder exists: every rule on, and nothing is created
        code, out, _ = run("--data", str(data), "show")
        assert code == 0 and out.startswith(f"switches in {file}") and modes(out) == every
        assert "on|advice|off" in out and "on|off " in out and "holds git push and gh pr merge" in out
        assert not data.exists()

        # set: the folder is created, and the file holds every rule's mode, in the list's order
        code, out, _ = run("--data", str(data), "set", "guard_git=advice", "norm_git=OFF", "remind_docs=off")
        assert code == 0, out
        want = {**every, "guard_git": "advice", "norm_git": "off", "remind_docs": "off"}
        assert json.loads(file.read_text(encoding="utf-8")) == want and list(json.loads(file.read_text())) == list(switches.RULES)
        assert modes(out) == want and not (data / "switches.json.tmp").exists()

        # what hooks read is what was written; a later set keeps the earlier ones
        env = {**os.environ, "CLAUDE_PLUGIN_DATA": str(data)}
        read = subprocess.run([PYTHON, "-c", "import switches; print(switches.switched())"], capture_output=True,
                              text=True, env=env, cwd=SCRIPT.parent).stdout
        assert read.strip() == str({"norm_git": "off", "guard_git": "advice", "remind_docs": "off"}), read
        assert run("--data", str(data), "set", "guard_git=on")[0] == 0
        assert json.loads(file.read_text(encoding="utf-8")) == {**want, "guard_git": "on"}

        # refused, and the file left byte for byte: an unknown switch, a mode it does not take, no pair
        before = file.read_bytes()
        for bad in (["set", "guard_gti=off"], ["set", "remind_docs=advice"], ["set", "norm_git=maybe"],
                    ["set", "norm_git"], ["set"], ["show-all"], ["set", "guard_git=off", "nope=off"]):
            code, _, err = run("--data", str(data), *bad)
            assert code == 2 and err.startswith("REFUSED:"), (bad, err)
            assert file.read_bytes() == before, bad

        # refused: no folder, a folder left unsubstituted by the host, a relative one
        for folder in ("", "${CLAUDE_PLUGIN_DATA}", "$CLAUDE_PLUGIN_DATA", "plugin-data"):
            code, _, err = run("--data", folder, "set", "guard_git=off")
            assert code == 2 and "not available on this host" in err, (folder, err)
            assert not Path(folder or "x").exists() and not (SCRIPT.parent / (folder or "x")).exists(), folder
        assert run("show")[0] == 2 and run("--data")[0] == 2

        # a file that is not JSON, or holds values nobody offered, reads as on and is rewritten whole
        file.write_text("{ not json", encoding="utf-8")
        assert modes(run("--data", str(data), "show")[1]) == every
        file.write_text(json.dumps({"guard_git": "maybe", "norm_scope": "ADVICE", "gone": "off"}), encoding="utf-8")
        assert modes(run("--data", str(data), "show")[1]) == {**every, "norm_scope": "advice"}
        assert run("--data", str(data), "set", "guard_output=off")[0] == 0
        assert json.loads(file.read_text(encoding="utf-8")) == {**every, "norm_scope": "advice", "guard_output": "off"}

    print("ok")


if __name__ == "__main__":
    demo()
