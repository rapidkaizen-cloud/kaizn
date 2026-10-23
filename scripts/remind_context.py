#!/usr/bin/env python3
"""After a commit, tell the session once that its context passed a milestone.

Called by `remind_docs.py`, in its process: a hook of its own would start one more
interpreter after every shell call. Claude Code only - its transcript carries each call's
token usage, and Antigravity's hook after a tool cannot hand the model text.

Every call re-reads the whole context, so a step costs what the context holds when it
runs. A session cannot read that size: told to advise a new session after every commit, it
did so in a session that had barely started. So this measures instead - the input side of
a call's usage is the context that call read - and speaks at the first commit after a
milestone is passed, once per milestone, silent in between.
"""
import json
import re

import switches

# A fresh session starts near 80k, so at the first a call costs about two and a half
# times a fresh one's. The steps after it are the user's choice.
MILESTONES = (200_000, 500_000, 800_000)

# Opens the note, the milestone after it: what marks one as said.
MARK = "CONTEXT CHECK - past "
SAID = re.compile(re.escape(MARK) + r"(\d+)k")


def read(transcript: str) -> tuple:
    """The context the session's first call read, the context its last call read, and the
    highest milestone a note already named."""
    first = last = said = 0
    try:
        with open(transcript, encoding="utf-8", errors="replace") as f:
            for line in f:
                if '"usage"' not in line and MARK not in line:
                    continue
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                # A subagent's calls read its own context, not the session's.
                if not isinstance(entry, dict) or entry.get("isSidechain"):
                    continue
                # Only where the host recorded this hook's output: the session quoting the
                # note, or a file holding these words, is not the note.
                if entry.get("type") == "attachment":
                    said = max([said, *(int(n) * 1000 for n in SAID.findall(line))])
                    continue
                message = entry.get("message")
                usage = message.get("usage") if isinstance(message, dict) else None
                if entry.get("type") != "assistant" or not isinstance(usage, dict):
                    continue
                size = sum(
                    usage.get(k) or 0
                    for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
                )
                if size:  # an entry the host wrote itself carries zeros
                    first, last = first or size, size
    except (OSError, TypeError):
        return 0, 0, 0
    return first, last, said


def note(transcript: str) -> str:
    """The note for the milestone this session just passed, or an empty string."""
    if switches.mode("remind_context") == switches.OFF:
        return ""
    first, last, said = read(transcript)
    passed = max((m for m in MILESTONES if last >= m), default=0)
    # A milestone below one already named stays silent: after a compaction the context
    # grows through the same numbers again, and the user was told at the higher one.
    if passed <= said:
        return ""
    times = f", about {last / first:.0f} times what its first call read" if last >= 2 * first else ""
    return (
        f"{MARK}{passed // 1000}k: this session's context holds {last // 1000}k tokens{times}, "
        "and every call re-reads all of it. Tell the user in one line at the end of this turn - "
        "that size, and that the next item costs less in a new session. Say it once: this note "
        "returns at the next milestone."
    )
