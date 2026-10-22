# build-flow

A session building your app opens by showing where the build stands, delivers whole pages that work, and keeps `docs/queue.md` as the one list of what is not built yet.

| | |
|---|---|
| Kind | Rule skill — a session loads it by its description; there is no command |
| Loads when | Before starting any page or feature, and when deciding what to build next |
| Governs | The queue in `docs/queue.md`, how much one session delivers, what a page holds, the order of work inside a page, the closed list of stops |
| Reads | `docs/queue.md`, `docs/product.md`, `docs/rules.md`, `docs/glossary.md`, `DESIGN.md`, the routes in the repo, the live schema, `git log`, `git diff` |
| Source | `skills/build-flow/SKILL.md` and its `references/` files |

A repo with a root `PRD.md` is read through the legacy map in [docs-format](docs-format.md).

## What a session is held to

**Orient first** (Section 0). Before it asks anything or touches code, a session about to build prints the block shown below. `Usable now` comes from `git log --oneline -- docs/queue.md`, from the routes in the repo, and from `git diff` — so a deletion not yet committed does not read as an unbuilt page. A backend batch adds live schema introspection; a UI batch adds the contract files. It is never copied from a record.

**One unit: what fits in a context window** (Section 1). A session delivers pages that can be opened and whose work their role can finish. The bound is the window, never a number.

| Batch | What one page carries | Pages per session |
|---|---|---|
| Backend | migration · RLS · role test · types · query · wiring · spec | One |
| UI | contract · fixtures · the page and its states | As many as fit |

Where a session takes several pages, the ones that set a pattern come first: the shell and navigation, one table page, one form page.

**Finish what spreads** (Section 1). One test sizes the session: *if I stop here, does any page that used to work stop working?* If yes — a shared column, a shared component's contract, a query other pages use — the work is finished in this session. If no, it becomes a line in `docs/queue.md`.

**A queue, not a record** (Section 2). The file holds only pages not usable yet, in build order, one line each, in the app's own locale: `- <page> — <role> — <the work that can be finished there>`.

- **A finished line is deleted at that moment**, never ticked and never left to the end of the session. History is `git log docs/queue.md`.
- **No status columns, checkboxes or dates.** The presence of a line is the status.
- **An empty queue is deleted**, not kept.

**Where a queue comes from** (Section 3, `references/new-queue.md`). Three routes, by the state of the repo:

- **No application code yet.** Built from the Roles in `docs/product.md` and from `docs/rules.md`.
- **Code present, app never finished.** Discovery first: the routes that exist and the live schema. A half-built page gets a line naming what is missing.
- **The app works and you want something.** The queue comes from the request. A change spanning more than one page or session, or adding a role or data kind, opens `docs/changes/<date>-<slug>.md` first. Rules go into `docs/rules.md` and terms into `docs/glossary.md` before any implementation.

Where the app keeps help inside it — the Help row of `docs/product.md` opens with `in-app` — the help page gets a line of its own until it exists.

Work may split into a UI batch, then a backend batch that wires it. An app built from nothing is built that way. An app that already runs splits only for three or more pages at once, or a requirement still vague. The UI queue running empty is the freeze: a contract changes after it only as a stated decision. A batch asked for while the queue holds lines of the other kind — a UI batch above `Prove:` lines, say — is written as a block of its own above them, with its own title and header; the session builds the first block, and a block that runs empty goes with its title.

**Propose the page before building it** (Section 4). The session names the page's archetype from `DESIGN.md`'s Page Composition, then proposes two lists. The **Bound** list comes from the Roles and `docs/rules.md` and is stated, never offered as a checkbox. The **Optional** list is a multi-select of what to drop, whose first option is `keep all`. Every open question for the page is asked in one turn; every other choice is made and announced. The bar for a full page is the proving page `DESIGN.md`'s Page Composition names, judged at the desktop width and the lower bound `DESIGN.md` fixes; where it names none, the session judges by its two questions alone and reports the gap. The decision is recorded in code a compiler checks, never in `docs/`. In a UI batch the proposal comes before the page's `Contract + fixtures` line, because the contract's type is that record.

**The order inside a page** (Section 5). The session writes its batch's chain as a visible todo list the moment the page starts, the proposal as its first entry and the audit offer as its last; anything unfinished lands as a `docs/queue.md` line before the session closes.

```
UI batch      contract → fixtures (six cases) → page with loading, empty, failed states
              → walk the six cases → `bulk` screenshot at both widths, beside the proving page
              → page copy count → lint
Backend batch rules → migration + RLS → role test → types → query returning the contract type
              → one rule test per rule → wire the page → walk the flow → Playwright spec → lint
              → documents
```

- **Backend first inside one page**, never across the whole app.
- **In a UI batch the walk of the six cases runs in a subagent** on a cheaper model, because a walk is dozens of browser calls and each one made in the session re-reads all of it. The subagent reports one line per case and saves the `bulk` screenshots; the session reads and judges them itself. A backend batch walks its flow in the session. Where your app has a sign-in and the session holds no account for it, you are asked once, before the first page is written, which account the walks sign in with: one created through `db-ops` (recommended; a login and a role row written to the app's database), or one you supply.
- **Dead space taller than one table row** at the desktop width is fixed in the session, not recorded.
- **Lint refusals are fixed before the commit.** A repo with no floor yet skips the step and says so.

**A UI batch is proven against a contract** (`references/contract.md`). `src/contracts/<page>.ts` holds types, `src/contracts/<page>.fixtures.ts` the six cases: `loading`, `empty`, `single`, `bulk`, `messy`, `failed`. A page is not accepted until all six render without the layout breaking. Fixtures are copied from the document the app replaces, with every name, phone number, e-mail, address and free-text value replaced by an invented one of the same shape; figures, dates, codes and statuses stay as they are. Two switches pick the case and the role: `?fixture=messy` and `?role=approver` on the web, the **Cases** line of the Proof profile elsewhere. No file under `src/pages` imports the database client or the generated database types; one grep at the close checks it.

**A backend batch wires, never patches** (`references/backend.md`). The query returns the contract type, with no `as any` and no `as unknown as`. A query that cannot satisfy the contract changes the contract, and the page returns to the queue. The mocked session is replaced.

**A wired page leaves a Playwright spec** (`references/backend.md`). `e2e/<page>.spec.ts` replays the flow the session walked, then the page's `failed` and `empty` states, with its reads answered by `page.route` so no real row is emptied or broken. It runs before the commit, and afterwards with `npx playwright test` at no model cost. A read made on the server cannot be answered that way, so those two tests are marked `test.fixme` and show as open in every run. The browser is your installed Chrome, started headless on a temporary profile of its own: your Chrome, its tabs and its sign-ins are not touched. The spec signs in through environment variables, and a write it makes lands on a `[CLAUDE]` row it deletes. A write that would send anything out — an e-mail, a webhook, a message — is always answered by `page.route`, so no run sends one. Before the session's last commit the whole suite runs once: a failure the session caused is fixed then, any other becomes a queue line. An app that is not on the web writes no spec.

**Closing** (Section 8). The session reports the closing block the session start prints, commits the page, and the commit carries a `docs/changelog.md` entry where the app's behaviour changed, the sentence of `docs/architecture.md` or `docs/runbook.md` the change made false, a glossary row for each term the page puts on screen, and — in an app that keeps help for its users — the guide page of every task the page serves. A UI batch on fixtures writes no changelog entry and no guide page. A commit that carries no document is reported `Docs: none` with its reason. See [Documents](../concepts/documents.md).

**Deploy stays unraised** (Section 9) while `main` carries nothing beyond the bootstrap commit and `docs/queue.md` has lines. When the file is gone and no batch is left, deploy is raised once. Asked to deploy, the session does it.

## What you will see

```
Batch      : UI
Usable now : Request list · Create request · Request detail
Queue left : 3 lines
Next       : Approval inbox — Approver
```

- **The proposal question**, with `keep all` as its recommended first option.
- **The whole queue**, before the file is written.
- **One question at the first backend page of a repo with no Playwright**, bundled with the page's other questions: install `@playwright/test` as a dev dependency (recommended; it downloads no browser) or carry on unproven, with one `Prove: <page> spec` line per page in `docs/queue.md`.
- **The page copy count**, in a UI batch, longest and median in words per class — `Action`, `Name`, `Explanation`:

```
/visits
Action       longest 2 · median 2
Name         longest 4 · median 2
Explanation  longest 8 · median 6
```

- **One audit question** after the last page, covering every page the session built or changed. You tick the passes you want — Accessibility, Interaction polish, Click path where handlers are wired, Platform conventions where the app is not on the web — and ticking none needs no reason. The ticked passes run in a subagent over the session's diff and write no document. A fix inside this session's pages is committed, and a page whose look changed is screenshotted again at both widths; everything else becomes a queue line.

## Where it stops

- **The queue.** Every route ends with the whole queue shown and a wait for your approval (Section 3).
- **The closed list** (Section 6): the `db-ops` destructive gate, a role test that misses, a business rule not in `docs/rules.md`. A UI batch can reach only the third. The working tree is left dirty, so the repo itself shows something waits on you.
- **Canvas file deletion.** A `src/design-canvas/<page>` file is proposed for deletion at a chat stop and deleted only on your confirmation.
- **No design system.** The page is not started at all (`ui-build`'s gate).

Anything else: the session keeps going and reports at the end.

## What it does not cover

- **Behaviour that crosses screens** cannot be proven by fixtures. It is verified in the backend batch.
- **Contracts are never retrofitted** to a page that already has a real query.
- **Storybook, a mock server, a fixture generator.** None is used.
- **Deploy work** before the first ship, unless you ask.

## Related

[docs-format](docs-format.md) · [ui-build](ui-build.md) · [db-ops](db-ops.md) · [logic-build](logic-build.md) · [design-settle](design-settle.md) · [Gates](../concepts/gates.md) · [Documents](../concepts/documents.md)
