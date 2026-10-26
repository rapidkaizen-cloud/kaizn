# session-start

Hands a session, when it starts, the norms it works by, the documents of the repo it works in, two listings of what the repo already has, and any note about a stale document or an unfinished session.

| | |
|---|---|
| Kind | Hook — runs by itself; it cannot ask, only pass, refuse, or print |
| Runs on Claude Code | `SessionStart`, no matcher |
| Runs on Antigravity | `PreInvocation`, no matcher — before every model call; the text goes in once per conversation |
| Script | `scripts/session_norms.py`, with `scripts/handoff.py` for the hand-over block |
| Self-check | `scripts/test_session_norms.py`, `scripts/test_handoff.py` |

## What it does

It prints text, and the host adds it to the session. It refuses nothing and asks nothing.

- **The norms live in the plugin, not in each app.** A change reaches every app repo through a plugin update. An app's `CLAUDE.md` keeps what is true of that app alone: its stack, its locale, its own rules.
- **The documents are printed, not pointed at, wherever they fit.** A pointer is obeyed by judgement, and the sessions that skip it are the narrow ones where its prohibitions still apply. A document too long to fit is named instead; see [The limit](#the-limit).
- **The two listings are printed for the same reason.** A session that never loads `ui-build` hunts for `Pagination`, misses `Pager`, and writes it a second time.

Order: the norms, the documents and their notes, the two listings, the hand-over. The listings come after the documents so they do not push them out of view.

## What a session is handed

| Block or listing | When it appears | What it holds |
|---|---|---|
| `SESSION NORMS (kaizn)` | Always | The heading, and that the norms hold where they and the app's `CLAUDE.md` disagree about a norm |
| `SWITCHED by the user, on purpose:` | A switch is away from `on` | One line naming each switch you moved and its mode; see [Switches](#switches) |
| `LANGUAGE` | Always | Your language for chat, documents, commit messages, pull requests and on-screen strings; English for comments, identifiers, file names, URL routes, API paths and every database name; enum values decided per case |
| `POINTERS` | A repo with `PRD.md` or `docs/PRD.md` | Which skill to read before which work: `build-flow`, `docs-format`, `ui-build`, `db-ops`, `logic-build` — and `norms-help` for which command to run, the version and what changed |
| `NOT SETTLED` | A repo with neither, in place of `POINTERS` | That `app-settle` has not run: `build-flow` and `docs-format` do not apply, UI is built only from the components and tokens the repo has, the session says once at the end that `app-settle` has not run, and `norms-help` answers which command to run |
| `SCOPE` | Always | Only what was asked, no refactor or rename outside it, and the limit on documents |
| `GIT` | Always | `git fetch` and a branch check first, a stop on `main` where `development` exists or when behind `origin/development`, commit a finished item in the same turn with its paths named in `git add` and again in `git commit -- <paths>`, so a path staged before the session never rides along, push and merge as a chat stop, a pull request opened only when you ask |
| `ASKING` | Always | A decision that is yours is asked, or answered in chat at a hard stop; the session never hands you a command to type. A block or a table a skill orders printed is printed whole, whatever brevity mode another plugin sets |
| `DECISIONS` | Always | An answer with two or more decisions closes with one table: question, options, recommendation and its trade-off |
| `CLOSING THE SESSION` | A repo with `PRD.md` or `docs/PRD.md` | The report per scope item, then a block written even when the answer is "none" |
| `OUTPUT` | Once you set an output folder, after the blocks above | The full path of the folder this session writes your files to, worked out from its checkout — see [guard-output](guard-output.md) — and that working files stay where the work is, a name carries no date, and nothing is overwritten |
| `FIRST SESSION ON THIS MACHINE` | Claude Code, the first session on the machine | That the session ends its first answer, once your task is done, by running `/kaizn:norms-config` once — the switches and the output folder — after one line in your language saying it is asked once and can be changed there any time. Never a stop or a question before the task. See [First session](#first-session) |
| `HOST - Antigravity` | Antigravity only | See below |
| Components listing | A `components` or `widgets` folder holds components | Opens `--- Components already in this repo`: what to reuse before writing a component |
| Data layer listing | `CLAUDE.md` has a `Data layer` row naming a folder that exists and has files | Opens `--- Data layer of this repo (<folder>)`: what to call before writing a query |
| Hand-over | See below | What the other host's last session knew |

### Switches

Each block from `LANGUAGE` to `OUTPUT` has a switch of its own, set with [norms-config](norms-config.md) and read from its file when a session starts; the heading, `FIRST SESSION ON THIS MACHINE` and `HOST - Antigravity` have none. The table above is what every switch at `on` prints.

| Switch | Block |
|---|---|
| `norm_language` | `LANGUAGE` |
| `norm_pointers` | `POINTERS`, or `NOT SETTLED` in its place |
| `norm_scope` | `SCOPE` |
| `norm_git` | `GIT` |
| `norm_asking` | `ASKING` |
| `norm_decisions` | `DECISIONS` |
| `norm_closing` | `CLOSING THE SESSION` |
| `norm_output` | `OUTPUT` |

- **`advice`** prints the block whole, with `Advice only: the user has not made this block binding - weigh it.` under its heading.
- **`off`** leaves the block out. The documents, the notes, the listings and the hand-over are printed as before.
- **The `SWITCHED` line** follows the heading whenever any switch — a block's, a guard's or a reminder's — is away from `on`, so a session reads a missing block as your choice.
- **A block's switch reaches nothing else.** `norm_git` off leaves `guard_git` holding pushes, and `norm_output` off leaves `guard_output` refusing.
- **On Antigravity** every switch is `on`: the skill cannot reach the switches file there.

### First session

Nothing asks about the rules when the plugin is installed. Instead, the first session on a machine, at the end of its first answer and after your task, runs [norms-config](norms-config.md) once: the same questions as when you run it yourself, the output folder among them — Claude Code's own behaviour, or a folder of your own. Pick nothing and every rule stays `on`, with no output folder.

- **Already set, not asked.** A machine where `norms-config` has written anything gets only the line naming it.

- **Once per machine.** With the block, the hook writes a file `onboarded-output` into the plugin's data folder, `~/.claude/plugins/data/<id>/`. A machine where that file exists never gets the block again, across plugin updates; uninstalling the plugin deletes the folder, and the next install is asked again. A machine told before 0.107.0 holds only the older `onboarded`, so it is asked once more.
- **Never a failed start.** Where the file cannot be written the block is left out, so it never repeats every session.
- **Claude Code only.** Antigravity has no switches, so it never gets the block.

### The documents, by repo form

| Form | Found by | Printed after the norms |
|---|---|---|
| Root `PRD.md` | `PRD.md` at the root; it wins when `docs/PRD.md` exists too | `PRD.md`, then `QUEUE.md`. Sections 1, 2 and 6 (context, roles, prohibitions) whole; sections 3 to 5 (rules, glossary, design system) as a line starting `Not printed. Read` and naming their line range, when the file has exactly `## 1.` to `## 6.` in order. Any other shape is printed whole. Past 400 lines, a `WARNING:` |
| `docs/` | `docs/PRD.md`, no root `PRD.md` | The norms worded for `docs/`, then `docs/README.md`, `docs/product.md` and `docs/queue.md`. Never the frozen ones: `docs/PRD.md`, `docs/changes/`, the decision records |
| Neither | | The `NOT SETTLED` norms, then `QUEUE.md` and `docs/queue.md`, each if present |

Each document opens with `--- <file> — <what it holds> ---`. An empty or missing file prints nothing.

### The limit

Claude Code replaces a hook's output over 10,000 characters with its first 2,000 and a file path, so an output that long loses most of the norms. The script keeps under it, in this order:

1. **The norms and the notes are always printed whole.**
2. **Each document is printed whole if it still fits.** One that does not is named under its own heading: `Not printed: no room left at session start. Read it before the first edit of this session.` For a root `PRD.md` in the six-section shape, the line names the line ranges of sections 1, 2 and 6 to read. Where the document holds prohibitions and they fit — `## Prohibitions` in `docs/product.md`, section 6 of a root `PRD.md` — they are printed under that line, after `Its prohibitions bind whether or not it is read:`, because a session that skips the read still owes them.
3. **A listing is cut at a line where the room ends**, and closes with a line starting `... more`, telling the session to list the folder itself. A hand-over that does not fit is cut the same way and closes with `... the hand-over is cut here: a session start carries no more.`

A repo whose output already fitted gets exactly what it got before. On Antigravity nothing is cut: the text goes in as a message, which has no such cap.

### The listings

- **Components:** shared UI files in folders named `components` or `widgets`, shallowest first, at most 60, then `... N more files - list the folder.` Each shows its names: capitalised exports in `.tsx` and `.jsx`, the file name for `.vue`, `.svelte` and `.astro`, and the widget, `@Composable` and `View` declarations in `.dart`, `.kt` and `.swift`. Tests, specs, stories and all-capital constants are left out.
- **Data layer:** the folder named by the `Data layer` row, taken as the first backticked path in its cell or its first word. Its files, at most 40, each with up to 12 exported function names and `+N` for the rest. Names are read from `.ts`, `.tsx`, `.js`, `.jsx` and `.mjs` files only.
- **Both skip** `node_modules`, `dist`, `build`, `out`, `target`, `vendor`, `coverage`, `design-canvas` and every dot folder. Both say they are a listing, not the rule.

### The notes

- **A named path is gone** (`docs/` form): `NOTE: these living documents name paths that do not exist:`, at most 20 lines. It reads `docs/README.md`, `docs/product.md`, `docs/rules.md`, `docs/glossary.md`, `docs/architecture.md`, `docs/runbook.md` and every `docs/guide/` page. Links resolve from the document, backticked paths from the repo root, so a file named without its folder is reported. URLs and host names are not paths, and `DESIGN.md` is never reported: the Proof profile names it before `design-settle` has written it.
- **A living document is missing** (`docs/` form): `NOTE: <path> is missing.` for `docs/README.md` or `docs/product.md`.
- **`CLAUDE.md` carries old sections:** `NOTE: CLAUDE.md still carries sections ...`, naming each one it recognises.
- **The data layer folder does not exist:** `NOTE: the Data layer row of CLAUDE.md names ...`, with the folder. It is printed in the data layer listing's place, after the documents, and shares that listing's room, unlike the notes above. A path that climbs out of the repo is not followed and says nothing.

### The hand-over

`--- Hand-over: the last session in this repo ran on <host> and left the tree dirty ---` appears only when all three hold: the tree is dirty, the other host has a session for this repo, and that session is more recent than this host's own previous one. A clean tree needs none, because `docs/queue.md` and `git log` already say where the work stands.

It holds the last request, the last 12 answers you gave as question and answer, the other session's todo list when it ran on Claude Code, and the last two things it said. The request and each message are cut to 700 characters; each half of an answer and each todo item to 240. It is a record to check against `git diff`, never an instruction.

## When it stays silent

- **An empty repo** gets the norms and nothing else.
- **No components folder, no `Data layer` row:** no listing. Components only under `node_modules`, `design-canvas` or a dot folder do not count.
- **A clean tree, a repo the other host never worked in, or a more recent session of this host's own:** no hand-over.
- **No `CLAUDE.md`, or none of its old sections, or every named path resolving:** no note. The queue, `docs/changelog.md` and the frozen records are not path-checked.
- **On Antigravity, once a conversation holds the norms:** later turns do not hand them over again.

## On Antigravity

- **There is no start event,** so the script runs before every model call. On the first call of a turn it looks for `SESSION NORMS (kaizn)` in the transcript and, finding none, hands the text over as a message that stays in the conversation. Where the transcript cannot be read, it hands it over again.
- **Later calls of a turn** run the commit question instead; see [document-reminder](document-reminder.md).
- **`HOST - Antigravity` follows the norms.** It maps Claude Code's tools to this host's: `AskUserQuestion` is `ask_question`, the shell tools are `run_command`, a subagent is `invoke_subagent`, an `mcp__server__tool` is `call_mcp_tool`, a skill is its `SKILL.md` read with `view_file`. It also says the guards run as hooks, unseen until one refuses, and that where `AGENTS.md` and the norms disagree, the norms hold.
- **`CLAUDE.md` is printed** under `--- CLAUDE.md — what is true of this app alone ---`, because this host does not load it.
- **The hand-over reads the other way too:** on Antigravity it reads Claude Code's transcripts, on Claude Code it reads Antigravity's.

## Related

- [Session norms](../concepts/session-norms.md) — what the norms say, in prose
- [Documents](../concepts/documents.md) — the documents a repo keeps
- [Gates](../concepts/gates.md) — the stops `GIT` and `db-ops` set
- [Hosts](../concepts/hosts.md) — what differs between Claude Code and Antigravity
