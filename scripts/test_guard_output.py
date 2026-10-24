#!/usr/bin/env python3
"""Self-check guard_output.py: what must pass first, then what must be refused.

Paths are composed from `R` rather than written whole, so that a guard on the machine
writing this file does not read the cases as output. Run directly: python3 test_guard_output.py
"""
import json
import os
import subprocess
import tempfile
from pathlib import Path

GUARD = Path(__file__).parent / "guard_output.py"

# `python3`, not sys.executable: this is the interpreter name hooks.json invokes, so a
# machine where only `python` resolves must fail here rather than pass a test whose
# subject never runs. The failure is the point.
PYTHON = "python3"

R = "C:\\Users\\me\\" + "Downloads\\Claude"
RP = "/c/Users/me/" + "Downloads/Claude"


def run(tool_name: str, tool_input: dict, cwd: Path, out_dir: Path) -> int:
    return send({"tool_name": tool_name, "tool_input": tool_input, "cwd": str(cwd)}, out_dir)


def send(payload: dict, out_dir: Path) -> int:
    env = {**os.environ, "CLAUDE_PLUGIN_OPTION_OUTPUT_DIR": str(out_dir)}
    result = subprocess.run([PYTHON, str(GUARD)], input=json.dumps(payload), capture_output=True, text=True, env=env)
    assert result.returncode in (0, 2), result.stderr
    return result.returncode


def git(*args: str) -> None:
    subprocess.run(["git", *args], check=True, capture_output=True)


def demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        out = tmp / "Downloads" / "Claude"
        (out / "some-app").mkdir(parents=True)
        plain = tmp / "plain"
        plain.mkdir()
        repo = tmp / "my-repo"
        git("init", "-q", str(repo))
        # A main checkout and a linked worktree, laid out as worktrees/<repo>/<name>.
        main = tmp / "wt-repo"
        git("init", "-q", str(main))
        git("-C", str(main), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "x")
        wt = tmp / "worktrees" / "wt-repo" / "fitur"
        git("-C", str(main), "worktree", "add", "-q", str(wt))
        (out / "wt-repo").mkdir()
        (out / "wt-repo" / "Laporan Lama.xlsx").write_text("")

        def check(tool: str, tool_input: dict, cwd: Path, expected: int, out_dir: Path = out) -> None:
            got = run(tool, tool_input, cwd, out_dir)
            assert got == expected, f"{tool} @ {cwd.name}: {tool_input} -> {got}"

        # --- must pass ---
        check("Write", {"file_path": f"{R}\\some-app\\laporan.xlsx", "content": "x"}, plain, 0)
        check("Write", {"file_path": f"{R}\\_general\\catatan.md", "content": "x"}, plain, 0)
        check("Write", {"file_path": f"{R}\\my-repo\\laporan.xlsx", "content": "x"}, repo, 0)
        # a placeholder names no folder
        check("Write", {"file_path": "D:\\x\\CLAUDE.md", "content": f"written to `{R}\\<repo>\\`."}, plain, 0)
        # listing the root, a glob, a variable
        check("Bash", {"command": f"ls {RP.replace('/c/Users/me', '~')}/*"}, plain, 0)
        check("PowerShell", {"command": f'Get-ChildItem "{R}"'}, plain, 0)
        check("PowerShell", {"command": f'Get-ChildItem "{R}\\some-app"'}, plain, 0)
        check("PowerShell", {"command": 'Copy-Item a.xlsx "$HOME\\' + 'Downloads\\Claude\\$repo\\a.xlsx"'}, plain, 0)
        # a repo path that merely looks alike
        check("Bash", {"command": 'cd "D:/Codes/some-app" && git status'}, plain, 0)
        # a worktree writes to its own folder, reads what its repo's folder already holds
        check("Write", {"file_path": f"{R}\\wt-repo-fitur\\laporan.xlsx", "content": "x"}, wt, 0)
        check("PowerShell", {"command": f'Get-Content "{R}\\wt-repo\\Laporan Lama.xlsx"'}, wt, 0)
        check("PowerShell", {"command": f'Get-ChildItem "{R}\\wt-repo"'}, wt, 0)
        check("Write", {"file_path": f"{R}\\_general\\catatan.md", "content": "x"}, wt, 0)
        # the main checkout writes to the repo's folder
        check("Write", {"file_path": f"{R}\\wt-repo\\laporan.xlsx", "content": "x"}, main, 0)

        # --- must be refused ---
        check("Write", {"file_path": f"{R}\\laporan.xlsx", "content": "x"}, plain, 2)
        check("Write", {"file_path": f"{R}\\mockup-x\\index.html", "content": "x"}, plain, 2)
        check("Write", {"file_path": f"{R}\\my-repo\\laporan.xlsx", "content": "x"}, plain, 2)
        # a path inside a script's text, and inside a shell command
        check("Write", {"file_path": "D:\\x\\make.py", "content": f'OUT = r"{R}\\out.xlsx"'.replace("\\", "\\\\")}, plain, 2)
        check("Bash", {"command": f"python make.py --out {RP}/laporan.pdf"}, plain, 2)
        check("mcp__chrome-devtools__take_screenshot", {"filePath": f"{RP.replace('/c/', 'C:/')}/shot.png"}, plain, 2)
        # a worktree never writes into its repo's folder, nor makes a folder of its own name there
        check("Write", {"file_path": f"{R}\\wt-repo\\laporan.xlsx", "content": "x"}, wt, 2)
        check("Write", {"file_path": f"{R}\\wt-repo\\fitur\\laporan.xlsx", "content": "x"}, wt, 2)
        # only the worktree's session may make its folder
        check("Write", {"file_path": f"{R}\\wt-repo-fitur\\laporan.xlsx", "content": "x"}, main, 2)
        # Antigravity's shell tool, read from its own payload shape
        agy = lambda command: {"toolCall": {"name": "run_command", "args": {"CommandLine": command}}, "workspacePaths": [str(plain)]}
        assert send(agy(f"python make.py --out {RP}/laporan.pdf"), out) == 2
        assert send(agy(f"python make.py --out {RP}/_general/laporan.pdf"), out) == 0

        # --- a custom output folder replaces the default one ---
        custom = tmp / "Hasil" / "Out"
        custom.mkdir(parents=True)
        check("Write", {"file_path": "E:\\Hasil\\Out\\laporan.xlsx", "content": "x"}, plain, 2, custom)
        check("Write", {"file_path": "E:\\Hasil\\Out\\_general\\laporan.xlsx", "content": "x"}, plain, 0, custom)
        check("Write", {"file_path": f"{R}\\laporan.xlsx", "content": "x"}, plain, 0, custom)

        # --- the user's switch: `advice` lets the file through and hands the model the
        # refusal, `off` does nothing, a value it does not know is `on` ---
        def switched(file_path: str, mode: str) -> tuple:
            payload = {"tool_name": "Write", "tool_input": {"file_path": file_path, "content": "x"}, "cwd": str(plain)}
            data = tmp / "plugin-data"
            data.mkdir(exist_ok=True)
            (data / "switches.json").write_text(json.dumps({"guard_output": mode}), encoding="utf-8")
            env = {**os.environ, "CLAUDE_PLUGIN_OPTION_OUTPUT_DIR": str(out), "CLAUDE_PLUGIN_DATA": str(data)}
            result = subprocess.run([PYTHON, str(GUARD)], input=json.dumps(payload), capture_output=True, text=True, env=env)
            told = json.loads(result.stdout)["hookSpecificOutput"] if result.stdout else {}
            return result.returncode, result.stderr, told

        for mode in ("on", "advice", "off"):
            assert switched(f"{R}\\_general\\catatan.md", mode) == (0, "", {}), mode
        assert switched(f"{R}\\laporan.xlsx", "off") == (0, "", {})
        code, err, told = switched(f"{R}\\laporan.xlsx", "advice")
        assert code == 0 and err == "" and told["hookEventName"] == "PreToolUse"
        assert told["additionalContext"].startswith("ADVICE - the user switched guard_output to advice")
        assert "is not this session's output folder" in told["additionalContext"]
        assert "norms-config" not in told["additionalContext"]
        # refused, ending on the one sentence that offers its switch - never on Antigravity
        offer = (
            "This guard is switchable: if it is in the user's way, tell them once that "
            "`/kaizn:norms-config` sets `guard_output` to `advice` or `off`, and never recommend turning it off.\n"
        )
        for mode in ("on", "maybe"):
            code, err, told = switched(f"{R}\\laporan.xlsx", mode)
            assert code == 2 and err.startswith("REFUSED:") and err.endswith(offer) and told == {}, mode
        result = subprocess.run([PYTHON, str(GUARD)], input=json.dumps(agy(f"python make.py --out {RP}/laporan.pdf")),
                                capture_output=True, text=True, env={**os.environ, "CLAUDE_PLUGIN_OPTION_OUTPUT_DIR": str(out)})
        assert result.returncode == 2 and result.stderr.startswith("REFUSED:") and "norms-config" not in result.stderr

    print("ok")


if __name__ == "__main__":
    demo()
