# Session norms

What every session is told before it reads your first message — the same text in every repo where the plugin is enabled.

Where an app's `CLAUDE.md` and the norms disagree about a norm, the norms are the newer. `CLAUDE.md` holds what is true of that app alone.

## The blocks

| Block | What a session does because of it |
|---|---|
| `LANGUAGE` | Writes chat, the documents, commit messages, pull requests and the strings the app puts on screen in your language. Writes comments, identifiers, file names, URL routes, endpoint paths and every database name in English. Decides enum values per case. Reports existing code in the other language as a finding instead of matching it |
| `POINTERS` | Reads the rule skill for the work in hand before touching it: `build-flow`, `docs-format`, `ui-build`, `db-ops`, `logic-build`. Loads `norms-help` when you ask which command to run, the version, or what changed |
| `SCOPE` | Does only what was asked — no refactor, no rename, nothing "while I'm here" — and writes no document outside the list `docs-format` keeps |
| `GIT` | Fetches and checks the branch before anything else. Commits a finished scope item in the same turn, without asking, with named paths and a message that says why. Asks you first when one of those paths holds a change it did not make. Leaves the tree dirty when it stops for you. Never commits on `main` while `development` exists. Treats a push or the merge of a pull request as a stop in chat, and opens a pull request only when asked |
| `ASKING` | Asks you what is yours to decide, then runs it itself. Never hands you a command to type — only what needs your own hands: a browser login, a dashboard, a key rotation, a payment. Prints a block or a table a skill orders whole, whatever brevity mode another plugin sets |
| `DECISIONS` | Closes an answer that carries two or more decisions with one table: question, options, recommendation. The recommendation names its trade-off, and the table comes before the work |
| `CLOSING THE SESSION` | Ends on a report per scope item, then a fixed block: the page usable now and its route, pages touched by spread, defaults it decided itself, unfinished steps as queue lines, what you must do by hand, the branch and the commits, and the documents it changed |
| `OUTPUT` | Once you set an output folder with [norms-config](../reference/norms-config.md): writes a file it makes for you — a report, a spreadsheet, a PDF — to its own folder in the output folder, one per repo and per worktree, and gives you the full path. Never into the repo, never with a date in the name, never over a file already there. See [guard-output](../reference/guard-output.md) |

## What the git block means for you

- **A clean tree means finished. A dirty tree means something is waiting on you.**
- **`git add -A` and `git add .` are refused**, and the commit names its paths again (`git commit -- <paths>`), so a commit never carries a path nobody named — one staged before the session included. A path that changed outside the scope is reported, never committed along.
- **Two sessions in one checkout do not commit each other's work.** Git commits a whole file, so a path that was already dirty when the session started, or that holds a change the session did not make, leaves its item uncommitted until you pick: commit the file whole, or leave it. Separate worktrees avoid the question.
- **A push is never a dialog.** The session ends its turn on the exact command and the commits it publishes, and runs it once when your reply is a clear yes. See [Gates](gates.md).

## Switching a block

Each block above is `on` until you switch it, for every repo at once, with [norms-config](../reference/norms-config.md). Nothing asks you at install: the first session on a machine runs that skill once, after its first answer, and a guard names its own switch when it refuses. A block's switch applies from the next session start:

- **`advice`**: the block is still printed, marked as advice you have not made binding. The session weighs it.
- **`off`**: the block is not printed, and the session does not follow it.
- **The session is told.** The norms open with one line naming every switch you moved, so a missing block reads as your choice, not a fault.
- **A hook is switched on its own.** Turning the `GIT` block off leaves [guard-git](../reference/guard-git.md) holding pushes, and turning the `OUTPUT` block off leaves [guard-output](../reference/guard-output.md) refusing.

## Three forms

The text follows the documents a repo has.

| The repo has | The norms |
|---|---|
| `docs/PRD.md` | Name the `docs/` files, and `docs/queue.md` as what is not built yet |
| A root `PRD.md` | Name `PRD.md` and `QUEUE.md`, as the form before `docs/` did |
| Neither | The `NOT SETTLED` form: no `POINTERS`, no closing block, and the limits listed in [How it works](how-it-works.md) |

## Related

- [session-start](../reference/session-start.md) — the hook that prints the norms, and everything else a session is handed at start.
- [guard-git](../reference/guard-git.md) — what enforces the git block where a session might not.
- The text itself: `scripts/session_norms.py`.
