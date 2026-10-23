#!/usr/bin/env python3
"""The user's switch for each rule this plugin prints or enforces: on, advice or off.

Each block of the session norms, each guard and each reminder is an option of the plugin's
settings - `userConfig` in `.claude-plugin/plugin.json`, a row in `/config` - and Claude
Code hands every hook its value as `CLAUDE_PLUGIN_OPTION_<KEY>`:
  - a block of the norms : `on` printed, `advice` printed and marked as advice, `off` not printed
  - a guard              : `on` refuses, `advice` lets the call through and warns, `off` does nothing
  - a reminder           : `on` or `off`
A value missing, empty or unknown is `on`, so a switch nobody set keeps the rule as it was.
Antigravity has no plugin settings: every rule there is `on`.

`RULES` is the one list. The manifest repeats it because JSON cannot import, and
`test_norms_config.py` fails when the two part.
"""
import json
import os
import sys

ON, ADVICE, OFF = "on", "advice", "off"
THREE = (ON, ADVICE, OFF)
TWO = (ON, OFF)

RULES = {
    "norm_language": THREE,
    "norm_pointers": THREE,  # `POINTERS`, and `NOT SETTLED` where it stands in its place
    "norm_scope": THREE,
    "norm_git": THREE,
    "norm_asking": THREE,
    "norm_decisions": THREE,
    "norm_closing": THREE,
    "norm_output": THREE,
    "guard_git": THREE,
    "guard_destructive": THREE,
    "guard_output": THREE,
    "remind_docs": TWO,
    "remind_context": TWO,
}


def read(value) -> str:
    return str(value or "").strip().lower()


def mode(key: str) -> str:
    """The mode the user set for `key`, read from the hook's environment."""
    value = read(os.environ.get("CLAUDE_PLUGIN_OPTION_" + key.upper()))
    return value if value in RULES[key] else ON


def switched() -> dict:
    """Every rule the user moved away from `on`, with its mode."""
    return {key: value for key in RULES if (value := mode(key)) != ON}


def refuse(key: str, message: str) -> None:
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
    sys.stderr.write(message.rstrip("\n") + "\n")
    sys.exit(2)
