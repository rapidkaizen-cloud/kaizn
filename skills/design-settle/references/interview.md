# The interview and the install gate — Steps 3 and 4

**The order is fixed:** the non-visual dialogs (the stack, four product calls) → the reference search and `ui-ux-pro-max`'s generator → the direction question → the install gate → the frames (`frames.md`). **Every dialog only locks an answer: nothing is installed before the gate, and no value of the look is asked after the pick.** Everything else is Claude's call, reported as a cancellable line (What the designer settles).

In Fast the dialogs are answered, not asked (`SKILL.md`, Fast or Full).

## Where options come from

- **Invent every option for this app**, from the corrected Step 1 reading — the kind of app, the platform, who uses it. No fixed option list exists anywhere; `ui-ux-pro-max`'s data is the one outside source, and anything taken from it is argued for this app like an invented option.
- **Name each option in plain words, its consequence in parentheses**, written fresh. This file holds no sample phrasing, because a written example gets copied.
- **Replace any option you cannot argue in one line from this app's documents or platform.**
- **Mark one real option "(Recommended)"**, first, with its reason from this app. `Decide for me` is never the recommendation.
- **A want the user stated — at invocation or at the reading's correction — outranks a rubric's ranking rule**: the option that meets it is the recommendation, the shift named in its reason.
- **Always accept an answer outside the options.** A package named there is verified the same way and used; state its consequence if known, or say it is not.
- **Off the web, the vocabulary changes first** (Non-web platforms). On a cross-OS shell (Tauri, Electron, Flutter desktop), read the target OS from where the Roles' users sit; pin it at the Step 1 correction where the documents do not settle it.

**Single-select, except the multi-select direction question. Batch four dialogs per call, fewest calls possible**; a dialog whose options read an earlier answer rides a later call in the same turn:

| Call | Dialogs |
|---|---|
| 1 | component library · supported widths · theme mode · copy voice |
| 2 | styling (where the library brings none) · icon pack (where it bundles none) · the two frame screens · one engine dialog per triggered category |

Past four dialogs, a third call in the same turn. Reconcile after every call: two answers that collide go back as one question naming both.

## Part 1 — the non-visual dialogs

### The product draft, before the stack

**Draft the full product first**, so the engine triggers it implies fire now: page by page, one line per feature, from `docs/product.md`, `docs/rules.md`, `docs/glossary.md` and domain knowledge — the product-type research `build-flow` Section 4 rules is its floor, never its ceiling; where UI exists the floor is `handover.md`'s function inventory. A need the user stated at the reading's correction — a feature, a page, a role — is a line of the draft, and is named at the close as a line `docs/product.md` lacks. Where UI exists, append the draft to `.design-audit/handover.md`, so any later session or subagent that draws reads it. It is drawn, tagged and cut at Step 5.

### The stack — one dialog per decision, installed at the gate

- **Where UI exists, a stack part the audit does not indict is not asked.** The library, the styling, the icon pack and each engine are one cancellable line each — `Keep — <what is installed> · the audit indicts nothing in it` — printed in chat above the interview's first call in Full, among the pre-answers in Fast; a cancelled line opens that dialog with *keep* first. In Full a line is cancelled by naming it under Other of any dialog in that call, or in chat. An indicted part is asked, *keep* among its options and never the recommendation; an icon pack indicted for two families offers each family alone and never both, the one more files import first and recommended.
- **Under a scope narrower than the app, nothing leaves the stack**: the pages outside it still import the library, the styling, the icon pack and each engine, so each is a `Keep` line that cannot be cancelled. An engine may still be added, and an indicted part is a finding the close names for a whole-app run.
- **Component library** — read `library-rubric.md` when this dialog is asked: 3–4 options, *own components* always one.
- **Styling** — **ask only where the library brings no styling system** (*own components*, headless). On the web **recommend Tailwind CSS**, plain CSS always an alternative. A library with its own styling (theme object, CSS-in-JS, own CSS layer) decides it without a dialog; one built on Tailwind (shadcn, HeroUI and kin) settles it as Tailwind; report either with the library it came from, cancellable. Off the web there is no Tailwind default: styling follows the platform, and a dialog opens only where the platform leaves a real choice.
- **Icon pack** — ask only when the library bundles none; recommend a pack already installed. The pack `ui-ux-pro-max`'s icon search names may be one option, verified like the rest, never with its fallback family. **One icon family per app, no exceptions** — a missing icon is a finding, never a hand-drawn SVG or a second family.
- **Engines** — no standing dialog. Read `engine-rubric.md` only when the user, the documents, or the product draft name a rendering job the component library does not ship — a chart, a heavy table, a date picker, drag-and-drop, an editor, an upload — or the audit indicts an installed engine.

**Verify the recommendation of every stack dialog before it is asked, in one subagent pass** (`SKILL.md`, What a run costs): hand it the rubric files and the candidates; it returns one line per candidate, as the rubric's verification duty names. **Offer every other option from model knowledge, marked `unverified` in its description, and verify it only when it is picked** — one pass for everything picked. A pick that fails verification re-opens that dialog once, naming what failed; a second failed pick re-opens nothing — the verified recommendation applies, as a cancellable line naming both failures.

**The family rule.** The decision records name logic-layer choices with their families (`TanStack Query — TanStack ecosystem`). A candidate from an already-installed family that passes the rubric rises to the recommendation, and the shift is named ("recommended also because Query is already installed"). It moves the recommendation, never removes an option.

### Four product calls — each with Claude's recommendation

Derive each recommendation from the reading and the Roles — who uses the app, when, where, on what — reason in its description. End each dialog with `Decide for me`: the derived value applies, reported as a cancellable line.

- **Supported widths** — phone, tablet, or desktop only, as the lowest width to hold. A field or phone role pulls it to phone; an all-desk cast keeps desktop. Off the web, use the platform's unit, consistent with the Proof profile's Bounds line. The desktop judged width becomes `DESIGN.md`'s desktop breakpoint; name both widths in the canvas assumptions block and take round-1 screenshots at them. **State the lower bound in `DESIGN.md`, so anything below it is *unsupported rather than broken*.**
- **Theme mode** — light, dark, or both following the system; a manual toggle arrives only through Other (a night shift argues for dark). **The answer binds every frame and the canvas**; with both, draw the frames in the mode the primary role works in. With two modes, prove the second on the foundations board and `/design-system`, compute every contrast pair in both, and record the modes in `DESIGN.md`.
- **The two screens the frames are drawn on** — offer 2–4 real pairs, `<proving page> + <second screen>`, from the Roles and `docs/rules.md` or, where UI exists, `handover.md`'s routes. The recommended pair leads with the page carrying the most of this app's own subject — chosen for what the user will see, never for how many controls or fields it holds — plus the screen of the archetype least like it, where a direction that suits the first most likely breaks.
- **Copy voice** — formal, neutral, or casual, and where the language has several forms of address, which (Indonesian: *Anda* or *kamu*). Where a first-visit page group earns a looser voice than the pages behind login, ask per page group. The answer is the copy voice in `DESIGN.md`'s Overview, read by `ui-build`'s Writing section. Read `ui-ux-pro-max`'s `brand` voice reference, located through that sub-skill's `SKILL.md`, before writing the options; never run that sub-skill.

## Part 2 — the reference search, then the direction question

### The reference search

**Run it once, in a subagent** (`SKILL.md`, What a run costs), briefed with the corrected reading and — where UI exists — `handover.md` alone: it searches the app's job, never its current look.

- **It finds real products** in this app's domain and platform — product sites, app-store pages, docs showing the product's own screens, galleries of shipped screens. **Concept shots (Dribbble, Behance and kin) are not references.** The platform scopes the search: a Windows tool is not answered with web SaaS.
- **It returns** 3–6 products — name · link · one line on what its screens show — and how many the search returned. Only links the search returned.
- **Show in chat, before the dialog**: each product with its link and one line on what this app could take from it, grouped into **2–4 directions**, each named on an axis sayable in a sentence, and the count in one line.
- **Fewer than three products, one without links, or WebSearch unavailable** → say so in one line, name products from model knowledge without links, mark the set unverified, and still ask the direction question. Never pass that set off as the search's result.

### `ui-ux-pro-max`'s generator

**Run its design-system generator once, after the search**, with a query built from the corrected reading — kind of app, domain, who uses it. Take its commands by searching its `SKILL.md` for `search.py`, never by reading the file whole, and **never pass `--persist`**. Its results are frame ingredients (`frames.md`), never a direction by themselves.

### The direction question

One AskUserQuestion, **multi-select**:

- Where UI exists, **`Keep — today's look`** first, its consequence in its text: ticked, the running app stands among the frames at its real routes, never redrawn. Never the recommendation.
- The **search's directions**, as many as fit — three, or two beside Keep — one "(Recommended)" with its reason.
- **`Decide for me`** last: Claude composes the set. No tick at all reads as this one.

The question text says, in the user's own words: *tick what appeals — it is inspiration, not a template; I draw 2–4 directions and you pick on screen. If you want one of them followed closely, say so in your own words under Other or in chat — it then gets a frame of its own drawn closely to it, and the finished design is checked against it point by point. A product the list missed, a screenshot, a URL: under Other — for a picture, answer "screenshot" and paste it in chat.* Read a screenshot or reachable page and take its numbers — density, type character, colour temperature, motion budget — before the first frame; never its code or its identity.

**A tick is inspiration, never an anchor.** A reference becomes the **stressed reference** only when the user stresses it in their own words — follow it closely, strictly, or as the main reference — never from a tick, a recommendation, or a product named under Other without that emphasis.

**A reference sets direction, never reproduction.** Refuse imitating a company's distinctive interface however phrased, and never offer an option amounting to it. **Followed closely means the rows the judgement lists against a stressed reference** (`canvas.md`, Judging) — its density, colour temperature, type character, motion budget, shell shape, how a recurring control is rendered. Its name, mark, illustrations, and a screen reproduced element for element stay refused, and its frame's motivation line says so.

## Step 4 — the install gate

**Its own chat stop, after the direction question and before the first frame — never inside an AskUserQuestion.** It holds only what the locked answers decided — in Fast, under the pre-answers; a reply changing an answer rewrites that line and re-shows the block. Present it, end the turn, wait for the reply.

```
Will install:
  npm install
  <component library>          [the library answer — nothing where UI exists and it was kept]
  <styling>                    [the styling answer, or what the library brings]
  <what the library omits>     [researched for the picked library under library-rubric.md]
  <icon pack>                  [bundled by the library, or the icon answer]
  <engines>                    [chart · table · date · drag-and-drop — only what an
                                engine dialog decided, nothing speculative]
  <linter>                     [only where the repo carries none — Step 7's lint floor is
                                written into it]
```

- Refused → hand over the commands for the user to run, then wait. Nothing to install → in Full, say so in one line — with what leaves, where UI exists — and continue without the stop: a removal is authorized at the Step 6 gate, never here.
- **Install nothing outside the block**; something extra → ask again. The font is the one exception (`ratify.md`).
- **Where UI exists, the block also says what leaves** — removed in the pass, never here — and every approved package is appended to `handover.md`'s UI stack line before the first frame, because the frames are drawn against that line.

Approved and installed → `frames.md`.

## What the designer settles

Everything beyond the dialogs is Claude's call on the canvas, one line each in the design plan, the assumptions block, or the ratification value report (Steps 5 and 6). **`Decide for me` is a real answer and never silent**: name what Claude chose in each frame's motivation line and in the ratification report. Any line may be cancelled, opening that value as a normal dialog — where UI exists, with `Keep today's value` first; picked, that one value is read from the styling files (`SKILL.md`, Blindness), and every other old value appears only at the gate. **A value a floor forced is the exception**: one line naming the floor and the value it replaced, never cancellable.

- **The picked frame's values** — palette and accent, surface, density, typography, motion, shell — read at ratification, never re-asked. **Motion honours `prefers-reduced-motion` whatever was drawn.**
- **Contrast** — WCAG AA floor (4.5:1 text, 3:1 non-text), from `impeccable`'s Verify list; off the web the platform's bar where stricter.
- **Status colours and markers.** **Colour is never the only marker** — an icon, label, or shape rides with it.
- **Text scale, spacing scale, hover steps** — read at ratification.
- **Tables, feedback placement, confirmation guards, form layout, validation timing** — the platform's conventions (a desktop app follows its OS), on the web the chosen direction. Always: an irreversible action gets a confirmation, permanent mass-deletion a stronger one, and **a placeholder never replaces a label**.
- **Copy on controls and labels** — in the answered voice, judged on the canvas in the app's on-screen language (`CLAUDE.md` Locale row); where UI exists, against the audit's measured label and supporting-text counts. An icon-only control carries its verb in `aria-label` and a tooltip; a destructive confirmation and a page's primary action are never icon-only.

**A correction that collides with the pick goes back as one question** (a brand hex under Other failing contrast on the picked frame's ground): name both sides, offer keeping either and a named middle path where one exists, with a recommendation. The resolved answer replaces the original before anything downstream reads it.

## The archetype table

**Group first, fill after the pick**, never page by page. Before the frame screens are asked — at Step 1 where UI exists, from the routes — group every page the Roles and `docs/rules.md` imply into **screen archetypes**, usually 4–7 (auth, dashboard, data table, form, wizard, detail/approval; on a landing page the unit is the section — hero, benefits, pricing, social proof, CTA/footer), and show the grouping once as a report for correction, never a dialog per row and never adopted silently: print it above the next AskUserQuestion call, take a correction naming a row under Other there or in chat, and let it stand as shown where neither names one. Every route lands in exactly one archetype; a page fitting none goes to the user as its own question, never a silent bespoke layout. Once the frame is picked, fill each row: shell layout in a sentence, components, density, empty wording — the shells settled at the canvas judgement (Step 5); in fix-the-drift and on a Keep pick, from `audit.md`, its screenshots and the pages themselves at Step 6. Write the ratified table into `DESIGN.md`'s Page Composition — at repair scale in fix-the-drift and on a Keep; `build-flow` Section 4 names the archetype in every later page proposal.

## Non-web platforms

Substitute the vocabulary before any option is written: **design language** — one frame in the target OS's own, named as such; **unit** — the platform's own (window minimum size, size classes in dp), not the CSS pixel; **shell** — one frame carries the platform's navigation model, not sidebar-or-top-bar; **search** — applications on that OS, not web products.

## What is not asked

Loading, empty state, and error placement, and the structural writing rules (button and link text, capitalization, toggle labels, error phrasing, the tone table), are fixed in `kaizn`'s `ui-build`; only the voice varies per app. **Copy length is capped by `ui-build`'s copy caps**, on tenth-use pages; first-visit page groups are exempt. `build-flow` prints each page's longest and median.
