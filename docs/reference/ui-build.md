# ui-build

A session writes no UI until `DESIGN.md` exists, reuses the components already in your repo, ships loading, empty and failed states with every component, and keeps interface copy inside fixed word caps.

| | |
|---|---|
| Kind | Rule skill — a session loads it by its description; there is no command |
| Loads when | Before creating or editing a component, touching a styling value, or writing any user-facing text |
| Governs | UI components, styling values, interface copy |
| Reads | `DESIGN.md`, the Surface in `docs/product.md`, the components already in the repo, the craft material of `impeccable`, `frontend-design` and `ui-ux-pro-max` |
| Source | `skills/ui-build/SKILL.md`, with `references/first-visit.md` |

## What a session is held to

**No UI before `DESIGN.md`** (Gate). Before any component, the session reads `DESIGN.md`. Absent, empty, or `[needs verification]` in every line, it stops and writes no component, styling value or token, and offers no way around the stop: `design-settle` is its one exit. A `DESIGN.md` with only some lines `[needs verification]` does not stop it: what such a line would rule is taken from a component already in your repo, never typed as a new value, and the closing block names the line, among the defaults the session decided, as owed by `design-settle`. It points you at `design-settle` and never names a path itself.

- **A repo the session start marks `NOT SETTLED`** is outside this gate; that block says what UI may be written there.
- **The design canvas and the `/design-system` scaffold** are exempt, because a design skill builds them to produce `DESIGN.md`.
- **The canvas folder belongs to the design session.** Any other session leaves `src/design-canvas/` and `.design-audit/` untouched and reports a problem found there.

**Craft material first** (The material). Before the first component the session reads the part of `impeccable`, `frontend-design` and `ui-ux-pro-max` that its edit needs, a part that is one section of a longer file read alone, by its heading. A session that writes a new page or a new component — a new file in the pages or the components folder, whatever pattern it repeats — always reads it; an edit inside a file that stands may skip a row. The rows are in the skill: a form, table or dialog adds the UX guidelines; iOS and Android add the platform references; shadcn or Tailwind adds the `ui-styling` references; animation on a web-technology Surface adds `review-animations`, where installed.

- **Three installs are Required.** One absent, the session says which and what it could not check, then carries on. An absence never stops the work.
- **The close says what was read.** The closing block names each row of the material that applied to the edit: read, or skipped with why.
- **`DESIGN.md` wins over all of it.** What the material finds is reported to you, never fixed in place inside another session's work.
- **`impeccable`'s reference files are read; its commands are never run**, and none that writes `PRODUCT.md` or `DESIGN.md`.
- **`ui-ux-pro-max` writes nothing, in any session.** No `--persist`, no sub-skill script unless you name it, no design-system generator outside `design-settle`'s interview. It never applies a value that skill names; `DESIGN.md` does.
- **Where `ui-ux-pro-max` and `impeccable` both set a floor**, the stricter holds. Any other contradiction between them is a finding for you.

**Components before code of its own** (Components). Before building any element, the session names which existing component covers each one in scope. It reads the shared set with one listing and one read, never a grep.

1. **A component already in the repo**, including components copied in from a library.
2. **A component the installed library ships.** The session lists the library's component directory before deciding it lacks one.
3. **A component of its own**, only when the library ships nothing that fits. It names what fails in the ones examined — looking slightly different is not a reason — follows the library's idiom, and states in its header which rule it holds: a `DESIGN.md` line it freezes, or the second appearance of a pattern. Neither, and it stays page code.

A pattern appearing a second time is extracted, not copied. Components that hold `DESIGN.md` rules live in one file; a component with a flow of its own, such as a wizard or the app shell, gets its own. An extracted component is added to the design-system route in the same turn, where the app has one. A library with no strings for the app's locale gets them from one dictionary file, passed through the library's own locale provider.

**Inputs that write.** A date field writes only a complete, valid date. A change that triggers a paid or slow call fires on an explicit action — a button, Enter, a picked option — never on each keystroke or on focus leaving.

**The lint floor** (The lint floor). Your repo's own linter refuses four failures in every session: a raw element the shared set or library already ships, a raw value in product code, a numbered ramp step in product code where an alias layer exists, and a primitive imported outside the components folder.

- **`design-settle` writes the floor** in its pass. A repo with a `DESIGN.md` and no floor gets it from `app-settle`'s align mode.
- **Lint runs before any UI scope item is committed.** A refusal is fixed in the code that caused it.
- **An inline disable, or a rule lowered to a warning, is a finding.**
- **A refusal that is wrong is reported.** The config is narrowed only on your word.
- **No floor in the repo**: the session says so in one line and carries on.

**Loading, empty, failed** (Loading, empty, and failed). Each state ships with its component.

- **Loading** is a skeleton shaped like the result. A spinner is for what has no shape, such as a button mid-submit.
- **Empty** says why it is empty and ends on the one action that fills it. A filtered result names the query and offers the exit. Persistent information is never parked there.
- **Failed** sits next to its cause: a form error under its field; a failed load or save where the content should have been, with a way to retry. A failure message never disappears on its own.

**Interface copy** (Writing). The voice is the copy voice in `DESIGN.md`'s Overview; none stated means neutral. Tone moves with the stakes: warm in success, onboarding and empty states; neutral in routine actions and settings; calm and plain in errors and destructive confirmations; serious and explicit in data loss and security. Caps count words in the app's on-screen language.

| Class | Cap |
|---|---|
| `Action` — button, link, menu and tab item | 2 words |
| `Name` — field label, column header, badge, heading | 3 words |
| `Explanation` — helper text, empty and error state, tooltip, toast, subtitle | 1 sentence, 8 words |

A string over its cap is cut before the page is shown or committed. A destructive confirmation may run two sentences, because it must name the consequence. The skill also fixes form: a button starts with a verb, a confirmation repeats its consequence, link text names its destination, a placeholder is an example and not a label, one term names one concept, and a state already visible is not written out again. Source is enough to check every rule here; none needs a rendered page.

## What you will see

- **The covering component named** for each element, before it is built.
- **Error copy written as an instruction beside its field.** `Choose a password with at least 8 characters`, not `That password is too short`. `Unable to save. Check your connection and try again.`, not `Oops! Something went wrong.`
- **A filtered empty state:** `No results for "quarterly". Clear filters`.
- **Findings reported to you**, not fixed: copy already in the repo that breaks a rule, a raw hex value, a missing design-system entry.

## Where it stops

- **`DESIGN.md` missing, empty, or unverified in every line.** Nothing UI is written until `design-settle` has run.

Nothing else stops the work: a missing install, a repo with no lint floor, and an absent `review-animations` are each reported or left unmentioned, and the session carries on.

## What it does not cover

- **First-visit page groups** — a landing page, a marketing site, the public front of a product — are exempt from the caps, and their copy is still counted. They speak in the copy voice `DESIGN.md` states for them (`references/first-visit.md`). Without one, the Writing rules apply. The structural rules hold on every register.
- **Copy already in the repo** that breaks a rule is a finding, never rewritten inside another session's work.
- **A second component doing an existing one's job under another name** is invisible to the lint floor. The listing and the read under Components catch it.

## Related

[build-flow](build-flow.md) · [design-settle](design-settle.md) · [app-settle](app-settle.md) · [logic-build](logic-build.md) · [docs-format](docs-format.md)
