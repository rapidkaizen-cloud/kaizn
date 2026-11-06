#!/usr/bin/env python3
"""Self-check remind_context.py both ways in: through the hook that carries it after a commit,
remind_docs.py, and as the hook on every message the user sends - when the context note stays
silent, what it says at a milestone, and when a message is held.

Every case exits 0; what differs is whether stdout carries the note, or the hold.
Run directly: python3 test_remind_context.py
"""
import json
import os
import subprocess
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

HOOK = Path(__file__).parent / "remind_docs.py"
PROMPT_HOOK = Path(__file__).parent / "remind_context.py"

# `python3`, not sys.executable: the interpreter name hooks.json invokes.
PYTHON = "python3"

COMMIT = "git commit -m 'add page' -- src/page.tsx"


# The plugin's data folder of every case: its `switches.json` holds the case's switches.
DATA = tempfile.TemporaryDirectory()


def switched(options: dict) -> dict:
    """The environment of a hook the user set these switches for."""
    (Path(DATA.name) / "switches.json").write_text(json.dumps(options), encoding="utf-8")
    return {**os.environ, "CLAUDE_PLUGIN_DATA": DATA.name}


def run(repo: Path, transcript: str = "", command: str = COMMIT, **options: str) -> str:
    payload = {"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(repo)}
    if transcript:
        payload["transcript_path"] = transcript
    result = subprocess.run(
        [PYTHON, str(HOOK)], input=json.dumps(payload), capture_output=True, text=True, cwd=repo,
        env=switched(options),
    )
    assert result.returncode == 0, result.stderr
    if not result.stdout:
        return ""
    return json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]


def sent(repo: Path, transcript: str = "", **options: str) -> tuple:
    """The prompt hook's answer to a message: ("hold", reason), ("note", text) or ("", "")."""
    payload = {"hook_event_name": "UserPromptSubmit", "prompt": "is it done?", "cwd": str(repo)}
    if transcript:
        payload["transcript_path"] = transcript
    result = subprocess.run(
        [PYTHON, str(PROMPT_HOOK)], input=json.dumps(payload), capture_output=True, text=True, cwd=repo,
        env=switched(options),
    )
    assert result.returncode == 0, result.stderr
    if not result.stdout:
        return "", ""
    out = json.loads(result.stdout)
    if out.get("decision") == "block":
        return "hold", out["reason"]
    assert out["hookSpecificOutput"]["hookEventName"] == "UserPromptSubmit"
    return "note", out["hookSpecificOutput"]["additionalContext"]


def ago(minutes: float) -> str:
    """A timestamp as the host writes one, `minutes` before now."""
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def called(fresh: int, cached: int = 0, written: int = 0, minutes: float = 1, **flags) -> dict:
    """An assistant entry as Claude Code writes it: the call's usage beside its content."""
    usage = {"input_tokens": fresh, "cache_read_input_tokens": cached, "cache_creation_input_tokens": written, "output_tokens": 900}
    return {"type": "assistant", "timestamp": ago(minutes), "message": {"role": "assistant", "content": [], "usage": usage}, **flags}


def held(reason: str) -> dict:
    """The entry the host writes when this hook holds a message."""
    content = f"UserPromptSubmit operation blocked by hook:\n{reason}\n\nOriginal prompt: is it done?"
    return {"type": "system", "subtype": "informational", "content": content, "level": "warning", "isSidechain": False}


def told(text: str) -> dict:
    """The entry the host writes when a hook hands the model text."""
    return {"type": "attachment", "attachment": {"type": "hook_additional_context", "content": [text], "hookEvent": "PostToolUse"}}


def demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "app"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "development", str(repo)], check=True)

        def transcript(*entries) -> str:
            path = Path(tmp) / f"t{len(list(Path(tmp).glob('t*.jsonl')))}.jsonl"
            path.write_text("\n".join(json.dumps(e) for e in entries) + "\nnot json\n", encoding="utf-8")
            return str(path)

        start = called(40, cached=60_000, written=14_000)  # 74k, as a session starts

        # silent first: no transcript, a short session, a long one that did not commit
        assert run(repo) == ""
        assert run(repo, str(Path(tmp) / "missing.jsonl")) == ""
        assert run(repo, transcript(start, called(40, cached=199_000))) == ""
        assert run(repo, transcript(start, called(40, cached=221_000)), "git status") == ""

        # the first commit past a milestone: the size, and what it is against the start
        long = [start, called(900, cached=215_000, written=5_085)]
        said = run(repo, transcript(*long))
        assert said.startswith("CONTEXT CHECK - past 200k: this session's context holds 220k tokens")
        assert "about 3 times what its first call read" in said and "Make this a seam" in said
        assert ".design-audit/resume.md" in said and "costs about 3 times a new session's" in said
        # the user switched it off: silent at the same milestone; the document reminder's switch is another
        assert run(repo, transcript(*long), remind_context="off") == ""
        assert run(repo, transcript(*long), remind_docs="off") == said

        # ... once: the host recorded the note, and the next commit says nothing
        assert run(repo, transcript(*long, told(said), called(40, cached=260_000))) == ""
        # ... and again at the next milestone, whatever was skipped on the way
        further = run(repo, transcript(*long, told(said), called(40, cached=510_000)))
        assert further.startswith("CONTEXT CHECK - past 500k") and "510k" in further
        assert run(repo, transcript(start, called(40, cached=550_000))).startswith("CONTEXT CHECK - past 500k")
        assert run(repo, transcript(start, called(40, cached=900_000))).startswith("CONTEXT CHECK - past 800k")

        # a compaction shrinks the context, and it grows through a named milestone unsaid
        assert run(repo, transcript(*long, told(further), called(40, cached=90_000), called(40, cached=250_000))) == ""

        # the note quoted by the session, or written into a file, is not the note
        quoted = {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": said}]}}
        assert run(repo, transcript(*long, quoted)).startswith("CONTEXT CHECK - past 200k")

        # a subagent's calls and an entry the host wrote itself say nothing of the session
        assert run(repo, transcript(start, called(40, cached=400_000, isSidechain=True))) == ""
        assert run(repo, transcript(*long, called(0))).startswith("CONTEXT CHECK - past 200k")

        # a session that starts large is given the size without a ratio
        large = run(repo, transcript(called(40, cached=150_000), called(40, cached=210_000)))
        assert "times" not in large and "each call here re-reads all 210k" in large

        # every message the user sends: what must pass first - no transcript, a short session,
        # the switch off - then the same note, once
        assert sent(repo) == ("", "")
        assert sent(repo, transcript(start, called(40, cached=199_000))) == ("", "")
        assert sent(repo, transcript(*long), remind_context="off") == ("", "")
        assert sent(repo, transcript(*long)) == ("note", said)
        assert sent(repo, transcript(*long, told(said), called(40, cached=260_000))) == ("", "")

        # a pause: what must pass - under an hour, a small context, the message sent again after
        # a hold, an unreadable time, the switch off
        assert sent(repo, transcript(start, called(40, cached=300_000, minutes=50), told(said))) == ("", "")
        assert sent(repo, transcript(start, called(40, cached=90_000, minutes=120))) == ("", "")
        cold = [start, called(40, cached=300_000, minutes=120), told(said)]
        kind, reason = sent(repo, transcript(*cold))
        assert kind == "hold" and reason.startswith("CONTEXT HOLD - not sent: this session sat idle 2.0 hours")
        assert "write all 300k tokens" in reason and "about 4 times what a new session starts with" in reason
        assert sent(repo, transcript(*cold, held(reason))) == ("", "")
        assert sent(repo, transcript(start, {**called(40, cached=300_000), "timestamp": "yesterday"}, told(said))) == ("", "")
        assert sent(repo, transcript(*cold), remind_context="off") == ("", "")
        # ... held again after the next pause, and a subagent's later call warms nothing of the session's
        assert sent(repo, transcript(*cold, held(reason), called(40, cached=320_000, minutes=90)))[0] == "hold"
        assert sent(repo, transcript(*cold, called(40, cached=50_000, minutes=1, isSidechain=True)))[0] == "hold"
        # ... the note waits for the message sent again
        assert sent(repo, transcript(start, called(40, cached=300_000, minutes=120)))[0] == "hold"
        late = sent(repo, transcript(start, called(40, cached=300_000, minutes=120), held(reason)))
        assert late[0] == "note" and late[1].startswith("CONTEXT CHECK - past 200k")
        # ... and a commit never holds: the call is already running
        assert run(repo, transcript(*cold)) == ""

        # beside the document reminder, in a repo that keeps documents
        for rel in ("docs/PRD.md", "src/page.tsx"):
            (repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (repo / rel).write_text("x\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", rel], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t.dev", "commit", "-q", "-m", rel],
                check=True,
            )
        both = run(repo, transcript(*long))
        assert both.startswith("DOCS CHECK - commit ") and "\n\nCONTEXT CHECK - past 200k" in both
        assert run(repo, transcript(*long), remind_context="off").startswith("DOCS CHECK - commit ")
        assert run(repo, transcript(*long), remind_docs="off").startswith("CONTEXT CHECK - past 200k")

    print("ok")


if __name__ == "__main__":
    demo()
