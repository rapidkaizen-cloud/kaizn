#!/usr/bin/env python3
"""Self-check remind_docs.py: when it stays silent, and what it asks when it does not.

It never blocks, so every case exits 0; what differs is whether stdout carries a question.
Run directly: python3 test_remind_docs.py
"""
import json
import os
import subprocess
import tempfile
from pathlib import Path

HOOK = Path(__file__).parent / "remind_docs.py"
NORMS = Path(__file__).parent / "session_norms.py"

# `python3`, not sys.executable: the interpreter name hooks.json invokes.
PYTHON = "python3"


# The plugin's data folder of every case: its `switches.json` holds the case's switches.
DATA = tempfile.TemporaryDirectory()


def switched(options: dict) -> dict:
    """The environment of a hook the user set these switches for."""
    (Path(DATA.name) / "switches.json").write_text(json.dumps(options), encoding="utf-8")
    return {**os.environ, "CLAUDE_PLUGIN_DATA": DATA.name}


def run(repo: Path, command: str = "git commit -m 'add page' -- src/page.tsx", **options: str) -> str:
    payload = {"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(repo)}
    result = subprocess.run(
        [PYTHON, str(HOOK)], input=json.dumps(payload), capture_output=True, text=True, cwd=repo,
        env=switched(options),
    )
    assert result.returncode == 0, result.stderr
    if not result.stdout:
        return ""
    out = json.loads(result.stdout)["hookSpecificOutput"]
    assert out["hookEventName"] == "PostToolUse"
    return out["additionalContext"]


def before_call(repo: Path, invocation: int, transcript: Path, **options: str) -> str:
    """Antigravity: no hook speaks after a tool, so `session_norms.py` asks before the
    next model call - started, as there, from the folder holding hooks.json."""
    payload = {"invocationNum": invocation, "workspacePaths": [str(repo)], "transcriptPath": str(transcript)}
    result = subprocess.run(
        [PYTHON, str(NORMS)], input=json.dumps(payload), capture_output=True,
        text=True, encoding="utf-8", cwd=NORMS.parent.parent, env=switched(options),
    )
    assert result.returncode == 0, result.stderr
    if not result.stdout:
        return ""
    steps = json.loads(result.stdout)["injectSteps"]
    assert len(steps) == 1 and list(steps[0]) == ["userMessage"]
    return steps[0]["userMessage"]


def git(repo: Path, *args: str, when: str = "") -> None:
    env = {**os.environ, **({"GIT_COMMITTER_DATE": when, "GIT_AUTHOR_DATE": when} if when else {})}
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t.dev", *args],
        check=True, capture_output=True, env=env,
    )


def commit(repo: Path, *paths: str, when: str = "") -> None:
    for rel in paths:
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(path.read_text(encoding="utf-8") + "x\n" if path.exists() else "x\n", encoding="utf-8")
    git(repo, "add", *paths)
    git(repo, "commit", "-q", "-m", "change", when=when)


def demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        def repo(name: str, *seed: str) -> Path:
            path = Path(tmp) / name
            path.mkdir()
            git(path, "init", "-q", "-b", "development")
            commit(path, *seed)
            return path

        docs = repo("docs-form", "docs/PRD.md", "docs/product.md", "README.md")
        legacy = repo("legacy", "PRD.md", "QUEUE.md")
        bare = repo("unsettled", "notes.txt")

        # silent first: what a session does all day must cost nothing
        assert run(docs, "git status --porcelain") == ""
        assert run(docs, "npm run build") == ""
        assert run(docs, 'echo "git commit is next"') == ""

        # a commit that carries a document, or is one, owes no question
        commit(docs, "src/page.tsx", "docs/guide/approve-a-request.md")
        assert run(docs) == ""
        commit(docs, "src/page.tsx", "README.md")
        assert run(docs) == ""
        commit(docs, "docs/changelog.md")
        assert run(docs) == ""
        commit(legacy, "src/page.tsx", "PRD.md")
        assert run(legacy) == ""

        # a repo that keeps no documents has none to keep true
        commit(bare, "src/page.tsx")
        assert run(bare) == ""

        # the question: the commit, and the documents of the form the repo is on
        commit(docs, "src/page.tsx", "src/lib/orders.ts")
        asked = run(docs)
        assert asked.startswith("DOCS CHECK - commit ") and "changed 2 file(s) and no document" in asked
        assert "`docs/changelog.md`" in asked and "`docs/architecture.md`" in asked and "`PRD.md`" not in asked
        assert "`Docs: none - <why>`" in asked and "amend" in asked
        # the user switched it off: silent on the same commit; `on` or a value nobody offered is not off
        assert run(docs, remind_docs="off") == ""
        assert run(docs, remind_docs="on") == asked and run(docs, remind_docs="maybe") == asked
        # the guide page is asked about only where the app keeps guide pages for its users
        assert "`docs/guide/`" not in asked
        for help_row, kept in (("none", False), ("guide pages", True), ("in-app — /help", True)):
            (docs / "docs" / "product.md").write_text(f"## Context\n\n| | |\n|---|---|\n| Help | {help_row} |\n", encoding="utf-8")
            assert ("`docs/guide/`" in run(docs)) is kept, help_row
        (docs / "docs" / "product.md").write_text("x\n", encoding="utf-8")
        # ... however the commit was spelled
        assert run(docs, "git -C . commit -q -F - <<'EOF'\nfeat: page\nEOF") == asked
        assert run(docs, "git add src/page.tsx && git commit -m 'page'") == asked

        commit(legacy, "src/page.tsx")
        asked = run(legacy)
        assert "`PRD.md`" in asked and "`QUEUE.md`" in asked and "docs/" not in asked

        # the amend that adds the document answers it
        (docs / "docs" / "changelog.md").write_text("# Changelog\n", encoding="utf-8")
        git(docs, "add", "docs/changelog.md")
        git(docs, "commit", "-q", "--amend", "--no-edit")
        assert run(docs, "git commit --amend --no-edit") == ""

        # Antigravity: the conversation's transcript says whether its last tool call committed
        norms = {"type": "USER_INPUT", "source": "SYSTEM_SDK", "content": "SESSION NORMS (kaizn)"}
        ran = {"type": "PLANNER_RESPONSE", "tool_calls": [{"name": "run_command", "args": {"CommandLine": 'git add src/page.tsx; git commit -m "page"'}}]}
        looked = {"type": "PLANNER_RESPONSE", "tool_calls": [{"name": "run_command", "args": {"CommandLine": "git status"}}]}
        done = {"type": "GENERIC", "content": "The command exited with code 0."}

        def heard(*steps) -> Path:
            path = Path(tmp) / f"heard{len(list(Path(tmp).glob('heard*')))}.jsonl"
            path.write_text("\n".join(json.dumps(s) for s in (norms, *steps)) + "\nnot json\n", encoding="utf-8")
            return path

        # silent first: a folder with no documents, a commit carrying one
        assert before_call(bare, 1, heard(ran, done)) == ""
        assert before_call(docs, 1, heard(ran, done)) == ""
        # asked before the model call that follows the commit, in the same words
        commit(docs, "src/page.tsx")
        asked = before_call(docs, 1, heard(ran, done))
        assert asked.startswith("DOCS CHECK - commit ") and asked == run(docs)
        assert before_call(docs, 1, heard(ran, done), remind_docs="off") == ""
        # ... once: the step that asked is in the transcript by the next call
        said = {"type": "USER_INPUT", "source": "SYSTEM_SDK", "content": asked}
        assert before_call(docs, 2, heard(ran, done, said)) == ""
        # ... and not once another tool has run since
        assert before_call(docs, 3, heard(ran, done, said, looked, done)) == ""
        assert before_call(docs, 3, heard(ran, done, looked, done)) == ""
        # a commit another conversation just made is not this one's to answer for
        assert before_call(docs, 1, heard(looked, done)) == ""
        # a second commit of its own is another question
        assert before_call(docs, 4, heard(ran, done, said, looked, done, ran, done)).startswith("DOCS CHECK - commit ")
        # the first call of a turn is the norms' own, and no transcript means no memory
        assert before_call(docs, 0, heard(ran, done)) == ""
        assert before_call(docs, 1, Path(tmp) / "missing.jsonl") == ""

        # a command that exits 0 with nothing committed leaves an old HEAD: not asked about
        commit(docs, "src/page.tsx", when="2020-01-01T00:00:00")
        assert run(docs, "git commit -m 'nothing staged'; git status") == ""

        # an unreadable payload is no reason to speak
        result = subprocess.run([PYTHON, str(HOOK)], input="not json", capture_output=True, text=True, cwd=docs)
        assert result.returncode == 0 and result.stdout == ""

    print("ok")


if __name__ == "__main__":
    demo()
