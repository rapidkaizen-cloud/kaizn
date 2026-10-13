# app-settle

Running it settles an app repo at the app level — what the app is for, who uses it, the rules it enforces, the stack it runs on — writes the documents that hold it, and brings an existing repo back onto the installed rules.

| | |
|---|---|
| Kind | Settle skill — runs only when you invoke it |
| Run | `/raizen-norms:app-settle` |
| Run it when | You start an app, document or migrate an existing one, check whether a repo follows the current rules, or want to re-plan one |
| Needs first | Nothing in an empty directory. Migrate and Align need a git repo with a clean working tree. A session never works on `main` |
| Writes | By mode: `docs/PRD.md` and the living documents it seeds, `CLAUDE.md`, `AGENTS.md`, `.claude/settings.json`, the root `README.md`. Align also changes existing code and agent files |
| Commits | Yes, by the `GIT` block of the session norms, paths named, when a mode has finished writing. Align makes one commit per finding |
| Source | `skills/app-settle/SKILL.md`, `skills/app-settle/references/` |

## What happens

Step 0 reads the directory and the code first, the documents as evidence. It prints one block — `Directory`, `Documents`, `CLAUDE.md`, `AGENTS.md`, `Git`, `Plugin`, `Mode`, `Owed after`, `Flow` — and names the fact that produced the mode. You can overrule the mode in one line. Under another plugin's brevity mode a session may skip this block where it does not end the turn — observed in migrate and document — and print only the closing block, so the mode is not always named before the work starts.

| Step 0 finds | Mode | Kind | What it does |
|---|---|---|---|
| Nothing | **Bootstrap** | Decision | Interviews the domain and the stack from zero, writes `docs/PRD.md`, seeds the living documents, scaffolds, runs `git init` |
| Application code, no PRD in either form | **Document** | Decision | Writes the documents; changes nothing about the app |
| A root `PRD.md` | **Migrate** | Mechanical | Moves the legacy documents into the `docs/` form, word for word, in one commit |
| `docs/PRD.md`, no change asked for | **Align** | Mechanical | Audits the repo against the installed rules, ranks the findings, fixes the ones you pick |
| `docs/PRD.md`, you want the app itself to change | **Rework** | Decision | Re-runs the interview, every decision starting from what the app already does |

One session runs one mode, in the order a repo owes them: Document, then Migrate, then Align or Rework. Decision work changes no existing code; every line it writes comes from one of your answers. Mechanical work changes what exists only where an installed rule already says how, and drops whatever turns out to need a decision. A `docs/PRD.md` with a living document missing gets only those documents seeded and reported, and the run closes.

### Bootstrap — N1 to N6

1. **N1, the domain.** One invitation to talk freely, then a one-paragraph reading and a stop for your correction. Then six themes, asked openly with no options: the problem before the app, who uses it and how they work without the app, the work each role must finish, business rules **and the reason behind each number**, domain terms easy to misread, non-goals. The same batch asks what no theme gathers, where your story left it out: the app's name, what must be true for the problem to count as solved, and what a user with no role may do. `none` is an answer for rules, terms and non-goals. If you would rather not tell the story, the themes come as one batch of open questions.
2. **N2, the stack.** Nine questions, up to four per call: kind of app, platform, framework and rendering, frontend hosting, database and login, which database, database environments, testing, and help for the app's users — none, guide pages in the repo, or a help page inside the app. Each option carries a one-sentence consequence, and each question a marked recommendation except frontend hosting and which database, which carry none. Supabase is offered as two options, Cloud and self-hosted. A question left with one option that fits is reported as a derived line instead. Then the derived lines (language, package manager, migrations, styling) and the defaults not asked, in one message for you to change — except the two branch names and English as the code language, which are shown and not re-opened. The component library is not asked here; `design-settle` asks it.
3. **N3, the summary.** One message, then a stop for your approval. It names the init command N5 will run, so approving the summary approves that command. Approving part of it writes nothing: the lines you reject are settled, then the summary is shown again whole.
4. **N4, `docs/PRD.md`.** Frozen from the moment it is written. It seeds `docs/product.md`, `docs/rules.md`, `docs/glossary.md` and one record per answered stack question in `docs/decisions/`. `docs/architecture.md` and `docs/runbook.md` are written from the stack answers, with `[needs verification]` where nothing has run yet. Then `docs/README.md` and the root `README.md`.
5. **N5, scaffold.** The app's skeleton comes from the platform's own init command — the framework's official scaffolder — run first, before the documents are written, because a scaffolder refuses a directory that is not empty; a `README.md`, `CLAUDE.md` or `AGENTS.md` it shipped is replaced. Then `CLAUDE.md`, `AGENTS.md`, `.claude/settings.json`; a host rewrite rule for a static SPA only; a CI workflow only if you ask. Every file is written for your answers, never copied. Then `git init`, `git branch -M main`, the one commit `main` ever takes directly, and `development` created and switched to.
6. **N6, close.** The files created, and what you must do by hand: create the database project (and its staging counterpart if question 7 asked for one) and connect it. It says plainly when there is no staging. It offers `/logic-settle`, then `/design-settle`, unless the product has no UI. `raizen-norms` becomes active once the next session starts in this repo.

**Pioneer and Not ready.** A Pioneer option opens with `Pioneer —` and what does not exist for it yet. Picking one, or typing a platform outside the list, adds three lines — no rubric row, no repo that has run it, what the destructive guard covers — and one confirmation; declining routes back to a Ready platform (`references/pioneer.md`). A Not ready option is never offered, but one you name is accepted with what you must set up yourself. A non-SQL store first gets a notice that the destructive guard does not cover it, then a question whether to proceed.

### Document — D1 to D6

1. **D1.** A subagent reads the stack from the repo into a `STACK` block. What it could read is not asked; a row that came out `not readable` is asked later, only where it changes what the documents must say.
2. **D2 and D3.** The story and reading as above; the reading says which parts drew on the code. Roles, rule values and terms read from code are shown with their `file:line` and confirmed. The problem before the app, how the work was done then, and the non-goals are asked openly. The locale is confirmed. A correction that contradicts a measurement is written by what it states — what the app is meant to do as you said it, what exists as measured — and the other side is a `Findings` line.
3. **D4.** The summary, then a stop. **D5.** `docs/PRD.md`, the living documents, `CLAUDE.md`, `AGENTS.md`, `.claude/settings.json`, then a commit. The stack is recorded as found and no decision record is seeded. An existing `CLAUDE.md`, `AGENTS.md` or root `README.md` is never overwritten. Where `CLAUDE.md` imports `AGENTS.md`, as a framework's template ships it, you are asked once whether the import line goes.
4. **D6.** A block — `Written`, `Not read`, `Unverified`, `Findings`, `DESIGN.md` — then `/logic-settle`, `/design-settle` and `/app-settle` in that order. `Findings` holds concrete stack findings and those corrections; "you would have picked differently" is not one.

### Migrate — M1 to M5

1. **M1.** Reads, prints a `MIGRATE` block of counts, and says whether the repo can move. An off-shape `PRD.md`, or a Section 5 of the adopted-whole shape, cannot: it names the blocker and what clears it, changes nothing, and offers Align or Rework.
2. **M2 and M3.** `git mv` of `PRD.md` and `QUEUE.md` into `docs/`, one `Frozen` line under the PRD's title, then the living documents written from it. `DESIGN.md` is written from Section 5 as a change of format, never of design; with Section 5 empty, absent or all `[needs verification]`, none is written.
3. **M4.** Corrects what still names the old form, in `CLAUDE.md`, `AGENTS.md`, `README.md` and other files, and writes `docs/README.md` last.
4. **M5.** Proves the counts, the rule-test titles, the linter and the session start, then makes one commit and prints `MIGRATED`. `git revert` undoes it.

### Align — A1 to A5

1. **A1.** One subagent audits the repo against the installed plugin copy and returns an `AUDIT` block: `C1 platform residue`, `C2 agent files`, `C3 language split`, `C4 guard coverage`, `C5 documents`, `C6 lint floor`, `C7 rule coverage`. Six rows run; `C3 language split` prints `not run`, because it reads every name in the repo and rarely finds more than untidiness. Every row that ran reports, a clean one included. A norm in `CLAUDE.md` that the plugin prints is listed with the plugin line that prints it, and counts as a copy only where that line covers every case the file's line covers; one the plugin prints nowhere, or only for one mode or one layer, is counted apart, stays in the file, and is reported on the `For app-eval` row. Every skill and command name in the file is checked against the plugin's skills.
2. **A2 and A3.** A table ranked by what breaks without anyone noticing, in three bands: a guarantee that does not hold, a rule that points somewhere wrong, drift that is merely untidy. You pick through a question: band 1 only, bands 1 and 2, everything, or nothing. A second question in the same call offers `C3`: audit the language split too, or skip it. With no finding in the first run, that question is asked alone. Picked, it is audited and its findings are put to you the same way.
3. **A4.** One finding per commit, named paths. A build or run config gets one real run first; a lint floor is proven before its commit. Where several findings you picked are destructive — renames, mostly — their `DESTRUCTIVE` blocks are shown at one stop before the first finding starts, and each one you approve still runs and commits on its own.
4. **A5.** An `ALIGN` block: `Fixed`, `Dropped`, `Left`, `Not audited`, `Still silent`, `Verified`, `For app-eval`. An empty audit is a normal ending.

### Rework — R1 to R6

1. **R1 and R2.** A subagent reads the stack and returns a `DRIFT` block; then what hurts, and a reading you correct. A rework touching only the design system closes and points to `design-settle`.
2. **R3.** Only the decisions the story touched, plus those their change forces open. Each shows what the app does today, with `keep` as the first option at no cost; a domain question shows the current value and asks openly for the changed value. The stack is on trial here.
3. **R4 to R6.** A summary and a stop, then edits to the sections touched, then a block of `Changed`, `Kept`, `Drift`, `Execution`, `Unverified`, `DESIGN.md`. The execution is named, never started.

## What it asks you

| Question | What your answer decides |
|---|---|
| The mode, when Step 0 reads it wrong | One line overrules it |
| Align or Rework — never asked, read from what you said | A wish to change what the app does, whom it serves or what it runs on makes it Rework; none stated, Align, and the block says so |
| Continue here or move | Whether bootstrap runs in a directory holding files that are neither code nor a PRD |
| Create `development` from `main`; `git init` | Where the session works; Migrate and Align need a repo |
| The six themes | The documents' content; no options, because options would steer the answer |
| Remove the `AGENTS.md` import from `CLAUDE.md` (Document) | Removed (recommended), Claude Code reads the norms from the plugin alone. Kept, `AGENTS.md` loads in every session and its opening line no longer says Claude Code does not read it |
| The nine stack questions | The stack, and whether the app keeps help for its users, with `docs/decisions/` records of each choice |
| Which bands to fix (Align) | What gets one commit each |
| Audit the language split too (Align) | Whether `C3` runs. Skipped, a name written in the UI language stays unreported, and the close block says `Not audited` |
| Keep or change, per decision (Rework) | What the documents record; a changed number needs a reason of its own |

## Where it stops

- **Step 0.** Files that are neither code nor a PRD in a directory read as bootstrap; branch `main`; no git repo before Migrate or Align; a dirty working tree before Migrate or Align (until you commit or stash).
- **The reading.** After N1, D2 or R2, until you correct or confirm it.
- **The summary.** N3, D4 and R4 are one message each. No file is written until you approve.
- **Align's ranked table.** Until you pick, including "nothing".
- **Align's destructive findings.** One [destructive stop](../concepts/gates.md) for all of them, before the first finding starts.

## What it never does

- **Open on its own initiative.** A session that finds a problem reports it in one line, or offers this skill once with the evidence. Declining closes the matter for that session.
- **Write outside `docs-format`'s closed list.** No `SCHEMA.md`, API reference, interview summary or audit report as a file. `docs/queue.md`, `docs/changelog.md`, `docs/guide/` and `docs/changes/` are written by building sessions; Migrate moves a root `QUEUE.md` and Align writes queue lines.
- **Write `DESIGN.md`** apart from Migrate's conversion of Section 5. It stays absent after Bootstrap and Document and untouched after Rework.
- **Invent.** An unsettled point is written `[needs verification]`. "I don't know" to a reason is written as given.
- **Put a secret in a file**, or ask for a token: it names the variable.
- **Change the app in Document or Rework.** No dependency, refactor, migration or bug fix; code catches up in building sessions. Bootstrap adds no dependency without your approval.
- **Re-open a decision in Align**, or edit a frozen record. A finding that needs a decision is dropped and reported.

## Related

- [logic-settle](logic-settle.md) and [design-settle](design-settle.md), the next two sessions
- [Documents](../concepts/documents.md) and [docs-format](docs-format.md), what gets written
- [Session norms](../concepts/session-norms.md), the `GIT` block
- [Starting an app](../guide/new-app.md), [existing app](../guide/existing-app.md), [maintain app repos](../guide/maintain-app-repos.md)
