# Verification and close — Steps 8 and 9

## Step 8 — evidence, not eyes

Every check leaves something the user can inspect. **A check here or in Step 7 that cannot run** — no data, no sign-in, no tooling — **is reported `not verified — <reason>`, never passed**, and becomes a `docs/queue.md` line (Step 9); one run against a verification double, standing in for data or sign-in, is reported as run on it, and its real-data line stays.

**Run the rendered and driven checks, function parity and the seeded walk on the surface the user gets**: the web → the dev server; a shell (Tauri, Electron) on Windows → the app its own build command built, launched with its webview's debugging port open (`WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=<port>` for Tauri, the same switch on Electron's command line) and reached by `connectOverCDP`; any other Surface → its Proof profile line, else `not verified — <surface>`. A mock of a shell's backend, or its frontend in a browser, serves the canvas alone and verifies none of them.

**The mechanical checks run in three subagents, one per group below, the two that open the browser one after the other** (`SKILL.md`, What a run costs), because a subagent's every call re-reads all it has gathered and the browser is shared. **Brief each with this file's path — Step 8's opening and its own group — plus what the repo does not show: the path this run took, the account it holds, the lines answered at the gate; the two that open the browser also get skill `build-flow`'s Section 5 browser rule. Never retype the checks**, because a retyped list loses some: each returns one line per check per page — verdict, the count or ratio, the evidence path — and fixes nothing. **The session runs the judged checks itself, fixes every failed item in the same session, and re-runs that check.** All of them pass before reporting done.

**A fix that changes what a ratified page renders is applied without a stop and written as one cancellable line at the close** — the page, what moved, the check that ordered it — and that page's pixel diff and keyboard walk run again, the diff's images showing the fix and nothing else.

**Where no canvas was drawn — fix-the-drift, a Keep — a check that reads a canvas file is `n/a — no canvas`**, never `not verified` and never a queue line: the structural diff, the pixel diff, the rendered-structure count, the signature. `Promoted page` reads as every page a repair touched, and each approved finding is re-read at its place — gone, or a failed item; a rejected finding stands and fails no check.

### Mechanical — three subagents

#### From the files

- **The build passes.** It does not → stop, fix it, do not report done.
- **The structural diff per canvas file — the primary evidence**, shared files included under their header's production path. Differences are confined to the data seam (fixture import → data layer plus loading and error wiring; with fixtures kept, the contract-shaped import), the routing seam (a link's target and the parameter a page reads, moved from the canvas's page switch to the app's routes), a block the lint floor refuses in a page, moved whole into the components folder, the removed wrapper and canvas-only instruments, a fix's cancellable line, and lines answered at the gate; anything else is failed. Verdict per file; an unshowable diff is not verified.
- **Zero raw values** across every promoted page and component — search again for hex, font sizes, raw spacing.
- **The lint floor passes, and bites.** Zero hits outside the baseline; each refusal seen refusing its planted violation, reported per refusal, `not enforceable on <stack>` named. Every path in `AGENTS.md`'s `## UI` part resolves.
- **`DESIGN.md` passes the format's linter** — zero errors, every warning listed (`design-md.md`). Not run on a legacy repo's generated copy.
- **Pages running on fixtures are listed by name**, matching the `docs/queue.md` wire lines one for one.
- **Where UI existed — the file plan matched.** Every file an approved gate line names changed, and no file outside the gate's plan did, the documents on `SKILL.md`'s closed list excepted.

#### From the rendered page

- **Run `<plugin folder>/scripts/verify_pages.js` once, for every promoted page at both widths, and write no checking code of your own** — the plugin folder three levels above this file, its usage its opening lines. Its table answers the loaded webfonts, axe-core and reduced motion below, and adds two counts that fail a page: rendered text pairs under their floor, and a page wider than its width. Open only the rows it marks `FAIL` or `n/v`.
- **The pixel diff per promoted page**, taken before its data swap (`pass.md`), its diff images shown.
- **Under a scope narrower than the app — each route the audit walked outside it is captured at desktop width**, its audit screenshot's path beside it. The session reads the pair: the new tokens and chrome landed and nothing else moved. Text that cannot be read, a layout that collapsed or a control that is gone is a failed item — fixed in the shared file that caused it, or written into that group's `docs/queue.md` line where only the page's own file can fix it.
- **Computed styles probed in the browser**: fonts are the loaded webfonts; token slots spot-checked against `DESIGN.md`'s tokens — against the theme files in a legacy repo — so the page shows the source's values, not a drifted copy. (No browser in the Proof profile → its Visual line, naming what could not be verified.)
- **The rendered structure matches, counted.** Canvas and live page in the same dev server; compare each body's element tree (names, classes, and the attributes the canvas source writes — `aria-*`, `role`, `href` — **text and numbers discarded**), one line per page: `canvas n · live n · differs n`. Above zero — outside an `href` at the routing seam, a fix's cancellable line and lines answered at the gate — names the elements and is failed. Unshared chrome is excluded and said; an uncountable page is not verified.
- **Every accessible name on the promoted pages reads in the app's locale**, a library's own included.
- **The design-system route passes its done-check** (`pass.md`), foundations rendered as specimens.
- **Every contrast ratio on the page was computed**, not recalled, for every pair `ratify.md` defines, in every ratified theme mode; every semantic dark shade clears 4.5 against its own light shade.
- **The numbers close** on every page — on its fixtures where it still runs on them, on its real rows where it is wired — totals, percentages, bar widths, pagination (`canvas.md`, Coverage).
- **The detector ran against the running app** (the dev server): hit count beside the audit's where UI existed, every hit listed. A signed-in page is scanned as its rendered HTML saved from the session's browser, stylesheets inlined — never through a session token on a command line; a check only the URL tier runs is `not verified` on that page. `impeccable` absent → the check could not run, never reported passed.
- **axe-core reports no serious or critical violation** on each promoted page, injected into the browser for the check only, never added to the app's dependencies.
- **Under emulated `prefers-reduced-motion: reduce`, nothing on the promoted pages moves**, library transitions included; one the library cannot turn off stands as a finding. **A browser tool with no such emulation runs the stand-in, and its verdict is the check's**: re-add the loaded stylesheets with every `prefers-reduced-motion: reduce` condition forced true, then count the animations still running and the elements still holding a transition — reported as run on the stand-in, with no queue line; motion a library switches from script is `not verified` on that page.

#### By driving the page

- **The UX floor holds on every promoted page**: each interaction on it — form, table, dialog, navigation, feedback — searched in `ui-ux-pro-max`'s UX guidelines, and on a native Surface its stack guidelines, every Critical or High don't listed. `ui-ux-pro-max` absent → the check could not run, never reported passed.
- **Every promoted page's primary flow completes by keyboard alone** on the running app — Tab, the arrow keys a composite widget expects, Enter, Escape — with nothing lost or re-run when focus leaves a field, and every dialog and popover named and closable.
- **Where UI existed — function parity holds.** Every function-inventory line is reachable **at both widths — a control hidden below the breakpoint is a missing function** — unless the user cut it and the gate said so.

### Judged — the session

- **Every listed hit and warning is fixed or left standing with one line why** — detector hits, UX-floor don'ts, linter warnings.
- **Every capture this step and Step 7 took was read by the session**; a visible defect is a failed item.
- **Motion holds `review-animations`' floor** on a web-technology Surface: every animation on the promoted pages read against it, each refusal fixed or left standing with one line why. Not installed → `n/a — not installed`, said aloud.
- **The signature survived promotion** on the pages that carry it.
- **The proving page holds at both widths**, screenshots taken.
- **Where UI existed — the seeded walk.** Seed `[CLAUDE]`-prefixed rows first. Walk the proving page at desktop and the lower bound; compare one page per archetype with its audit screenshot — each reads redesigned unless all behind it was *keep* and the gate said so; where no canvas was drawn, each reads as its screenshot except where a repair landed.

### The canvas after promotion

**A ratified canvas file outlives its promotion as a frozen reference, and dies with its page's real implementation — never before, and never unasked.**

- **Frozen.** Never edit a ratified canvas file again, and never use it as a source of values or patterns — `DESIGN.md`, the theme files, and the promoted page are the sources.
- **Passing checks earn a proposal to delete — never a deletion.** Where real data was wired in-session: report the per-page diff verdict, invite a side-by-side walk at `/design-canvas`, end the turn and ask whether the canvas and seed rows may go — a chat stop, never an AskUserQuestion. Only a granted confirmation deletes page files, entry route, foundations board, canvas CSS and `.design-audit/` together, `.design-audit/gate.md` excepted until the pass's commit is made. The seed rows go only on a yes that names them; kept, Step 9 lists them as `[CLAUDE]` rows still in the database. A refusal or a named page makes that page a failed item now; the canvas stays.
- **Where no canvas was drawn, the same stop asks for what is left** — `.design-audit/`, any file still under `src/design-canvas/`, and the seed rows — once the checks pass, under the same rules; refused, they stay and Step 9 names them.
- **A page left on fixtures, or wired but never seen on real data, keeps its canvas file** until the session that wires it sees it survive both widths, compares page and canvas file, fixes silent divergence, and the user confirms the side-by-side at a chat stop — carried by `build-flow`. The remnants go with the last page file.

## Step 9 — Close

**Nothing stays a draft.** Every canvas page ends promoted into a real route. **A pass this session could not finish is written down, not implied**: every page not yet promoted and every verification item not yet passing becomes a `docs/queue.md` line in `build-flow`'s page shape — a failing item rides its page's line; the canvas stays alive until those lines clear.

One block, a line nothing fills left out:

- the detector's numbers — Step 8's count, beside the audit's where UI existed — and every hit left standing with its one-line justification;
- every `review-animations` refusal, UX-floor don't and linter warning left standing, with its line;
- the `DESIGN.md` lines that changed, where there was an old one · the decision records written;
- files changed, with their count, and files `UNTOUCHED` · every `CLAUDE.md` line naming a file the pass deleted, left for the user to edit;
- each page's fate — promoted and wired, or promoted on fixtures with its `docs/queue.md` wire line;
- items the user rejected — ratified as exceptions, or still standing as findings;
- the product draft's proposals a Keep left undrawn, named once · every need stated at the reading's correction that `docs/product.md` lacks;
- every decision the pass took at the data seam — an error slot, a control disabled during a paid call, retry wording — and every Step 8 fix that changed a ratified page, one cancellable line each; a cancelled one is redone to what the user says and its Step 8 checks re-run, in a commit of its own;
- the canvas outcome and how many rounds it took · the verification results, per-page diff verdicts included;
- the canvas files still standing and the queue line that will retire each · `.design-audit/` and `[CLAUDE]` seed rows still standing;
- the `/design-system` route named as staying dev-only, deletable at the user's word;
- the lint floor — refusals written, the baseline's size, anything `not enforceable`;
- what is still `[needs verification]` · every conflict the Step 1 reading named, with its `docs/queue.md` line where the pass depends on it;
- **the documents `app-settle` still owes**, where they were missing — `build-flow` will not open a page until the Roles and the rules exist.

State that this gate **no longer applies** to later pages — from here on `DESIGN.md` and `ui-build`'s component rules bind.

**Commit by the session norms' `GIT` block, once, with nothing else in it** — where UI exists on the pass's branch, its message body the gate block from `.design-audit/gate.md`, which goes once that commit is made; where none exists on the current branch, its body the `DESIGN.md` sections and decision records written. Merging is the user's move.

Nothing changed — nothing approved at the gate, or the canvas reverted → say so in one line and list the audit findings that remain.
