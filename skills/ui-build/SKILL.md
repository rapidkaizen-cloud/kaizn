---
name: ui-build
description: Rules for building or changing any UI — the DESIGN.md gate, component reuse, loading, empty and failed states, interface copy, and the craft material read first. Use before creating or editing a component, touching a styling value, or writing any user-facing text.
---

# ui-build — touching the UI

Documents are named by their `docs/` path; a repo with a root `PRD.md` reads each through `docs-format`'s legacy map.

## What a load costs — four rules

- **Run independent reads, searches and commands in one turn** — parallel calls, or one chained command — because every extra model call re-reads the whole session.
- **Never re-read what the session start printed** — its component listing stands in for listing the components folder (Components).
- **Load only the craft material the edit at hand needs** — the rows of the table below whose condition it meets.
- **Read a part that is one section of a longer file alone, by its heading**, here and in `design-settle`, because every later call re-reads the whole file.

## The material — loaded before the first component

`impeccable` and `frontend-design` carry the craft rules this file does not state: icons, tokens and raw values, library defaults, accessibility. Read each row's part before writing what the row names, located through that skill's own `SKILL.md`, never by a file name remembered from here:

| Read | Before writing |
|---|---|
| `impeccable`'s craft floor, and on an operational app its operational register | any component |
| `impeccable`'s iOS or Android reference, both on an adaptive Surface — the platform's navigation, type scale, insets, and touch-target floor live only there | any component, where the Surface in `docs/product.md` is iOS or Android |
| `frontend-design` | any component |
| `ui-ux-pro-max`'s UX guidelines for that interaction — searched, its `SKILL.md` read for the search commands only | a component carrying an interaction: a form, table, dialog, navigation, feedback |
| `ui-ux-pro-max`'s stack guidelines for that framework, searched likewise | the same, on a native Surface (SwiftUI, Compose, a XAML stack, Flutter, React Native and kin) |
| `ui-ux-pro-max`'s `ui-styling` references on theming, accessibility, and responsive layout, through that sub-skill's `SKILL.md` | any component, where the library is shadcn or the styling is Tailwind |
| `review-animations`' standards reference, where installed | any animation or transition, on a web-technology Surface |

- **`impeccable`, `frontend-design` and `ui-ux-pro-max` are Required installs, and the load is not optional for a session that writes a new page or a new component — a new file in the pages or the components folder, whatever pattern it repeats.** An edit inside a file that stands — a repair, a retoken, a pattern repeated there — may skip a row. One absent → say which, and what could not be checked because of it, then carry on; an absence never stops the work.
- **Name in the closing block, among the defaults decided, every row whose condition the edit met — read, or skipped with why**: a row skipped with no reason reads as forgotten.
- **Material, never an authority.** `DESIGN.md` wins over all of it. What the material finds is reported to the user, never fixed in place inside another session's work.
- **Read `impeccable`'s reference files; never run its commands.** Never run one that writes `PRODUCT.md` or `DESIGN.md` from the built world — `init`, `extract`, `document` at the time of writing — because an app repo keeps only `docs-format`'s closed list, and `DESIGN.md` is `design-settle`'s alone. Its menu leads with `init` whenever it finds no `PRODUCT.md`: answer by pointing at `DESIGN.md`.
- **`ui-ux-pro-max` is the UX floor, level with `impeccable`.** Keep only results that fit this interaction and Surface, and hold what they mark as a don't. Where both set a floor, hold the stricter one; any other contradiction between them is a finding for the user. Never apply a value it names — a hex, a font, an icon library, a chart colour; `DESIGN.md`'s is. Where its `ui-styling` references disagree with the installed package, the package wins.
- **`ui-ux-pro-max` writes nothing, in any session.** Never pass its `--persist` flag, never run a script or command of its sub-skills — `ui-styling`, `design-system`, `brand`, `design`, `banner-design`, `slides` — and invoke one only when the user names it, because each writes files outside `DESIGN.md`. Outside `design-settle`'s interview, never run its design-system generator or its look searches — style, colour, typography, fonts, motion presets, landing, product.
- **`review-animations` is the motion floor on a web-technology Surface — Optional, and unmentioned when absent.** Hidden from the skill list and not invocable, it counts as installed when `review-animations/SKILL.md` exists under `~/.claude/skills/` or the repo's `.claude/skills/`. Hold what it forbids; its curves and durations are defaults `DESIGN.md` overrides. A library's own motion counts; motion the library cannot retune without replacing the component stands as a finding. Skip its opening-message and review-verdict instructions.

## Gate — the visual direction must already be set

**Before writing any UI component, read `DESIGN.md`.** Absent, empty, or `[needs verification]` in every line → **STOP**: write no component, no styling value, no token, because every rule below measures the code against `DESIGN.md`. Offer no way around the stop: `design-settle` is its one exit.

- **A `DESIGN.md` with only some lines `[needs verification]` is written, and binds.** Take what such a line would rule from a component already in the repo, never type it as a new value, and name the line in the closing block, among the defaults decided, as owed by `design-settle`.
- **A repo the session start marks `NOT SETTLED` is outside this gate**: that block says what UI may be written there.
- **Point the user at `design-settle`, whatever state the repo is in.** Never name a path or decide one; its own audit decides. Components with no `DESIGN.md` are its normal input, not an error — `app-settle`'s document mode leaves the design system unwritten.
- **One exemption: the design canvas and the `/design-system` scaffold** — `src/design-canvas/` and the design-system route; on a non-web Surface, whatever `canvas.md` defines for that platform. A design skill builds them to produce `DESIGN.md`, and the exemption is theirs alone: no real page, component, or token is written until it lands.
- **The canvas folder belongs to the design session building it.** A session doing any other work never edits, moves, or deletes anything under it or `.design-audit/`; a problem found there is a finding reported to the user, because an outside edit silently changes what the user approved.

`DESIGN.md` written → this gate is done: later pages need no further visual approval, and the rules below bind them.

## Components — named before execution

**Before building any UI element, check the components already in the repo and name which one covers each element in scope.** Required, not a suggestion.

**Read the ratified set first, do not search for it** — one listing, one read of the file holding the app's shared set, never a grep: a session hunting for `Pagination` misses a `Pager` and writes it a second time. The session-start block's listing stands in for listing the components folder — none printed, or cut short → list it — never for the read. A repo whose `DESIGN.md` was ratified rather than redrawn may have no single file yet: the listing is still the first move, and the first extraction follows the placement rule below.

The order of sources is fixed:

1. **A component already in the repo.** Components copied in from a library (shadcn and the like) are **existing code**, not a dependency to be ignored.
2. **A component from the installed component library.** An element the library ships is used, not rebuilt. **List the library's component directory before deciding it lacks something** — one command against `node_modules/<library>/dist/components` or that package's equivalent; "it probably doesn't have one" is not a reason to build.
3. **A new component**, only when the library ships nothing for the case or nothing that genuinely fits. Three conditions:
   - **Say what fails**: which component was examined, and what it cannot do here. **Looking slightly different is NOT a reason** — that is what props are for.
   - **Follow the library's idiom**: its compound shape (`Root` / `Trigger` / `Item`), its prop names (`isDisabled`, `isActive`, `size`), its source of styling. **No library → the first shared component sets the idiom, and every later one follows it**, read from that file.
   - **Say which rule it holds, in its header**: it freezes a `DESIGN.md` line so no call site can break it — a status marker deriving its icon from its tone cannot pair a warning colour with a success icon — or it is the second appearance of a pattern. Neither → page code; leave it in the page.

**A visual pattern appearing a second time → extract it into a component, do not copy it.**

**Where it lands is fixed too.** Components holding `DESIGN.md` rules live in **one file**, read whole in a single pass — the file the ratified-set rule points at. A component carrying a flow of its own — a wizard, the app shell — gets its own file. Split the shared file by group, never one file per component, and only once it is no longer readable in one pass.

**Where the app has a design-system route** — `/design-system`, or `/styleguide` where it already sits there — add the extracted component to it in the same turn; a shared component missing from it is a finding.

**A library shipping no strings for the app's locale** (`CLAUDE.md` Locale row) gets them from one dictionary file beside the shared set, passed through the library's own locale provider at the app root — its API read live, never strings patched per call site.

## Inputs that write

- **A date field writes only a complete, valid date** — a year typed keystroke by keystroke (2, 20, 202) never reaches storage.
- **A change that triggers a paid or slow call fires on an explicit action** — a button, Enter, a picked option — never on focus leaving the field or on each keystroke.

## The lint floor — what the repo itself refuses

The repo's own linter refuses the four failures that cost the most, in every session and for every agent, whatever it read:

1. **A raw element the shared set or the library already ships**, written outside the components folder — a bare `<button>`, `<input>`, `<select>`, `<dialog>`, `<table>` on the web, and only the ones this app has a component for.
2. **A raw value in product code** — a colour literal, or an inline style or arbitrary-value utility carrying a colour, a radius, a font size, or a step of the spacing scale. The styling files are the one place a value is typed.
3. **A numbered ramp step in product code**, where the alias layer exists. Product code reads a role.
4. **A primitive the shared set is built on, imported outside the components folder** — the package a dialog wraps, pulled into a page to hand-roll a second dialog.

`design-settle` writes the floor in its pass, derived from this app's shared set and styling files; a repo with a `DESIGN.md` and no floor gets it from `app-settle`'s align mode. Live with it this way:

- **Run the repo's lint command before committing any UI scope item**, and fix a refusal in the code that caused it.
- **An inline disable of a floor rule is a finding**, the same standing as a raw hex value; so is a floor rule lowered to a warning.
- **The floor grows with the set**: extracting a shared component that replaces a raw element adds that element to the first refusal in the same turn.
- **A refusal that is wrong is reported, never worked around**: a layout expression caught as a raw value is a pattern too wide, narrowed in the config only on the user's word, never silenced at the call site.
- **No floor in the repo → say so in one line and carry on**; its absence is a finding for `app-settle`'s align mode, not a stop.
- A hook refusing the config write follows `logic-build` Section 9.
- The floor cannot see a second component doing an existing one's job under another name — the listing and the read under Components hold that one.

## Loading, empty, and failed

Fixed norms — not asked per app, not restated in any document. Write each state **together with its component**; a component with only a success state is not finished.

- **Loading → a skeleton shaped like the final result**, so the layout does not jump when data arrives. A spinner only for what has no shape: a button mid-submit, work running in the background.
- **Empty → explain why it is empty and what comes next**, ending on the one action that fills it; "No data yet" is not enough. Empty because of a filter and empty because nothing has ever existed take different sentences; the filtered one names the query and offers the exit — `No results for "quarterly". Clear filters`.
- **Never park persistent information in an empty state** — it disappears the moment content exists. **Delete it, never relocate it** to the page header: information worth keeping is an element on the page; a mechanism the user does not act on belongs in `docs/rules.md`.
- **Failed → put the message next to its cause**: a form error under its field, never stacked at the top of the page; an error with no field of its own (failed to load, failed to save) where the content should have been, with a way to retry.
- **A failure message never disappears on its own**; only success notifications may.

**Where the app has contract files, these states are proven rather than claimed**: `build-flow` builds each page of a UI batch against six named fixture cases, held in its `references/contract.md`. Three are these states — `loading`, `empty`, `failed`. Two more must render without the layout breaking before the page is accepted: `bulk`, 500+ rows, and `messy`, null in every nullable field with the longest string that really occurs.

## Writing

Fixed norms for the tenth-use register — the pages somebody comes back to — not asked per app, not restated in any document. Write copy **together with its component**. Clear and brief beats clever; consistent beats varied; the best error message is the interaction redesigned so the error cannot happen.

**The one exception is the voice** — formal, neutral, or casual, and the form of address where the language has more than one: asked by `design-settle`, recorded as the copy voice in `DESIGN.md`'s Overview. Write in that voice; none stated → neutral.

**A first-visit page group speaks in its own voice** — a landing page, a marketing site, the public front of a product: read `references/first-visit.md` before writing its copy.

**Copy caps, on every tenth-use page** — counted in words, in the app's on-screen language:

| Class | Cap |
|---|---|
| `Action` — button, link, menu and tab item | 2 words |
| `Name` — field label, column header, badge, heading | 3 words |
| `Explanation` — helper text, empty and error state, tooltip, toast, subtitle | 1 sentence, 8 words |

A string over its cap is a defect: cut it before the page is shown or committed. A destructive confirmation's body may run two sentences, because it must name the consequence. Put a subtitle under a heading only when it says something the heading does not, and helper text only under a field whose input is ambiguous. First-visit page groups are exempt, and their copy is still counted.

**Read the copy already on screen before writing more** — it sets the product's one voice, and a local edit invents no new one. One term per concept: `Archive` in the menu is not `Move to storage` in the toast.

**Voice is `DESIGN.md`'s, tone moves with the stakes:**

| Context | Tone |
|---|---|
| Success, onboarding, empty states | Warm, may be light |
| Routine actions, settings | Neutral, minimal |
| Errors, destructive confirmations | Calm, plain, zero playfulness |
| Data loss, security | Serious, explicit |

- **Address the reader directly**: "you", never "the user". In an error drop the actor rather than reaching for "we" — `Unable to load content`, not `We're having trouble loading this content`. Possessives sparingly: `Favorites` beats `Your favorites`. Hold one perspective for a whole flow.
- **Plain words, and no word that does no work**: no idioms, no colloquialisms, no humour that does not survive translation, no unnecessary gender. Match the input device — `tap` on touch, `click` with a pointer, `select` where both are possible.
- **Never assemble a sentence from fragments around a variable** — `"You have " + n + " new messages"` breaks when word order changes. Use a full templated string with proper pluralization.
- **A button label starts with a verb naming the action** — `Send`, `Save draft`, `Delete project`; never `OK`, `Let's go`, or a bare `Yes` / `No` on a consequential action. **A confirmation button repeats the consequence**, so the dialog is answerable without its body: `Delete this project?` offers `Delete project` and `Cancel`.
- **One vocabulary for a whole flow**: `Get started` to enter, `Continue` or `Next` — pick one — to advance, `Done` to finish.
- **Link text names its destination**, readable out of context in a screen reader's list of links: `Read the billing docs`, never `Click here`. Suffix every `Learn more` — `Learn more about exports`.
- **Sentence case, one policy per element type.** Sentence case is the default; never `Save Changes` beside `Discard changes`.
- **A toggle is labelled for its ON state** — `Send read receipts`, never its negative. Link straight to a referenced setting rather than describing the path to it.
- **A placeholder is an example, not a label** — `name@example.com`, `DD/MM/YYYY`; it vanishes on input, so every field keeps a visible label of its own.
- **A state already visible is not written out again.** A selected card carrying the selection in its border, a check mark, an `ACTIVE` badge, and a heading repeating the item's name draws one fact four times: keep the strongest signal and delete the rest — where the strongest is not reachable for everyone, the accessible one survives, never the decorative one. The same holds for a subtitle repeating a word of the title above it, and a count printed beside a list whose length is on screen. **The test is subtraction**: remove the label; nothing became unanswerable → delete it.

**An error is an instruction, and it belongs beside the field that failed.** No blame, no `Oops`, no exclamation marks. Phrase the hint positively, and show it before the mistake rather than after:

| Refused | Written |
|---|---|
| `That password is too short` | `Choose a password with at least 8 characters` |
| `Invalid name` | `Use only letters for your name` |
| `Oops! Something went wrong.` | `Unable to save. Check your connection and try again.` |

The same error firing over and over is a finding about the interaction, not a rewording job.

These bind new code. Copy already in the repo that breaks one is a **finding** reported to the user, the same standing as a raw hex value — never rewritten in place inside another session's work. **Source is enough to check every rule here**; none needs a rendered page.

Adapted from the `better-writing` skill of [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (MIT).
