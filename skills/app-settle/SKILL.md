---
name: app-settle
description: Settle an app repo at the app level, whatever state it is in — the problem domain, the stack, the documents that record them, and existing code brought back onto the installed rules. Step 0 reads the directory and decides the work. Empty — bootstrap a new app, interview, documents, scaffold, git init. Code but no documents — document it, changing nothing about the app. A root PRD.md — migrate it to the docs/ form. Documents in place — audit the repo against the rules and fix what the user picks, one finding per commit; or, when the user wants the app itself to change, rework its decisions, keep first. Use to start a new app, to document or migrate an existing one, to check whether a repo follows the current rules, or to re-plan one.
---

# app-settle — the app-level decisions, and the repo held to them

`logic-settle` decides the layer between the database and the UI, `design-settle` how the app looks. This skill decides what sits above both — what the app is for, who uses it, the rules it enforces, the stack it runs on — writes the documents holding it, `docs-format`'s closed list in the `docs/` form, and brings a repo that predates these rules or drifted from them back onto them. Documents are named by their `docs/` path; a repo with a root `PRD.md` reads each through `docs-format`'s legacy map.

**Five modes, and what Step 0 reads decides which** — the directory and the code first, the documents as evidence. There is no second skill to route to.

| Step 0 finds | Mode | Kind | What the session does |
|---|---|---|---|
| Nothing | **Bootstrap** | Decision | Interview the domain and the stack from zero, write `docs/PRD.md`, seed the living documents, scaffold, `git init` |
| Application code, no PRD in either form | **Document** | Decision | Write the documents — what code can never supply is **why any of it is the way it is**. Change nothing |
| A root `PRD.md` | **Migrate** | Mechanical | Move the legacy documents into the `docs/` form, word for word, in one commit |
| `docs/PRD.md`, and no change asked for | **Align** | Mechanical | Audit the repo against the installed rules, rank what it finds, fix what the user picks, one finding per commit |
| `docs/PRD.md`, and the user wants the app itself to change | **Rework** | Decision | The same interview, every decision starting from what the app already does |

**One session runs one mode, never a mix, in the order a repo owes them: Document, then Migrate, then Align or Rework.** A repo with no documents is documented before anything is re-decided, because re-deciding rules never written down loses behaviour.

**A mode is decision work or mechanical work, never both.** Decision work changes no existing code: every line it writes comes from an answer the user gave. Mechanical work changes what exists only where an installed rule already says how, and drops whatever turns out to need a decision.

The user is a junior developer: give a reasoned default, and **ask only what changes the shape of the repo**.

## What a run costs — four rules

- **Read a step's file when the flow reaches that step, never earlier.** The table under The steps names each one; a file for another mode, or for a branch not taken, is never read.
- **Run a step's independent reads, searches and commands in one turn** — parallel calls, or one chained command — because every extra model call re-reads the whole session.
- **Hand non-taste work to one subagent on a cheaper model than the session's** (`sonnet` on Claude Code): the repo read of D1 and R1, the audit of A1, the live verification of package candidates, the Pioneer research. Brief it with the file that rules the job and take back only the compact result that file names — its raw results never enter this session. No subagent → run it here and say so; no model choice → the session's model. **Verify a recommended package live before its question is asked; offer every other option from model knowledge, marked `unverified`, and verify it only when picked.**
- **Never re-read what the session start printed** — the documents and the two listings.

## Hard limits — every mode

**Never opened on your own initiative.** A session that trips over a finding reports it in one line and carries on. Offer this skill through **AskUserQuestion**, once, with its evidence attached — the measured finding, what it costs to leave, a recommendation; a finding too thin to state in files and counts is a report line, not an offer. Declining closes the matter for the session.

**Write only `docs-format`'s closed list.** No `SCHEMA.md`, API reference, interview summary, or audit report as a file. A document another skill produces in this session is **not committed**.

**`docs/queue.md`, `docs/changelog.md`, `docs/guide/`, and `docs/changes/` are not born here** — `build-flow` writes them in the building sessions. Two exceptions, each stated in its own file: Migrate moves a root `QUEUE.md`, and Align writes the queue lines for work it may not do itself.

**`DESIGN.md` is never written here, nor a legacy PRD's Section 5.** Bootstrap and Document leave it absent; Rework leaves it untouched even when the whole point of the rework is a new look. `design-settle` owns it, and until it exists `ui-build` blocks every component — a gate not yet opened, never a hole to fill. Copying today's CSS into it reverses `user → DESIGN.md → CSS` and makes every accident a norm. One exception: Migrate converts a ratified Section 5 into it, changing no value (`references/migrate.md`).

**Commit by the session norms' `GIT` block**: what a mode wrote is committed when it is finished, paths named.

**Do not invent.** Not settled yet → write `[needs verification]` in the document.

**No secret goes into any file, and no token is asked for**: name the variable, never its value.

**Run the domain interview alone, without third-party skills.** Another interview skill offering itself in this session (a keyword trigger, for instance) is ignored — its output would collide with the documents, which change only by the user's decision.

**N3, D4 and R4 are one message, then a STOP for explicit approval.** No file is written or edited before it is answered. A reply approving part of it writes nothing: settle the lines it rejects, then show the summary again whole, the changed lines marked.

**Bootstrap only — no `npm install` and no dependency added without the user's approval**: the N3 summary names the init command N5 runs, and question 8 the test runner.

**Document and Rework only — nothing about the app itself changes.** No dependency added, none removed, no file refactored, no migration run, no bug fixed on the way past. Decisions land in the documents; code catches up in build sessions under `build-flow`, never here.

## Step 0 — Declare

Check the working directory and the files it holds in one turn, then report one short block:

```
Directory  : [path] — [empty / N files]
Documents  : [none / root PRD.md — legacy form / docs/ form]
CLAUDE.md  : [absent / present]
AGENTS.md  : [absent / present]
Git        : [branch · N commits · clean or N uncommitted paths]  or  [not a repo]
Plugin     : [kaizn vX — the installed copy, which is what governs this repo]
Mode       : [bootstrap — empty directory]
             [document  — application code, no documents]
             [migrate   — a root PRD.md]
             [align     — documents in place, no change asked for]
             [rework    — documents in place, and the user asked for <what>]
             [seed      — docs/PRD.md in place, a living document missing: seeded, then close]
Owed after : [the modes this repo still owes once this one is done, in the order above — or "none known"]
Flow       : [bootstrap: story → reading → 6 domain themes → 9 stack questions → summary
                         → init command → docs/PRD.md → living docs → scaffold]
             [document:  read stack → story → reading → 6 themes → summary → docs/PRD.md
                         → living docs + CLAUDE.md]
             [migrate:   read → move → DESIGN.md → what names the old form → prove → commit]
             [align:     audit → rank → user picks → one finding per commit]
             [rework:    read documents + stack → drift → story → keep-first decisions
                         → summary → document edits]
```

- **What Step 0 reads decides the mode, and nothing else does**: "start fresh" in a directory full of code is never bootstrap, "fix up" an empty directory is. Report the mode with the fact that produced it; the user may overrule it in one line.
- **Read the `Plugin` row from `.claude-plugin/plugin.json`** of the plugin folder this skill is read from.
- **Align or Rework is the user's word.** A wish to change what the app does, whom it serves, or what it runs on → Rework. None stated → Align, and the block says that asking for such a change is what turns it into Rework.
- **Not empty, yet read as bootstrap** — files that are neither application code nor a PRD, a stray `README` or a `.git` and nothing else → **STOP**, ask whether to continue here or move. Overwrite nothing.
- **Branch `main` → STOP**: a session never works on `main`. No `development` branch exists → offer through AskUserQuestion to create it from `main` and switch to it.
- **Not a git repo, with code present** → say so and offer `git init`. Document continues either way; Migrate and Align **STOP** without one, because their commits are what makes them undoable.
- **Working tree dirty, before Migrate or Align → name the paths and STOP** until the user commits or stashes, because their commits must carry nobody else's uncommitted work.
- **`docs/PRD.md` present but a living document it seeds missing** → the Mode row reads `seed`, a repair no mode runs before: read `references/prd-structure.md`, seed only the missing ones as N4 does, report them, and close; any other mode waits for a later session. A missing `docs/architecture.md` or `docs/runbook.md` has no section to seed it: launch the subagent on `references/repo-read.md` as D1 does, and write the two from its block as D5 does.

Then run the mode's own rows of The steps.

## The interview — N1, D2 and D3, R2 and R3

**Open with one invitation to talk freely, never a list of questions.** Then **state your reading in one paragraph and STOP for correction**, because digging on a wrong reading yields answers that are all correct for the wrong app.

| Mode | Invite the user to say | The reading |
|---|---|---|
| Bootstrap | What problem they want solved, who uses it, why this app needs to exist now | *"I read this as [problem] experienced by [who], currently handled by [the old way], with this app replacing [which part]."* |
| Document | What problem this app solves, who uses it, what they did before it existed | *"I read this as [problem] experienced by [who], previously handled by [the old way], with this app now covering [which part]."* |
| Rework | What feels wrong, what triggered the rework, what must be true when it is over | *"I read this as [what hurts] driving changes to [which decisions], with [what] staying as it is."* |

- **A user who declines to tell the story gets the themes below as one batch of open questions**, and the reading is stated from the answers.
- **A corrected reading is restated in one line and the digging continues**; it stops for correction again only where the correction replaced the problem or the people.

**Bootstrap and Document then cover six themes, and do not continue without them** — Rework walks decisions instead (`references/rework.md`):

- The real problem before this app existed, and why that state was intolerable
- Who uses it, and how they do the work **today** without this app — in Document, how they did it **before** it
- The work each role must be able to finish, plus the limits that bind them
- Business rules **and the reason behind each number** — not just the value
- Domain terms that are easy to misread
- **Non-goals**: what is deliberately not built, and why that is a decision rather than a gap

Rules of the digging:

- **Never dig for table names, screen names, or folder structure** — they are born from the code and belong in no document.
- **Once the reading is agreed, summarize back what you captured per theme**, then ask what is still empty or ambiguous in one batch, in your own words; only a follow-up whose wording depends on an earlier answer waits for it.
- **Domain questions carry no options** — their answers cannot be enumerated, and a guess offered as a choice steers the answer. "More than two options plus a recommendation" is the rule for technical questions only.
- **Ask in that batch what no theme gathers, where the story or the repo left it out**: the app's name · what must be true for the problem to count as solved, which is `## Success` · what a user with no role or an unknown one may do, which is the closing sentence of Roles.
- **`none` is an answer for rules, terms and non-goals — write it as said.** The problem, the people and the work each role finishes cannot be none: without them, STOP.
- **Never skip the reason behind a number.** A live check finds the value in a constant or an RLS predicate and never recovers the reason. *"I don't know, it has always been that way"* is a valid answer — write it as-is, never invent or improve one.
- **Stop when the six are answered, not when the questions run out.**

## The steps — read on arrival

| Step | Read | What it runs |
|---|---|---|
| **Bootstrap** · N1 — Domain | Nothing more | The interview above |
| N2 — Stack, nine questions | `references/stack-questions.md` and `references/stack-consequences.md`, in one turn. `references/pioneer.md` only on a Pioneer answer, or a platform typed from outside the list | The questions in batches, then the derived lines and the defaults not asked |
| N3 — Summary, then STOP | Nothing more | One message: app name · Surface/Data/Deploy · roles · key business rules · domain terms · non-goals · stack decisions · rejected alternatives with their reasons · the init command N5 runs |
| N4 — Write `docs/PRD.md`, then seed the living documents · N5 — Scaffold · N6 — Close | After the approval, in one turn: `references/prd-structure.md` (N4) and `references/scaffold.md` (N5, N6) | The platform's init command, the frozen PRD and what it seeds, the repo files, `git init`, the bootstrap commit, the close block |
| **Document** · D1 to D6 | `references/document.md`, in the turn that launches D1's subagent on `references/repo-read.md`. After D4's approval, in one turn: `references/prd-structure.md` and `references/scaffold.md` | The stack read from the repo, the interview above, the summary and its STOP, the documents, the close block |
| **Migrate** · M1 to M5 | `references/migrate.md`, which names what each of its steps reads | The read and its block, the move, `DESIGN.md`, the files naming the old form, the proof, one commit, the close block |
| **Align** · A1 to A5 | `references/align.md`, in the turn that launches A1's subagent on `references/audit.md` — never read here | The audit, the ranked table and its STOP, one finding per commit, the close block |
| **Rework** · R1 to R6 | `references/rework.md`, in the turn that launches R1's subagent on `references/repo-read.md`. `references/stack-questions.md` and `references/stack-consequences.md` only when a stack decision opens | The drift, the interview above, keep-first decisions, the summary and its STOP, the document edits, the close block |
