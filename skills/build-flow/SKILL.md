---
name: build-flow
description: Rules for building an app — the queue in docs/queue.md, how much one session delivers, what a page holds, the order of work inside a page, the closed list of stops. Use before starting any page or feature, and when deciding what to build next.
---

# build-flow — what is next, and when a unit is finished

Documents are named by their `docs/` path; a repo with a root `PRD.md` reads each through `docs-format`'s legacy map.

## What a load costs — two rules

- **Run a step's independent reads, searches and commands in one turn** — parallel calls, or one chained command — because every extra model call re-reads the whole session.
- **Never re-read what the session start printed** — the documents and the two listings. The one Read an edit of `docs/queue.md` requires is the exception.

## 0 — Orient before anything

Open a session that is going to build with one block, before asking anything and before touching code:

```
Batch      : UI
Usable now : Request list · Create request · Request detail
Queue left : 3 lines
Next       : Approval inbox — Approver
```

- **`Batch` names the batch that is running**, and so what *usable* means this session — in a UI batch, that the page's UI is accepted; the queue's header lines state it. An app that never split its work runs a single batch and the line says so. A file holding two blocks runs the first.
- **Never take `Usable now` from a record.** Take it from `git log --oneline -- docs/queue.md` — every line a commit removed is one line finished — and from the routes present in the repo, plus live schema introspection in a backend batch and the contract files in a UI batch.
- **Read `git diff` as well as `git log`**: a deletion still uncommitted otherwise reports a finished page as unbuilt.

## 1 — The unit is what fits in one context window

One session delivers pages that can be opened and whose work their role can actually finish — pages, not features, because a page is bounded and a feature is not.

| Batch | What one page carries | Pages per session |
|---|---|---|
| Backend | migration · RLS · role test · types · query · wiring · spec | One |
| UI | contract · fixtures · the page and its states | As many as fit |

The bound is the window, never a number. Where a session takes several pages, build the ones that establish a pattern first — the shell and navigation, one table page, one form page — and reuse them in the rest, so each pattern is decided once.

### When the feature spreads to other pages

One test sets the size of the session; counting pages does not:

> *If I stop here, does any page that used to work stop working?*

- **Yes → finish it in this same session**: a shared column or table changing, a shared component changing its contract, a query other pages depend on, a page that cannot be reached on its own (a detail with no list).
- **No → it becomes a new line in `docs/queue.md`.** A page that *could* use the new thing but works without it is separate work, not spread.

## 2 — `docs/queue.md` is a queue, not a record

One copy, holding only pages that are **not yet usable**, in build order, one line each, in the app's own locale:

```
- <page> — <role> — <the work that can be finished there>
```

Add `(needs: <page>)` only where a real dependency exists.

| Rule | |
|---|---|
| Line finished | **Delete it at that moment**, never at the end of the session, and never tick it — a deletion made then is true when written and survives a session that dies early |
| What a line may be | A page, or a step inside one that passes the Section 7 test. A step that fails it is a todo entry (Section 5), never a line: the todo list dies with the session |
| History | `git log docs/queue.md`. One deleted line per line finished, tied to the commit that built it |
| File runs empty | Delete the file. Never leave an empty queue. A block that runs empty above another is deleted with its title and header, and the file stays |
| Status columns, checkboxes, dates | **Forbidden.** The presence of a line is the status |
| Header | The three lines under the title name the batch and what *usable* means in it. They stay for the life of their block |
| Creating the file | Its shape, per batch, is in `references/new-queue.md` |

Never put in a line what `docs/rules.md`, `docs/glossary.md`, or `docs/product.md` hold. A line needing more than one sentence means the rule behind it is missing from `docs/rules.md`.

## 3 — Where a queue comes from

**`docs/queue.md` absent or just run empty, or the user asks for what it does not hold → read `references/new-queue.md` before building anything**: the three routes a queue comes from, the change record a big change opens first, when the work splits into a UI batch and a backend batch, and the file's shape. Every route ends with the whole queue shown and a **STOP** for the user's approval before the file is written.

## 4 — Before touching code: propose the content, collect the questions once

**Decide what a page holds before it is built** — for any page entering the queue, new or long since built. A page that exists is proposed as *what is missing from this page*. **In a UI batch, propose before the page's `Contract + fixtures` line, never before its page line**: the contract's type is where the decision is recorded.

**Open the proposal by naming the page's archetype** from the screen archetype table in `DESIGN.md`'s Page Composition: its shell layout, components, and density profile are the skeleton the two lists hang on.

- **No archetype fits → that is the first of the bundled questions below**: a new archetype enters `DESIGN.md` through `design-settle`, or the page is reshaped to fit an existing one. Never invent a bespoke layout silently.
- **`DESIGN.md` has no archetype table → propose from the two lists alone**, and report the missing table as a finding pointing at `design-settle`, which retrofits it.

**Derive the two lists, never invent them:**

- **Bound** — taken from `docs/product.md`'s Roles and `docs/rules.md`, and stated, never offered as a checkbox: dropping one means changing `docs/rules.md`, a separate decision of the user's. Read each rule for the screen content it carries — an invariant demanding a reconciliation is a figure on screen; an unregistered code that still appears, marked, is a row and its marker; *every figure can be traced back to the transactions behind it* is a drill-down.
- **Harvest the element, never a sentence about it** — a figure, a column, a marker, a branch of a form, a control present or absent. A rule about what the system does after the user acts lands as the new row appearing, never as a paragraph announcing it. A rule yielding no element yields nothing on this page and stays in `docs/rules.md`: never restate a rule on screen.
- **Optional** — everything else that fits, asked as a multi-select of what to drop: first option `keep all`, recommended, then one option per item — the user ticks what is not wanted, because AskUserQuestion cannot pre-select. Propose the full page and let the user cut it down; a thin proposal is never recovered later.
- **Where the documents run out**, take optional candidates first from the components of the page's archetype in `DESIGN.md`, then from live product-type research — what a mature product of this kind conventionally carries, the floor `design-settle`'s product draft also starts from. That research may run in one subagent on a cheaper model than the session's (`sonnet` on Claude Code), returning a compact list.
- **Both lists coming out short is an answer** — a login screen or a small settings page is legitimately quiet. Never pad one.

### How full is full enough

- **The bar is the app's proving page** — the page `DESIGN.md`'s Page Composition names, the one its direction was proven on. A page far emptier than it is a page to go back to, not a new norm. None named → judge by the two questions below alone, and report the gap as a finding pointing at `design-settle`.
- **Test at the widths `DESIGN.md`'s Layout fixes, never at ones picked per session**: the desktop breakpoint it names — 1440px when it names none — and the supported lower bound.
- **Capture proof as the Proof profile in `docs/product.md` says.** *Browser* and *dev server* in this skill are the web default: a profile naming an emulator or a window capture substitutes its own Run and Visual lines wherever those words appear, at the same two widths or the platform's equivalent bounds. No Proof profile → the web default as written. A profile line still `[needs verification]` → capture what is possible and report what was not, never claim it.

Two questions decide:

> With the `bulk` fixture, at the desktop width: is there dead space taller than one table row carrying nothing?

> Once this role has finished reading this page, what do they ask next — and is the answer here, or does it force a navigation?

The second is the one that produces the summary row, the reconciliation figure, and the drill-down.

### Then the questions

With `docs/product.md`, `docs/rules.md`, and the live schema read, ask **everything** still unclear about this page **in a single turn**, together with the content proposal — a page's unknowns read nothing from each other. Decide everything else yourself, with each default **announced**.

### Where the decision is recorded

**Not in `docs/`** — `docs-format` bans enumeration. It records itself in code a compiler checks: in a UI batch the shape of the page's contract type, in a backend batch the query and the page.

## 5 — The order inside one page

Two chains, one per batch. The backend one extends the chain `db-ops` fixes (`migration → run → introspect → types → frontend`), which owns the detail:

```
UI batch
  the proposal with its two lists, answered — Section 4
    → contract → fixtures, six cases → page + loading, empty, failed states
    → walk all six cases in a browser
    → screenshot the bulk case at both Section 4 widths, judged beside the proving page
    → count the page copy and print the three lines
    → run the lint command — the floor in `ui-build`

Backend batch
  the proposal with its two lists, answered — Section 4 — where no contract holds the page
    → rules from docs/rules.md → migration + RLS → role test → regenerate types
    → query returning the contract type, in the data layer folder
    → one rule test per docs/rules.md topic this page implements — `logic-build` Section 10
    → wire the page → walk the flow in a browser → the page's Playwright spec, run
    → run the lint command — the floors in `ui-build` and `logic-build`
    → the documents this page owes — Section 8
```

- **Write the chain as a visible todo list the moment the page starts** — one entry per step of this batch's chain, plus one per spread page that passed the test in Section 1, in a backend batch the whole spec suite (`references/backend.md`), and the audit offer below as its last entry. Required: it lets the user see the next step without asking. Anything unfinished **lands as a `docs/queue.md` line** before the session closes.
- **Read the running batch's file before its first page**: a UI batch → `references/contract.md` — the contract files, the six fixture cases, the two switches, the copy count; a backend batch, or an app that never split its work → `references/backend.md` — the rule test, the wiring rules, the page spec, retiring a `src/design-canvas/<page>` file still standing. Neither batch needs the other's file.
- **A page with no data contract** — a landing section, a static page — has no fixture cases; prove it at the two widths with its real copy.
- **Settle the account a walk signs in with before the first page is written, where a sign-in already guards the app's routes.** One the session's own instructions carry is used. None → ask once: create one under `db-ops` (`references/agent-account.md`), recommended — a login and a role row written to the app's database · wait for one the user supplies. A page its walk cannot reach is never accepted.
- **Backend first inside one page**, never backend first across the whole app.
- **Loading, empty, and failed states ship with the page**, never as follow-up work — `ui-build` binds them to their component.
- **End the walk with proof, not recall.** Screenshot the `bulk` case at the two Section 4 widths with the session's browser tooling — in a UI batch the walk's subagent saves them (`references/contract.md`) — put the desktop shot beside the proving page at the same width, and answer Section 4's two questions from those screenshots. Dead space taller than one table row at the desktop width → fix the page in this session; it is not a finding to record and move past. No browser tooling → say so and walk the widths live at the dev server; never claim the widths were judged when neither happened.
- **Fix the lint step's refusals before the commit**, under `ui-build`'s rules for living with the floor. A repo with no floor yet skips the step and says so.

### The audit, offered once — never page by page

Once the last page of the session has been walked, offer the audit in one multi-select question covering every page this session built or changed — once per session, never once per page. Its options are the passes that apply — `Accessibility`, `Interaction polish`, `Click path` where handlers are wired, `Platform conventions` where the Surface is not the web — and the question says that more than one may be ticked. Offered, never imposed: ticking none is not one of the Section 6 stops, needs no reason, and changes nothing else about how the session closes.

**A pass ticked → hand the ticked passes to one subagent on a cheaper model than the session's** (`sonnet` on Claude Code) **whose whole brief is `references/audit.md`**: give it that path, the pass names, this session's commit range, the routes it built, and the dev server's address where one runs — and never read that file here, because the audit runs when the session is at its largest. No subagent → say so and run the passes here from that file.

- **Fix a finding inside the pages this session built now, and commit the fix** by the git norms `raizen-norms` prints. Everything else becomes a `docs/queue.md` line.
- **After a fix that changes how a page looks, screenshot its `bulk` case again at the two Section 4 widths**, and judge the result rather than the intention.

## 6 — Do not stop; the list of legitimate stops is closed

| Legitimate stop | Why it cannot be dropped |
|---|---|
| The `db-ops` destructive gate | The user approves a **number**, not an intent — lost data does not come back |
| A role test that misses | RLS fails silently; carrying on to the frontend locks the leak in |
| A business rule that is not in `docs/rules.md` | Guessing it invents a norm through the back door |

- **The list binds from the first line of a page's code.** The queue's approval (Section 3), the content questions (Section 4) and the account question (Section 5) are asked before any page starts, and are not stops of the build.
- **In a UI batch only the third can occur** — there is no migration to gate and no RLS to test. Both return in full in the backend batch, where the role test checks against what the UI already declares each role sees.
- **Anything else: keep going until the page is usable**, and report at the end, never between steps.
- **Stopped for one of the three → leave the working tree dirty**, so the repository itself says something is waiting on the user.
- **`ui-build`'s gate is not overridden**: no design system yet → the page is not started at all.

## 7 — Too big: split, but only where nothing breaks

Splitting is always allowed; only **where** is constrained:

> A legitimate split point is one where **every page that used to be usable still is.**

- **The same test decides what may be a queue line** (Section 2): one whose deletion leaves every page that used to work still working. Work that *adds* passes — a contract and its fixtures, a drill-down the page works fine without. Work that *changes something already shared* fails — a column, a component's contract or props, a table's pagination, a query other pages depend on.
- **The spread from Section 1 is never a split point.** No legitimate split point exists → build it whole; that is the real size of the unit.
- **After splitting, replace the queue line with two lines that each stand alone**, finish the first, and let the rest rise to the next session. Never leave a half-built page unrecorded in the queue.

## 8 — Closing the session

Report the closing block `raizen-norms` prints at session start under `CLOSING THE SESSION`, as written there. Two of its lines rest on this skill: the page usable now **with its route**, and every unfinished step as a `docs/queue.md` line, never as a sentence.

Commit the page as part of finishing it, by the git norms `raizen-norms` prints. **The commit carries the documents its change made false or incomplete** (`docs-format`, same commit), never a later one:

- **A `docs/changelog.md` entry** for a commit that changes how the app behaves — mandatory, in the batch that makes the page usable. A UI batch on fixtures changes no behaviour and writes none.
- **The sentence of `docs/architecture.md` or `docs/runbook.md` the change made false** — a part added or moved, a step of the deploy changed.
- **The guide page of every task the page serves** (`docs/guide/`), where `docs/product.md`'s Help row is not `none` — mandatory in the batch that makes the page usable to its role. A UI batch on fixtures writes none.
- **Delete the page's queue line in the commit carrying these**, never before.
- **A `docs/glossary.md` row** for each domain term the page puts on screen that the glossary lacks — written before the page, per `docs-format`, and committed with it.

A commit that carries none of them is reported `Docs: none — <why>` (`docs-format`, Same commit). A legacy repo writes none of the three: its queue line is deleted when the page is usable.

## 9 — Before the app has ever shipped

**Applies only while `main` carries nothing beyond the bootstrap commit** — anything merged there means the app has shipped, and deploy is then ordinary business. The queue is not that test: a running app growing a feature has one too.

| `docs/queue.md` | What to do about deploy |
|---|---|
| Still has lines | **Never raise deploy, hosting, CI, or production environment variables on your own initiative.** None is needed to build a page and use it locally |
| Gone | **Raise it, once** — the only time this skill brings deploy up by itself. Name what is still unwired: hosting connection, production environment variables, CI migrations. Add that the host chosen at bootstrap *may* have a Claude connector automating the first of those — derived from the stack actually chosen, never promised. A shortcut offered, not a step required. Then leave it to the user |

- **Read the table against the last batch, not the current one.** A UI queue running empty means every screen is accepted, not that the app works; `Gone` applies when no batch is left.
- **The user asks to deploy → do it**, with no lecture and no gate: one sentence naming any table whose RLS has not been role-tested, and only if such a table exists.
- **State the commits as a fact in the close block, never as a question** — *shall I commit?* is never asked: a finished page is already committed (Section 8).
