# context-reminder

After a commit, tells the session once that its context passed a milestone — 200k, 500k or 800k tokens — so it tells you the next item costs less in a new session. It never blocks.

| | |
|---|---|
| Kind | Hook — runs by itself; it cannot ask, only pass, refuse, or print |
| Runs on Claude Code | `PostToolUse`, matcher `Bash\|PowerShell`, inside the [document reminder](document-reminder.md)'s process |
| Runs on Antigravity | Not at all |
| Script | `scripts/remind_context.py`, called by `scripts/remind_docs.py` |
| Self-check | `scripts/test_remind_context.py` |

## What it does

Every call re-reads the whole context, so a step costs what the context holds when it runs. A session cannot read that size, so the hook measures it and speaks only when a milestone is passed.

- **It measures tokens, not percent.** The size is read from the transcript: the input side of the last call's usage. A fresh session starts near 80k, so at 200k a call costs about two and a half times a fresh one's — whatever the window is. On a 1M window that is 20%.
- **It speaks at a commit**, where an item ends and a new session can start clean.
- **Once per milestone.** The first commit past 200k, the first past 500k, the first past 800k. The commits in between hear nothing.
- **The note opens** `CONTEXT CHECK - past 200k:` and gives the size, and how many times the session's first call that is.
- **The session then tells you in one line**, at the end of that turn. It is advice: you may stay.

## What it lets through

It stays silent when any of these holds:

- **The command was not a `git commit`.**
- **The context is under 200k tokens.**
- **The milestone was already named.** The host records the note in the transcript, and that record is what is looked for. The session quoting the note does not count.
- **A higher milestone was already named.** After a compaction the context grows through the same numbers again, and you were told at the higher one.
- **The transcript cannot be read,** or carries no usage.

## What it does not reach

- **The window.** It cannot see how large the window is, so it cannot speak in percent.
- **A session that never commits.** Nothing is said in a long conversation with no commit.
- **A subagent's context.** Its calls are left out: they read its own context, not the session's.
- **Antigravity.** A hook there cannot hand the model text after a tool has run.
- **What a new session saves.** The milestones are a judgement from the cost of a call, not a measured saving.

## Related

- [document-reminder](document-reminder.md) — the hook whose process carries it
- [Hosts](../concepts/hosts.md) — what differs between Claude Code and Antigravity
- [design-settle](design-settle.md) — its two session breaks, a separate rule
