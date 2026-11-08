#!/usr/bin/env python3
"""Tell the session once that its context passed a milestone, and hold the user's first
message after a long idle on a large context.

Claude Code only - its transcript carries each call's token usage, and Antigravity's hooks
can neither hand the model text after a tool nor hold a message. Two ways in:
  - `UserPromptSubmit`, this file's `main`: every message the user sends.
  - `remind_docs.py`, in its process after a `git commit`: a hook of its own would start
    one more interpreter after every shell call.

Every call re-reads the whole context, so a step costs what the context holds when it
runs. A session cannot read that size: told to advise a new session after every commit, it
did so in a session that had barely started. So this measures instead - the input side of
a call's usage is the context that call read - and speaks at the first message or commit
after a milestone is passed, once per milestone, silent in between. The note makes that
point a seam, because a session told only the size carried on at it.
"""
import json
import re
import sys
import time
from datetime import datetime

import host
import switches

# A fresh session starts near 80k, so at the first a call costs about two and a half
# times a fresh one's. The steps after it are the user's choice.
MILESTONES = (200_000, 500_000, 800_000)

# Opens the note, the milestone after it: what marks one as said.
MARK = "CONTEXT CHECK - past "
SAID = re.compile(re.escape(MARK) + r"(\d+)k")

# The cache a subscription session writes lives an hour: the first call after it writes the
# whole context again. Below the floor that rewrite costs little more than a new session's.
EXPIRED_SECONDS = 3600
HOLD_FROM = 100_000

# Opens a held message's reason: what marks the message sent again as already told.
HOLD = "CONTEXT HOLD - "


def read(transcript: str) -> tuple:
    """The context the session's first call read, the context its last call read, the
    highest milestone a note already named, when that last call ran, and whether a message
    was held since it."""
    first = last = said = 0
    at, held = "", False
    try:
        with open(transcript, encoding="utf-8", errors="replace") as f:
            for line in f:
                if '"usage"' not in line and MARK not in line and HOLD not in line:
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
                # The host records a held message as a notice of its own, the reason in it.
                if entry.get("type") == "system":
                    held = held or HOLD in str(entry.get("content") or "")
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
                    at, held = str(entry.get("timestamp") or ""), False
    except (OSError, TypeError):
        return 0, 0, 0, "", False
    return first, last, said, at, held


def idle(at: str) -> float:
    """Seconds since the host's timestamp `at`; 0 when it cannot be read."""
    try:
        return time.time() - datetime.fromisoformat(at.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return 0


def against(first: int, last: int, what: str) -> str:
    """`last` as a multiple of a new session's first call, where it is one worth saying."""
    return f", about {last / first:.0f} times what {what}" if last >= 2 * first else ""


def milestone(first: int, last: int, said: int) -> str:
    """The note for the milestone `last` just passed, or an empty string."""
    passed = max((m for m in MILESTONES if last >= m), default=0)
    # A milestone below one already named stays silent: after a compaction the context
    # grows through the same numbers again, and the user was told at the higher one.
    if passed <= said:
        return ""
    price = (
        f"each call here costs about {last / first:.0f} times a new session's"
        if last >= 2 * first
        else f"each call here re-reads all {last // 1000}k"
    )
    return (
        f"{MARK}{passed // 1000}k: this session's context holds {last // 1000}k tokens"
        f"{against(first, last, 'its first call read')}, and every call re-reads all of it. "
        "Make this a seam: write where the work stands where a new session will read it - "
        "`.design-audit/resume.md` in a `design-settle` run, else a `docs/queue.md` line where the "
        "repo keeps that file, else your closing line - then end the turn at the next point the "
        f"work can be left, never mid-edit. Tell the user in one line: that size, that {price}, "
        "and that a reply here continues at that price. Say it once: this note returns at the "
        "next milestone."
    )


def note(transcript: str) -> str:
    """The note for the milestone this session just passed, or an empty string."""
    if switches.mode("remind_context") == switches.OFF:
        return ""
    first, last, said, _, _ = read(transcript)
    return milestone(first, last, said)


def hold(first: int, last: int, at: str, held: bool) -> str:
    """The reason the user's message is not sent, or an empty string. The user reads it, not
    the model, so it names what sending costs and how to send anyway."""
    gone = idle(at) if at else 0
    if held or last < HOLD_FROM or gone <= EXPIRED_SECONDS:
        return ""
    return (
        f"{HOLD}not sent: this session sat idle {gone / 3600:.1f} hours, past its one-hour cache, "
        f"so this message would write all {last // 1000}k tokens of its context again"
        f"{against(first, last, 'a new session starts with')}. A status question or a new item "
        "costs less in a new session. Send it again to continue here."
    )


def main() -> None:
    payload = host.read_payload()
    if switches.mode("remind_context") == switches.OFF:
        sys.exit(0)
    first, last, said, at, held = read(str(payload.get("transcript_path") or ""))
    reason = hold(first, last, at, held)
    if reason:
        # The host shows the reason and records it in the transcript, which is how the same
        # message sent again passes.
        json.dump({"decision": "block", "reason": reason}, sys.stdout)
    elif text := milestone(first, last, said):
        json.dump({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": text}}, sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
