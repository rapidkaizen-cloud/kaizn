---
name: design-settle
description: Settle the visual direction and component library of an app, with or without existing UI — non-visual dialogs, a search for real products, 2-4 direction frames picked on screen, then a canvas of every page in production-grade code, approved once and promoted into the app. Existing UI is audited first and today's look is one candidate; a written DESIGN.md adds the offer to fix only the drift. Fast or Full changes only who answers the dialogs. Use before the first UI component of a repo is written, and whenever the user wants to redesign, restyle, or overhaul the look of an app that already has one.
---

# design-settle — the visual direction, from nothing or from what exists

`app-settle` writes the documents, `logic-settle` the layer under the UI. This skill decides how the app looks, and it alone writes **`DESIGN.md`**. Documents are named by their `docs/` path; a repo with a root `PRD.md` reads each through `docs-format`'s legacy map.

**One path, two facts.** Step 0 reads whether **UI components exist** and whether **`DESIGN.md` is written**. Fast or Full changes who answers the dialogs, never which steps run.

| UI components | `DESIGN.md` | What switches on |
|---|---|---|
| none | absent | The shortest path: reading → interview → frames → canvas → ratify → promote in place → verify |
| present | absent | The scope, the audit, the function and frame inventories, `Keep — today's look` as one candidate, the gate before any real page moves, the pass on its own branch, parity checks |
| present | written | All of the above, plus the fix-or-redesign question before the interview and the `DESIGN.md` diff at the gate |
| none | written | STOP — ask whether the user really means to redesign an app whose UI was removed, and treat the answer as the row above |

A rule marked *UI exists* or *`DESIGN.md` written* runs only under that fact; an unmarked one runs on every repo.

## What a run costs — five rules

- **Read a step's file when the flow reaches that step, never earlier.** The table under Step 2 names each one; a file for a switch that is off is never read, and a section named from another step is read alone, by its heading.
- **Run a step's independent reads, searches and commands in one turn** — parallel calls, or one chained command — because every extra model call re-reads the whole session.
- **Hand non-taste work to one subagent on a cheaper model than the session's** (`sonnet` on Claude Code): the stack verification, the reference search, the platform research — the audit in the two Step 1 names, and Step 8's mechanical checks in the three `verify.md` names. Brief it with the file that rules the job and take back only the compact result that file names — its raw results never enter this session. No subagent → run it here and say so; no model choice → the session's model.
- **Never re-read what the session start printed** — the documents and the two listings.
- **End the turn at two seams and tell the user to run this skill again in a new session**, because every later call would re-read the drawing, then the pass: once the documents are written — after Step 6 where no UI exists, after the pass's first act where it does — and after the pass's last point, before Step 8. First write `.design-audit/resume.md`: what the steps ahead need and the repo does not show — the path taken, the scope, the account held, every line answered or cancelled, the canvas rounds, what Step 9's block owes from the steps behind. A reply in the same session continues there.

## Hard limits

**The confirmed reading is the precondition, not the documents.** Missing documents, or an off-shape legacy `PRD.md`, do not stop this skill; nothing is asked about the look and nothing is drawn until the user confirms the Step 1 reading.

**`DESIGN.md` is never written from existing code.** The audit produces findings; a finding becomes a line only once the user ratifies it, line by line.

**`DESIGN.md` and the decision records are written once, never before their stop** — at Step 6 where no UI exists; where UI exists, after the gate approves, as the pass's first act on its own branch. No draft stands in for them, and a rejected gate leaves every document as it was.

**Decisions are written in four places and no fifth:** `DESIGN.md` (`references/design-md.md`), with any sidecar `impeccable`'s schema puts beside it — in a legacy repo, Section 5 and the `DESIGN.md` generated from it · `docs/decisions/`, one record per stack part settled (`ratify.md`) — none in a legacy repo · the Component library row of `CLAUDE.md` when the library answer is not *keep* or the row names none · the `## UI` part of `AGENTS.md` — paths and a command, never a value.

**Every other write is on this closed list and records no decision:** the styling files and the library's theme file · the `/design-system` route · the linter config, the one local plugin file it loads (`pass.md`, The lint floor) and its suppression baseline · a whole `AGENTS.md` where none exists · `docs/queue.md` lines, and the file where none exists — to the shape `build-flow`'s `references/new-queue.md` gives an app that never split its work, with no approval stop, because the gate and the close show its lines · the `docs/README.md` line for `DESIGN.md`, and for `docs/decisions/` where the folder is new · the `docs/guide/` pages quoting a label the pass changed · the dependency and lock files, through an approved install · everything under `src/design-canvas/` and `.design-audit/` · the files the pass writes — the approved file plan where UI exists, the promoted pages, contracts and routes where none does. Anything else is a finding. Never create `MASTER.md` or the `design-system/` folder `ui-ux-pro-max` persists, a staging document, or a `DESIGN.md` written from code. A document another skill produces in this session is neither committed nor referenced.

**The canvas is the final front-end, staged**: production-grade files that promotion relocates, differing from the live page only in data. The canvas phase only adds files under `src/design-canvas/`, which no other session touches; where UI exists the pass runs isolated on its own branch or worktree, otherwise in place.

**Blindness — where UI exists, the current design is not an input, and `DESIGN.md`'s prose is the current design.** Its visual-direction prose, signature, ornament rules, and archetype shell column are not constraints; a signature is redrawn only because the new direction earns it, tagged. The audit's numbers price the pass and power the before/after, never anchor the direction. **It is enforced by distance**: only the audit's subagents open the old UI; the drawing session works from `.design-audit/handover.md` and the answers, opens no file of the app beyond `docs/product.md`, `docs/rules.md`, `docs/glossary.md`, `CLAUDE.md`, and the data-layer files `handover.md` names, and never reads the dependency file. **The one exception is a value the user chose to keep**: that value alone is read from the styling files. A value meets the one it replaces only at the Step 6 gate, where the blindness ends.

**Keeping everything is a valid ending.** All *keep*, `Keep — today's look`, or a revert redraws nothing: the code changes only by a repair approved at the gate, and `DESIGN.md` only by what that gate ratifies — a Keep that finds none writes it whole, from the ratified measured values, as the pass's first act (`gate.md`). Say so, report the findings, manufacture no change.

**A code-minimizing session mode governs the how, never the what.** Write every file lean, but never remove what this skill requests: the full product draft with its proposals tagged, every state drawn, the fixtures file that closes, the two-layer palette and the component-token table, the `/design-system` route, the compare page, the signature, and every engine or library approved at the install gate, used where it covers the job.

**Commit once, at the close, by the session norms' `GIT` block** — on the pass's branch where UI exists, on the current branch where none does (`verify.md`, Step 9). Nothing is committed before it, so a pass stopped at a seam leaves its tree dirty. Never push, merge, or open a PR.

**What the session does not know with confidence is researched with WebSearch at the step that needs it, source named** — platform guidelines, a package's current API or version, a product's current screens, a standard's wording — never recalled, never written into this toolkit. Load a search tool the harness defers before use: unavailable means the load itself failed, never that the name was absent from the tool list. Unavailable → say so and mark the finding unverified.

**Not decided by the user → `[needs verification]`.**

**Every question goes through AskUserQuestion, never prose**, in auto mode too — recommendation first and marked "(Recommended)", each option's consequence in its description, everything needed inside the dialog, up to four per call, every label in the words the user uses and never this skill's (*ratify*, *seam*, *archetype*, *departure*, *escalate*). Two questions mark no recommendation: Fast or Full, and the verdict on a round — the session does not grade its own drawing. The chat stops are the exceptions, each ending the turn and waiting for a reply: the scope (Step 1), the install gate, the one-line package approvals (font, linter), the Step 6 gate and its REPAIR list, the Step 8 deletion.

**Nothing the user did not choose is silent**: every value decided beyond the picked frame surfaces as one cancellable line with its basis (`interview.md`, What the designer settles).

## Fast or Full

**Ask Fast or Full on every repo, as a second question in the reading's call, with neither option marked recommended.** Skip it when the user named one at invocation (`/design-settle fast`); ask it again in a resumed session's re-entry call. Full runs every step as written. Fast changes who answers, never what is decided, drawn, or checked:

- **Answer every dialog with its recommendation** — the stack, the four product calls, the triggered engines, the archetype grouping — **and the direction question with `Decide for me` alone**, because its recommended direction is one tick, never a set. Compose and verify only the recommendation; the other options are composed when its line is cancelled.
- **Where UI exists, still ask a stack dialog whose recommendation is not *keep***, because a replaced library or styling rewrites every component.
- **Put Step 2's question in the reading's call where Fast was named at invocation**; chosen in that call, ask it alone in the next one.
- **Show every pre-answer as one cancellable line with its basis, above the install gate's lines, in the same chat stop** — held even when nothing installs. A cancelled line opens that dialog alone, several cancelled in one reply in one call; every line that read its answer — the styling, the icon pack and the install lines after a cancelled library — is answered again from the new one, then the block is shown again.
- **Where UI exists, say in the direction line that cancelling it offers `Keep — today's look`**, because Fast never asks the question that names it.
- **Ask the canvas judgement in one call: the verdict and the signature question.** Print the features, assumptions, hand-rolled controls, shells, and departures above it as cancellable lines. A line is cancelled by naming it under the verdict's Other or in chat; it then opens the question Full asks for it (`canvas.md`, Judging), several in one call, and the verdict is asked again after.
- **Fix a failing contrast pair to the nearest step that passes**, reported as a floor-forced line (`interview.md`, What the designer settles).
- **Where UI exists, put the font's install line in the Step 6 gate.**

Fast skips no step: the search, the frames and the pick, every scan and floor, the gate's removals, and every Step 8 check run as in Full.

## Step 0 — Preconditions

```
Skill build     : [kaizn x.y.z — read from this plugin's own .claude-plugin/plugin.json]
Documents       : [docs/ form / legacy PRD.md / legacy PRD.md, off-shape / none]
DESIGN.md       : [written / absent / product without UI — written or absent from its presence
                   alone; product without UI from the Surface row naming a CLI or a service
                   nobody looks at, never from `DESIGN.md` being absent; in a legacy repo from
                   Section 5's heading and `[needs verification]` markers, never from its
                   prose: that is the old look]
UI components   : [file count — 0 on a repo with no UI]
Scope           : [the whole app / the page groups named, n pages of n — settled before the
                   audit where UI exists (Step 1); in a resumed session from
                   .design-audit/resume.md; `whole app` on a repo with no UI]
Kind of app     : [from docs/product.md, else read from the code, else asked at Step 1 — a label, never a branch]
Register        : [first visit / tenth use / both, per page group — from the Roles, else from the routes]
Platform        : [from the Surface row, else from the manifest and platform files — web, or the
                   platform found; a non-web value routes every browser-named check to that
                   Surface's Proof profile line, or to the platform's own tooling where none is written]
Primary role    : [from the Roles, else from the roles the code enforces, else asked at Step 1]
Design material : [impeccable · frontend-design · ui-ux-pro-max present/absent — Required ·
                   review-animations present/absent, found on disk per ui-build, never from
                   the skill list — Optional.
                   Presence only: read from Step 5, ui-ux-pro-max from Step 3]
Logic layer     : [settled — CLAUDE.md carries a Data layer row / not settled]
Branch          : [name · clean or has uncommitted changes]
Leftover        : [none / canvas alive / pass partly applied / pass applied — from
                   src/design-canvas/, .design-audit/gate.md and git state]
Switches        : [UI exists: yes/no · DESIGN.md written: yes/no]
Answers         : [Fast / Full — named at invocation, else asked in the reading's call]
Reading         : [one sentence — see Step 1]
Flow            : reading + Fast or Full (+ scope, then audit in two subagents, where UI exists)
                  → fix or redesign (where DESIGN.md written)
                  → non-visual dialogs, answers locked → reference search → direction question
                  → install gate → material loaded → 2–4 direction frames → pick → refine
                  → design plan → canvas rounds → ratify (+ gate where UI exists)
                  → pass → verify → close
```

**Print the block on every invocation**, before any work beyond the reads that fill it — one turn of parallel reads. A Required `Design material` absence is asked right after the block (Step 1); a stale `Skill build` is shown, not blocked on.

**Re-entry is a gate, never an inference.** When `Leftover` is not `none`, one mandatory AskUserQuestion follows the block, before any other work, however obvious the state looks:

- **Continue** — resume at the step the state shows, reading `.design-audit/resume.md` where it stands, then that step's file: pass applied but unverified → Step 8; pass partly applied → Step 7 at the next seam point, `.design-audit/gate.md` read first where UI exists; canvas ratified but not promoted → Step 7; canvas mid-rounds → Step 5; frames drawn but not picked → the pick. Announce the resumed step and what remains before touching anything.
- **Start over** — the full path from Step 1. The leftover canvas is an audit finding; its deletion is proposed at Step 8's chat stop, never assumed.
- **Stop** — report the detected state in one block and close.

Documents missing, or a legacy `PRD.md` off-shape → **not a stop**: say so in the block, read around it as Step 1 describes, and name at the close what `app-settle` still owes. Product without UI → **STOP**, this skill does not apply. Branch `main` → **STOP**. Working tree not clean, where UI exists → name the dirty paths in one line and carry on, noting uncommitted work will not reach the pass's branch until committed.

## Step 1 — The reading, and the audit where UI exists

**Sources, in rank: the user, then the code, then the documents.** An explicit user statement outranks everything. Where the user was silent, read what exists from the code — router for pages, manifest and platform files for the platform, auth and guard code for roles, rendered strings for the locale, dependency file for the stack; where UI exists, through `.design-audit/handover.md` and never the files themselves (Blindness) — then `docs/product.md` where readable. A gap all three leave is named inside the reading and settled at its correction, never as its own question. **A conflict is a finding named in the reading, never a silent pick**: a user statement against the code is followed and reported; between code and documents, the code wins on what exists, the documents on what ought to be, and the loser is reported.

**The reading** is one sentence, your own conclusion before asking anything: *"I read this as [kind of app] on [platform] for [who uses it], leaning [the feel that fits], because [reason from the documents]."* The platform slot is mandatory — taken from the Surface row where it holds one, otherwise read from the code and confirmed inside the reading.

**Ask for correction through AskUserQuestion, the full sentence inside the question field itself**, Fast or Full in the same call. Its options are the reading as written, first and recommended, then up to three others, each the reading with one slot changed — a slot the sources left open or in conflict first, else the one the reading rests on least; any other correction arrives under Other. Nothing after this runs before it is answered: no dialog, no search, no frame.

**One Required skill absent is asked through AskUserQuestion, never merely reported**, naming what is lost — `impeccable`'s ban list, display-face and convergence calibrations, the Operate register, every later detector count; `frontend-design`'s direction method and restraint; `ui-ux-pro-max`'s UX floor, every later UX-floor check, and its frame ingredients — with continue-without or stop-to-install (the README's install lines); continuing is recommended where installing is unavailable here. The answer rides every canvas round and the ratification report as its own line. An Optional skill absent is only shown in the row.

### The audit — where UI exists

**Run it before the reading is put for correction, in two subagents, one after the other**, because a walk run by the subagent that read the source re-reads all of it on every call: the first reads the source, its whole brief `references/audit.md`; the second walks the running app, its whole brief `references/audit-walk.md`. Hand each its file's path, the repo root and the scope — the first also the page-group list, the second the account that signs in — and never read either file here. **The session that draws never opens the old UI** (Hard limits, Blindness).

- **Settle the scope before the launch.** List the app's page groups — the top folders its page files sit in, a module package as one — each with its page count, by one command that prints names and counts and nothing of a file. One group → the scope is the whole app, not asked. More → print the list with its total and end the turn on it, a chat stop, in Fast too: the stop says that every page in scope is read, drawn, promoted and checked, and the reply names the groups this run redraws, or the whole app. **From here on `every page`, `every route` and `the whole app` mean the scope and the chrome its pages share, in every file of this skill.** What still reaches the whole app is named where it stands: the audit's counts and its walk outside the scope (`audit.md`), the stack (`interview.md`), the gate's first lines (`gate.md`), the queue lines (`pass.md`), Step 8's captures outside the scope (`verify.md`).
- **Settle the account before the launch, where the app signs its users in.** An account for this app that the session's own instructions carry is handed over. None → ask once, in Fast too: create one under `db-ops` (`references/agent-account.md`), recommended — a login and a role row written to the app's database, its sign-in proven by the audit's walk and never here · wait for one the user supplies · walk signed out, every route behind the sign-in then measured `from source`.
- **Their reports carry only counts, names and paths, never a word on the look**: what prices the pass, the pages holding too little, any logic-layer bleeding, what it indicts — in `DESIGN.md` where it is written, in the stack — whether the running app was walked, the path of `.design-audit/audit.md`, and the screenshot paths. The user reads `audit.md` now; this session opens it only at Step 6.
- **`Components affected` sizes the pass**; show it before the user decides anything.
- **What the subagents cannot do runs here, after their reports and the confirmed reading**: the archetype grouping's ratify-or-correct (`interview.md`, The archetype table) — where `DESIGN.md` is written and carries no archetype table, that absence is a finding — then the `logic-settle` offer for logic-layer bleeding, under that skill's rule — only where Step 0's Logic layer row reads `not settled`; bleeding that skill already priced and baselined is a report line. Declined → continue. Accepted → close here, run `logic-settle` in its own session, then `design-settle` from Step 0, because its pass reads every page and would end this session's blindness.
- **No subagent available → say so, run both here from those files, and report the redesign as drawn with the old UI in context.**
- **App could not be run, or no credentials → say so here and at Step 6**, whose removals group then opens `no route walked — every part read from source`.

## Step 2 — Fix, or redesign — where `DESIGN.md` is written

No `DESIGN.md` → not asked; continue at Step 3. Otherwise one question, two options, with a recommendation:

| Choice | What changes | Questions asked | Components touched |
|---|---|---|---|
| **Fix the drift** | No new norm — code is brought back in line with the existing `DESIGN.md`, or a departure kept on purpose is ratified as its exception | None about the look | Only the deviating ones |
| **Redesign** | **`DESIGN.md` is rebuilt from zero** — every line re-decided, archetype shells and visual-direction prose included; today's values survive only as *keep* answers. The app looks redesigned afterwards, not retuned | The full interview, *keep* first on the stack and `Keep — today's look` among the directions; the gate names the value each replaces | Every page, replaced by its canvas file |

Offer no third, narrower option: the change is narrowed by *keep* answers, which every decision carries, and the pages by the scope (Step 1).

**Recommendation:** fix the drift unless the audit's indictment count is above zero.

**Consequence, said in the question:** the affected-component count · a redesign re-opens the component library — a dialog where the audit indicts it, a cancellable `Keep` line where it does not — and a non-*keep* library answer rewrites every component and revokes `CLAUDE.md`'s stack lock · the app looks different afterwards · picking `Keep — today's look` at the frames turns a redesign into fix-the-drift · the pages holding too little, by name — drawn whole in a redesign, handed to `build-flow` Section 4 as one `docs/queue.md` line each in fix-the-drift.

Fix the drift → straight to `references/gate.md`, whose REPAIR list shows the findings, then the pass. `DESIGN.md` changes only by what that gate ratifies at repair scale.

## Steps 3 to 9 — one file each, read on arrival

| Step | Read | What it runs |
|---|---|---|
| 3 — The interview · 4 — The install gate | `references/interview.md` | The stack and four product calls that only lock answers, the reference search, the direction question, then the one install block. Nothing is installed while it runs |
| 5, first half — The frames | `references/frames.md` | The material loaded, 2–4 direction frames on two screens, the pick on screen, one refine round. No value of the look is asked after the pick |
| 5, after the pick — The canvas | `references/canvas.md`, and the five-rules section of `references/ratify.md` | The design plan, every page drawn in production-grade code, the three scans, the judgement of what was drawn — two correction rounds, then the look re-opens |
| 6 — Ratification | `references/ratify.md`, and `references/gate.md` where UI exists | `DESIGN.md`, the decision records, the styling files — and the single stop that authorizes changing existing UI |
| 7 — The pass | `references/pass.md` | Every canvas page promoted, in a fixed order, then `/design-system` and the lint floor, across sessions where it must |
| 8 — Verification · 9 — Close | `references/verify.md` | Every check with its evidence, the canvas deletion proposal, the closing block |

The archetype table, the `/design-system` route and real running pages are produced whatever was picked.
