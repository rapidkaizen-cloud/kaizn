# design-settle

Running it settles how the app looks — a direction picked on screen from 2–4 drawn frames, then every page drawn on a canvas, approved once and promoted into the app — and it alone writes `DESIGN.md`.

| | |
|---|---|
| Kind | Settle skill — run by name; a session that finds no `DESIGN.md` points you to it instead of writing UI |
| Run | `/kaizn:design-settle`; name `fast` or `full` at invocation (`/kaizn:design-settle fast`) to skip the Fast or Full question |
| Run it when | Before the first UI component of a repo is written, and whenever you want to redesign, restyle or overhaul an app that already has a look |
| Needs first | A product with UI; not on `main`. `impeccable`, `frontend-design` and `ui-ux-pro-max` are Required: when one is absent you are asked to continue without it or stop to install. Missing documents do not stop it |
| Writes | `DESIGN.md`, `docs/decisions/` records, `CLAUDE.md`'s Component library row, the `## UI` part of `AGENTS.md`, styling and theme files, the `/design-system` route, the lint floor in the linter's config with its baseline, plus one local plugin file where the linter has no rule for a refusal, a whole `AGENTS.md` where none exists, `src/design-canvas/`, `.design-audit/`, the promoted pages, `docs/queue.md` lines and the file itself where the repo has none, the `docs/README.md` lines for `DESIGN.md` and `docs/decisions/`, the `docs/guide/` pages quoting a label the pass changed, the dependency and lock files through an approved install |
| Commits | Once, at the close, by the session norms' `GIT` block: on the pass's own branch where UI exists, on the current branch where none does. Nothing is committed before the close. Never pushes, merges or opens a PR |
| Source | `skills/design-settle/SKILL.md`, `skills/design-settle/references/` |

## What happens

Step 0 reads two facts, whether UI components exist and whether `DESIGN.md` is written, and prints a block from `Skill build` to `Flow`. **Fast or Full** changes who answers the dialogs, never which steps run.

| UI components | `DESIGN.md` | What switches on |
|---|---|---|
| none | absent | The shortest path: reading, interview, frames, canvas, ratify, promote in place, verify |
| present | absent | The audit, function and frame inventories, `Keep — today's look` as one candidate, a gate before any real page moves, the pass on its own branch |
| present | written | All of that, plus the fix-or-redesign question and the `DESIGN.md` diff at the gate |
| none | written | STOP: you are asked whether you really mean to redesign an app whose UI was removed |

When a canvas, a half-applied pass or `.design-audit/gate.md` is left over, one question follows the block: **Continue** at the step the state shows, **Start over**, or **Stop**.

1. **Step 1, the reading.** One sentence: *"I read this as [kind of app] on [platform] for [who uses it], leaning [the feel that fits], because [reason]."* You correct it, and answer Fast or Full in the same call. Nothing else runs first. Where UI exists, you are first shown the app's page groups with their page counts and asked the scope: the whole app, or the groups this run redraws. An app with one page group is not asked. Two subagents then audit the old UI before the reading, one after the other, and write `.design-audit/audit.md`, which you read, and `.design-audit/handover.md` for the drawing session. The first reads the source: a script the plugin ships counts the values outside the tokens over the whole app and writes `places.md`, and the subagent reads page files in the scope only. The second walks the running app: it opens and screenshots one route of each kind of page inside the scope and one of each kind outside it, and measures what they render with one function the plugin ships, so two audits of one app count and measure the same things. Where the app has a sign-in and the session holds no account for it, you are asked once before the audit which account walks the app. The audit also writes `.design-audit/places.md`, the file and line of every finding, which only a gate that redraws nothing reads. `audit.md` also lists the size of each component as the running app renders it — control and input heights, padding, radius, table row height, focus ring, icon size and stroke — and the contrast of each pair of colours it found. A real row copied into `handover.md` carries no personal data: names, phone numbers, e-mails, addresses and free text are replaced by invented values of the same shape.
2. **Step 2, fix or redesign.** Only where `DESIGN.md` is written. **Fix the drift** asks nothing about the look and touches only deviating components; `DESIGN.md` changes only by what its gate ratifies. **Redesign** rebuilds `DESIGN.md` from zero with the full interview; the existing values survive only as *keep* answers. Recommended: fix the drift unless the audit's indictment count is above zero.
3. **Step 3, the interview.** A full product draft, then the stack dialogs (component library with `own components` always an option, styling, icon pack, engines only on a trigger), four product calls (supported widths, theme mode, the two frame screens, copy voice), a reference search of real products with links, then a multi-select direction question. Every dialog only locks an answer; nothing is installed yet.
4. **Step 4, the install gate.** A chat stop listing `Will install:`. In Full, with nothing to install, it is one line and no stop.
5. **Step 5, the frames.** The line `Material loaded:` names every file read. 2–4 frames on two screens each are drawn as files under `src/design-canvas/`, shown at two widths in a phone frame and a window frame, and you pick one on screen. A pick carrying a change gets one refine round. The picked frame is the direction; its values are read at ratification.
6. **Step 5, the canvas.** A narrated design plan and a block of assumptions, then every page drawn in `src/design-canvas/`: production-grade code, static data, live chrome, every state drawn, one signature element. Three scans run before each round. Then the judgement call.
7. **Step 6, ratification.** Contrast pairs are computed and each value reported as a cancellable line. Where no UI exists, `DESIGN.md`, the decision records and the styling files are written here. Where UI exists, a gate shows `DESIGN.md` as a before-and-after diff, a file plan (`PASS — [n] files`), the detector's count, and what approval orders, contradicts and removes. Fix-the-drift shows `REPAIR — [n] findings` instead, with one line each for the archetype table and the proving page where `DESIGN.md` lacks them. A finding you reject there is asked once: kept on purpose, it becomes an exception line in `DESIGN.md`'s Do's and Don'ts with your reason; left for later, it stays a finding. A finding only a new value would repair — a colour of `DESIGN.md` under the floor it states, a detector hit on a font it does not name — is listed under `OWED` and asked once the same way: kept on purpose as an exception line, or left for a redesign, which is the recommendation for a value under a floor. `DESIGN.md` names the proving page — the first of the two frame screens you chose — and the one icon family, beside its tokens and rules. Under a scope narrower than the app the gate opens with what changes for the rest: the styling files and the shared chrome for every page, and each page group left out with how many of its files hold a finding.
8. **Step 7, the pass.** Foundations, chrome and shared components, pages with the proving page first, then `/design-system`, assets, removals, the lint floor and `AGENTS.md`'s `## UI` part. Each canvas file is copied to its real path; the proof is a diff, not a look. Under a narrower scope the pass first writes one `docs/queue.md` line per page group left out that holds a finding, cleared by a later run scoped to that group.
9. **Step 8 and 9, verify and close.** Each check leaves evidence; one that cannot run is reported `not verified — <reason>` and becomes a `docs/queue.md` line. Three mechanical subagents — one reading the files, one the rendered pages, one driving them — run the build, structural and pixel diffs, lint floor, contrast, detector, UX floor, keyboard flow, axe-core and reduced-motion checks; a browser tool that cannot emulate reduced motion runs a stand-in, and the check is reported as run on it. A fix that changes a page you ratified is applied without asking, listed at the close as one line you can cancel, and that page's pixel diff and keyboard walk run again. Where no canvas was drawn — fix-the-drift, or Keep — the checks that compare a page with its canvas file read `n/a — no canvas`, each repair you approved is read again at its place, and one you rejected fails no check. Under a narrower scope each route the audit opened outside it is captured again and read beside its audit screenshot: unreadable text, a collapsed layout or a missing control there is a failed item. The close block lists the numbers, files changed and each page's fate.

**Keep.** Picking `Keep — today's look` ends the drawing: the other frames are deleted and the flow continues at Step 6, as fix-the-drift where `DESIGN.md` is written and as ratification of the measured values where none exists. A Keep pick carrying a change, such as a brand colour, is a redesign. With no `DESIGN.md` you ratify only what the audit measured. The component sizes are listed one line each above one confirmation: a line you name is asked alone, and a component the app renders at more than one size is always its own question. The gate then shows `DESIGN.md` as it will be written and a `REPAIR` list of the places that depart from an answer differing from the measurement; the pass writes `DESIGN.md` first and retokens those places, and nothing is redrawn. Its contrast section is written from the pairs the audit measured, and a pair under its floor is put to you. A stack part you kept without a dialog still gets its decision record. Once the checks pass you are asked whether `.design-audit/` and the seed rows may go.

**Quarantine.** Nothing in the app imports the canvas, and the app renders identically with it deleted. The canvas is dev-only, out of navigation and out of the production build.

Where UI exists, the drawing session never sees the existing look: only the audit's two subagents open the old UI, and the blindness ends at the Step 6 gate.

## What it asks you

| Question | What your answer decides |
|---|---|
| Fast or Full, neither marked recommended | Fast answers every dialog with its recommendation and the direction question with `Decide for me`, shown as cancellable lines above the install gate — where UI exists, the direction line says that cancelling it offers `Keep — today's look`; the frames, pick and every check still run |
| The scope, where UI exists and the app has more than one page group — a chat stop, in Fast too | The whole app, or the page groups you name. Every page in scope is read, drawn, promoted and checked. With a narrower scope the tokens and the shared chrome still change for every page, the stack is kept, and each group left out becomes one `docs/queue.md` line |
| The account for the audit, where the app has a sign-in and the session holds none | Create one (recommended; a login and a role row written to your app's database), wait for one you supply, or walk signed out — every route behind the sign-in is then measured from source. Asked in Fast too |
| The reading | Whether the kind of app, platform, user and feel are right. The options are the reading as written, then the reading with one unsettled part changed |
| Stack dialogs | Library, styling, icon pack, engines. Where UI exists, an unindicted part is one cancellable `Keep —` line. A part is indicted in three cases only: a floor failed inside a package's own stylesheet (a copy-in library's files count as yours), two packages in use for one job, or an engine that paints where your styling files cannot reach. An icon pack indicted for two families offers each family alone, the one more files import recommended. Under a scope narrower than the app no part is asked: each is kept, an engine may still be added, and an indicted part is named at the close for a whole-app run |
| Four product calls | Lowest supported width, theme mode, the two frame screens, copy voice; each ends with `Decide for me` |
| The direction question | A tick is inspiration, and no tick reads as `Decide for me`. Following a reference closely only when you say so in your own words: its density, colour temperature, type and shell, never its name, mark or a screen copied element for element. Picking another frame releases it |
| The pick, then the judgement call | A frame; then approve, rework, or start the look over (none marked recommended), the feature cut (`keep all` first), hand-rolled controls, the shells |
| The signature | Keep (recommended), redraw once, or drop it and accept the quieter page |
| The gate lines (UI exists) | Approve or reject by name; removals item by item. A rejected value opens its question first; a rejected file-plan, ordered-work or deviation line is asked what stands instead. What changes the drawing is redrawn, then the gate is shown again whole with its changed lines marked |
| Font and linter install lines | The one-line package approvals outside the install gate |

Anything the skill decides beyond a dialog appears as one cancellable line with its basis, and a cancelled line opens that value as a dialog.

## Where it stops

- **Step 0.** A product without UI; branch `main`; no UI with a written `DESIGN.md`; leftover state (the question above).
- **Step 1.** The reading, before any dialog, search or frame.
- **The pick.** A single-select with the frames on screen. Rejecting the set redraws one fresh set; a second rejected set re-opens the look.
- **Chat stops**, each ending the turn until you reply: the scope, the install gate, font and linter lines, the Step 6 gate and its `REPAIR` list, the Step 8 deletion — of the canvas, or of `.design-audit/` and the seed rows where no canvas was drawn.
- **Judging.** Two correction rounds per canvas; a third does not run, and the escalation re-opens the look, not the interview.
- **Seam points.** The pass can span sessions, stopping only after Foundations, after chrome and shared components, or after a page. It writes `docs/queue.md` lines for what is left, and the next session resumes through the leftover question.
- **Two session breaks.** Once the documents are written, and again after the pass, the turn ends and asks you to run the skill again in a new session: every call re-reads the whole session, so the pass and the checks start small instead of carrying the drawing. The new session resumes through the leftover question; a reply in the same session continues there.

> [!WARNING]
> `Approve everything` at the gate never covers removals. A reply naming each ID, or a range, does. Removals you leave unnamed are shown again alone, and a clear yes to that message covers them.

## What it never does

- **Write `DESIGN.md` from existing code.** The audit produces findings; a finding becomes a line only when you ratify it. Nothing is written before its stop, and a rejection leaves every document as it was.
- **Write outside its closed list**, or create `MASTER.md` or a `design-system/` folder.
- **Install outside the install gate.** The exceptions are one-line approvals in chat: the font, and a linter in fix-the-drift.
- **Push, merge or open a PR**, or commit before the close.
- **Delete the canvas unasked.** A ratified canvas file is frozen and survives until its page's real implementation is wired and you confirm.
- **Reproduce a company's distinctive interface**, however the request is phrased.
- **Run `impeccable` commands that write `PRODUCT.md` or `DESIGN.md`**, or spawn its agents.
- **Lower a lint rule to a warning.** Existing hits are baselined, and the baseline only shrinks.
- **Report an unrun check as passed.**
- **Manufacture a change.** Keeping everything, or picking `Keep — today's look`, is a valid ending with nothing redrawn: the code changes only where you approve a repair at the gate. With no `DESIGN.md`, Keep still writes the measured values you ratify.

## Related

- [app-settle](app-settle.md) and [logic-settle](logic-settle.md), the sessions before it
- [ui-build](ui-build.md) and [build-flow](build-flow.md), the rules that bind pages after it
- [docs-format](docs-format.md), where `DESIGN.md` sits among the documents
- [Redesign](../guide/redesign.md), [starting an app](../guide/new-app.md) and [Antigravity](../guide/antigravity.md)
