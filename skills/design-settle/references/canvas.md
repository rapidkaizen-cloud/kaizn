# The design canvas — Step 5, after the pick

One temporary route — **every page of the app, redesigned** — where every shell is designed whole, judged in the real browser, then ratified value by value into `DESIGN.md`. It replaces every taste question beyond the interview's dialogs, the direction question and the frames, never those.

## The chosen frame is carried in, never redrawn from nothing

Rename it to its real page's name, then **refactor** it: raw values into canvas variables under production token names, held to `ratify.md`'s five rules (read that section now), controls into the shared set, data into the contract-shaped fixtures file, every state drawn, the three scans run. **Prove the refactor on screen before any other page is drawn**: capture it at the desktop width beside the picked frame's capture taken after its last change — pixel diff where a tool exists, side by side otherwise — and fix any visible difference now, whichever side reads better. Change only by addition, plus the correction attached to the pick. A departure large enough that the page no longer reads as the picked frame is a line at the judgement, never a silent redraw.

## The design plan — narrated, not gated

**Write it in the turn after the pick, before the first full canvas file**, to the picked candidate, without ending the turn, asking or waiting; no document is touched during rounds.

| Part | What is stated |
|---|---|
| Direction | Purpose · the one tone held · what makes this app memorable rather than adequate (`frontend-design`) · the copy voice answered at Step 3, per page group where it was asked per group (`ui-build`, Writing) |
| Colour | The named values with their roles — as many as the direction needs — and their source: a brand palette, a reference, a `ui-ux-pro-max` palette with its adjustment, or an accent chosen first and the neutrals pulled toward it |
| Type | The pairing and each face's job. A face on `impeccable`'s calibration list is named with the reason it was still chosen |
| Layout | The shell and the composition in one or two sentences — where the density sits, what breaks the grid |
| Signature | The picked frame's candidate signature, kept or replaced as a departure |

Old values appear only at the gate, never in the plan. **Then critique it against the brief in the same turn:** a part a session with a similar brief would also arrive at is a default — revise it and say in one line what changed and why. Revise only what the picked frame did not settle; revising a picked value is a departure line at the judgement.

## The brief — features in, interpretation free

The input is the **user's feature list** plus what the documents hold; the canvas decides how it looks, and the user judges the result rather than pre-approving a layout.

- **Function is faithful.** A feature shows what it actually does — its real fields, states, and the figures a business rule demands. Never draw an improvised feature without its proposal tag, and never promote one without ratification.
- **It renders working — static data, live chrome.** Real fixtures, not lorem. The **data** is static: nothing fetches, writes, authenticates, validates, or runs business logic. The **chrome** is alive, as local state: nav items navigate between canvas pages (plain anchors to sibling files, no router import), tabs switch, rows open panels, dialogs and drawers open and close. **An action whose real outcome is navigation navigates** — login lands on home with any input its fields accept — so the walk from login to the deepest page works end to end; a field's required and format attributes are markup, drawn as production carries them. Every interaction written here is real component code that survives promotion. A conditional branch interaction cannot reach cheaply gets its own frame (Coverage).
- **Assume the product whole — expansion is a duty, not a permission.** Draw the full draft written at Step 3 (`interview.md`); **a canvas that renders a thin brief as thin pages has failed.** Mark every improvised feature visibly as a proposal (a small tag on its section). Ask the cut in the judgement call as a multi-select of what to remove — first option `keep all`, recommended, then one option per feature with a one-line description, more questions in the same call past four — and remove what is ticked. A kept proposal carrying a business rule the documents lack becomes a `docs/rules.md` line put to the user, per `docs-format`; one carrying none is recorded by its page alone.
- **Where UI exists, the floor is `handover.md`'s function inventory, never the pages.** Re-allocate functions freely — another page, the chrome, merged, shrunk to a line; never redraw as page content what the new chrome carries. Only a function absent from **every** canvas page is a cut, asked at the judgement, never silent. Still improvise and reshape shells, tagged — redrawing today's pages in new tokens is a repaint and has failed.

**Where UI exists, the drawing session stays blind to today's look** (`SKILL.md`, Blindness).

**Measured, never transplanted.** A reference — ticked, named under Other, or arriving later as a file, screenshot, or URL — is inspiration only, unless the user stressed it (`interview.md`). Never import a reference's code, copy its components, or reproduce its visual identity. Where it is reachable, **look at it and take the numbers off it**: density, type character, colour temperature, motion budget. Unreachable, or reachable with no screen of the product → say so, and that the direction is drawn from memory.

**Assumptions are declared before drawing, in one block — mandatory.** After the pick and before the first canvas file, list every product and behavior call that no answer, function-inventory line, or data-layer file settles — layout calls, invented sections, data assumptions, conditional behaviors — one line each (`bottom bar: 3 slots, input as the primary action`). Never list visual values; they are read at ratification. The block is a cancellable report, not a gate; its lines return at the judgement call, attached to what they produced.

## The canvas file

**One folder, one file per page.** `src/design-canvas/`: one TSX file per page (off the web, the platform's page format and source layout, same rules), **named exactly as its real page is or will be named**, plus an entry route landing on the primary role's landing page (the chrome's nav is the page list; the route shows the compare page while only frames exist, and the first canvas page until that landing page is drawn) and one CSS file carrying the canvas variables. Dev-only, out of navigation and the production build. Never one monolithic file, never files outside the folder. **A file more than one page imports — a shared wizard, a shared card — names its production path in its own header line**, decided the round it is created, and enters the pass's file plan as its own line.

**Production-grade from the first file after the pick**: real library components, production token names, and **every state drawn** — loading skeleton, empty state with its wording, failed, busy — since a state added at promotion is markup the user never approved. **Fixtures live in one file, shaped as the data contract** the real layer returns — `build-flow`'s contract shape where no data layer exists, the existing modules where one does — so promotion swaps one import. Cases and roles are reached through `build-flow`'s two switches (`contract.md`).

**Every page, drawn.** Derive the archetype table first (`interview.md`); where UI exists the **grouping** comes from the existing routes, and that is all the old app contributes. **Propose each archetype's shell fresh** from the picked frame, the brief, and your judgement — never read an existing page to learn its shell. Draw **every page** to its archetype's shell — content from the function inventory where UI exists, from the documents where it does not.

**Above 12 pages in scope, draw the representative pages alone** — the proving page and, for every other archetype, its page holding the most functions — because every drawn page is context each later call re-reads. The design plan names them and how many are left undrawn; the pass builds each of those on its archetype's promoted page (`pass.md`), and a function or part only an undrawn page carries is neither a cut at the judgement nor a removal at the gate.

**`/design-system` is not written here** — the pass writes it once (`pass.md`). An existing route renders the old theme: leave it alone and never look at it.

**Quarantine, both directions.** Nothing in the app imports the canvas. The canvas imports only from the **declared UI stack** — the chosen component library, the chosen icon pack, the engine libraries the dependency file carries for UI jobs, and the packages their install documentation names beside them — its own CSS, and type-only imports (`import type`) from the data layer — the files `handover.md` names where UI exists, the existing data-layer modules where it does not — or from the contracts where no data layer exists. Never the production theme, tokens, or components. **A copy-in library (shadcn and kin) enters the canvas as a fresh copy from its registry** under `src/design-canvas/ui/`, the CLI's path option verified live and the copy's internal imports pointing at the copy — never imported from the app's components folder, which carries today's look; promotion replaces the app's copy file for file. The app must render identically with the canvas deleted.

**Real components, canvas-owned theme.** Library components render inside a scoped theme wrapper carrying the canvas's values (CSS variables on the web) — on the portal's root too where the library portals overlays out of it, frames included. **Element selectors in the canvas CSS style native controls only** — scope them out of library components (`:not([data-slot])` or equivalent) the moment a native control is swapped. **Draw every control the chosen library ships with the library's component**; hand-roll only where the library has none for the job, each as its own line in the judgement call. **The rule governs the control, never the composition**: compositions of primitives and domain components no library ships — a ledger row, a shift strip — are the canvas's to invent; stock components alone is the generic outcome. Extract a component appearing twice under `ui-build`'s reuse rule. **With *own components*, every control is the canvas's own and none is a line**; a second form of one control across pages is the finding.

**The declared stack binds the engines too.** Draw a job an installed engine owns — chart, virtualized table, date picker — with that engine, never re-implemented beside it. Hand-rolling where an engine covers the job is a departure line at the judgement (`recharts installed → drawn as CSS bars, because Z`); swapping or dropping an engine is an explicit user decision there, and an approved swap becomes its own install/remove line in the pass. An engine need that emerges while drawing follows `engine-rubric.md`: draw the no-engine rendering tagged, settle it at the judgement, and on approved adoption install and redraw that frame next round.

**The canvas's variables carry the production token names** exactly as the theme files will name them, so ratification is a copy, not a translation. **Where the styling answer is Tailwind**, canvas utilities read those variables and ratification moves them into the production Tailwind theme under the same names — look the syntax for both up for the installed Tailwind version at write time (WebSearch; the package ships no docs). **Where a class-merging utility is in the stack, register the production token names with it** before the first canvas file uses them, or it drops them. A utility internal to the library, outside the import whitelist, cannot be registered: name tokens only in shapes it already classifies — t-shirt sizes (`sm`, `md`, `lg`).

### Three scans before each round is shown

A round that fails any is not ready to show; report the scan with the round as a short list of what it caught and fixed. A round handed to an agent outside this session is briefed and reviewed by `build-flow`'s `references/delegate.md`, these scans its brief's last part.

1. **Imports.** Every control maps to a library component, the canvas's own shared set (*own components*), or a named hand-rolled line; every engine import comes from the declared stack.
2. **The render** — `frames.md`'s render scan, on every round.
3. **The arithmetic.** Compute every number printed as a claim — ratio, percentage, count, total — never recall it, and make the fixtures close (Coverage). Count the copy too: cut every string on a tenth-use page over `ui-build`'s copy caps, the direction frames included. Read the assumption lines against each other and the fixtures; fix a contradiction before the round is shown.

**Where UI exists the scan covers the fixtures too**: take value types and field names (enums, state labels, column names) from the existing contract or data-layer modules, and never redefine an existing type name with different values. Do not import page-structure types — filter shapes, page sizes, and query keys stay the canvas's to redesign. Draw a field with no source in either tagged as a proposal.

### The taste licence, and the one signature

**Design with a free hand.** The licence owns outright everything the picked frame did not settle — palette steps, surfaces, elevation, type scale, spacing, every other page's composition. What the user settled — the pick, its correction, a named reference — is their **preference — the baseline, not a cage**, and **departing is part of the job**: draw the better call, tag it, and list every departure in one cancellable report above the judgement call, one line each shaped `picked X → drawn Y, because Z`. A cancelled line reverts to the pick; the rest enter ratification.

**The licence covers `frontend-design`; `impeccable` is the floor it stands on.** Depart from any `frontend-design` value — a palette count, a family count, a composition habit — only drawn, tagged, reasoned in one line, and settled at the judgement. `impeccable`'s Refuse list, Verify list, calibrations, and detector bind every round as written: a Refuse-list hit is fixed, or stands at the judgement as a finding under the detector's own name; a detector hit stands on its own rule whether or not a calibration list names the value; a hit the library's own stylesheet or component anatomy causes stands as a finding with that reason — never restyle the library to silence it. No direction departs from `interview.md`'s floors — contrast, colour never the only marker, reduced motion honoured, a visible label for every field, the platform's touch targets — nor from this file's engineering rules: quarantine, token names, fixtures that close, one-to-one promotion.

**One signature.** Every canvas draws a **single element this app is remembered by** — a treatment, a shell move, a way one recurring thing is rendered — where the boldness is spent; everything around it stays quiet. Never three competing signatures, never none. **Tag it on the canvas like a proposal**; it is settled in its own question (Judging).

### The foundations board

**A page of its own** — palette roles and steps, text scale, spacing, radius, shadow, status triads — rendered from the canvas's variables inside the same chrome shell as every other canvas page, its nav entry **set apart from the page groups**. The entry route never lands on it.

**Show a token applied to itself, every other variable held constant. Never a table row.**

- **Spacing**: a square that many pixels, steps side by side as a staircase; floor the drawn size so a degenerate value still renders a labelled marker.
- **Radius**: identical tiles differing only in corner. **Border width**: identical tiles differing only in stroke.
- **Shadow**: identical surface tiles that actually cast, with vertical room so the shadow is not clipped.
- **Colour**: fixed-size swatches carrying step name, resolved value, and the semantic alias pointing at it, with a hairline inset ring so near-white steps keep an edge. **Grouping is carried by the gap** — tight within a ramp, looser between families.
- **Type**: every step shows **a different real sentence from this app's domain** — the one it carries on a screen; one repeated neutral string only on the weight specimen.
- **The alias layer gets its own row**: role, step it points at, resolved value.
- **Every specimen carries a caption in one identical treatment** — monospace, muted, small — printing the token key **and** resolved value (`lg · 8px`, `hairline · 0.5px`). Relabel an absurd literal (`full`, not `9999px`).
- **The contrast section** — one row per pair `ratify.md` defines, in every ratified theme mode: a live chip of the real foreground on the real background, the computed ratio beside it, and its mark against the 4.5 / 3.0 floors.

## Coverage

**Show the whole visual language once across the pages:** every colour role on real surfaces · text steps on real sentences · the densest data view with messy fixtures (long labels, large numbers, missing values), if any · form controls in their states · **every conditional branch of a form as its own frame — a status that reshapes the fields (deal / no deal) is two frames, never one with a note** · status markers · one card or KPI group · **the busy state of every long-running operation — import, matching, bulk delete — as its own frame with real counts** · the loading, empty, and failed state of every page that has one · the behavior at both widths. Realistic domain data from `docs/glossary.md`. Rows no source holds — a `bulk` case the replaced process never reached — are synthetic and named so (`contract.md`).

**The numbers must close** wherever figures were invented rather than copied from the document the app replaces. On every page:

- A headline total equals the sum of the parts beside it; a remainder equals the difference it claims.
- A percentage, ring, or progress bar equals part over total to its displayed precision.
- A top-N list sums to less than its headline.
- A bar width is **computed from the value printed next to it**, normalised against the largest in the set — never typed.
- A pagination label's range matches the rows rendered; its last page equals total ÷ page size, rounded up.
- A sort affordance's direction matches the data's order.
- One fictional record named in two places is named identically.
- Totals are **derived from the fixture array**, never typed as literals; a total larger than the rows shown is declared once in the fixture and every figure derived from it, never padded with rows nobody sees.

Numbers, dates, thousands separators, and currency follow the app's locale per `CLAUDE.md`'s Locale row. **Fixture text and labels are written in the user's language**, as on production screens.

**One pattern per recurring control.** Row actions, pagination, summary bars, filter rows each take exactly one form across every page — the active page visibly marked, the same action affordance on every table. A second form is a finding at the judgement.

## Judging

Capture every round as `frames.md` rules — the desktop width, inside its device. **A verdict that approves adds the lowest supported width**: every page captured at it and put to one more verdict, none recommended — approve at this width too · rework it, a correction round — before Step 6.

**The platform is proven, not assumed — as a list.** Off the web, put the canvas beside one real native application — the picked frame's source where it is one, else one named here — and list the differences: window chrome, navigation shape, control size and radius, icon family, type, accent. Settle each as a **departure** with its one-line reason or a **correction round**. "It looks native" is not an output. **The same list runs on any platform when the picked frame was drawn to a stressed reference**: density, colour temperature, type character, motion budget, shell shape, how a recurring control is rendered. Where the reference is not a product, list what can be measured — colour, type character, material, a marker or shape — and name the rows that could not be written.

**The judgement call** holds, four questions per call, more in a second call the same turn:

- a single-select verdict, none of its options recommended — approve · rework this round · start the look over, with new references and new frames, which opens the escalation at once, whatever the round;
- the marked-feature multi-select (The brief);
- the assumption lines and the hand-rolled-control lines;
- the shells — one report, each archetype's new shell in a sentence, **whether it departed or not**; where UI exists beside the audit screenshot paths of its routes, or `not walked`, never a description of an old shell this session has not seen; where it does not, only the archetypes the user's archetype-table correction did not already settle — then one multi-select of the shells to redraw, first option `keep all`, recommended, more questions in the same call past four.

- **`keep all` ticked beside another option changes nothing yet**: one question naming both settles which was meant.
- **A cancelled assumption or hand-rolled line opens one question — what stands instead — and its redraw is a correction round.**
- **A verdict that starts the look over keeps that call's feature answers and drops the rest**: the shells, departures and signature of a canvas about to be replaced are neither asked nor applied.

Ask contrast failures, cancelled value lines, and reopened questions the same way. **Two more lines join the departure report whenever they exist**: the reference differences against a stressed reference · the direction candidate the user picked, named, so later rounds cannot drift off it.

**The signature is its own question, asked on its own** — one AskUserQuestion naming the element and what it costs the pages around it: keep, first and recommended · redraw it once · drop it and accept the quieter page. A rejected signature is redrawn once; only the user drops it. In Fast it rides the verdict call (`SKILL.md`, Fast or Full).

**Two correction rounds per canvas**, a correction round being one the user opens by rejecting what was drawn; a third does not run — the escalation opens. A round the user opens by **asking for something new** is not counted and quotes the request it serves; a round that cannot quote one is a correction round.

**The escalation — a canvas that misses twice, or two rejected frame sets, re-opens the look, not the interview.** Re-read the parts of `impeccable` and `frontend-design` `frames.md` loaded — the only second read in the flow — re-run the reference search **steered away from what was rejected**, re-ask the direction question from its results, draw **a fresh set of frames** (the old ones predate the rejections), and regenerate the canvas fresh from the new pick, never patched, under the same two-round rule. The stack and the four product calls stay closed; a rejection that names a product call re-asks that one dialog alone. It decides values, not pixels: its answers become the brief's constraints. **Regeneration replaces the direction, never the decisions**: every approved feature proposal and every ratified shell carries into the regenerated canvas.

## What the canvas never decides

Page content (`build-flow` Section 4) · the archetype table — the canvas proposes every shell, but the table becomes real only through the user's archetype-table correction and the judgement's shell answers · loading, empty, and error norms (`ui-build`) · anything the user does not ratify.

Approved → `ratify.md`.
