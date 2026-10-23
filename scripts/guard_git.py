#!/usr/bin/env python3
"""Guard git operations: block what must never happen, hold publishing for the user's reply.

Reads the hook payload from stdin.
Exit 0 = pass, exit 2 = block (the agent reads stderr). The user's `guard_git` switch
(`switches.py`) can make it warn instead of refusing or holding, or do nothing.

Refused, and fixed by the agent itself:
  - commit while HEAD is on main, in a repo that has a development branch
  - git add -A / git add .  (a commit holds explicit paths from SCOPE)
  - a bare force push: --force / -f, and the flagless force spelled as a refspec
    (push origin +main). --force-with-lease refuses when the remote moved, so it is
    the only force a session runs.

Held until the user replies:
  - git push, --force-with-lease included
  - gh pr merge

A push passes once the transcript shows a turn the session ended on the exact command,
in backticks on a line of its own, something the user typed after it, and no call of
that command since - one stop, one run. What the user typed, and how many messages
later the yes came, is the session's to read: a question answered first and a yes after
it is still one stop. A merge is held to more, because it is what reaches production:
the reply is the one to the session's last message, with nothing typed since. A message
may put several held commands, each on a line of its own: the one reply then covers one
run of each. `gh pr create` is not held: it publishes nothing a push has not, and with no
prompt to answer it stops on a branch that is not pushed. What is enforced here is the
stop, not the yes: a hook cannot read what a reply means, so the session reads it and
runs the command only on a yes. The reply is typed in chat rather than picked on a question
dialog, because a dialog gets clicked before it is read. It is read from the transcript
rather than asked for with a permission prompt, because an SDK host never shows that
prompt: "ask" there is a silent refusal that leaves the user typing the command by hand.
Antigravity gets the same reading for a second reason: its hook `ask` is approved
unasked under `--dangerously-skip-permissions`.
"""
import json
import re
import subprocess
import sys

import host
import switches

# Global options are allowed to sit between `git` and its subcommand: `git -c k=v push`,
# `git -C dir commit`, `git --no-pager add`. Anchoring on `git push` alone reads only the
# bare spelling, and the long way round walks past every rule below. `-c`/`-C` take a
# separate argument, so they need their own alternative.
GIT = r"\bgit\s+(?:-[cC]\s+\S+\s+|--?[\w-]+(?:=\S+)?\s+)*"
# What follows a subcommand up to the end of its own command. A rule that reads further
# takes the `-f` of `git push origin dev && rm -f x` for a force push.
ARGS = r"\b[^;&|\n]*?"

SHELLS = ("Bash", "PowerShell")
# Antigravity wraps what the user typed; the steps a hook injects carry another `source`.
REQUEST = re.compile(r"<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>", re.S)

# A commit message that mentions `gh pr create` is data, not a call. Heredoc bodies and
# quoted strings are blanked before any rule reads the command; the heredoc's opening
# line stays, since commands may follow `<<'EOF'` on it.
# ponytail: `sh -c 'git push'` hides inside quotes too; parse the shell if agents start wrapping git.
HEREDOC = re.compile(r"(<<-?\s*(['\"]?)(\w+)\2[^\n]*\n).*?^\s*\3\s*$", re.S | re.M)
QUOTED = re.compile(r"'[^']*'|\"(?:[^\"\\]|\\.)*\"")


def head_branch() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        return out.stdout.strip()
    except Exception:
        return ""


def has_development() -> bool:
    """True when the repo has a `development` branch, local or on origin. A repo with only
    `main` has nowhere else to commit, and refusing there leaves the session no way out."""
    try:
        out = subprocess.run(
            ["git", "for-each-ref", "--count=1", "refs/heads/development", "refs/remotes/origin/development"],
            capture_output=True, text=True, timeout=5,
        )
        return bool(out.stdout.strip())
    except Exception:
        return True  # unreadable: refuse, as before the branch was looked for


def norm(text: str) -> str:
    return " ".join(text.split())


def entries(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    yield json.loads(line)
                except ValueError:
                    continue
    except OSError:
        return


FENCED = re.compile(r"```[^\n]*\n(.*?)```", re.S)


def names(text: str, want: str) -> bool:
    """True when `text` puts the command to the user: backticked on a line of its own, or
    alone in a fence. A command named inside a sentence was mentioned, not put - a closing
    report says what it pushed, and the next thing the user types is no reply to that."""
    return any(norm(line) == f"`{want}`" for line in text.splitlines()) or any(
        norm(block) == want for block in FENCED.findall(text)
    )


def approved_antigravity(payload: dict, cmd: str, strict: bool) -> bool:
    """`approved`, read from Antigravity's transcript: one step per line, a planner step
    carrying `tool_calls` and the step after it carrying their result."""
    # ponytail: the result is paired to its call by position, which holds while a planner
    # step carries one call.
    want = norm(cmd)
    granted = named = running = False
    for step in entries(payload.get("transcript_path") or ""):
        if not isinstance(step, dict):
            continue
        content = str(step.get("content") or "")
        calls = step.get("tool_calls")
        if isinstance(calls, list):
            running = False
            for call in calls:
                args = call.get("args") if isinstance(call, dict) else None
                if (
                    isinstance(args, dict)
                    and call.get("name") == "run_command"
                    and norm(str(args.get("CommandLine") or "")) == want
                ):
                    running = True
        elif running:
            granted = running = False
        elif step.get("type") == "USER_INPUT" and step.get("source") == "USER_EXPLICIT":
            request = REQUEST.search(content)
            if (request.group(1) if request else content).strip():
                granted, named = named or (granted and not strict), False
        if step.get("type") == "PLANNER_RESPONSE" and content:
            named = names(content, want)
    return granted


def approved(payload: dict, cmd: str, strict: bool = False) -> bool:
    """True when the user replied to a message naming `cmd`, and no run of it has spent that.

    The message is the session's last before the reply: a command named earlier in the
    turn, with other text after it, was never put to the user as a stop. What is typed
    after the reply leaves the grant standing - the yes may follow a question - unless
    `strict`: there the reply is the user's last, and anything typed after it takes the
    grant back. A call of the command counts as spent once its tool_result is in the
    transcript, so the call being checked right now - written, not yet answered - never
    spends it.
    """
    if payload.get("host") == host.ANTIGRAVITY:
        return approved_antigravity(payload, cmd, strict)
    want = norm(cmd)
    granted = named = False
    pending = set()
    for entry in entries(payload.get("transcript_path") or ""):
        if not isinstance(entry, dict):
            continue
        content = (entry.get("message") or {}).get("content")
        blocks = [{"type": "text", "text": content}] if isinstance(content, str) else content
        said, result = [], False
        for block in blocks if isinstance(blocks, list) else []:
            if not isinstance(block, dict):
                continue
            if (
                block.get("type") == "tool_use"
                and block.get("name") in SHELLS
                and norm(str((block.get("input") or {}).get("command") or "")) == want
            ):
                pending.add(block.get("id"))
            elif block.get("type") == "tool_result":
                result = True
                if block.get("tool_use_id") in pending:
                    granted = False
            elif block.get("type") == "text" and str(block.get("text") or "").strip():
                said.append(str(block.get("text")))
        # A tool's result, a subagent's prompt and a host-written note are user entries
        # nobody typed.
        # ponytail: every other user entry is taken as typed by the user; read its origin
        # if a host starts writing prompts of its own there.
        if not said or result or entry.get("isSidechain") or entry.get("isMeta"):
            continue
        if entry.get("type") == "assistant":
            named = any(names(text, want) for text in said)
        elif entry.get("type") == "user":
            if named:
                pending.clear()
            granted, named = named or (granted and not strict), False
    return granted


def block(msg: str) -> None:
    switches.refuse("guard_git", msg)


# A held command the call adds anything to: chained, piped or redirected. A reply covers
# the command the message names, and a session names the bare command and then retries the
# wrapped one - held a second time, after the user's yes.
WRAPPED = re.compile(r"&&|\|\||[;|\n]|\d?>")


def hold(payload: dict, cmd: str, what: str, wrapped: bool = False, strict: bool = False) -> None:
    if approved(payload, cmd, strict):
        sys.exit(0)
    alone = (
        " This call adds other commands to it, and a reply covers the command the message "
        "names and no other: name it and run it alone - no `cd`, no `&&`, no pipe, no "
        "redirection."
    )
    run = "run the command as named" if wrapped else "retry the same command unchanged"
    # What a question in between costs: nothing for a push, the stop for a merge.
    after = (
        f"{run} before anything else is typed. A question, a condition or another instruction "
        "is not a yes: answer it in a message that puts the command again, since this one is "
        "held to the reply itself."
        if strict
        else f"{run}. A question, a condition or another instruction is not a yes: answer it "
        "and wait - the stop stays open, and the yes may come in a later message."
    )
    block(
        f"HELD: {what} runs only on the user's yes in chat.{alone if wrapped else ''} End this "
        f"turn on a message that puts {'that' if wrapped else 'this exact'} command in backticks "
        "on a line of its own, lists under it every commit it publishes as `- ` bullets, short "
        "hash and subject, and asks whether to run it. Another held command the request also "
        "needs goes in that message on a line of its own, and the one reply is read for both. "
        "No question dialog - one gets clicked before it is read. Read the reply yourself: on a "
        f"clear yes, in whatever words, {after} One stop covers one run of each command named. "
        "Never hand the command to the user to type."
        + ("" if wrapped else f"\nCommand: {norm(cmd)}")
    )


def main() -> None:
    payload = host.read_payload()
    if switches.mode("guard_git") == switches.OFF:
        sys.exit(0)
    cmd = (payload.get("tool_input") or {}).get("command") or ""
    code = QUOTED.sub("''", HEREDOC.sub(r"\1", cmd))
    # A command continued over lines is one command to every rule below.
    code = re.sub(r"\\\r?\n", " ", code)
    if not re.search(r"\b(git|gh)\b", code):
        sys.exit(0)

    # Any argument of the add, not only the first: `git add src -A` and `git add -- .` add
    # everything too, and `./` is `.`. `.gitignore` and `./src/a.ts` are paths and pass.
    if re.search(GIT + r"add" + ARGS + r"\s(--all|-[a-zA-Z]*A[a-zA-Z]*|\./?)(?=[\s;&|)]|$)", code):
        block(
            "REFUSED: git add -A / git add . is not used in this repo.\n"
            "A commit contains only paths that are in SCOPE, named explicitly.\n"
            "Files changed outside SCOPE are findings reported to the user, "
            "not things to commit along."
        )

    # `\s\+\S` is `push origin +main` — a force with no flag to grep for.
    if re.search(GIT + r"push" + ARGS + r"(--force(?![-\w])|\s-f\b|\s\+\S)", code):
        block(
            "REFUSED: a bare force push. Use --force-with-lease instead - it refuses when "
            "the remote moved since your last fetch - and ask for it as for any push."
        )

    if re.search(GIT + r"commit\b", code):
        branch = head_branch()
        if branch == "main" and has_development():
            block(
                "REFUSED: HEAD is on main. A session never works on main.\n"
                "Switch to development first, then retry."
            )

    wrapped = WRAPPED.search(code) is not None
    if re.search(r"\bgh\s+pr\s+merge\b", code):
        hold(payload, cmd, "merging a pull request", wrapped, strict=True)

    if re.search(GIT + r"push\b", code):
        hold(payload, cmd, "a push", wrapped)

    sys.exit(0)


if __name__ == "__main__":
    main()
