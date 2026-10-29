# kaizn docs

`kaizn` settles an app one layer at a time and holds every later session to what was settled. These pages are for the people who install it. What an agent obeys is in `skills/` and `scripts/`; nothing here is a rule, and where a page and a skill disagree the skill is right and the page is the defect.

New here: [Overview](start/overview.md), then [Install](start/install.md), then [Quickstart](start/quickstart.md). In a session: `/kaizn:norms-help`.

## Getting started

| Page | Holds |
|---|---|
| [Overview](start/overview.md) | What the plugin is, its five parts, and how a repo moves through them |
| [Install](start/install.md) | Requirements, the two commands, the companion skills, and how to check it loaded |
| [Quickstart](start/quickstart.md) | The first run, on a new app or on one that already exists |

## Concepts

| Page | Holds |
|---|---|
| [How it works](concepts/how-it-works.md) | Settle, then hold: what decides, what enforces, what loads when, and what a repo that was never settled gets |
| [Session norms](concepts/session-norms.md) | What every session is told before it starts: language, scope, git, asking, decisions, the closing report |
| [Gates](concepts/gates.md) | The two stops a hook enforces — publishing, and destructive SQL: what you see, what you answer, what the hook checks and what it does not |
| [Documents](concepts/documents.md) | The documents an app repo keeps: where to look for what, and what gets each one written — the rule, the reminder after a commit, the audit |
| [Hosts](concepts/hosts.md) | Claude Code and Antigravity: what differs, what is the same, and switching mid-work |

## Guides

| Page | Holds |
|---|---|
| [Start a new app](guide/new-app.md) | From an empty directory to the first page built |
| [Bring in an existing app](guide/existing-app.md) | Document it, migrate a root `PRD.md`, audit it against the rules, or rework its decisions |
| [Redesign the look](guide/redesign.md) | `design-settle` alone: Fast or Full, the frames, the canvas, and what changes where UI exists |
| [Update the plugin](guide/update.md) | Getting a new version onto a machine, and checking which one a session runs |
| [Run on Antigravity](guide/antigravity.md) | Requirements, the one command, the companion skills, how to check it loaded, updating, and what a headless run must be allowed |
| [Maintain app repos](guide/maintain-app-repos.md) | Old sections in an app's `CLAUDE.md`, a root `PRD.md`, a shadowing `.mcp.json` |

## Reference: commands and skills

| Page | Holds |
|---|---|
| [Commands](reference/commands.md) | What to run in which situation, and which skills need no command |
| [app-settle](reference/app-settle.md) | The app level: bootstrap, document, migrate, align, rework |
| [logic-settle](reference/logic-settle.md) | The layer between database and UI, its one folder and its lint floor |
| [design-settle](reference/design-settle.md) | The visual direction, the canvas, and `DESIGN.md` |
| [build-flow](reference/build-flow.md) | The queue, how much one session delivers, the order of work, the closed list of stops |
| [docs-format](reference/docs-format.md) | The documents an app repo keeps, and who may write what |
| [ui-build](reference/ui-build.md) | The `DESIGN.md` gate, component reuse, states, interface copy |
| [db-ops](reference/db-ops.md) | Introspection, migrations, RLS and role testing, destructive operations |
| [logic-build](reference/logic-build.md) | Keys, where a rule lives, validation, transactions, error shape, the data layer |
| [norms-help](reference/norms-help.md) | Asking a session for help: the card it prints — version, commands, pages, last change |
| [norms-config](reference/norms-config.md) | Each block of the norms, each guard and each reminder switched on, to advice, or off, for every repo |

## Reference: hooks

| Page | Holds |
|---|---|
| [session-start](reference/session-start.md) | What a session is handed when it starts: the norms, the documents, the listings, the hand-over |
| [guard-git](reference/guard-git.md) | What is refused and what is held around commits, pushes and merges |
| [guard-destructive](reference/guard-destructive.md) | Destructive SQL sent without its guard |
| [guard-output](reference/guard-output.md) | Where a session's files for you go, and a file written into the root of that folder or into another session's folder |
| [document-reminder](reference/document-reminder.md) | The three questions a session is handed after a commit that touched no document |
| [context-reminder](reference/context-reminder.md) | The one line you are told when a session's context passes 200k, 500k or 800k tokens |

## Project

| Page | Holds |
|---|---|
| [What is proven](reference/status.md) | What has run for real on each host, and what has not |
| [Changelog](https://github.com/rapidkaizen-cloud/kaizn/blob/main/CHANGELOG.md) | What changed in each version, newest first. Kept at the repo root, where `norms-help` reads it in an installed copy |

A feature with no page here has its skill as the only source: `skills/<name>/SKILL.md`.
