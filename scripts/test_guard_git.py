#!/usr/bin/env python3
"""Self-check guard_git.py: what is refused, what is held, what a reply lets through.

The outcomes are distinct and a regression turns one into another silently, so each is
asserted on both the exit code and the word that opens stderr.
Run directly: python3 test_guard_git.py
"""
import json
import os
import subprocess
import tempfile
from pathlib import Path

GUARD = Path(__file__).parent / "guard_git.py"

# `python3`, not sys.executable: this is the interpreter name hooks.json invokes, so a
# machine where only `python` resolves must fail here rather than pass a test whose
# subject never runs. The failure is the point.
PYTHON = "python3"


def run(command: str, transcript: str = "") -> tuple:
    payload = {"tool_name": "Bash", "tool_input": {"command": command}}
    if transcript:
        payload["transcript_path"] = transcript
    result = subprocess.run(
        [PYTHON, str(GUARD)], input=json.dumps(payload), capture_output=True, text=True
    )
    word = result.stderr.split(":", 1)[0] if result.stderr else ""
    return result.returncode, word


def showed(text: str) -> dict:
    return {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": text}]}}


def said(content, **flags) -> dict:
    """A user entry: `content` is a string, or the list of blocks a real transcript holds."""
    return {"type": "user", "message": {"role": "user", "content": content}, **flags}


def asked(question: str, answer, use_id: str = "ask") -> dict:
    return {
        "type": "user",
        "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": use_id, "content": "answered"}]},
        "toolUseResult": {"questions": [{"question": question}], "answers": {question: answer}},
    }


def called(use_id: str, command: str, name: str = "Bash") -> dict:
    return {
        "type": "assistant",
        "message": {"role": "assistant", "content": [{"type": "tool_use", "id": use_id, "name": name, "input": {"command": command}}]},
    }


def ran(use_id: str) -> dict:
    return {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": use_id, "content": "done"}]}}


def demo() -> None:
    refused, held, passed = (2, "REFUSED"), (2, "HELD"), (0, "")

    # refused outright, and fixed by the agent without the user
    assert run("git add -A") == refused
    assert run("git add .") == refused
    assert run("git push --force origin dev") == refused
    assert run("git push -f origin dev") == refused

    # a global option between `git` and the subcommand must not shake the guard off
    assert run("git -c core.hooksPath=/dev/null push --force origin dev") == refused
    assert run("git -C . add -A") == refused
    assert run("git --no-pager push origin development") == held

    # force with no flag to grep for: the leading + on the refspec
    assert run("git push origin +main") == refused
    assert run("git push origin +refs/heads/dev:refs/heads/dev") == refused

    # a + inside a branch name is not a force; the lease is a push like any other
    assert run("git push origin feature+search") == held
    assert run("git push --force-with-lease") == held

    # held without a reply
    assert run("git push origin development") == held
    assert run("gh pr merge 12 --squash") == held

    # opening a pull request is not held: it publishes nothing a push has not
    assert run("gh pr create --fill") == passed
    assert run("gh pr create --base main --head development --title 'Orders' --body-file pr.md") == passed
    assert run("gh pr create --help") == passed

    with tempfile.TemporaryDirectory() as tmp:
        def transcript(*lines) -> str:
            path = Path(tmp) / f"t{len(list(Path(tmp).iterdir()))}.jsonl"
            path.write_text("\n".join(json.dumps(x) for x in lines) + "\nnot json\n", encoding="utf-8")
            return str(path)

        push = "git push origin development"
        gate = showed(f"`{push}`\n- 4cc1af0 feat: push waits for a reply\n- e2bd00d docs: README\n\nRun it?")
        yes = transcript(gate, said("ok"))

        # a reply lets exactly that command through, whitespace aside
        assert run(push, yes) == passed
        assert run("git  push  origin development", yes) == passed
        assert run("git push origin main", yes) == held

        # the reply in whatever words - the session reads them, this guard does not
        for reply in ("gas", "run", "ya, push", "lanjut"):
            assert run(push, transcript(gate, said(reply))) == passed, reply

        # the reply as a host writes it: a text block, an IDE's open file beside it
        assert run(push, transcript(gate, said([{"type": "text", "text": "ok"}]))) == passed
        beside = [{"type": "text", "text": "<ide_opened_file>a.ts</ide_opened_file>"}, {"type": "text", "text": "ok\n"}]
        assert run(push, transcript(gate, said(beside))) == passed

        # the command alone in a fence is named as well as the command inline
        assert run(push, transcript(showed(f"```\n{push}\n```\n- 4cc1af0 feat"), said("ok"))) == passed
        assert run(push, transcript(showed(f"```bash\n{push}\n```"), said("ok"))) == passed

        # a tool call after the message does not take the stop back, and one between the
        # reply and the push does not take the reply back
        assert run(push, transcript(gate, called("t0", "git status"), ran("t0"), said("ok"))) == passed
        assert run(push, transcript(gate, said("ok"), called("t0", "git fetch"), ran("t0"))) == passed

        # the call being checked is already written, not yet answered: not spent
        assert run(push, transcript(gate, said("ok"), called("t1", push))) == passed

        # spent by a run; a new reply to a new message grants one more
        spent = [gate, said("ok"), called("t1", push), ran("t1")]
        assert run(push, transcript(*spent)) == held
        assert run(push, transcript(*spent, said("ok"))) == held
        assert run(push, transcript(*spent, gate, said("ok"))) == passed

        # a held attempt before the reply spends nothing; the other shell's run spends it
        assert run(push, transcript(called("t0", push), ran("t0"), gate, said("ok"))) == passed
        assert run(push, transcript(gate, said("ok"), called("t1", push, "PowerShell"), ran("t1"))) == held

        # no reply yet, or one with nothing in it
        assert run(push, transcript(gate)) == held
        assert run(push, transcript(gate, said(""))) == held
        assert run(push, transcript(gate, said(" \n"))) == held

        # a reply to a message that does not name this command
        assert run(push, transcript(said("ok"))) == held
        assert run(push, transcript(showed("Push to development?"), said("ok"))) == held
        assert run(push, transcript(showed("`git push origin dev`"), said("ok"))) == held
        assert run("git push origin dev", transcript(gate, said("ok"))) == held

        # named mid-turn with other words after it: never the stop the user replied to
        assert run(push, transcript(gate, showed("Tests pass. Run them again?"), said("ok"))) == held

        # named inside a sentence: mentioned, not put to the user - a closing report says
        # what it pushed, and the next thing typed is no reply to that
        assert run(push, transcript(showed(f"Published with `{push}`: 4cc1af0 and e2bd00d."), said("ok"))) == held
        assert run(push, transcript(showed(f"- **Publish with `{push}`**: done"), said("next page"))) == held

        # typed after the reply: the stop stays open. A question answered first and the
        # yes after it is one stop, and the session reads which message was the yes
        answered = [gate, said("did you pull main first?"), showed("Yes: 0 behind, 81 ahead."), said("ok")]
        assert run(push, transcript(*answered)) == passed
        assert run(push, transcript(gate, said("wait"), said("now"))) == passed
        assert run(push, transcript(gate, said("ok"), showed("Tagging first."), said("and the changelog"))) == passed
        # ... for one run: the stop is spent as any other, and what is typed after is no new one
        assert run(push, transcript(*answered, called("t1", push), ran("t1"))) == held
        assert run(push, transcript(*answered, called("t1", push), ran("t1"), said("again"))) == held

        # a merge is what reaches production, and is held to the reply itself: a question
        # in between takes the stop back until the answer puts the command again
        merge = "gh pr merge 12 --squash"
        merge_gate = showed(f"`{merge}`\n- 4cc1af0 feat: push waits for a reply\n\nMerge it?")
        assert run(merge, transcript(merge_gate, said("ok"))) == passed
        assert run(merge, transcript(merge_gate, said("is CI green?"), showed("Yes."), said("ok"))) == held
        assert run(merge, transcript(merge_gate, said("wait"), said("now"))) == held
        assert run(merge, transcript(merge_gate, said("is CI green?"), showed(f"Yes.\n\n`{merge}`"), said("ok"))) == passed

        # user entries nobody typed neither grant nor take a grant back: a subagent's
        # prompt, a host-written note, a tool's result with a note beside it
        mixed = said([{"type": "tool_result", "tool_use_id": "x", "content": "done"}, {"type": "text", "text": "note"}])
        for unseen in (said("ok", isSidechain=True), said("ok", isMeta=True), mixed):
            assert run(push, transcript(gate, unseen)) == held
            assert run(push, transcript(gate, said("ok"), unseen)) == passed

        # `Run` picked on a question dialog is no reply
        assert run(push, transcript(asked(f"Run `{push}`?", ["Run"]))) == held
        assert run(push, transcript(gate, asked(f"Run `{push}`?", ["Run"]))) == held
        assert run(push, str(Path(tmp) / "missing.jsonl")) == held

        # the lease goes through the same reply; a bare force never does
        lease = "git push --force-with-lease=master:90aa7fc origin master"
        assert run(lease, transcript(showed(f"Force push:\n`{lease}`"), said("ok"))) == passed
        bare = "git push --force origin master"
        assert run(bare, transcript(showed(f"`{bare}`"), said("ok"))) == refused
        assert run(merge, transcript(showed(f"Merge it:\n\n  `{merge}`\n- 4cc1af0 feat"), said("ok"))) == passed
        # a command of several lines can only be put in a fence
        body = "gh pr merge 12 --squash --body \"$(cat <<'EOF'\nStatus filter.\nEOF\n)\""
        assert run(body, transcript(showed(f"```bash\n{body}\n```\n- 4cc1af0 feat"), said("ok"))) == passed

        # a push and a merge put in one message: one reply covers one run of each, and
        # the run of one spends nothing of the other
        pr = merge
        pair = [showed(f"`{push}`\n- 4cc1af0 feat\n\n`{pr}`\n\nRun both?"), said("ok")]
        pushed = [*pair, called("t1", push), ran("t1")]
        assert run(push, transcript(*pair)) == passed
        assert run(pr, transcript(*pushed)) == passed
        assert run(pr, transcript(*pushed, showed("Pushed."), called("t2", pr))) == passed
        assert run(push, transcript(*pushed)) == held
        assert run(pr, transcript(*pushed, called("t2", pr), ran("t2"))) == held
        # ... a command that message did not put still waits for a stop of its own, and
        # two commands sharing one fence are neither of them put
        assert run("gh pr merge 13 --squash", transcript(*pair)) == held
        assert run(push, transcript(showed(f"```\n{push}\n{pr}\n```"), said("ok"))) == held

    # a message that mentions a held or refused command is data, not a call
    assert run('git commit -m "docs: gh pr create and git push --force are held"') == passed
    assert run("git commit -F - <<'EOF'\nfeat: never git add -A, gh pr merge waits\nEOF\ngit log -1") == passed
    assert run("git commit -m 'why git push is held' && git status") == passed

    # blanking quotes and heredoc bodies must not hide a real call
    assert run('cd "D:/Codes/my app" && git push origin dev') == held
    assert run("cat <<'EOF' > notes.md && git push origin dev\nbody\nEOF") == held
    assert run("git commit -F - <<'EOF'\nmsg\nEOF\ngit push --force origin dev") == refused

    # auto-commit must not be slowed down by the guard.
    # Run this from a branch other than main — the commit assertion reads the real
    # HEAD, and on main the guard is supposed to refuse.
    assert run("git commit -m 'add page' -- src/app/orders/page.tsx") == passed
    assert run("git add src/app/orders/page.tsx") == passed
    assert run("git status --porcelain") == passed
    assert run("git fetch") == passed

    # paths that only open like `.`, and a flag that belongs to the next command, pass
    assert run("git add .gitignore ./src/a.ts .github/workflows/docs.yml") == passed
    assert run("git add -- src/a.ts") == passed
    assert run("git add src/a.ts && ls -A") == passed
    # ... while everything added by another spelling is the same refusal
    for everything in ("git add src -A", "git add -- .", "git add ./", "git add -Av", "git add src --all", "(cd app && git add .)"):
        assert run(everything) == refused, everything

    # a held command the call adds to is told to run alone, and is handed no compound to
    # name; the bare one is handed its own text. A push is told the stop stays open through
    # a question, a merge that the answer puts the command again
    def message(command: str) -> str:
        payload = {"tool_name": "Bash", "tool_input": {"command": command}}
        return subprocess.run([PYTHON, str(GUARD)], input=json.dumps(payload), capture_output=True, text=True).stderr

    for wrapped in (
        'cd "D:/Codes/my app" && git push origin dev 2>&1 | tail -5',
        "git push origin dev 2>&1",
        "git push origin dev; git status",
        "gh pr merge 12 --squash | cat",
    ):
        assert "run it alone" in message(wrapped) and "Command:" not in message(wrapped), wrapped
    for bare in ("git push origin dev", "gh pr merge 12 --squash --subject 'a | b; c > d'"):
        assert "run it alone" not in message(bare) and f"Command: {bare}" in message(bare), bare
    assert "stays open" in message("git push origin dev") and "puts the command again" not in message("git push origin dev")
    assert "puts the command again" in message("gh pr merge 12") and "stays open" not in message("gh pr merge 12")

    # a force flag belongs to the push it follows: one on a later command is not a force
    assert run("git push origin dev && rm -f x") == held
    assert run("git push origin dev 2>&1 | tail -f") == held
    assert run("git push origin dev; echo a +b") == held
    # ... and a force continued onto the next line is still one
    assert run("git push \\\n  --force origin dev") == refused

    # unrelated commands are none of this guard's business
    assert run("npm run dev") == passed
    assert run("gh release list") == passed
    assert run("gh pr view 12") == passed

    print("ok")


def run_antigravity(command: str, transcript: str = "", workspace: str = "") -> tuple:
    """The payload Antigravity 1.2.16 sends before `run_command`, with the hook started
    where Antigravity starts it: the folder holding hooks.json, not the project."""
    payload = {
        "toolCall": {"name": "run_command", "args": {"CommandLine": command, "Cwd": workspace}},
        "workspacePaths": [workspace or str(Path.cwd())],
        "transcriptPath": transcript,
    }
    result = subprocess.run(
        [PYTHON, str(GUARD)], input=json.dumps(payload), capture_output=True, text=True, cwd=GUARD.parent.parent
    )
    word = result.stderr.split(":", 1)[0] if result.stderr else ""
    return result.returncode, word, result.stderr


def planned(name: str, args: dict) -> dict:
    return {"type": "PLANNER_RESPONSE", "tool_calls": [{"name": name, "args": args}]}


def told(text: str) -> dict:
    return {"type": "PLANNER_RESPONSE", "content": text}


def typed(text: str, source: str = "USER_EXPLICIT") -> dict:
    return {"type": "USER_INPUT", "source": source, "content": f"<USER_REQUEST>\n{text}\n</USER_REQUEST>"}


def question(*texts) -> dict:
    return planned("ask_question", {"questions": [{"question": t, "options": ["Run", "Cancel"]} for t in texts]})


def result(content: str = "The command exited with code 0.") -> dict:
    return {"type": "GENERIC", "content": f"Created At: 2026-10-04T20:42:25+07:00\n{content}"}


def antigravity() -> None:
    def outcome(command: str, transcript: str = "", workspace: str = "") -> tuple:
        return run_antigravity(command, transcript, workspace)[:2]

    refused, held, passed = (2, "REFUSED"), (2, "HELD"), (0, "")

    # passes first: what a session does all day must not be slowed down
    assert outcome("git status --porcelain") == passed
    assert outcome("git add src/app/orders/page.tsx") == passed
    assert outcome("git commit -m 'add page' -- src/app/orders/page.tsx") == passed
    assert outcome("npm run dev") == passed

    assert outcome("git add -A") == refused
    assert outcome("git push --force origin dev") == refused

    push = "git push origin development"
    code, word, message = run_antigravity(push)
    assert (code, word) == held
    # the held message asks for a chat reply on either host, and names no question tool
    assert "in chat" in message and "ask_question" not in message and "AskUserQuestion" not in message

    with tempfile.TemporaryDirectory() as tmp:
        def transcript(*steps) -> str:
            path = Path(tmp) / f"t{len(list(Path(tmp).iterdir()))}.jsonl"
            path.write_text("\n".join(json.dumps(x) for x in steps) + "\nnot json\n", encoding="utf-8")
            return str(path)

        gate = told(f"`{push}`\n- 4cc1af0 feat: push waits for a reply\n\nRun it?")
        yes = [gate, typed("ok")]

        assert outcome(push, transcript(*yes)) == passed
        assert outcome("git push origin main", transcript(*yes)) == held
        assert outcome(push, transcript(gate, typed("ya, push"))) == passed
        # the reply with nothing wrapped around it
        bare = {"type": "USER_INPUT", "source": "USER_EXPLICIT", "content": "ok"}
        assert outcome(push, transcript(gate, bare)) == passed

        # the call being checked is already written, not yet answered: not spent
        mine = planned("run_command", {"CommandLine": push})
        assert outcome(push, transcript(*yes, mine)) == passed

        # another command run between the reply and the push does not take the reply back
        fetch = planned("run_command", {"CommandLine": "git fetch"})
        assert outcome(push, transcript(*yes, fetch, result(), mine)) == passed

        # spent by a run; a new reply to a new message grants one more
        assert outcome(push, transcript(*yes, mine, result())) == held
        assert outcome(push, transcript(*yes, mine, result(), typed("ok"))) == held
        assert outcome(push, transcript(*yes, mine, result(), *yes)) == passed

        # a held attempt before the reply spends nothing
        assert outcome(push, transcript(mine, result("HELD: a push"), *yes, mine)) == passed

        # a planner step that names the command and calls a tool still names it
        both = {**planned("run_command", {"CommandLine": "git log --oneline -3"}), "content": gate["content"]}
        assert outcome(push, transcript(both, result(), typed("ok"))) == passed

        # opening a pull request is not held
        assert outcome("gh pr create --fill") == passed

        # a push and a merge put in one message: one reply, one run of each
        pr = "gh pr merge 12 --squash"
        pair = [told(f"`{push}`\n- 4cc1af0 feat\n\n`{pr}`\n\nRun both?"), typed("ok")]
        opened = planned("run_command", {"CommandLine": pr})
        assert outcome(pr, transcript(*pair, mine, result(), opened)) == passed
        assert outcome(push, transcript(*pair, mine, result())) == held
        assert outcome(pr, transcript(*pair, mine, result(), opened, result())) == held

        # no reply, an empty one, a message that does not name the command, other words
        # after the one that did, something typed after the reply
        assert outcome(push, transcript(gate)) == held
        assert outcome(push, transcript(gate, typed(""))) == held
        assert outcome(push, transcript(told("Push to development?"), typed("ok"))) == held
        assert outcome(push, transcript(gate, told("Anything else?"), typed("ok"))) == held
        # named inside a sentence of a closing report: mentioned, not put to the user
        assert outcome(push, transcript(told(f"- **Publish with `{push}`**: done"), typed("next page"))) == held
        # typed after the reply: a push stays open through it - a question answered, then
        # the yes - and a merge does not
        assert outcome(push, transcript(*yes, told("Tagging first."), typed("and the changelog"))) == passed
        assert outcome(push, transcript(gate, typed("did you pull main?"), told("Yes."), typed("ok"))) == passed
        assert outcome(push, transcript(gate, typed("did you pull main?"), told("Yes."), typed("ok"), mine, result())) == held
        merge_gate = told(f"`{pr}`\n- 4cc1af0 feat\n\nMerge it?")
        assert outcome(pr, transcript(merge_gate, typed("ok"))) == passed
        assert outcome(pr, transcript(merge_gate, typed("is CI green?"), told("Yes."), typed("ok"))) == held
        assert outcome(pr, transcript(merge_gate, typed("is CI green?"), told(f"Yes.\n\n`{pr}`"), typed("ok"))) == passed

        # a step the user never typed neither grants nor takes a grant back
        injected = typed("SESSION NORMS", "SYSTEM_SDK")
        assert outcome(push, transcript(gate, injected)) == held
        assert outcome(push, transcript(*yes, injected)) == passed

        # `Run` picked on `ask_question` is no reply
        assert outcome(push, transcript(question(f"Run `{push}`?"), result("A1: Run"))) == held

        # the branch is read in the workspace, not in the folder the hook starts in
        repo = Path(tmp) / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
        subprocess.run(
            ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t.dev",
             "commit", "-q", "--allow-empty", "-m", "init"],
            check=True,
        )
        commit = "git commit -m 'add page' -- a.txt"
        # a repo with only `main` has no other branch to commit on: it passes
        assert outcome(commit, workspace=str(repo)) == passed
        subprocess.run(["git", "-C", str(repo), "branch", "development"], check=True)
        assert outcome(commit, workspace=str(repo)) == refused
        # the remote's `development` counts before anyone has checked it out
        subprocess.run(["git", "-C", str(repo), "branch", "-D", "-q", "development"], check=True)
        subprocess.run(["git", "-C", str(repo), "update-ref", "refs/remotes/origin/development", "HEAD"], check=True)
        assert outcome(commit, workspace=str(repo)) == refused

    print("ok antigravity")


def switched() -> None:
    """The user's switch: `advice` lets every call through and hands the model what the
    hook would have said, `off` does nothing, and a value it does not know is `on`."""

    def call(command: str, mode: str) -> tuple:
        payload = {"tool_name": "Bash", "tool_input": {"command": command}}
        env = {**os.environ, "CLAUDE_PLUGIN_OPTION_GUARD_GIT": mode}
        result = subprocess.run([PYTHON, str(GUARD)], input=json.dumps(payload), capture_output=True, text=True, env=env)
        told = json.loads(result.stdout)["hookSpecificOutput"] if result.stdout else {}
        return result.returncode, result.stderr, told

    # must pass, and say nothing: what passes under `on` passes silent under every mode
    for mode in ("on", "advice", "off"):
        assert call("git status", mode) == (0, "", {})
        assert call("git commit -m 'x' -- src/a.ts", mode) == (0, "", {})
    for command in ("git add -A", "git push --force origin dev", "git push origin development", "gh pr merge 12"):
        assert call(command, "off") == (0, "", {}), command

    # advice: let through, the refusal or the hold handed over as context, never as stderr
    for command, word in (("git add -A", "REFUSED: git add -A"), ("git push origin development", "HELD: a push")):
        code, err, told = call(command, "advice")
        assert code == 0 and err == "" and told["hookEventName"] == "PreToolUse", command
        assert told["additionalContext"].startswith("ADVICE - the user switched guard_git to advice"), command
        assert word in told["additionalContext"] and "permissionDecision" not in told, command

    # refused as before: `on` spelled out, or a value nobody offered
    for mode in ("on", " ON ", "maybe", ""):
        code, err, told = call("git add -A", mode)
        assert code == 2 and err.startswith("REFUSED:") and told == {}, mode

    print("ok switched")


if __name__ == "__main__":
    demo()
    antigravity()
    switched()
