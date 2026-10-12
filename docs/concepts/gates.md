# Gates — the two stops a hook enforces

A session decides most things with you through a question. Two actions are different: a hook refuses them until a stop has happened, whatever the session intends. They work the same on Claude Code and on Antigravity.

| | Publishing | Destructive SQL |
|---|---|---|
| Covers | `git push`, `gh pr create`, `gh pr merge` | `DROP`, `TRUNCATE`, `DELETE`, a rename, `ALTER TYPE`, `ALTER ... DROP COLUMN`, an `UPDATE` with no narrow `WHERE` |
| You see | The exact command and the commits it publishes | The `DESTRUCTIVE` block, with a real row count |
| You answer | In chat, in your own words | In chat: you approve the number |
| The hook checks | That the stop happened and you replied | That the statement carries its own guard |
| The hook does not check | What your reply means | Whether you agreed |

## Publishing — push and pull requests

The session ends its turn on a message like this, and does nothing until you reply:

```
`git push origin development`
- 4cc1af0 feat(orders): status filter on the order list
- e2bd00d fix(orders): cancelled rows left out of the total

Run it?
```

- **Reply in chat, in any words.** A clear yes runs the command once.
- **A question, a condition, or another instruction is not a yes.** The session answers or does what you said, and shows the command again before it publishes.
- **There is no dialog to click.** A dialog gets clicked before it is read.
- **A push and its pull request share one stop** when you asked for both. The message puts each command on a line of its own, the commits once, and one reply covers both. A reply that names one — `push only` — runs that one, and the other is shown again before it runs.

```
`git push origin development`
- 4cc1af0 feat(orders): status filter on the order list

`gh pr create --base main --head development --fill`

Run both?
```

What `guard_git` holds each command for, all four at once:

1. The session's last message puts the exact command in backticks on a line of its own. A command named inside a sentence — a closing report saying what it pushed — does not count.
2. You typed a reply to that message.
3. Nothing else has been typed since.
4. The command has not already run on that reply — one reply, one run of each command the message puts.

**The hook proves the stop, not the yes.** It cannot read what a reply means, so the session reads it — which of two commands a reply covers included. A session that misreads a no is not stopped by the hook.

Refused outright, with no reply that lets them through: a bare force push (`--force`, `-f`, `+branch`) — `--force-with-lease` is the only force, and it is held like any push; a commit while on `main`, in a repo that has a `development` branch; `git add -A` and `git add .`.

The rule: the `GIT` block of the session norms (`scripts/session_norms.py`). The hook: `scripts/guard_git.py`.

## Destructive SQL

The session counts first, shows the block, and stops:

```
DESTRUCTIVE
Operation  : delete the cancelled orders of 2024
Affected   : 1,204
Expected   : 1,204
Reversible : no — the rows are gone
```

- **You approve the number, not the intent.** The number you approve goes into the statement's guard unchanged.
- **The statement then runs wrapped in a guard**: it counts what it touched and aborts the whole transaction when the count is not the number you approved. Nothing is lost on a mismatch.
- **Several operations one request needs share one stop** — deleting an order and its lines is two. You see one block per operation, each with its own number, and answer once; an operation your reply leaves out does not run. The approved ones run in one guarded block, so a count that misses on one aborts all of them.
- **In `app-settle`'s Align, the destructive findings you picked are shown together the same way**, before the first one starts. There each runs in a guarded block and a commit of its own, so one finding can be reverted alone; a count that went stale because an earlier finding changed the data aborts that finding only, and nothing is lost.

What `guard_destructive` refuses: a destructive statement that arrives without that guard — one `DO` block with a `RAISE EXCEPTION`, per statement.

**The hook proves the guard, not the approval.** It cannot know whether you answered; it relies on the guard needing a number that only your answer gives.

What it lets through, and what it does not reach:

- **A `DELETE` narrowed to rows opening with `[CLAUDE]`** passes unguarded: those are the test rows the session made itself.
- **A repo can switch the hook off** with a file at `.claude/destructive-gate.off`. That is your decision, never the session's, and the rule still stands there.
- **A migration file applied by CI is not gated.** The gate stands where the SQL is written, not where it runs.
- **A store that is not SQL is not covered.**

The rule: `skills/db-ops/SKILL.md`, Destructive operations. The hook: `scripts/guard_destructive.py`.
