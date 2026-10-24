#!/usr/bin/env python3
"""The user's switch for each rule this plugin prints or enforces: on, advice or off.

Every switch sits in one file for every repo on the machine: `switches.json` in the
plugin's data folder, which Claude Code hands every hook as `CLAUDE_PLUGIN_DATA` and keeps
across plugin updates. `norms_config.py` writes it. Nothing asks for a switch up front: a
user cannot judge a rule before meeting it, so a guard's refusal names its switch instead.
  - a block of the norms : `on` printed, `advice` printed and marked as advice, `off` not printed
  - a guard              : `on` refuses, `advice` lets the call through and warns, `off` does nothing
  - a reminder           : `on` or `off`
No folder, no file, a file that is not a JSON object, a key or a value it does not know: `on`,
so a machine that switched nothing keeps every rule as it was. A guard reads the file on
every call; the norms read it at session start. On Antigravity the skill cannot reach the
folder, so every rule there stays `on`.

`RULES` is the one list: each rule's modes, and what it does in one line.
"""
import json
import os
import sys
from pathlib import Path

import host

ON, ADVICE, OFF = "on", "advice", "off"
THREE = (ON, ADVICE, OFF)
TWO = (ON, OFF)
FILE = "switches.json"

RULES = {
    "norm_language": (THREE, "The LANGUAGE block: chat, documents, commits and on-screen text in your language; code, file names, routes and database names in English."),
    "norm_pointers": (THREE, "The POINTERS block, or NOT SETTLED where app-settle has not run: which rule skill to read before UI, SQL, queries or documents."),
    "norm_scope": (THREE, "The SCOPE block: only what was asked - no refactor, rename or document nobody requested."),
    "norm_git": (THREE, "The GIT block: fetch and check the branch first, commit each finished item with named paths, push or merge only on your yes in chat. Leaves guard_git as it is."),
    "norm_asking": (THREE, "The ASKING block: your decisions are asked, and the session runs commands itself instead of handing them to you."),
    "norm_decisions": (THREE, "The DECISIONS block: an answer with two or more decisions closes with one table - options, and a recommendation with its trade-off."),
    "norm_closing": (THREE, "The CLOSING THE SESSION block, in a settled repo: a report per scope item, then a fixed block - routes, defaults decided, unfinished steps, branch and commits."),
    "norm_output": (THREE, "The OUTPUT block: files made for you go to this session's folder in the output folder, named without a date, never overwritten. Leaves guard_output as it is."),
    "guard_git": (THREE, "Refuses git add -A, a bare force push and a commit on main; holds git push and gh pr merge until your yes in chat."),
    "guard_destructive": (THREE, "Refuses DROP, TRUNCATE, DELETE, a rename or an UPDATE with no narrow WHERE unless it runs inside a guard holding the row count you approved."),
    "guard_output": (THREE, "Refuses a file written to the root of the output folder, or into a folder there that is not the session's own."),
    "remind_docs": (TWO, "After a commit that changed no document, asks the session whether one became false."),
    "remind_context": (TWO, "At the first commit past 200k, 500k or 800k tokens of context, the session tells you the next item costs less in a new session."),
}


def read(value) -> str:
    return str(value or "").strip().lower()


def stored(folder) -> dict:
    """Every rule's mode as `switches.json` in `folder` holds it; anything unreadable is `on`."""
    try:
        found = json.loads((Path(folder) / FILE).read_bytes().decode("utf-8-sig"))
    except (OSError, ValueError, TypeError):
        found = {}
    found = found if isinstance(found, dict) else {}
    return {key: value if (value := read(found.get(key))) in modes else ON for key, (modes, _) in RULES.items()}


def mode(key: str) -> str:
    """The mode the user set for `key`, read from the file each time it is asked."""
    folder = os.environ.get("CLAUDE_PLUGIN_DATA", "").strip()
    return stored(folder)[key] if folder else ON


def switched() -> dict:
    """Every rule the user moved away from `on`, with its mode."""
    return {key: value for key in RULES if (value := mode(key)) != ON}


def refuse(key: str, message: str, payload: dict) -> None:
    """End a guard's call as its switch says: refused under `on`; under `advice` let through,
    with what the refusal would have said handed to the model."""
    if mode(key) == ADVICE:
        # Exit 0 with `additionalContext` and no decision: the call goes on through the normal
        # permission flow, and the text reaches the model beside the tool's result.
        text = (
            f"ADVICE - the user switched {key} to advice, so this call was let through. "
            "Tell the user in one line what it would have stopped. It would have said:\n" + message.rstrip("\n")
        )
        json.dump({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": text}}, sys.stdout)
        sys.exit(0)
    message = message.rstrip("\n")
    if payload.get("host") != host.ANTIGRAVITY:
        # The user meets a rule here, so here is where its switch is offered - never up front.
        message += (
            f"\nThis guard is switchable: if it is in the user's way, tell them once that "
            f"`/raizen-norms:norms-config` sets `{key}` to `advice` or `off`, and never recommend turning it off."
        )
    sys.stderr.write(message + "\n")
    sys.exit(2)
