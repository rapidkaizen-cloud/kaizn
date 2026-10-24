# Bring in an existing app

One command reads the repo and runs the mode it owes next: document it, migrate it, audit it, or rework it.

> [!WARNING]
> The migrate and align modes have never run in a real app. Run them on a copy of the app first. See [What is proven](../reference/status.md).

## Steps

1. **Commit or stash your own work.** Migrate and align stop on a dirty working tree and name the paths, because their commits must carry nobody else's changes.
2. **Open Claude Code in the repo and run `/kaizn:app-settle`.** Its first block reports the mode, with the fact that produced it. You may overrule it in one line.
3. **Answer what the mode asks.**

   | The repo has | Mode | What happens |
   |---|---|---|
   | Code, no documents | Document | The app is documented as it is. Nothing about the app changes |
   | A root `PRD.md` | Migrate | `PRD.md`, `QUEUE.md` and their sections move to the `docs/` form, in one commit |
   | Documents in place | Align | The repo is audited against the installed rules, the findings are ranked, and you pick what is fixed — one finding per commit |
   | Documents in place, and you want the app itself to change | Rework | The decisions are reopened, keeping first, and the documents are edited to match |

4. **Run `/kaizn:app-settle` again** when you want the next mode. It runs one mode per run.
5. **Settle the other two layers**, or only the one you need:
   - `/kaizn:logic-settle` — also the right command when a repo has grown handwritten data-fetching or validation and you want to know what to adopt. A session never starts it on a running app by itself.
   - `/kaizn:design-settle` — existing UI is audited first, and today's look is one of the candidates. Where a `DESIGN.md` is already written, it also offers to fix only the drift.

## Align or rework

Which of the two runs is your word. A wish to change what the app does, whom it serves, or what it runs on makes it rework. With none stated it is align, and the first block says that asking for such a change is what turns it into rework.

## An app on the old form

An app started before the `docs/` form keeps its root `PRD.md` and `QUEUE.md` until `app-settle` migrates them. Until then every skill reads the repo through `docs-format`'s legacy map, and nothing breaks: the sessions there get the norms that name `PRD.md` and `QUEUE.md`.

## If something goes wrong

- **The repo is not a git repo.** `app-settle` says so and offers `git init`. Document continues either way; migrate and align stop without one, because their commits are what makes them undoable.
- **The branch is `main`.** A session never works on `main`; `app-settle` offers to create `development`.
- **The `PRD.md` does not have the expected shape.** It has no mechanical route and stays on the old form for that run.

## Related

- [app-settle](../reference/app-settle.md) — every mode in detail.
- [Maintain app repos](maintain-app-repos.md) — old sections left in an app's `CLAUDE.md`.
- [Documents](../concepts/documents.md)
