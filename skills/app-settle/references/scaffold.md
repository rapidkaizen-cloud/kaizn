# The scaffold and the close — N5 and N6, and the files D5 shares

## N5 — Scaffold

**Nothing is copied — write every file for the answers this session got.** This plugin ships no template folder: a stock file is a decision taken before its question was asked, and it goes stale without anyone re-reading it. A Pioneer platform receives exactly what a Ready one does.

**The app's skeleton comes from the platform's own init command, never from a file written here** — a Ready framework's official scaffolder, a Pioneer platform's own, the toolchain's where no framework was chosen. Its command is verified live (`stack-questions.md`, How they are asked) and named in the N3 summary, whose approval covers it. **Run it first after that approval, before N4 writes `docs/`**, because a scaffolder refuses or overwrites a directory that is not empty. A `README.md`, `CLAUDE.md` or `AGENTS.md` it shipped is replaced by this step's own.

| File | Mode | Contents |
|---|---|---|
| `CLAUDE.md` | Both | **Thin**, written to the shape below |
| `AGENTS.md` | Both | **Thinner**, written to its own shape below — for the agents that never see the plugin |
| `.claude/settings.json` | Both | `{"enabledPlugins": {"raizen-norms@raizen": true}}` — that key and nothing else; a repo that already has the file keeps the rest of it |
| Host rewrite rule | Bootstrap | Only when the framework is a **static SPA**, and written for the host chosen at Question 4 — `vercel.json` on Vercel, `netlify.toml` on Netlify, a `try_files` line on an own server. Next.js, Nuxt, SvelteKit, and Astro carry their own server layer — do not write one |
| CI workflow | Bootstrap | Only when the user asks for migrations through CI — the session never raises it (N6). Written for the host and migration tool actually chosen: one written for the wrong runner is worse than none |

**No `.mcp.json` is written — ever.** Database MCP servers are connected **user scope**, once per machine, never per repo; for Supabase the exact `claude mcp add -s user` one-liner is printed at N6. A database whose official MCP server exists follows the same pattern; a database with no server → say so rather than leaving the gap silent.

**Bootstrap, after the files:** `git init` — skipped where the init command already made the repo — `git branch -M main`, and commit the new files there, paths named — the one commit `main` ever takes directly. Then create `development` from `main` and switch to it.

### The shape of `CLAUDE.md`

**English prose, whatever the app's UI language** — only the values follow the app's locale. A translated file is invisible to the stale-section detector in `session_norms.py`, which matches English phrases from retired sections, so nothing would migrate the file later.

Six parts, nothing else. A rule that would hold in another app belongs in the plugin, never here.

| Part | Holds |
|---|---|
| Opening line | That this file holds what is true of this app alone, and that norms are printed by `raizen-norms` every session — a norm living in two places is a norm that will disagree with itself |
| `## Locale` | On screen · in the code · dates · numbers. The first two rows stay separate: a UI language is never a licence for an identifier, a route, or a database name written in it |
| `## Stack` | One row per N2 answer — platform, frontend, hosting, database, auth, component library, environments, migrations — the component library row reading `not decided — design-settle` until that skill writes it, and left out where no screen exists — and the line stating this app's stack is locked, its reasons in `docs/decisions/`, re-opened only through `app-settle` rework mode |
| `## Ground truth` | Code and the live database are ground truth for **facts**; the living documents `docs/README.md` lists for **intent and prohibitions**, `DESIGN.md` for the design system; `docs/PRD.md` and `docs/changes/` are history, never current truth |
| `## Gate` | No `DESIGN.md` → `ui-build` refuses to write components, and `design-settle` is what writes it |
| `## Rules for this app only` | Empty at bootstrap. Only rules that would be wrong in another app |

- **The last two parts stay in the file on purpose**: they must still bite in a session where the plugin is absent, disabled, or failed to start. Everything else there is a value, not a rule.
- **Name the skills that exist today, never from memory of an older flow** — never `/app-init`, `/app-align`, or `/design-rework`, all folded into `app-settle` and `design-settle`.

### The shape of `AGENTS.md`

**Written for the agents that never see the plugin.** Claude Code reads `CLAUDE.md`, is handed the norms and the living documents by `raizen-norms` at every session start, and never loads this file. Codex, Cursor, Copilot, and whatever comes next read `AGENTS.md` and nothing else here — no norms, no injected documents, no guard behind any command — and build from their own defaults: unable to know a shared set exists, they write a second design system first.

**This file may restate a norm, which `CLAUDE.md` must never do**: no agent holds both — except Antigravity, which loads this file and, where `raizen-norms` is installed, is handed the norms too; their `HOST` block says the norms hold. A restatement still goes stale, so keep the file short and pointing at the repo — the documents, the shared set, the lint command — never paraphrasing a skill.

English prose, five parts, nothing else:

| Part | Holds |
|---|---|
| Opening line | That Claude Code does not read this file, that every other agent starts here, and that nothing enforces what follows except the repo's own linter — the rest is on the agent's honour |
| `## Read first` | `CLAUDE.md` whole — locale, stack, ground truth, the gate. Then `docs/README.md` and every living document it lists: `DESIGN.md` is the design system and it is normative; the Prohibitions in `docs/product.md` are what a well-meaning session must not "fix"; `docs/PRD.md` and `docs/changes/` are history. A change that makes a living document false corrects it in the same commit |
| `## UI` | At bootstrap, the gate alone: no UI component is written while `DESIGN.md` is absent. `design-settle` replaces it in its pass with this app's own values — the file and folder holding the shared set, read before any element is written · the order of sources: a component in this repo, then the named library, then a new one that says what the existing ones cannot do, because looking slightly different is a prop · styling values read by role from the named styling file, never typed · the `/design-system` route a new shared component is added to · the lint command, run before finishing, its refusals fixed and never disabled |
| `## Logic` | At bootstrap, one line: every rule the app enforces is in `docs/rules.md`, and a rule not written there is asked for, never invented. `logic-settle` replaces it at its Step 7 (`references/floor.md`) with this app's own values — the data layer folder, and that no database call is written outside it · that access rules live in the database and are never re-implemented in application code · the settled libraries by pointer to `CLAUDE.md`'s Stack table · the lint command and the test command · that a failing rule test is never fixed by editing the test |
| `## Never` | What the plugin refuses by hook and this file can only ask: no commit on `main`, no push, no staging of everything at once — paths are named · no destructive SQL statement and no unscoped update without the user's word in chat · no secret value in any file — name the variable |

- A product without UI gets no `## UI` part; an app with no database and no remote API gets no `## Logic` part.
- **A legacy repo** — `design-settle`, `logic-settle`, or align mode writing this file into one that could not migrate — names what the map names: `## Read first` reads `PRD.md` whole, Section 5 the design system and Section 6 the prohibitions; the `## UI` gate holds while Section 5 is empty or `[needs verification]`; `## Logic` points at Section 3.
- **It is not `CLAUDE.md` imported or symlinked**: the two files have different readers and hold different things, and a symlink does not survive a Windows checkout without Developer Mode.

### Connectors are recommended, never a precondition — bootstrap

Where the database chosen at Question 6 has a Claude connector or an MCP server, say so once, say what it automates, and carry on whatever the answer is. Bootstrap never waits for one — every connector replaces work the user can also do by hand.

- **Derive it from the stack, not from this file.** Name what Question 6 actually produced.
- **Never claim a connector exists** — the catalogue changes and this file does not. Point at the connector settings and let the user see what is really there.
- **Do not raise connectors for hosting here**; `build-flow` raises them at the one moment they matter.

### The database connection

**Supabase Cloud** — only on a machine not yet set up, the MCP server is connected user-scope, the browser login approved on first use:

```
claude mcp add -s user --transport http supabase "https://mcp.supabase.com/mcp"
```

The URL must stay **bare** — Supabase's OAuth rejects any query string, so adding `?features=` or `?project_ref=` breaks the login itself.

**Self-hosted Supabase does not get that line.** Write its route on `CLAUDE.md`'s Database row — `psql` inside the database container over `ssh <host alias>`, the alias and never a credential — and hand the user the permission rule that `ssh` command needs. `guard_destructive` covers that route. Studio's own MCP endpoint is the alternative, reached only through an `ssh` tunnel because it carries no authentication.

Both are once per machine and account, never per repo, so a machine already set up needs nothing. Another database → whatever its own equivalent is.

## N6 — Close — bootstrap

Report one block: the files created, then what the **user must do by hand right now** — create the database project chosen at Question 6, plus its staging counterpart if Question 7 asked for one, and connect it as The database connection states, its one-liner printed.

- **Pointed at production because there is no staging → say that plainly**: from then on every guarded destructive statement lands on live data.
- **Say that without a live database there is no migration and no role test, so not a single page can be built.**
- **Do not mention the hosting connection, production environment variables, or the CI migration workflow.** None is needed to build a page locally; `build-flow` raises them once the app is ready to ship.
- **On a Pioneer platform, list what is still owed** (`pioneer.md`, rule 4).

Then offer the next steps, unless the product has no UI:

```
Two sessions remain before pages can be built, in this order:
  /logic-settle — the logic layer: cache, validation, dates, logging,
                 scheduling, audit trail. Scored from the documents; often
                 installs nothing.
  /design-settle — the visual direction: the stack and product questions,
                 a reference search, 2–4 direction frames picked on screen,
                 then every page drawn on a canvas, judged, and promoted.
Until design-settle is done, any session will refuse to write UI components.
```

`logic-settle` runs first because the pages `design-settle` promotes carry loading, empty, and failed states, and those belong to the data layer. **Do not run either now**: bootstrap installs only what an answer approved — the platform's init command, question 8's test runner — and `design-settle` installs several more behind its own gate.

Say what follows them: building runs under `build-flow`, which writes `docs/queue.md` on its first run and sets the size of one session — a new app builds its screens first, a UI batch with every page against a hand-written contract and no database behind it, then wires them in a backend batch.

Close by reminding the user that `raizen-norms` only becomes active once the next session starts in this repo.
