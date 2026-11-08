# context-reminder

Tells the session once that its context passed a milestone — 200k, 500k or 800k tokens — so it stops at the next safe point and offers you a new session, and holds your first message after an hour idle on a large context.

| | |
|---|---|
| Kind | Hook — runs by itself; it cannot ask, only pass, refuse, or print |
| Runs on Claude Code | `UserPromptSubmit`, on every message you send · `PostToolUse`, matcher `Bash\|PowerShell`, inside the [document reminder](document-reminder.md)'s process |
| Runs on Antigravity | Not at all |
| Script | `scripts/remind_context.py` |
| Self-check | `scripts/test_remind_context.py` |

## What it does

Every call re-reads the whole context, so a step costs what the context holds when it runs. A session cannot read that size, so the hook measures it and speaks only when a milestone is passed.

- **It measures tokens, not percent.** The size is read from the transcript: the input side of the last call's usage. A fresh session starts near 80k, so at 200k a call costs about two and a half times a fresh one's — whatever the window is. On a 1M window that is 20%.
- **It speaks at your message, or at a commit** — whichever comes first after the milestone.
- **Once per milestone.** The first message or commit past 200k, the first past 500k, the first past 800k. Everything in between hears nothing.
- **The note opens** `CONTEXT CHECK - past 200k:` and gives the size, and how many times the session's first call that is.
- **The session makes it a seam.** It writes where the work stands where a new session will read it — `.design-audit/resume.md` in a `design-settle` run, else a `docs/queue.md` line, else its closing line — and ends the turn at the next point the work can be left, never mid-edit.
- **Then it tells you in one line**: the size, what each call costs against a new session's, and that a reply in the same session continues at that price. You may stay.

## Holding a message after a pause

The cache of a subscription session lives an hour. The first message after that writes the whole context again: one "is it done?" in a session left for two days rewrote 431k tokens.

- **Held once** when the session sat idle more than an hour and its last call read more than 100k tokens. Your message is not sent; the notice opens `CONTEXT HOLD - not sent:` and says how long it sat, how many tokens sending would write again, and that a status question or a new item costs less in a new session.
- **Send it again to continue here.** The same message, or another, passes: the host records the hold in the transcript, and that record is what is looked for.
- **Held again** after the next pause, once a call has run in between.
- **A commit is never held.** Only a message you send.

## What it lets through

It stays silent when any of these holds:

- **The context is under 200k tokens.**
- **The milestone was already named.** The host records the note in the transcript, and that record is what is looked for. The session quoting the note does not count.
- **A higher milestone was already named.** After a compaction the context grows through the same numbers again, and you were told at the higher one.
- **The transcript cannot be read,** or carries no usage.

A message passes the hold when the session sat idle an hour or less, when its context is 100k tokens or less, when the time of its last call cannot be read, or when it was held once since that call.

## What it does not reach

- **The window.** It cannot see how large the window is, so it cannot speak in percent.
- **The cache's real lifetime.** It assumes an hour. A key on the 5-minute cache loses it sooner, and is held only past the hour.
- **A subagent's context.** Its calls are left out: they read its own context, not the session's, and warm nothing of the session's cache.
- **Antigravity.** A hook there can neither hand the model text after a tool has run nor hold a message.
- **What a new session saves.** The milestones are a judgement from the cost of a call, not a measured saving.

## Switching it

Ask [norms-config](norms-config.md): `on`, the default, or `off`, which leaves every milestone unsaid and every message unheld, in every repo, from the next message. Switching the [document reminder](document-reminder.md) off leaves this one as it is.

## Related

- [document-reminder](document-reminder.md) — the hook whose process carries it at a commit
- [Hosts](../concepts/hosts.md) — what differs between Claude Code and Antigravity
- [design-settle](design-settle.md) — its own session breaks, a separate rule
