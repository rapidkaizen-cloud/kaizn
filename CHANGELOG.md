# Changelog

All notable changes to the `raizen-norms` plugin, and to `raizen-hub` until 0.70.0 merged it in, newest first. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions before these are in `git log`.

## [raizen-norms 0.101.0] - 2026-10-13

The publishing stop is a gate, not a lock. In a real app a question typed between the stop and the yes brought the whole stop a second time: `guard_git` counted only a reply to the very message that named the command, and the session's answer to the question did not name it again. The hook now proves that the stop happened and leaves the reading to the session, as the gate was meant since 0.74.0. The price: a push that was shown and never run stays open, so telling a yes for it from a yes for something else is the session's.

### Changed

- `guard_git`, `git push`: a push passes once the session ended a turn on the command and you replied, whatever is typed after — a question, its answer, then your yes are one stop. Still one run per stop.
- `guard_git`, `gh pr merge`: held as before, and now the only command held to the reply itself — it is what reaches production, so a question in between needs the command put again.
- Session norms, `GIT`, and the hold's message: say what a question leaves open, a push, and what it does not, a merge.

### Removed

- `guard_git`: the hold on `gh pr create`. Opening a pull request publishes nothing a push has not, `gh` with no prompt to answer stops on a branch that is not pushed, and the hold caught `gh pr create --help`. The norms keep the rule: a pull request is opened only when asked.

To act on:

- Nothing. From this version a session opens a pull request you asked for without a stop; it still stops for the push before it.

## [raizen-norms 0.100.0] - 2026-10-13

The project pin is gone. `guard_project_ref` refused a Supabase MCP call aimed at a project other than the one `supabase/config.toml` declared. The account-wide Supabase MCP server it existed for is no longer in use where this toolkit is developed, and in the transcripts on hand it had refused no call in an app.

### Removed

- `guard_project_ref`, its self-check and its page: no hook reads `supabase/config.toml` any more, on either host.
- `app-settle`, bootstrap and document modes: `supabase/config.toml` is no longer written, and the close no longer asks for the project ref.
- `app-settle`, audit, C4: a `project_id` that is not a hosted project ref is no longer a finding.

To act on:

- An app on Supabase Cloud: after this update nothing pins a Supabase MCP call to the repo's project — a call reaches whichever project it names. `supabase/config.toml` may stay; nothing reads it.

## [raizen-norms 0.99.0] - 2026-10-12

A session tells you it has grown large when it has, measured. The line 0.98.0 removed was said after every commit because a session cannot read its own size; a hook can, from the usage the transcript records. The milestones are a judgement from the cost of a call — a fresh session starts near 80k tokens — not a measured saving.

### Added

- `remind_context.py`, carried by the document reminder's hook on Claude Code: at the first commit after the context passes 200k, 500k or 800k tokens, the session is handed the size and tells you in one line that the next item costs less in a new session. Once per milestone, silent in between, and nothing on Antigravity.

To act on:

- Nothing.

## [raizen-norms 0.98.0] - 2026-10-12

The new-session line is gone. Since 0.82.0 a turn that committed ended by telling you to start the next item in a new session. A session cannot read how full its context is, so it said so after every commit — in a session that had barely started as in a long one — and a line said every time says nothing.

### Removed

- Session norms, `GIT`: the line after a commit that told you to start the next item in a new session. `design-settle`'s two session breaks are unchanged.

To act on:

- Nothing.

## [raizen-norms 0.97.0] - 2026-10-12

Align stops once for the destructive findings you picked. Each finding is its own commit, so each rename went through the destructive gate alone — and 0.96.0's one block for operations approved together left it unsaid whether findings join one. Read from the rule's text; no session has run Align with two destructive findings.

### Changed

- `app-settle`, Align, A4: several picked findings that are destructive are counted and shown at one stop, a `DESTRUCTIVE` block each, before the first finding starts. Each approved one still runs in a guarded block and a commit of its own.

To act on:

- Nothing.

## [raizen-norms 0.96.0] - 2026-10-12

The destructive gate stops once for one request. `db-ops` described one `DESTRUCTIVE` block and one stop, and said nothing of a request that needs several operations — deleting a row and its children — so each could get a stop of its own. This is read from the rule's text, after the push gate showed the same shape: no session was seen stopping once per operation.

### Changed

- `db-ops`, Destructive operations: several operations one request needs are shown at one stop, a block each with its own numbers, and the session runs only those your reply approves. They run in one `DO` block with a check each, so a count that misses on one aborts them all.
- `guard_destructive`: the refusal names the one stop. What it refuses and lets through are unchanged; its self-check now pins several operations in one block.

To act on:

- Nothing.

## [raizen-norms 0.95.0] - 2026-10-12

A push and its pull request share one stop. Asked for both, a session stopped for the push, ran it on the yes, then stopped again for the pull request — the same question twice. `guard_git` already let two commands put in one message each run once on the one reply; the norms never said to put them together.

### Changed

- Session norms, `GIT`: where the request needs several held commands — a push, then its pull request — the session puts each in the one message on a line of its own, and runs only what the reply clearly says yes to. One reply covers one run of each.
- `guard_git`: the held message says the same. What it holds and what it lets through are unchanged; its self-check now pins two commands in one message on both hosts.

To act on:

- Nothing.

## [raizen-norms 0.94.0] - 2026-10-10

`audit_count.py` prints three rows more. The audit that ran with the script at 0.92.0 still wrote scans of its own in a real app — six commands, at 169k to 189k tokens of context — for the tokens nothing reads, the icon sizes and the label lengths. Run alone on that app, the script now prints what those scans had counted. No audit has run with the new rows, so the saving is not measured.

### Changed

- `scripts/audit_count.py`: `Token health` — the tokens never read, the tokens read only where a config or another token maps them, and one colour under several names, per block · `Icon sizes` — the sizes and weights of every element of an imported icon, the scope's beside the whole app's · `Repeated labels` — longest, median and the labels repeating within a file, over the scope's files, translation keys left out.
- `design-settle`, the audit's block: `Token health`, `Icons` and `Repeated labels` are copied as the script prints them; the library slots unmapped stay the subagent's count, and a row printed `not counted` is counted by a command of its own.

To act on:

- Nothing.

## [raizen-norms 0.93.0] - 2026-10-10

Four rules for the logic layer, from one real app. A read-only audit of it — 14 subagents over its source and its migrations — found faults `logic-build` did not name: a returned error left unread in 8 of 14 slices, and an unpaged read behind a row cap in 6. One audit, read from code and proven by no test or query, so the counts are an observation.

### Added

- `logic-build`: uniqueness is a constraint, never a check before the insert; a call that returns its error is read for it at the call site; a list read pages wherever the API caps rows; a bug fix leaves the test that fails without it.

To act on:

- Nothing.

## [raizen-norms 0.92.0] - 2026-10-10

`design-settle`'s audit counts and measures with two scripts the plugin ships. Two audits of one real app, each counting by commands of its own, read the same rows two ways — the files a token change touches came out as 793 and as 616 — and each wrote its own scan script and its own measuring code. With the scripts, a third audit of the same scope took 128 calls and 17.8 million input tokens — 9.9 for the source, 7.9 for the walk — and 29 minutes, where the two before took 23.3 and 21.3 million. One run each, so the difference is an observation, not a rate.

### Added

- `scripts/audit_count.py`: counts over the whole source what sits outside the tokens — hex, colour functions, font sizes, spacings, numbered ramp classes — the files holding them, the imports, the icon families and the packages nothing imports, and writes `places.md`. The audit's first subagent runs it once and copies its rows.
- `scripts/audit_measure.js`: one function the audit's second subagent pastes into the page once and calls on every route — the contrast pairs with their ratios and floors, and the component values.

### Changed

- `design-settle`, the audit's block: `Stray raw values` adds colour functions and numbered ramp classes, and `Components affected` is the files holding a value the tokens do not reach — both as the script prints them.
- `design-settle`, the audit: the first subagent is handed the page-group list instead of counting it again, and runs the detector's command once — an error is `n/a — not installed`, and no other copy is looked for.

To act on:

- Nothing. Both scripts need only what the plugin's hooks already need: `python3`, and the browser MCP server.

## [raizen-norms 0.91.0] - 2026-10-10

`design-settle`'s audit runs in two subagents. Under a scope of 8 page files in one real app, one subagent took 111 calls and 23.3 million input tokens, half of them after its walk, at a context above 237k. Split, the same audit took 140 calls and 21.3 million — 10.4 for the source, 10.9 for the walk — and 37 minutes where it had taken 24, and it measured 118 contrast pairs where the one subagent measured 61. One run each, so the difference is an observation, not a rate.

### Changed

- `design-settle`, the audit: two subagents, one after the other. The first reads the source — the counts, `places.md`, `handover.md`, the inventories — and picks the routes to walk; its brief is `references/audit.md`. The second walks the running app — screenshots, component measurements, contrast pairs — and adds them to `.design-audit/audit.md`; its brief is the new `references/audit-walk.md`, and it reads no page file.

To act on:

- Nothing.

## [raizen-norms 0.90.0] - 2026-10-10

`design-settle` on an app with existing UI is bounded by a scope. Its audit opened every route and read every page in one subagent, with no limit: in one real app of 696 page files — about 2.3 million tokens of page source — it cannot finish, and the five audits tallied so far each opened at most one route, signed out, in a copy of one small app. The audit alone has run under a scope, once, in that app (`docs/reference/status.md`); no session has run the other rules below.

### Added

- `design-settle`, Step 1: where UI exists and the app has more than one page group, you are shown the groups with their page counts and asked the scope at a chat stop, in Fast too — the whole app, or the groups this run redraws. Every page in scope is read, drawn, promoted and checked.
- `design-settle`, the gate: under a scope narrower than the app its first lines say what changes for the rest — the styling files and the shared chrome for every page — and name each page group left out with how many of its files hold a finding. A file only those pages import is `UNTOUCHED`, never deleted.
- `design-settle`, the pass: one `docs/queue.md` line per page group left out that holds a finding, cleared by a later run scoped to that group.
- `design-settle`, Step 8: each route the audit opened outside the scope is captured again and read beside its audit screenshot; unreadable text, a collapsed layout or a missing control is a failed item.

### Changed

- `design-settle`, the audit: counts and `places.md` come from commands over the whole app, never from a page file printed to be counted in; page files are read in the scope only; the walk opens one route of each kind of page inside the scope and one of each kind outside it, where it opened every route. Screenshots are of the walked routes. The frame inventory is read from the page files, a walked route checked against what it rendered, and the gate's removals open with how many routes were walked — `frame coverage unverified` is gone.
- `design-settle`, the stack: under a scope narrower than the app no part is asked or cancelled, because the pages left out still import it. An engine may still be added, and an indicted part is named at the close for a whole-app run.

To act on:

- Nothing in an installed app. A run on an app with one page group is not asked the scope; on any other, answer `whole app` to redesign every page as before.

## [raizen-norms 0.89.0] - 2026-10-08

Two cuts to what a `design-settle` run costs, decided from the token count of one close at 0.87.0: 25.5 million input tokens, 18.5 million of them one subagent whose context grew from 32k to 267k over 120 calls. Every check stays. No session has run either cut, so the saving is an estimate.

### Changed

- `design-settle` ends its turn at two seams and asks you to run it again in a new session: once the documents are written, and after the pass, before the checks. It first writes `.design-audit/resume.md` — the path taken, the account held, the lines answered or cancelled, the canvas rounds — and the next session reads it at the leftover question. A reply in the same session continues there. One session carried the drawing through every call of the pass and the checks.
- `design-settle`, Step 8: the mechanical checks run in three subagents — from the files, from the rendered page, by driving the page — the two that open the browser one after the other. The checks and their wording are unchanged.

To act on:

- Nothing. A run stopped at a seam leaves its tree uncommitted, as a pass stopped at a seam already did.

## [raizen-norms 0.88.0] - 2026-10-08

Four decisions that two runs of `design-settle`'s Steps 8 and 9 on 0.87.0 left owed, each answered as recommended, and the start page's advice on the model widened to that skill. No session has run them: the local plugin file alone was seen refusing its planted violations, in the proof app on oxlint 1.87.0.

### Added

- `design-settle`, Step 8: a fix that changes what a page you ratified renders is applied without a stop and listed at the close as one cancellable line — the page, what moved, the check that ordered it — and that page's pixel diff and keyboard walk run again. A session closed touch targets and a detector hit on three pages, which then no longer matched their canvas, and no rule said whether to apply the fix, stop or queue it.
- `design-settle`, Step 8: where the browser tool cannot emulate reduced motion, the session runs a stand-in — the stylesheets' reduced-motion rules forced on, then the running animations and standing transitions counted — and reports the check as run on it, with no queue line. Chrome DevTools MCP 1.10.1 has no such emulation: two sessions reported `not verified`, and one wrote a queue line no later session could clear.
- `design-settle`, the lint floor: a linter with no rule for a refusal gets one local plugin file its config loads, and that file is on the skill's closed list of writes. In an app on oxlint one session left three of the four refusals unwritten, and another wrote them as a plugin file the list did not allow.

### Changed

- `design-settle`, Step 8: the structural diff and the rendered-structure count allow the routing seam — a link's target and the parameter a page reads, moved from the canvas's page switch to the app's routes — and a block the lint floor refuses in a page, moved whole into the components folder. The diff failed on six files of one promotion for these, and neither session that met the failure gave it a queue line.
- `docs/start/quickstart.md`: the advice to run on Opus covers `design-settle` as well as the sessions that build pages.

To act on:

- Nothing.

## [raizen-norms 0.87.0] - 2026-10-07

Three decisions the runs of 0.86.0 left owed, each answered as recommended, and one chain line corrected from the sessions that ran them. Run in throwaway clones the same day: the first two decisions held on Sonnet, and so did the corrections of 0.86.1 to `design-settle`, `review-animations` excepted, which no session showed. `build-flow`'s todo list, proposal and audit offer, and the material on a new page, held together in one session on Opus; of two on Sonnet, each dropped at least one of the three and neither read all of the material.

### Added

- `design-settle`: where the repo has no `docs/queue.md`, the session creates it for the lines its pass and its close leave, in the shape of a queue that never split its work and with no approval stop of its own — the gate and the close already show the lines. Two sessions ended with lines owed, wrote no file because `build-flow` gives a new queue an approval stop, and listed them in chat for you to add.
- `design-settle`, Fast, where UI exists: the direction line says that cancelling it offers `Keep — today's look`. Fast pre-answers the direction with `Decide for me`, so nothing named Keep; a Keep typed at the pick was honoured after three frames had been drawn and deleted.

### Changed

- `ui-build`, the material: the load is mandatory for a session that writes a new page or a new component — a new file in the pages or the components folder, whatever pattern it repeats. An edit inside a file that stands may skip a row, and the close says why. Of four sessions that wrote UI, three had read none of it, one of them for a whole page.
- `build-flow`: the first step of a page's chain is the proposal with its two lists. A session named the archetype, asked three questions about rules and counted the proposal as made; it then decided sorting and a drill-down alone.

To act on:

- Nothing.

## [raizen-norms 0.86.1] - 2026-10-07

Corrections from seven sessions that ran the rules of 0.85.1 and 0.86.0 in throwaway clones, all on Sonnet — one headless, six on a scripted `sdk-ts` host that answers a dialog, five of them with a headless browser. Each was written from what a session did. The first two were run again on Sonnet and held; the rest were read on paper by a Sonnet subagent answering case questions, three sentences rewritten after it, and run by no session since.

### Fixed

- `build-flow`: the content proposal is the first step of a page's chain, so it lands in the todo list the session writes, and the audit offer is that list's last entry. A session wrote no todo list, built a page whose filters and summary row it decided alone, and closed without offering the audit; the order sentence of 0.85.1 changed nothing, because the proposal never ran. Run again: the proposal came as its multi-select before the contract was written.
- `app-settle`, the audit: a line of `CLAUDE.md` counts as a copy of a plugin norm only where the plugin line rules every case the file's line rules, and every skill and command name in the file is checked against the plugin's skills. An audit listed "no dependency without approval" as a copy, citing a `logic-build` line that rules one layer and an `app-settle` line that rules one mode, and align deleted it again; it also missed the name of a skill merged away. Run again: the line was counted apart and the name found.
- `design-settle`, the audit: the detector runs with `--json`. A clean scan printed nothing, the audit read the silence as an absent detector, and the session reported `n/a — not installed` through to its close.
- `design-settle`, Step 0: `review-animations` is looked for on disk, never in the skill list. Two sessions reported it not installed; it was.
- `design-settle`, Step 8: the subagent that runs the mechanical checks is briefed with `verify.md` itself. A session retyped ten checks into a brief of its own, and the checks that read a canvas, the UX floor and the accessible names were never reported — neither run nor `n/a — no canvas`.
- `design-settle`, the gate: the reason for a line kept on purpose is asked for in Fast too. A session wrote `[needs verification]` in its place.

### Changed

- `design-settle`, the audit: its list of places is `.design-audit/places.md`; it was `findings.md`. Claude Code refuses a subagent's write of a file named `findings.md`, `report.md` or `summary.md`, so in two runs the file was never written and the gate searched the code for every place again.

To act on:

- Nothing. `.design-audit/` belongs to one run, and the next audit writes it again.

## [raizen-norms 0.86.0] - 2026-10-07

Four decisions the runs of 0.85.0 left owed, each answered as recommended. Written from what a session did where no rule stood. Checked on paper by a Sonnet subagent answering case questions; five sentences it read two ways were rewritten and not read again. No session has run them.

### Added

- `build-flow`, the queue: a batch asked for while `docs/queue.md` holds lines of the other kind — a UI batch above `Prove:` lines — is written as a block of its own above them, with its own title and header. A session builds the first block, and a block that runs empty is deleted with its title. A session had put UI lines under the standing header, which is where the running batch is read from.
- `build-flow`, the walks: where the app has a sign-in and the session holds no account for it, you are asked once, before the first page is written, which account the walks sign in with — one created through `db-ops` (recommended; a login and a role row written to the app's database), or one you supply. A session wrote a page, could not reach it, and stopped with the tree dirty.
- `design-settle`, fix-the-drift over a written `DESIGN.md`: a finding only a new value would repair — a colour under the floor `DESIGN.md` states, a detector hit on a font it does not name — is listed under `OWED`, never as a `REPAIR` item, and asked once: kept on purpose as an exception line, or left for a redesign, which is recommended for a value under a floor.
- `ui-build`, the material: the closing block names every row that applied to the edit — read, or skipped with why. Three Sonnet sessions wrote UI without reading any of it, and one said so.

To act on:

- Nothing. A `docs/queue.md` holding two kinds of lines under one header is rewritten into two blocks by the next session that adds a batch.

## [raizen-norms 0.85.1] - 2026-10-07

Corrections from sessions that ran the rules of 0.85.0 in throwaway clones — headless, and on a scripted `sdk-ts` host that answers a dialog. Each was written from what a session did. The first two were run again on Sonnet and held; the last two were run by no session after the correction.

### Fixed

- `ui-build`, the gate: at its stop the session offers no way around it. A Sonnet session stopped on a `DESIGN.md` marked `[needs verification]` in every line, then offered to build anyway on your word and recommended that over `design-settle`. Where only some lines are marked, the closing block names the line as owed by `design-settle`; a Sonnet session built correctly and reported nothing.
- Session start and the document reminder: a commit that changes how the app behaves writes its `docs/changelog.md` entry in a new file where the repo has none, to the file's shape and with its `docs/README.md` line. Two Sonnet sessions wrote no entry and gave the missing file as the reason — one after a rule change.
- `build-flow`: in a UI batch the content proposal comes before the page's `Contract + fixtures` line. A session built that line first and shaped the contract — filters, a summary row, pagination — from no proposal.
- `app-settle`, align: the audit lists a norm copied into `CLAUDE.md` with the plugin line that prints it, and counts apart a norm the plugin prints nowhere. Such a norm stays in the file and is reported on the `For app-eval` row. An audit counted a line the plugin does not print as a copy, and align deleted it.

To act on:

- Nothing. A `docs/` repo with no `docs/changelog.md` gets the file from the next commit that changes behaviour.

## [raizen-norms 0.85.0] - 2026-10-06

Five decisions the proof of 0.84.3 left owed, each answered as recommended. Checked on paper by case questions; no session has run them.

### Added

- `design-settle`, before the audit: where the app has a sign-in and the session holds no account for it, you are asked once which account walks the app — create one through `db-ops` (recommended; a login and a role row written to the app's database), wait for one you supply, or walk signed out. It is asked in Fast too. With no walk, every measurement was read from source.
- `design-settle`, the audit: it writes `.design-audit/findings.md`, every finding with its file and line. A gate that redraws nothing builds its `REPAIR` list from that file; the session searched the code for every place again.
- `design-settle`, a finding rejected at a `REPAIR` gate: it is asked once. Kept on purpose, it becomes an exception line in `DESIGN.md`'s Do's and Don'ts with your reason, and later audits no longer list it; left for later, it stays a finding. It returned in every audit.

### Changed

- `ui-build`, the gate: it stops where `DESIGN.md` is absent, empty, or `[needs verification]` in every line. With only some lines `[needs verification]` — what a Keep writes for what nothing measured — the session builds, takes what such a line would rule from a component already in the repo, and reports the line.
- `build-flow`, fixtures: a fixture copied from the document the app replaces has every name, phone number, e-mail, address and free-text value replaced by an invented one of the same shape. Figures, dates, codes and statuses stay. The fixtures file is committed.

To act on:

- A fixtures file copied from a real document before this version may hold real names and phone numbers. Nothing looks for them: replace them in the next session that touches the page.

## [raizen-norms 0.84.3] - 2026-10-06

Rules for what the proof of 0.84.2 found on the two paths that draw no canvas, `Keep — today's look` and fix-the-drift. Walked on paper by three subagents on invented apps, fix-the-drift through to its close for the first time; what they found in the new text was corrected and not walked again. No session has run any of it.

### Changed

- `design-settle`, `DESIGN.md`: `## Components` names the one icon family and holds icon sizes and stroke weight in its component-token table, and `## Page Composition` names the proving page, the first of the two frame screens. `build-flow` judges every later page beside that page, and no file said which one it is.
- `design-settle`, the audit: it measures the contrast of each pair of colours the app renders, and a Keep with no `DESIGN.md` writes `## Contrast` from them, because a Keep draws no foundations board to compute them on; a pair under its floor is put to you. In a real row copied into `handover.md`, every name, phone number, e-mail, address and free-text value is replaced by an invented one of the same shape, and no file holding real rows is listed. The report back says whether the running app was walked. Routes are read from the routes folder of a file-routed app, fonts from the root layout where the framework writes no HTML entry, and a copy-in library's slots from the tokens its copied files read.
- `design-settle`, the stack where UI exists: a part is indicted in three cases only — a floor failed inside a package's own stylesheet, two packages in use for one job, an engine that paints where the styling files cannot reach. An icon pack indicted for two families offers each family alone, the one more files import recommended. A part kept by a `Keep` line left standing gets its decision record, and `CLAUDE.md`'s Component library row is written where it names none.
- `design-settle`, Step 8 where no canvas was drawn: the structural diff, the pixel diff, the rendered-structure count and the signature read `n/a — no canvas` instead of each becoming a queue line. Each approved repair is read again at its place, a rejected one fails no check, a page is compared with its audit screenshot except where a repair landed, and the chat stop that proposes a deletion offers `.design-audit/` and the seed rows.
- `design-settle`, fix-the-drift: a `DESIGN.md` naming no proving page gets one line for it at the gate. The gate's file plan counts the files the pass writes on every path — `/design-system`, the lint floor, `AGENTS.md` — so the file-plan check no longer fails on them. The pass repairs the approved findings and nothing else of the app's UI.
- `build-flow`: with no proving page named, a page is judged by Section 4's two questions alone and the gap is reported.

### Fixed

- `design-settle`, sentences that disagreed: `ui-ux-pro-max` is read from Step 3 and the rest of the design material from Step 5. A section named from another step is read alone. A Keep redraws nothing, and its code changes only by a repair approved at the gate. Fix-the-drift changes `DESIGN.md` only by what its gate ratifies. The Step 9 block names a Keep's undrawn proposals, each need `docs/product.md` lacks, linter warnings left standing and seed rows still in the database, and leaves out a line nothing fills.
- The lint floor and `AGENTS.md`'s `## UI` part are written in `design-settle`'s pass: `ui-build`, `app-settle`'s scaffold and the install block said ratification.

To act on:

- Nothing. A `DESIGN.md` written before this version names no proving page and no icon family: `build-flow` reports the first, and the next `design-settle` run writes both — fix-the-drift writes the proving page alone.

## [raizen-norms 0.84.2] - 2026-10-06

### Changed

- `design-settle`, the audit: it measures the component-token table — each component's size as the running app renders it, read from the source where the walk cannot reach one — and lists the result in `.design-audit/audit.md`. `Keep — today's look` with no `DESIGN.md` ratifies the measurements as lines above one confirmation, with a question for each line you name and for each component rendered at more than one size. Nothing measured them, so a Keep wrote the table `[needs verification]` and every later page was built from it. Written from a `simulate` self-run's finding and walked once more on paper; no session has run it.

To act on:

- Nothing.

## [raizen-norms 0.84.1] - 2026-10-06

### Fixed

- `app-settle`, document: where the `AGENTS.md` import is kept, the opening line of `AGENTS.md` is written without its claim that Claude Code does not read the file. A session read the old wording as its opposite.
- `docs-format`: a `docs/` repo with no `docs/changelog.md` gets the file in the commit that owes an entry. A session gave the missing file as a reason to write none.

To act on:

- Nothing.

## [raizen-norms 0.84.0] - 2026-10-06

### Added

- Session start: a `docs/product.md` or a root `PRD.md` too long to print still gets its prohibitions printed under the order to read it, where they fit. Sessions on a cheaper model skipped the read.
- Session norms: `POINTERS` and `NOT SETTLED` name `norms-help` for which command to run, the version and what changed — on a machine with many skills its description never reaches the model.
- Session norms, `ASKING`: a block or a table a skill orders printed is printed whole, whatever brevity mode another plugin sets. Under one, a session printed neither Step 0's block nor the `MIGRATE` block.
- `app-settle`, bootstrap: N5 runs the platform's own init command for a Ready platform too, first after the summary's approval, which names it. No step created the app's skeleton, so question 8's `install now` had nothing to install into.
- `app-settle`, document: a `CLAUDE.md` that imports `AGENTS.md` is asked once — remove the import line, recommended, or keep it.

### Changed

- Session norms, `GIT`: a commit names its paths again, `git commit -- <paths>`, so a path staged before the session never rides along.

To act on:

- Nothing. The norms grow by about 300 characters of the 9,500 a session start may print, so a repo near that limit has its listings cut a few lines earlier.

## [raizen-norms 0.83.4] - 2026-10-06

Rules for what three `simulate` self-runs found with no rule to follow. None has run in a session yet.

### Changed

- `app-settle`, the interview: the batch after the reading also asks the app's name, what must be true for the problem to count as solved, and what a user with no role may do — the title, `## Success` and the closing sentence of Roles were written from no answer. `none` is an answer for rules, terms and non-goals. A user who declines to tell the story gets the themes as one batch of questions. A corrected reading is restated, and stops again only where the problem or the people changed. A partial approval of the summary writes nothing.
- `app-settle`, the stack questions: fewer than three rows that fit are offered as they are, and one row is a derived line. An app with no screen gets its Platform as a derived line. Question 6 no longer offers `No database`. Question 9 recommends `None` where the story and the Roles say nothing of training or a hand-over. Branches and Code language are shown and never re-opened.
- `app-settle`, bootstrap: where the database project does not exist at N5, `supabase/config.toml` is written at N6 from the ref the user replies with. `CLAUDE.md`'s component library row reads `not decided — design-settle` until that skill writes it.
- `app-settle`, document: a correction of the reading that contradicts a measurement is written by what it states, and the other side is a `Findings` line.
- `logic-settle`: L1 counts only the list screens fetched on the client. L4 reads the Deploy row for people other than the app's builders. Each `Will migrate` line of the install block says `this session` or `queue line`, and a library the answers leave unused is a `Will remove` line.
- `design-settle`: Step 0 prints a `Logic layer` row, and `logic-settle` is offered only where it reads `not settled`. A redesign is judged at 1440px until its `DESIGN.md` is rebuilt. Picking another frame, or an escalation, releases a stressed reference. Followed closely means the judgement's measurable rows, never a product's identity. The verdict marks no recommendation and its third option reads `start the look over`; the signature question recommends keep. The audit reports whether `DESIGN.md` carries an archetype table.
- `design-settle`, replies that had no rule: no tick at the direction question · `keep all` beside another tick · shells past four options · a cancelled assumption or hand-rolled line · a verdict that starts over beside other answers · a rejected value, file-plan, ordered-work or deviation line at the gate · a cancelled data-seam line at the close · seed rows kept while the canvas goes.

### Fixed

- `design-settle`: Step 2 no longer promises a component-library decision where the audit indicts nothing. The Keep lines of Full say how one is cancelled, and the archetype grouping how it is corrected. The two-screens dialog no longer names a direction before one is asked.
- `build-flow` and `design-settle` no longer point at each other for the product draft's floor: `build-flow` Section 4 holds it.

To act on:

- Nothing.

## [raizen-norms 0.83.3] - 2026-10-06

### Changed

- `app-settle`, question 6: Supabase is offered as two options, Cloud and self-hosted, because bootstrap writes a different connection for each.
- `build-flow`: a Help row that opens with `in-app` owes the help page a queue line until that page exists. Question 9 promised the line and nothing wrote it.
- `logic-settle`: where the folder holding the most database calls is a page or component folder, the data layer is the next one that is neither. A queue line for a deferred migration creates `docs/queue.md` where the repo has none.

### Fixed

- `app-settle`: the Flow row counts nine stack questions. Step 0 no longer checks skills it reads nothing from. The live check before a question is of a recommended package. The stack rubric and question 4 no longer say nothing is scaffolded where N5 writes a host file.
- `logic-settle`: a library beside handwritten code for one need is that need's question, never a `Duplicates` line.
- `design-settle`: Step 1 reads the code through the audit's hand-over where UI exists, as Blindness orders. The font package is installed in the pass's Foundations where UI exists.

To act on:

- Nothing.

## [raizen-norms 0.83.2] - 2026-10-06

### Changed

- `guard_git`: a held push or pull request that the call wraps in other commands — a `cd`, `&&`, a pipe, a redirection — is told to be named and run alone. A session named the bare command, was answered yes, retried the wrapped one and was held a second time.
- `docs-format`: a path a document names is written whole, from the repo root, where the session start resolves it.

### Fixed

- Session start: `DESIGN.md` named in a living document is no longer reported as a path that does not exist. The Proof profile names it from bootstrap, before `design-settle` has written it, and the note told every session to correct a correct line.

To act on:

- Nothing. A living document that names a file without its folder — `accounts.ts` for `api/accounts.ts` — is still reported at session start: write the path whole.

## [raizen-norms 0.83.1] - 2026-10-06

### Changed

- `logic-settle` commits at the close by the session norms' `GIT` block, a migration that ran in a commit of its own. It said `Do not commit`.
- `guard_project_ref`: the refusal no longer tells the session to ask for a go-ahead the hook cannot read. It says that nothing said in the session lifts it, and that work on another project runs from a session in that project's own repo.

### Fixed

- `logic-settle`: with nothing scored, the install block still runs where the repo has no linter, because Step 7 writes its floor into one. The skill no longer says both that it has no mode and that it asks Fast or Full, nor that it writes in three places while it also writes a queue line and a migration file.
- `db-ops`: `SKILL.md` points to the agent-account reference for a session that must sign in and holds no account. The role-test pattern is marked as Supabase's. A guarded statement that aborted is named as the stop, where the text spoke of a mismatch no abort leaves.
- `app-settle`: the Mode row names `seed`. Bootstrap no longer claims zero dependencies where question 8 or a Pioneer init command installs some. Questions 8 and 9 are named as the two-answer exceptions. The files Align may create include the linter's config and its baseline.
- `build-flow`: the closed list of stops binds from a page's first line of code, so the queue's approval and the content questions are not on it.
- `ui-build`: the components heading no longer names a Plan that only a host with plan mode has.

To act on:

- Nothing. A `logic-settle` session that closed under an older version left its work uncommitted: commit it before the next settle skill runs.

## [raizen-norms 0.83.0] - 2026-10-06

### Changed

- `design-settle` commits its work once, at the close, by the session norms' `GIT` block: on the pass's own branch where UI exists, on the current branch where none does. It said `Do not commit` and left its files staged, which `app-settle`'s migrate and align modes stop on.
- `design-settle`, `Keep — today's look` with no `DESIGN.md`: only what the audit measured is ratified, the gate shows `DESIGN.md` as it will be written and a `REPAIR` list, and an answer that differs from the measurement is retokened in the pass. It was to be redrawn at Step 5, on a path where the drawing has ended. `DESIGN.md` is written as the pass's first act even where nothing is repaired.
- `design-settle`, the gate: removals a reply leaves unnamed are shown again alone, and a clear yes to that message covers them. A rejected line is redrawn and the gate shown again whole, its changed lines marked.
- `design-settle`, Fast: the direction question is answered `Decide for me`. Step 2's question rides the reading's call only where Fast was named at invocation. A cancelled pre-answer re-answers the lines that read it, and a line above the canvas call is cancelled under the verdict's Other or in chat.
- `design-settle`, Full, with nothing to install: one line and no stop. What leaves is authorized at the Step 6 gate.

### Fixed

- `design-settle`: replies that had no rule have one — `Decide for me` ticked beside directions, a second pick failing verification, a refused font line, `escalate to the questions` on a first round, an icon pack indicted for two families, an answered width or theme mode the kept app does not hold. The reading's correction has defined options. A want stated there moves a recommendation, and a need stated there enters the product draft.
- `design-settle`: a product without UI is read from the Surface row, never from `DESIGN.md` being absent. Canvas type imports name their source where a data layer exists and no UI does. The Barcode / QR engine category no longer fires for a hardware scanner that types into a field.

To act on:

- Nothing. A `design-settle` session that closed under an older version left its work uncommitted: commit it before the next settle skill runs.

## [raizen-norms 0.82.0] - 2026-10-05

### Added

- Session norms, `GIT`: a turn that committed ends with one line telling the user to start the next item in a new session. Every call re-reads the whole session, so a step late in a long session costs several times the same step in a fresh one. It is advice and stops nothing.
- `db-ops`, Invocation: a step is one command up to its next STOP, its statements in one file or one call. A read spans environments in that command; a write reaches one environment per command. The role test keeps its call per role.

## [raizen-norms 0.81.1] - 2026-10-05

### Fixed

- Session start, on Claude Code: the output stays under the host's cap of 10,000 characters. Past it Claude Code hands a session only the first 2,000 characters and a file path, so in a repo with a long `PRD.md` or many components the session received `LANGUAGE` and part of `POINTERS`, and never `SCOPE`, `GIT`, `ASKING`, `DECISIONS`, the closing block or the documents. The norms and the notes are now always printed whole; a document that no longer fits is named under its heading with `Not printed` and an order to read it, and a listing is cut at a line with a closing `... more`. A repo whose output already fitted gets what it got before. Antigravity is not capped and is unchanged.

To act on:

- Nothing. An app whose `PRD.md` is named instead of printed is read by the session itself, from the lines the note gives.

## [raizen-norms 0.81.0] - 2026-10-05

### Changed

- `build-flow`, the audit: the one question after the last page is a multi-select of the passes that apply — Accessibility, Interaction polish, Click path, Platform conventions — where it was all five or none. The ticked passes run in a subagent on a cheaper model, which reports findings and fixes nothing; the session fixes them. The audit ran in the session itself, at the point where every call re-reads the most.
- `build-flow`, a UI batch: the walk of a page's six cases runs in a subagent on a cheaper model. It returns one line per case and the paths of the `bulk` screenshots; the session still reads and judges them. A backend batch walks its flow in the session, as before.

### Removed

- `build-flow`, the audit's `Screenshot` pass. A fix that changes how a page looks is followed by the same screenshots, as a rule of the audit and not an option of it.

## [raizen-norms 0.80.0] - 2026-10-05

### Changed

- `app-settle`, Align: the audit runs six rows and prints `C3 language split` as `not run`. The question that puts the ranked table also offers C3 — audit it too, or skip it — and the close block has a `Not audited` row. C3 reads every identifier, route and database name in the repo, and what it finds is mostly renames recommended to leave; it was run on every repo whether or not anyone wanted it.

## [raizen-norms 0.79.0] - 2026-10-05

### Added

- `docs/architecture.md` and `docs/runbook.md` in every settled app, for the developer who continues it and the agent that builds it: how the parts connect and where code lives; how the app is deployed, rolled back and restored. `app-settle` writes them — from the stack answers at bootstrap, from the repo in document mode — with `[needs verification]` where nothing has run. Session start checks the paths both name.
- `docs/changelog.md`: one entry per commit that changes how the app behaves. A commit that changes no document is reported `Docs: none` with its reason, so no commit goes unreported.
- `app-settle`, a ninth stack question: help for the app's users — none, guide pages in the repo, or a help page inside the app. The answer is Context's `Help` row.

### Changed

- `docs/guide/` is kept only where the `Help` row is not `none`. It was mandatory in every app, with or without anyone to read it. The reminder after a commit asks about a guide page only there.
- Every document of the list is written for a technical reader, in the user's language; `docs/guide/` alone is written for the app's users.

### Removed

- `docs/whats-new.md`. `docs/changelog.md` replaces it, written for developers rather than users.

To act on:

- An app on the `docs/` form: run `app-settle`. It finds `docs/architecture.md` and `docs/runbook.md` missing and writes them from the repo.
- An app with a `docs/whats-new.md`: rename it `docs/changelog.md`, in the commit that corrects its `docs/README.md` line.
- An app that wants its guide pages kept: add a `Help` row to Context in `docs/product.md`, opening with `guide pages` or `in-app`. Without the row, guide pages are no longer asked for.

## [raizen-norms 0.78.1] - 2026-10-05

### Fixed

`guard_destructive` let these through with no guard; each is refused now:

- A `DELETE` whose `WHERE` compares a `[CLAUDE]` value with `!=`, `<=` or `>=` — every row but the test rows — and one that joins a table in with `USING`.
- SQL after a `--` flag in a shell command, such as `psql --host=localhost -c "..."`: everything from `--` on was dropped as a comment. In a shell command only a line opening with `-- ` is a comment now, and a `--` inside a quoted string is data on either route.
- Lowercase SQL run through a client named by a path with `/`, such as `/usr/bin/psql`.
- `DROP` of a `DATABASE`, `DOMAIN`, `PROCEDURE`, `MATERIALIZED VIEW`, `SEQUENCE`, `TRIGGER`, `EXTENSION`, `ROLE`, `FOREIGN TABLE` or `OWNED`; a column dropped without the word `COLUMN`; a rename of anything but a table.

`guard_git`:

- `git add src -A`, `git add -- .`, `git add ./` and `git add -Av` passed; any argument of the add is read now.
- `git push origin dev && rm -f x` was refused as a bare force push with no reply that let it through; a force flag counts only among the push's own arguments, a continued line included.

To act on:

- A migration that drops a column without the word `COLUMN`, or drops or renames one of the kinds above, now meets the destructive gate where it is written.

## [raizen-norms 0.78.0] - 2026-10-05

### Added

- `docs/` as a documentation site in four groups — Getting started, Concepts, Guides, Reference — with one page per skill, per hook and for the commands. `docs/README.md` is the index on GitHub, the site's home and its sidebar. `docs/.vitepress/` and `.github/workflows/docs.yml` build it for GitHub Pages on a push to `master` that touches `docs/`.

### Changed

- `norms-help` prints its commands from `docs/reference/commands.md`; `README.md` no longer holds a `Use` section.
- `README.md` is the landing only: what the plugin holds, the two install commands, and where each page is. The install details, the update, Antigravity, maintaining app repos and what is not yet verified moved to pages under `docs/`.
- `docs/guide/gates.md` and `docs/guide/documents.md` are `docs/concepts/gates.md` and `docs/concepts/documents.md`; `docs/guide/help.md` is `docs/reference/norms-help.md`.

Nothing to act on in an installed app.

## [raizen-norms 0.77.0] - 2026-10-05

### Added

- `norms-help`: one card holding the version number, the commands of `README.md`'s `Use` section, the pages `docs/README.md` lists, and the newest changelog entry. A question asked with it is answered from the page that covers it, and the file is named. `scripts/norms_help.py` prints each part as its file holds it, so the card cannot disagree with them.
- `docs/guide/help.md`: what the card holds and where each part comes from.

### Removed

- `norms-version`, with its comparison against origin and the update it offered. The version is now its number and one changelog entry. A machine with `autoUpdate` on gets a new version at its next start; `README.md` holds the update under `Update`.

To act on:

- A note or a habit naming `/raizen-norms:norms-version`: the command is `/raizen-norms:norms-help`.

## [raizen-norms 0.76.1] - 2026-10-05

### Fixed

Both found by running 0.76.0 on Antigravity, before any of it was published:

- The document reminder, on Antigravity: a conversation opened within minutes of another one's commit was asked about that commit, and spent thirty steps on it. It is asked only after its own last tool call ran a `git commit`.
- `guard_git`: a command named inside a sentence counted as put to the user, so a closing report saying what it pushed turned the next thing typed into a reply that let one more push through. The command counts only backticked on a line of its own, or alone in a fence; the session norms and the held message say so.

Nothing to act on in an installed app.

## [raizen-norms 0.76.0] - 2026-10-05

### Added

- A document reminder: after a commit that touched no document, in a repo with `docs/PRD.md` or a root `PRD.md`, the session is asked whether a sentence in a document became false, whether a page became usable with no guide page, and whether users will notice. It writes the document into that commit or reports `Docs: none`. `scripts/remind_docs.py` never blocks a commit, and is silent in a repo that keeps no documents. On Claude Code it comes with the result of the `git commit`; on Antigravity, where no hook speaks after a tool, the session-start script hands it over before the next model call, once per commit.

### Changed

- `docs-format` and `build-flow`: `docs/whats-new.md` gets an entry for every commit users will notice, with or without an in-app help page. It was written only where the app had one, which left an app without a help page with no record of change but `git log`.

To act on:

- An app on the `docs/` form with no help page: `docs/whats-new.md` is written from the next commit users notice. Nothing is owed for commits already made.

## [raizen-norms 0.75.0] - 2026-10-05

### Added

- Session start: a repo with no PRD in either form gets `docs/queue.md` printed where it keeps its queue there, as it gets a root `QUEUE.md`.
- `docs/` in the plugin's own repo, written for the people who install it. `docs/guide/gates.md` says what the publishing stop and the destructive gate show, what each waits for, and what its hook checks and does not. The toolkit's own queue moved to `docs/queue.md`.

Nothing to act on in an installed app.

## [raizen-norms 0.74.0] - 2026-10-05

### Changed

- Session norms, `GIT`, and `guard_git`: a push, `gh pr create` and `gh pr merge` are a chat stop, on Claude Code and Antigravity alike. The session ends its turn on a message naming the exact command in backticks, with the commits it publishes under it, and runs the command once when the reply typed in chat is a clear yes, in whatever words. A question, a condition or another instruction is not one.
- `guard_git` enforces the stop, not the yes: the command is held until the session's last message names it and the user has typed a reply to that message, with nothing typed since. One reply covers one run. Reading the reply is the session's.

### Removed

- `guard_git`: `Run` picked on an AskUserQuestion, or on `ask_question`, no longer lets a held command through — a dialog gets clicked before it is read.

To act on:

- Nothing in an installed app's files. At the next held push or pull request, answer in chat where `Run` used to be picked.

## [raizen-norms 0.73.0] - 2026-10-05

### Added

- `norms-version`: reports the version of the copy the session runs, the date it was released and the time it reached the machine, whether origin holds a newer one, and its changelog entry — with every entry the machine lacks when it is behind. `scripts/norms_version.py` does the reading: origin is its changelog, fetched over HTTPS from the public repo, and a machine that cannot reach it still gets its own lines. Behind, on Claude Code, it asks whether to update now and runs the `README.md` commands on `Update`; on Antigravity it reports only.

Nothing to act on in an installed app.

## [raizen-norms 0.72.2] - 2026-10-05

### Changed

`app-settle`'s migrate mode, corrected from two runs on copies of legacy apps:

- A block of `CLAUDE.md` telling a session how to write, keep, or format the PRD is deleted and named in the close block. Left standing, it ordered the next session to write a root `PRD.md` back.
- A Section 3 list item keeps its whole text under its topic. Its topic is the opening words a rule test already quotes, else its bold lead-in, else its opening words up to the first punctuation mark. A paragraph is never a topic.
- Everything inside the six sections moves: a part its shape has no heading for stays under its own label, and only text outside the sections is left in `docs/PRD.md` alone.
- `DESIGN.md` gets no `## Contrast`, its sections follow the format's order, and the five token groups it marks `omitted` are named.
- The rule-test check, the session-start check, the frozen line and the files that name the old form are each stated one way.

Also:

- Session start, the stale-path note: a backticked token with no letter in it — a document number, a fraction — is no longer read as a path.

To act on:

- An app repo migrated under 0.72.0 or 0.72.1: read its `CLAUDE.md` for a block that still tells sessions to maintain `PRD.md`, and delete it.

## [raizen-norms 0.72.1] - 2026-10-05

### Changed

- `design-settle`, the frames: the session prints `Material loaded:` with the path of every file it read before the first frame, and names the detector command and its hit count in each round's report — `detector not run` and why where it did not. A full run on Antigravity drew frames and a canvas having read no `impeccable` or `frontend-design` file and run no detector, and nothing in its output showed it.
- The Antigravity `HOST` block says what loading a skill means there: read its `SKILL.md`, then the files it names.
- The Antigravity `HOST` block sends a session to Claude Code's own copy of `frontend-design` where one exists: no installer puts that skill on Antigravity, and a linked folder is not listed there. The copy follows Claude Code's updates; a machine without Claude Code copies the folder.

Nothing to act on in an installed app. On Antigravity, uninstall and install again to get it; a headless run there also allows `read_file` on Claude Code's `frontend-design` folder.

## [raizen-norms 0.72.0] - 2026-10-05

### Added

- `app-settle`, migrate mode: a repo with a root `PRD.md` is moved to the `docs/` form in one commit — `PRD.md` to a frozen `docs/PRD.md`, `QUEUE.md` to `docs/queue.md`, its sections copied word for word into `docs/product.md`, `docs/rules.md`, `docs/glossary.md` and `docs/decisions/`, a ratified Section 5 converted into `DESIGN.md` with no value changed. It runs before align or rework, and a repo that cannot move mechanically stays legacy for that run.
- `app-settle`, align mode: the audit, the ranked table and the one-finding-per-commit fixes that were `app-align`.

### Changed

- `app-settle` has five modes — bootstrap, document, migrate, align, rework — and Step 0 decides which from the directory and the code. With documents in place it audits for align unless the user asks for a change, which is rework. Each mode is decision work or mechanical work, never both.
- `app-settle` commits what a mode wrote, by the norms' `GIT` block. Bootstrap makes the first commit on `main`, then creates `development` and switches to it.
- `app-settle` Step 0: on `main` with no `development` branch it offers to create one; migrate and align stop on a dirty working tree.
- `docs-format`: a root `PRD.md` is the legacy form until `app-settle` migrates it, and `DESIGN.md` has one writer besides `design-settle` — that conversion.
- Align corrects a document only where it states what exists and the code shows otherwise; a mismatch about what ought to be is left for rework.

### Removed

- The skill `app-align`. `/raizen-norms:app-align` no longer exists; run `/raizen-norms:app-settle`.

To act on:

- An app repo whose `CLAUDE.md` or `AGENTS.md` names `app-align`: the next align run counts it under C2 and corrects it.
- An app repo with a root `PRD.md`: the next `app-settle` run there migrates it. Migrate has not run in a real app — try it on a copy first.

## [raizen-norms 0.71.0] - 2026-10-05

### Changed

- Session norms: a repo with neither a root `PRD.md` nor `docs/PRD.md` gets a shorter block. `POINTERS` and `CLOSING THE SESSION` are cut, and a `NOT SETTLED` section stands in their place: `build-flow` and `docs-format` do not apply there, `ui-build`, `db-ops` and `logic-build` hold except where a rule reads `docs/` or `DESIGN.md`, and in an app repo the session says once that `app-settle` has not run.
- `ui-build`: the `DESIGN.md` gate does not bind a repo marked `NOT SETTLED`. UI there is built only from the components and tokens the repo already has, with no new styling value.
- `guard_git`: a commit on `main` is refused only where the repo has a `development` branch, local or on `origin`. The `GIT` block of the norms says the same.
- `app-settle`, `logic-settle`, `app-align`: the stop on branch `main` gives the rule as its reason, no longer the guard.

To act on:

- An app repo with a PRD in either form: nothing — its session start and its gates are unchanged.
- An app repo with only `main`: sessions now commit there. Create `development` to get the refusal back.

## [raizen-norms 0.70.0] - 2026-10-05

### Changed

- One plugin instead of two: `raizen-hub` is merged into `raizen-norms`, which holds all nine skills, the session norms and the guards. The version continues above both — 0.70.0 follows `raizen-hub` 0.69.0 and `raizen-norms` 0.37.1.
- The plugin is the repo root: `skills/`, `scripts/`, `hooks/` and both manifests moved up from `plugins/raizen-norms/`, so Antigravity installs it from the repo URL with `agy plugin install`.
- The four settle skills are invoked as `/raizen-norms:app-settle`, `/raizen-norms:logic-settle`, `/raizen-norms:design-settle` and `/raizen-norms:app-align`.
- `design-settle` Step 0 and `app-align` print one plugin version.

### Removed

- The plugin `raizen-hub`. The marketplace's `renames` map sends the name to `raizen-norms`, so Claude Code moves an enabled `raizen-hub@raizen` onto it.
- The `plugins/` folder.

To act on:

- An app repo: nothing — its `enabledPlugins` line names `raizen-norms@raizen` already.
- A Claude Code machine: after the update, `/plugin` lists `raizen-norms` and no `raizen-hub`. Where `raizen-hub` is still listed, uninstall it — its copy of the four skills is stale. A machine that enabled only `raizen-hub` now runs the norms and the guards in every folder.
- An Antigravity machine: a `~/.gemini/config/plugins.json` entry naming `…/raizen/plugins` resolves to nothing once that clone updates, and every session there runs without norms or guards. Remove the entry and install as the README's Antigravity section says.

## [raizen-norms 0.37.1] - 2026-10-04

### Changed

- `build-flow`: commit timing follows the session norms' `GIT` block everywhere. Section 9 no longer says the commit is never made mid-session, and the audit is no longer offered before anything is committed — a finished page is committed when it is finished, and an audit fix is its own commit.
- `build-flow` Section 9: no longer says bootstrap wrote no host config and no CI workflow; `app-settle` N5 writes a rewrite rule for a static SPA, and a CI workflow when the user asks for one.
- `ui-build`: the `bulk` fixture case is 500+ rows, the number `build-flow`'s `references/contract.md` gives.

Nothing to act on in an installed app.

## [raizen-hub 0.69.0] - 2026-10-04

### Changed

- `app-settle`, `logic-settle` and `app-align` are read one step at a time, as `design-settle` is since 0.68.0: `SKILL.md` keeps the cost rules, the hard limits and the first steps, and names per later step the file to read on arrival. Step and question numbers and the finding codes C1 to C7 are unchanged. Every `description` is shorter.
- `app-settle`: `SKILL.md` is a quarter of its size. Document mode is `references/document.md`, rework `references/rework.md`, N5 and N6 `references/scaffold.md`, the Pioneer path `references/pioneer.md`. The repo read of D1 and R1 runs in a subagent briefed with `references/repo-read.md`.
- `logic-settle`: Steps 3 to 8 are `references/interview.md`, `install.md`, `pass.md` and `floor.md`; each need of the rubric is its own `references/need-*.md`, read only when that need is asked. The audit runs in a subagent briefed with `references/audit.md`.
- `app-align`: the audit runs in a subagent briefed with `references/audit.md`.
- All three: a subagent doing an audit or a live verification runs on a cheaper model than the session's. Only a question's recommendation is verified before it is asked; another option is marked `unverified` and verified when picked.

### Removed

- `app-settle`, N6: the sentence that the toolkit writes no hosting or CI file at bootstrap, which the N5 table contradicted. The table stands; the session still never raises hosting, production env or CI.

Nothing to act on in an installed app.

## [raizen-norms 0.37.0] - 2026-10-04

### Changed

- All five skills are shorter to load, with the same rules: each states a rule once, drops the sentences that argued for it, and opens with the cost rules — independent reads and commands in one turn, nothing the session start printed re-read. Section numbers and names are unchanged. Every `description` is shorter.
- `build-flow`: `SKILL.md` is half its size. Section 3 — the three routes of a new queue, the change record, the UI and backend split — and the two queue file templates are `references/new-queue.md`, read when `docs/queue.md` is absent or just emptied or the user asks for something outside it. The rule test before wiring, the wiring rules and canvas-file retirement are `references/backend.md`, read by a backend batch or an app that never split. The audit pass is `references/audit.md`, read when the user accepts it. The wiring rules were in two places and are now in one, which a backend batch reads.
- `ui-build`: the craft material is one table naming what to read before which edit. The voice of a first-visit page group is `references/first-visit.md`.
- `logic-build`: the rule-test table per enforcement point and the no-test-runner procedure are `references/rule-test.md`; Section 10 keeps the rules.
- `docs-format`: the legacy map is in `references/legacy.md`, read at once in a repo with a root `PRD.md`.

Nothing to act on in an installed app.

## [raizen-hub 0.68.0] - 2026-10-04

### Changed

- `design-settle` is read one step at a time. `SKILL.md` keeps the switches, the hard limits, Fast or Full and Steps 0 to 2; each later step is a file read when the flow reaches it — `references/interview.md` (Steps 3 and 4), `frames.md` and `canvas.md` (Step 5), `ratify.md` and, where UI exists, `gate.md` (Step 6), `pass.md` (Step 7), `verify.md` (Steps 8 and 9). The audit is `references/audit.md`, read only by the subagent that runs it. Step numbers are unchanged.
- `design-settle`, cost rules: a step's independent reads, searches and commands run in one turn; the audit, the stack verification, the reference search, the platform research and Step 8's mechanical checks run in a subagent on a cheaper model than the session's; what the session start printed is not re-read.
- `design-settle`: `impeccable`, `frontend-design` and `review-animations` are loaded after the install gate, before the first frame, instead of before the reading.
- `design-settle`, the stack where UI exists: a library, styling, icon pack or engine the audit does not indict is one cancellable `Keep` line, not a dialog. On every repo only a dialog's recommendation is verified before it is asked; another option is marked `unverified` and verified when picked.
- `design-settle`: the `/design-system` route is written once, in the pass, instead of before the frames; the lint floor's rules moved with it to `pass.md`.
- `design-settle`: every frame's `ui-ux-pro-max` searches run in one command; its commands are taken by searching its `SKILL.md`, not by reading it whole.

Nothing to act on in an installed app.

## [raizen-norms 0.36.1] - 2026-10-04

### Changed

- `build-flow`: the pointer to `design-settle`'s product draft names its new file.

## [raizen-norms 0.36.0] - 2026-10-04

### Changed

- Session start, legacy `PRD.md` repos: the hook prints Sections 1, 2 and 6 only — context, roles, prohibitions, what `docs/product.md` holds in the other form. Sections 3, 4 and 5 are named with their line range and read from the file when a skill sends a session there. A `PRD.md` whose six numbered sections cannot be located is still printed whole. Nothing to act on in an installed app.

## [raizen-norms 0.35.1] - 2026-10-04

### Changed

- Session norms, `HOST - Antigravity`: three lines an Antigravity session got wrong without them — the guards run there as hooks it cannot see, the installed plugins are the folders the skills are read from, and a `claude mcp add` line means the same server in `~/.gemini/config/mcp_config.json`.

## [raizen-norms 0.35.0] - 2026-10-04

### Added

- Antigravity support: `plugin.json` and `hooks.json` at the plugin root, read by `agy`. The same guards run before `run_command` and `call_mcp_tool`, and the norms are injected before the first model call of a conversation, with the app's `CLAUDE.md` and a `HOST` block mapping Claude Code's tool names. Proven on `agy` 1.2.16 — README, Antigravity, holds the registration and what is not yet verified.
- `scripts/host.py`: hands every hook one payload shape on either host.
- Hand-over block at session start: when the working tree is dirty and the other host ran the last session in the repo, the norms end with that session's last request, the user's answers, its todo list and its last messages, read from its transcript on the same machine.

### Changed

- `guard_git`: on Antigravity a held command passes on `Run` answered to `ask_question`, and the held message names the host's own question tool.
- `guard_project_ref`: a crash passes the call on every host.
- Hook payloads are decoded as UTF-8 whatever the console codepage.

## [raizen-hub 0.67.0] - 2026-10-04

### Added

- Antigravity support: `plugin.json` at the plugin root, so `agy` loads the four skills.

### Changed

- `app-settle`, the shape of `AGENTS.md`: Antigravity loads that file and is handed the norms too; the norms' `HOST` block says which holds.

## [raizen-norms 0.34.0] - 2026-10-02

### Changed

- Session norms, `GIT`, and the `guard_git` held message: the commits under a push or pull-request command are `- ` bullets, one per commit, and the question offers exactly two options, `Run` and `Cancel`.

## [raizen-norms 0.33.0] - 2026-10-02

### Changed

- Session norms, `GIT`: the AskUserQuestion that asks for a push or a pull request lists every commit the command publishes under it, one line each: short hash and subject.
- `guard_git`: the held message asks for that list.

## [raizen-hub 0.66.0] - 2026-09-29

### Removed

- The bundled Playwright MCP server pinned to WebKit, with every WebKit capture in `design-settle`: the `Design material` row, the ask when it is absent, and the Judging and verify lines. Screenshots use Chrome DevTools only. The WebKit browser a machine installed for it is no longer used and may be deleted.

## [raizen-norms 0.32.0] - 2026-09-29

### Added

- Session norms, `ASKING`: a decision that is the user's is asked through AskUserQuestion, or in chat at a hard stop, and the session runs it. The user is never handed a command to type, only what needs their own hands: a browser login, a dashboard, a key rotation, a payment.

### Changed

- `guard_git`: a push (`--force-with-lease` included), `gh pr create`, and `gh pr merge` run once the user picks `Run` on an AskUserQuestion that names the exact command; one answer covers one run. The permission prompt is gone, because an SDK host never showed it.
- `guard_git`: a bare force push (`--force`, `-f`, `+branch`) is refused with a pointer to `--force-with-lease`.
- Session norms: a session behind `origin/development` asks to run `git pull --ff-only` instead of telling the user to run it.

### Fixed

- `guard_git`: a command mentioned inside a commit message, a heredoc, or a quoted string is no longer read as a call, so a message naming `git add -A` or `gh pr create` commits.

## [raizen-hub 0.65.0, raizen-norms 0.31.0] - 2026-09-28

### Changed

- `ui-ux-pro-max` is Required, level with `impeccable`: a session without it asks before continuing.
- `ui-build`: where both skills set a UX floor, the stricter one applies; any other contradiction is reported to the user; `DESIGN.md` outranks both.
- `design-settle`: style, colour, and typography search runs once per frame, with that frame's direction as the query.
- `design-settle`: every frame and canvas round meets the UX floor. Step 8 checks Critical and High don'ts per interaction on every promoted page; Step 9 reports any left standing.

### Removed

- `design-settle`: the pure frame, its draw question, and the rule that one frame is drawn without `ui-ux-pro-max`.
