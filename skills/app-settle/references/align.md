# Align — existing code catches up with the rules

Mechanical work: change **code and agent files that already exist**, and only where they disagree with the conventions the installed plugin states.

## Limits

**The stack is not on trial, and no decision is re-opened.** Remove what a departed platform left behind; never choose its replacement. Swapping a framework, a host, or a database is Rework, and a finding only a new decision can settle is dropped at A4.

**No feature work and no drive-by fixes.** A bug found during the audit is a finding, reported and left: fixed inside an alignment commit, it hides from the diff that was approved.

**A document that disagrees with the code is corrected only where it states what exists** — a path, a name, something the code has never done: the code wins, and that one line changes. A mismatch about what ought to be — a rule, a role's limit, a prohibition — is never settled here in either direction: list it under `Dropped`, because Rework is where the user says which side is right. In doubt → the second. Never edit a frozen record.

**The findings live in the session and the commits** — no audit report, migration plan, or checklist as a file. Align creates only files that record nothing about the app: `AGENTS.md` under C2, `docs/queue.md` under C5, C7 and C8, and under C6 the linter's config and its suppression baseline.

**An empty audit is a normal ending.** Close having changed nothing and say so; manufacture no finding.

## A1 — Audit, before asking anything

**Run the audit in one subagent on a cheaper model than the session's** (`sonnet` on Claude Code) **whose whole brief is `audit.md`**: hand it that path, the repo root, the installed plugin path, every `NOTE` line the session start printed, and `Rows: C1 C2 C4 C5 C6 C7 C8`, and never read that file here. No subagent → say so and run the audit here from that file. No model choice → the session's model.

**C3 is never run unasked**: it reads every identifier, route and database name in the repo, and what it finds is band 3 unless a rename is cheap. A3 offers it.

**The installed plugin copy is the standard, not the toolkit repo's `main`** — an unreleased fix reaches no app. Read a rule's exact text from the installed plugin. A rule that looks wrong is a finding for `app-eval`, in the toolkit repo, in another session.

**It returns only the `AUDIT` block — eight rows, C1 to C8, a clean one included and C3 as `not run` — with what each row counts listed under it.** Print it as returned.

Each row's cost if left, and the fix Align allows:

- **C1 platform residue** — what still references the platform the app left.
- **C2 agent files** — a norm copied into `CLAUDE.md` contradicts the plugin once the plugin changes; a stale skill or command name sends the next session somewhere that is not there. **A norm the plugin prints nowhere stays in the file**: it goes on the `For app-eval` row, never into the table. **With no `AGENTS.md`, every agent that is not Claude Code works here with no rules at all** — no norms, no injected documents, no idea a shared set of components exists — and its first UI edit writes a second one: say that as the cost, and ask which other agents touch this repo, because the answer ranks the finding. Write the file to the shape `scaffold.md` gives (N5) — the `## UI` part, where `DESIGN.md` exists, as `design-settle`'s `pass.md` fills it under The lint floor; the `## Logic` part, where the `Data layer` row exists, as `logic-settle` Step 7 (`references/floor.md`) fills it; every path either names must resolve. **Never produce it by moving `CLAUDE.md`'s content or by linking the two**: they have different readers.
- **C3 language split** — rename only at A4, with the cost stated: a database name is a migration, a type regeneration, and every call site; a route is a link somebody may have bookmarked.
- **C4 guard coverage** — a norm that silently cannot apply here: the repo reads as protected and is not.
- **C5 documents** — a stray competes with `docs-format`'s closed list, and the loser goes stale silently. **Never rewrite a frozen record**: revert an edit made after freezing only on the user's word, and move what it meant to say to the living document or a superseding record. A missing living document is seeded as `SKILL.md`'s Step 0 says, in its own run; a missing guide page is a `docs/queue.md` line; a stale path is the one line corrected.
- **C6 lint floor** — two halves in one config behind one lint command, each proven as A4 orders.
  - **UI half, only where `DESIGN.md` exists** — without it there is nothing to derive a floor from, and `design-settle` writes both. With no floor, each session, and each agent that never loads `ui-build`, re-decides the design system by judgement. **The fix is `design-settle`'s lint floor, unchanged** (its `pass.md`, The lint floor), derived from this app's shared set and styling files, **existing hits baselined, not fixed**: repairing them is `design-settle`'s fix-the-drift path, a diff the user has not approved here. No linter in the repo → its install is one line inside the finding's cost-to-fix: a dev dependency, not the stack.
  - **Logic half, owed by every app with a database or a remote API** — with no `Data layer` row in `CLAUDE.md`, the first refusal has no path to scope to and the session-start listing prints nothing. **The fix is `logic-settle` Step 7's floor (`references/floor.md`), unchanged**: the folder named as that skill's Step 2 derives it, as found and never renamed; the five refusals derived from this app; everything already standing baselined. **Never move old call sites into the folder**: that is a migration priced in files, and `logic-settle` is where the user approves one.
- **C7 rule coverage** — an uncovered topic is a rule the next session, or another agent, can change while every page still renders. **Never write the test here**: a rule test attacks an enforcement point and a failing one is a bug, both build work. Write one `docs/queue.md` line per uncovered topic, `Prove: <topic>`, in `build-flow`'s shape, creating the file with its header where a finished app no longer has one. No runner → never ask here whether to install one: the build session that reaches the first line asks, under `logic-build`.
- **C8 page specs** — a page with no spec has its flow and its `failed` and `empty` states checked by nobody once its walk is over. Fix it as C7: one `docs/queue.md` line per page, `Prove: <page> spec`, and no install question here — the build session that reaches the first line asks, under `build-flow`.

## A2 — Rank, with the cost of leaving each one

One table, worst first, ordered by **what breaks without anyone noticing**, never by how easy the fix is.

| Rank | Finding | Costs if left | Costs to fix |
|---|---|---|---|
| 1 | … | … | … |

Three bands, in this order:

1. **A guarantee that does not hold** — C4, a C6 floor that is absent or hollowed out, a C7 topic carrying money or permissions with no test, a missing `AGENTS.md` where the user named another agent working here, and any C1 row that can break an install or a build on a machine that has not run one yet. Silent until it is expensive.
2. **A rule that points somewhere wrong** — C2 stale names and an `AGENTS.md` path that does not resolve, a missing `AGENTS.md` where no other agent is in use yet, the remaining C7 topics, C8 pages with no spec, C5 documents — competing, stale, or edited after freezing. Costs the next session, every session.
3. **Drift that is merely untidy** — C3 renames whose blast radius exceeds their benefit, leftover files nobody reads.

**A fix whose cost exceeds what it buys is still listed**, in band 3, with the recommendation *leave it* — a column renamed for tidiness states its C3 cost rather than dropping the row.

## A3 — The user picks, then STOP

Put the ranked table up through **AskUserQuestion**, never as prose at the end of a turn. Assemble the options from the bands: band 1 only · bands 1 and 2 · everything · nothing. Recommend **band 1 only** unless the session has room and the bands below carry no migration. Individual lines are added or dropped through the answer or "Other". Then **STOP** and wait.

**Offer C3 in the same call while it reads `not run`** — a second question, `Audit the language split too` or `Skip it`, each with its cost: the scan reads the whole repo; skipped, a name in the UI language stays unreported. Recommend `Skip it` unless a finding of the first run quotes such a name. No finding in the first run → ask this question alone. Picked → run the subagent again with `Rows: C3`, add what it finds to the table in its band, and ask again for those lines only.

Nothing selected is a valid answer and a normal ending: close with the audit reported and no commits.

## A4 — Execute, one finding per commit

**One finding, one commit, named paths — never a batch**: a finding that turns out wrong is then one `git revert`, and the approved diff is the diff in the commit. Work in ranked order; a later finding that depends on an earlier one says so before the first is started.

Five checks bind every commit:

- **Anything touching build or run config gets one real run before the commit** — the build command, or the dev server reaching one page — because a config swap can type-check and not boot. It is the only check Align requires.
- **A lint floor is proven before its commit, in the order `design-settle`'s `pass.md` gives under The lint floor** — the lint command over the whole app first, where every hit is either baselined or a pattern too wide to keep, then one planted violation per refusal seen refused, the scratch file deleted. A floor committed unrun is a C4 finding Align wrote itself.
- **Anything touching the database is under `db-ops` unchanged** — the destructive gate, the mandatory order, the role test. A rename is destructive, however tidy.
- **Several picked findings that are destructive share one STOP, before the first finding starts**: count them all, show a `DESTRUCTIVE` block per finding, and run only the ones the reply approves. Each still runs in its own guarded block and its own commit, never in the one block `db-ops` gives operations approved together, because a finding is reverted alone.
- **A finding that turns out to need a decision is dropped, not decided** — the stack, a business rule absent from `docs/rules.md`, a prohibition nobody stated: stop on that line, leave the working tree as it stands, report it, and carry on with the next finding.

**Scope is the selected lines and nothing else.** A path that changed outside them is reported, never committed along — the `kaizn` rule, unchanged.

## A5 — Close

```
ALIGN
Fixed        : [one line per finding, with the commit]
Dropped      : [findings that needed a decision — and which decision]
Left         : [band 3 lines the user declined, or that were recommended to leave]
Not audited  : [C3 — offered and skipped]  or  [none]
Still silent : [any C4 guarantee that is still not in force, and why]
Verified     : [what was actually run — the build, the page, the role test]
For app-eval : [findings that are defects in the rules rather than in this app — or "none"]
```

Never soften the last two rows. **`Verified` names what was executed**: a build that was not run is written as not run. **`For app-eval`** reports a rule that produced this drift; never fix it from inside the app repo — it is fixed in the toolkit repo, in another session (`app-eval` Step 0).
