# The pass — Step 7: every page, across sessions where it must

**The approved canvas is the specification.** Drawn elements land as drawn; undrawn ones, and prose it left out, do not. A difference the session would prefer is refused, not asked. A page handed to an agent outside this session is briefed and reviewed by `build-flow`'s `references/delegate.md`. **The UI code is the pass's to rewrite — the behavior is not**: queries and mutations, guards, route paths, and every action's outcome stay unchanged, except the work the gate ordered. No unrelated fixes.

## Before the first file moves

**Where no UI exists, no branch**; the pass runs in place.

**Where UI exists, branch first** — its own branch or worktree from a committed base (`design/rework-<date>` or the user's naming), the untracked canvas folder and `.design-audit/` brought along. Dropping the branch reverts everything, at the user's word, closing at Step 9.

- **First act: write `DESIGN.md`** in full — in fix-the-drift only the lines its gate ratified — and the decision records (`ratify.md`, What is written), then `CLAUDE.md`'s Component library row if the library changed or the row names none — the only moment any of them is written. **Save the gate block as `.design-audit/gate.md`** — the `DESIGN.md` diff, file plan, ordered work, answered deviations — read on every resume, and the body of the close's commit. **Under a scope narrower than the app, write one `docs/queue.md` line per page group outside it that `places.md` names a file of** — the group and its page count · `not redrawn` · how many of its files hold a value outside `DESIGN.md` — cleared by a later run scoped to that group.
- **Second act: the freshness check.** Re-walk the function inventory against current code; a flow changed since ratification is a new deviation line put to the user **before** its page moves.

**The pass may span sessions, stopping only at a seam point** — after its first act, after Foundations, after chrome and shared components, after any page. **Nothing is committed on the way**: a session stopping at a seam first writes Step 9's `docs/queue.md` lines for what is left, and the next session resumes from the working tree through Step 0's re-entry gate.

## The fixed order — all canvas pages in one pass, element for element

1. **Foundations.** Where UI exists, first the font install — one line approved in chat — and the detector run (`ratify.md`). Theme files take the new values, old tokens **deleted**, plus everything the canvas CSS carries beyond values: the font loading itself, element rules, shadows, motion durations, and the setup files the canvas relies on (a class-merge registration). Verify in the browser that every declared face and weight loads (`document.fonts`), not only those a page renders — off the browser, through the Proof profile's Visual line, naming what could not be verified. `ratify.md`'s five rules bind.
2. **Chrome and shared components, from the canvas chrome** — in production before any page importing them counts as moved; production logic (auth, navigation, data) is wired into the canvas markup, never the reverse. Placement follows `ui-build`'s placement rule.
3. **Pages — the proving page first**, each canvas file **copied to its real path**, the theme wrapper and canvas-only instruments (proposal tags, canvas nav entries) removed. **Copied means the canvas file becomes the page**; a production page re-tokened from its old markup is not promoted.
   - **Before its data swap, pixel-diff each promoted page on the canvas fixtures against its canvas file** at both widths, with a diff tool run outside the app's dependencies, the diff images kept for Step 8; a differing pixel outside the removed instruments fails the promotion; no tool → `not verified — pixel diff`.
   - **With a data layer**, swap the fixture import for it, per `build-flow` and `logic-settle`, changing only what Step 8's structural diff allows at the data seam, and check each page at both widths: holding → report and continue; first collapse → stop, a rework round of that page. Where `logic-settle` chose the data layer, loading, empty and failed states come from its cache, never a handwritten effect.
   - **With no backend yet**, pages keep fixtures reshaped to `build-flow`'s contract form (`src/contracts/<page>.ts`, `src/contracts/<page>.fixtures.ts`, per its `references/contract.md`), and **each gets a `docs/queue.md` line** `wire <page> to real data`.
4. **Components not on the canvas** — **fix-the-drift only**: repair each approved finding — a raw value retokened, a prop or theme value departing from the library default returned to it unless `DESIGN.md` requires it. **In a redesign this step is empty**; a file here is a failed inventory to report, never to retoken.
5. **`/design-system`** — written here, once (below).
6. **Assets** locked to the old colors — where UI exists: inline SVG, favicon, brand-coloured images.
7. **The old library, icon pack, engines and font packages are removed**, if their decisions changed.
8. **The lint floor, then `AGENTS.md`'s `## UI` part** (below) — fix-the-drift writes them too.

**Fix the drift** runs here too, on the same isolated branch: points 2 and 3 are empty and point 4 repairs the approved findings, nothing else; every other point runs as written.

## Promotion rules

- **Element for element.** Every visible element survives into the page (fixtures swapped for data, real states added) or appears as a named deviation line at the recap with its reason — real behavior contradicts the drawing · the backend does not exist yet · the control is obsolete. Never substitute a plainer equivalent silently (a bare file input for a drawn dropzone). A canvas control the real flow never had is a canvas error reported for the user's decision, never quietly dropped.
- **The proof is a diff, not a look.** Differences between canvas file and promoted page are confined to what Step 8's structural diff allows (`verify.md`) and approved deviation lines; any other difference is a failed promotion to fix, whichever side reads better.
- **The proving page is the bar** for every later page; with data, its fixtures include `bulk` and `messy` cases. `ui-build` binds every promoted page.
- **On a shell or desktop Surface, once the proving page is promoted, launch the app by its own run command and end the turn asking the user to look at that page in its window** — a chat stop, in the same message as the seam after the proving page — because a look the real window changes, found after the pass, is redone on every page that copied the proving page. The reply is the go-ahead or that page's rework round.
- **Page running → prove it at two widths with screenshots** (`DESIGN.md`'s desktop breakpoint and lowest supported width) per the Proof profile. No capture tooling → say so, name the run target and both widths; never claim they were judged.
- **Survival of real data**, per page at both widths: a layout collapsing under real rows, a token that did not land, or a vanished section stops the pass as a rework round of that page. Real rows differing from fixtures is not divergence.
- **A ratified element whose data does not exist yet** — a gate-ordered migration not yet applied included, since `db-ops` puts the frontend after the run — gets no query: promote it **rendered empty and labelled as waiting**, with one `docs/queue.md` line naming the data. Never dropped or hidden behind a flag.
- **The pass also stops** for a drawn element that would make the app claim what it cannot do — a `build-flow` stop.
- **Detector findings are deferred** to Step 8, overriding `impeccable`'s act-on-findings instruction.
- **Rework rounds.** A page collapsing, or a user-requested rework, gets one. **Two per page at most — a third does not run, and `DESIGN.md` reopens** through the escalation (`canvas.md`, Judging). A changed `DESIGN.md` updates the styling values and rebuilds pages from the new tokens, never patched.

## The `/design-system` route

**Written once, at point 5 — never before the canvas is approved.** An app whose route already sits at `/styleguide` keeps it there, never renamed: every rule naming `/design-system` means that route. It embeds no page — the app itself is the composition.

**One route file** (e.g. `src/pages/design-system.tsx`) at `/design-system` in dev, out of navigation, outside the auth guard, and out of the production build. **It imports the production components and tokens** — never copies, a separate HTML file, or a second source of values. **Render every specimen's actions inert** — a sign-out, write, or send is stubbed through the component's props; a component that cannot take a stub is listed `live only`. Offer deleting it later; never require it.

| Section | Contents |
|---|---|
| Foundations | Color roles or scales as `DESIGN.md` defines them, with the semantic token list read from the styling files · every text step with a real sample sentence · spacing scale · the density profile table with its numbers, both profiles where a role split produced two · radius, shadow, breakpoints, motion · the contrast section, one row per pair with its computed ratio, in every ratified theme mode. **Rendered by `canvas.md`'s specimen rule** (The foundations board) |
| Components | Every component the app uses or an archetype names — variants, sizes, and states per component, including loading, empty, and failed where they apply, with a short real-usage snippet |
| Archetypes | `DESIGN.md`'s archetype table, one card per archetype on its ratified shell: shell sketch, components, routes |

**Done is measured against the table, not the page looking full**: every semantic token appears; a component checklist written first, never recalled — every component an archetype names with its variants and states (inputs: default, focus, disabled, error; buttons: hover, focus, disabled, loading; stepper, dialog, dropzone rendered open through their own props; a hover or focus state the component's props cannot set is listed `live only`); every archetype card has all three parts. Report **archetype → components it names → where each renders**. The only allowed absences are a component no archetype or flow uses and a foundation `DESIGN.md` holds as `[needs verification]`, each stated with that reason.

## The lint floor

Write **the four refusals `ui-build` names under its lint floor into the stack's own linter, derived from this app and never pasted from a stock config.**

| Refusal | Derived from |
|---|---|
| Raw element | The shared set the pass promoted, plus what the library ships — only elements this app has a component for |
| Raw value | The utilities and style properties that carry a `DESIGN.md` value — colour, radius, font size, the spacing scale — and the engine props that take one (a chart's `fill`) |
| Numbered ramp step | The ramp names in the styling files. Not written where a legacy adopted-whole Section 5 left no alias layer to read instead |
| Primitive import | The packages the shared set wraps. None → not written |

- **Scoped by path**: the components folder is exempt from the first and fourth, the styling files from the second and third, the `/design-system` route file from the third, `src/design-canvas/` from all four.
- JS/TS web on ESLint: `no-restricted-syntax` and `no-restricted-imports`. Any other linter or stack: its own rule, and for a refusal it has no rule for, **one local plugin file the config loads**, derived like the config — each **verified live at write time**, a refusal neither expresses reported as `not enforceable on <stack>`. No linter → Step 4 installed one; in fix-the-drift, one install line approved in chat.
- **Proven on what must pass before what must fail.** Lint the promoted app first; a hit on a freshly written page is a raw value to fix or a pattern too wide (`grid-cols-[1fr_auto]`, a `calc()` is not a raw value). Then plant one violation per refusal in a scratch page, see each refused, delete it.
- **Files the pass did not rewrite are baselined, never excused** — in the linter's own suppression baseline, verified live. Never lower a rule to a warning. Report the baseline's size at the close; it only shrinks.
- **One floor, one command**: these four join `logic-settle` Step 7's config (`references/floor.md`) where it exists, or found it. The detector stays alongside.

**Write `AGENTS.md`'s `## UI` part in the same act**, to the shape in `app-settle`'s `references/scaffold.md` (N5): the shared-set file and folder, the library, the styling file, `/design-system`, the lint command (no file → write it whole). A path that does not resolve is a failed item.

Promoted → `verify.md`.
