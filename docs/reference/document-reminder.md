# document-reminder

After a commit that changed no document, hands the session a few questions about whether one became false. It never blocks.

| | |
|---|---|
| Kind | Hook — runs by itself; it cannot ask, only pass, refuse, or print |
| Runs on Claude Code | `PostToolUse`, matcher `Bash\|PowerShell` |
| Runs on Antigravity | `PreInvocation`, through `scripts/session_norms.py`, before each model call after the first of a turn |
| Script | `scripts/remind_docs.py` |
| Self-check | `scripts/test_remind_docs.py` |

## What it does

Most commits owe no document, and a hook cannot tell which do. So it asks, at the one moment a missing correction can still be amended into the commit, and takes "none" for an answer.

- **On Claude Code** the reminder arrives with the result of the commit command.
- **On Antigravity** a hook that runs after a tool cannot hand the model text. `scripts/session_norms.py` asks before the next model call instead, once per commit.
- **The reminder opens** `DOCS CHECK - commit <short hash> changed <N> file(s) and no document.`
- **The session answers** by amending the document into that commit while it is unpushed, or by carrying on and reporting `Docs: none - <why>` for the commit at the close.

## What it asks

The questions follow the form the repo is on:

| Repo form | Found by | Questions |
|---|---|---|
| `docs/` form | `docs/PRD.md` | Did a sentence in `docs/product.md`, `docs/rules.md`, `docs/glossary.md`, `docs/architecture.md`, `docs/runbook.md` or `README.md` become false? Did it change how the app behaves — then it owes a `docs/changelog.md` entry, in a new file where the repo has none. Did it finish a `docs/queue.md` line that is still standing? Where the Help row of `docs/product.md` is not `none`: did a page become usable to its role with no `docs/guide/` page for its task? |
| Legacy form | A root `PRD.md` | Did a sentence in `PRD.md` become false? Did it finish a `QUEUE.md` line that is still standing? |

Any yes means writing the document and amending it into the commit. The rule behind the questions is in [Documents](../concepts/documents.md).

## What it lets through

It stays silent unless all four hold:

1. **The repo keeps documents.** A `docs/PRD.md` or a root `PRD.md`. A repo with neither is never asked.
2. **The session's own command ran `git commit`.** `git -C . commit` and `git add ... && git commit` count. A commit named inside a quoted string or a heredoc body does not, such as `echo "git commit is next"`.
3. **HEAD is that commit.** It must have been made within the last five minutes. A command that exits 0 with nothing committed, such as `git commit ...; git status` with nothing staged, leaves an older HEAD and is not asked about.
4. **The commit changed no document.** Nothing under `docs/`, and none of `PRD.md`, `QUEUE.md`, `DESIGN.md` or `README.md` at the root. A merge commit lists no files and is silent.

Two more cases are silent:

- **The amend that adds the document.** `git commit --amend --no-edit` afterwards finds a document in HEAD and asks nothing.
- **A payload it cannot read.**

On Antigravity the reminder also needs the conversation's own last tool call to have run `git commit`, and no step since to carry the `DOCS CHECK - commit ` line:

- **Once per commit.** The step that asked is in the transcript by the next call.
- **Not after another tool.** Once a later tool has run, the commit is not the last call.
- **Not for another conversation's commit.** A session opened a minute after another one committed is not asked about it.
- **Not on the first call of a turn,** which is the norms' own, and not without a transcript to read.

## What it does not reach

- **Which commits owe a document.** It asks each commit that passes the conditions above; the answer is the session's.
- **A way to hold a commit.** It exits 0 in every case, so a commit is never held up.

## Switching it

Set `remind_docs` in `/config`, or ask [norms-config](norms-config.md): `on`, the default, or `off`, which leaves every commit unasked, in every repo. It switches apart from the [context reminder](context-reminder.md) that rides in its process. On Antigravity it is always `on`.

## Related

- [Documents](../concepts/documents.md) — what an app repo keeps, and what gets it written
- [context-reminder](context-reminder.md) — the note on the session's size that rides in this hook's process
- [session-start](session-start.md) — the script that carries the reminder on Antigravity
- [docs-format](docs-format.md) — the rule that a commit carries its own correction
- [Hosts](../concepts/hosts.md) — what differs between Claude Code and Antigravity
