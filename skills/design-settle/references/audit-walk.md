# The audit, from the running app — the second of two subagents' briefs, where UI exists

You walk an app a first subagent has already read from its source. Measure what the app renders, for a session that will redesign it **without ever seeing it**. Change nothing in the app: submit no form, and click nothing that creates, changes or deletes a row. Read no page file, and not the first subagent's brief. Run independent commands in one turn.

You are handed the repo root, the scope, and the account that signs in, which you write into no file. Create no account.

## What you open

- **The routes under `## Routes for the walk` in `.design-audit/audit.md`** — read that section alone, by its heading: one of each kind of page inside the scope, and one of each kind outside it. A route that will not open is named in your report with why, and another of its kind is opened from the router where one exists.
- **The app** is started by the Proof profile's Run line in `docs/product.md`, or by the repo's own dev command where it has none — unless you are told it is already running.
- **The browser** is the one skill `build-flow` Section 5 drives every browser step in — read that rule alone.

## How you measure

**Measure with the function in `<plugin folder>/scripts/audit_measure.js`**, the plugin folder three levels above this file, and write no measuring code of your own.

- **Paste it once, on the first route**, whole, into one evaluate call: `() => { const M = <the file>; window.name = M.toString(); return M(); }`.
- **On every later route call what `window.name` kept**, which survives navigation: `() => (0, eval)('(' + window.name + ')')()` — with `('pairs')` for a second theme mode, and `('focus')` once for the focus ring. A page that refuses `eval` gets the function pasted again.
- **It returns** the contrast pairs with their ratios and floors, and the component values, each with how often it rendered.

## What you write

- **A screenshot of every walked route at desktop width**, per the Proof profile — 1440px where it names none — saved under `.design-audit/`.
- **Into `.design-audit/audit.md`, without reading the rest of it**: the three block rows that read `pending — the walk`, replaced in place, and three sections appended at its end — `## Component measurements`, `## Contrast pairs`, `## Screenshots`.

```
Walked              : [each route opened, with the kind of page it stands for · inside the scope
                       or outside it]
Component values    : [how many items read on the walk · how many `from source` · how many
                       rendered differently from place to place]
Contrast pairs      : [how many read on the walk · how many `from source` · how many under
                       their floor]
```

Nothing you measure goes in `handover.md`.

## How each part is read

- **The component measurements** — one line per item of the component-token table, as the `## Components` row of `design-md.md` beside this file lists them, for each whose component the app has: what the function returned on the walked routes — off the web, what the platform's own tooling reads — and the route it was read on. An item rendered differently from place to place — on the walked routes, or by an override a search of the source finds — lists each value with its files. An item the walk cannot read — the app not run, a dialog never opened, a native Surface — is read from the shared components' source and the library's theme, marked `from source`.
- **The contrast pairs** — one line per distinct pair the function returned, in each theme mode the app holds: the foreground colour, the background it sat on, text or non-text, its WCAG ratio, its floor — 4.5:1 for text, 3:1 for large text and non-text — and one route it was read on. A pair the walk cannot read is taken from the styling files and the shared components' source, marked `from source`.
- **Where `DESIGN.md` is written**, a measurement off its value in the component-token table is a deviation, marked so on its line.
- **App could not be run, or no credentials → say so in the report**, write `Walked` as `none — <reason>`, and read every item and pair `from source`.

## What you report back

Only this, never a word on the look: whether the running app was walked, and why not where it was not · the routes walked, each with its kind · the three rows' counts · a pair under its floor whose two colours come from a package's own stylesheet, as an indictment of that package · the deviations counted, where `DESIGN.md` is written · the screenshot paths.
