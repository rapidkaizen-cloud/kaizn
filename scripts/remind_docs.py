#!/usr/bin/env python3
"""After a commit that touched no document, ask the session whether one became false.

PostToolUse hook on the shell tools, on Claude Code. On Antigravity a hook that runs
after a tool cannot hand the model text, so `session_norms.py` asks through `unasked`
before the next model call instead. It never blocks. Most commits owe no document, and a
hook cannot tell which do - so it asks, at the one moment the same-commit rule can still
be met by an amend, and takes "none" for an answer.

Silent unless all hold: the project keeps documents (`docs/PRD.md`, or a root `PRD.md`),
the session's own command just ran a `git commit`, HEAD is that commit, and nothing it
changed is a document.

The same commit carries `remind_context`'s note, in any repo, when the session's context
has passed a milestone. Each of the two is silent when the user switched it `off`.
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import guard_git
import host
import remind_context
import switches

# Documents kept at the root, in either form; everything under `docs/` is one too.
DOCUMENTS = ("PRD.md", "QUEUE.md", "DESIGN.md", "README.md")

# PostToolUse fires when the command exits 0, and `git commit ...; git status` exits 0
# with nothing committed. HEAD is taken as this command's commit only while it is fresh.
# ponytail: a clock, not the command's output; read `tool_response` if a stale HEAD is
# ever asked about.
FRESH_SECONDS = 300

# Opens the reminder, the commit's short hash after it: what `unasked` looks for.
MARK = "DOCS CHECK - commit "

DOCS_FORM = (
    "  - Did a sentence in `docs/product.md`, `docs/rules.md`, `docs/glossary.md`, "
    "`docs/architecture.md`, `docs/runbook.md` or `README.md` become false?\n"
    "  - Did it change how the app behaves? Then it owes a `docs/changelog.md` entry, in a "
    "new file where the repo has none.\n"
    "  - Did it finish a `docs/queue.md` line that is still standing?\n"
)
# Asked only where the app keeps guide pages for its users: `product.md`'s Help row, which
# opens with `none` where it keeps none. A Context without the row keeps none.
GUIDE = "  - Did a page become usable to its role with no `docs/guide/` page for its task?\n"
HELP = re.compile(r"^\|\s*Help\s*\|\s*(.*?)\s*\|\s*$", re.M)
LEGACY_FORM = (
    "  - Did a sentence in `PRD.md` become false?\n"
    "  - Did it finish a `QUEUE.md` line that is still standing?\n"
)


def git(*args: str) -> str:
    try:
        out = subprocess.run(["git", *args], capture_output=True, text=True, timeout=10)
    except Exception:
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def questions() -> str:
    """The questions for the form this project is on; empty where it keeps no documents."""
    # The project directory, as `session_norms` reads the form from it.
    if Path("docs", "PRD.md").is_file():
        try:
            row = HELP.search(Path("docs", "product.md").read_text(encoding="utf-8", errors="replace"))
        except OSError:
            row = None
        return DOCS_FORM + (GUIDE if row and not row[1].lower().startswith("none") else "")
    if Path("PRD.md").is_file():
        return LEGACY_FORM
    return ""


def committed(cmd: str) -> bool:
    """True when the shell command ran a `git commit`, a message that mentions one aside."""
    code = guard_git.QUOTED.sub("''", guard_git.HEREDOC.sub(r"\1", cmd))
    return re.search(guard_git.GIT + r"commit\b", code) is not None


def reminder() -> str:
    """The text for HEAD, or an empty string when HEAD owes no question."""
    if switches.mode("remind_docs") == switches.OFF:
        return ""
    asks = questions()
    if not asks:
        return ""  # never settled: no document here to keep true
    stamp = git("log", "-1", "--format=%ct")
    if not stamp.isdigit() or time.time() - int(stamp) > FRESH_SECONDS:
        return ""
    # A merge lists nothing here, and owes nothing its parents did not.
    files = [f for f in git("show", "--name-only", "--format=", "HEAD").splitlines() if f]
    if not files or any(f.startswith("docs/") or f in DOCUMENTS for f in files):
        return ""
    return (
        f"{MARK}{git('rev-parse', '--short', 'HEAD')} changed {len(files)} "
        "file(s) and no document.\n"
        "A commit that makes a document false carries its correction (`docs-format`, Same "
        "commit). Answer for this commit before the next step:\n"
        + asks
        + "Any yes -> write it and amend it into this commit while it is unpushed. All no -> "
        "carry on, and report `Docs: none - <why>` for this commit at the close. Write nothing a "
        "live check of the code can recover."
    )


def unasked(transcript: str) -> str:
    """`reminder`, for a host that can only speak before a model call: empty unless this
    conversation's last tool call ran a `git commit` and nothing has asked about it since.

    The commit must be the conversation's own. A fresh HEAD alone is not: a session opened
    a minute after another one committed was asked about that commit, and spent thirty
    steps on work that was not its own.
    """
    if not questions():
        return ""  # before the transcript is read: this runs ahead of every model call
    ran = asked = False
    # ponytail: the whole transcript, before each model call of a repo that keeps
    # documents; read its tail only if a long conversation ever shows the cost.
    try:
        with open(transcript, encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    step = json.loads(line)
                except ValueError:
                    continue
                if not isinstance(step, dict):
                    continue
                calls = step.get("tool_calls")
                if isinstance(calls, list):
                    asked = False
                    ran = any(
                        isinstance(call, dict)
                        and call.get("name") == "run_command"
                        and isinstance(call.get("args"), dict)
                        and committed(str(call["args"].get("CommandLine") or ""))
                        for call in calls
                    )
                elif MARK in str(step.get("content") or ""):
                    asked = True
    except OSError:
        return ""  # nothing remembers what was asked: silence, not a question before every call
    return reminder() if ran and not asked else ""


def main() -> None:
    payload = host.read_payload()
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict) or not committed(str(tool_input.get("command") or "")):
        sys.exit(0)
    # The context note rides here: a commit is where an item ends, and this process is
    # already running.
    size = remind_context.note(str(payload.get("transcript_path") or ""))
    text = "\n\n".join(part for part in (reminder(), size) if part)
    if text:
        # Plain stdout from this event goes to a debug log; only this shape reaches the model.
        json.dump({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": text}}, sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
