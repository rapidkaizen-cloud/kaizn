# logic-settle

Running it decides what sits between the database and the UI — fetching, validating, dating, error reporting, scheduled work, change attribution — installs only what you approve, and writes the lint floor that keeps every database call in one folder.

| | |
|---|---|
| Kind | Settle skill — runs only when you invoke it |
| Run | `/kaizn:logic-settle` |
| Run it when | After `app-settle` and before `design-settle` on a repo started from scratch; or when a repo grows handwritten data fetching or validation and you ask what to adopt |
| Needs first | `docs/PRD.md`, or a root `PRD.md` read through the legacy map. Not on `main`. A clean working tree is advised, not required |
| Writes | `docs/decisions/` records (and a `docs/README.md` line where `docs/decisions/` is created), `CLAUDE.md`'s Stack table and its `Data layer` row, the `## Logic` part of `AGENTS.md`, the lint floor config; installs only what the Step 5 block lists |
| Commits | At the close, by the session norms' `GIT` block; a migration that ran gets a commit of its own. Never pushes |
| Source | `skills/logic-settle/SKILL.md`, `skills/logic-settle/references/` |

## What happens

There is one path and no repo state to pick: the Step 1 audit decides the rest.

1. **Step 0, preconditions.** One block: `PRD`, `Decisions`, `Stack`, `Server surface`, `Application code`, `Branch`, `Flow`. The server surface is read from the Stack table and `docs/product.md`, and from the code where code exists; the code wins when they disagree.
2. **Step 1, the audit.** One subagent reads what the repo does, never what the decision records claim, and returns an `AUDIT` block. It is printed on every repo, an empty one included. Rows: `L1 cache` to `L6 attribution`, `Data layer`, `Health`, `Duplicates`, `Call sites`, `Deviates`. Two libraries covering one need are consolidated as repair: it needs approval, not an interview. The count of unvalidated boundary handlers is always reported.
3. **Step 2, the score.** Six needs are read from the documents, never asked; a need the documents do not mention scores no. The block gives one line per need with its source, plus a `Data layer` line: the folder holding most database calls, as found and never renamed for tidiness.

   | Need | Scores yes when | Recommended by default |
   |---|---|---|
   | L1 cache | A role reads, searches or filters records | Handwritten below roughly three list screens, the researched standard from three up |
   | L2 validation | A server surface exists | The runtime decides; handwritten parsing fits one handler with one or two fields |
   | L3 dates | `docs/rules.md` holds timing or deadline rules | The platform first (`Intl`, Temporal where shipped); a library only for a rule the platform cannot cover |
   | L4 errors | A server surface exists, or the Surface ships as an installed binary, and the Deploy row of `docs/product.md` names people other than its builders | Host logs until someone is on the hook for failures, then an error-triage service |
   | L5 jobs | A rule names a recurring run | Not yet; then `pg_cron` for pure SQL, host cron for anything calling an external API |
   | L6 attribution | A role may change or delete another role's records, or `docs/rules.md` holds approval rules | A database trigger writing an append-only audit table |

4. **Step 3, the interview.** Asked only for the needs that scored, through questions with a marked recommendation and a consequence per option. Unless exactly one need scored, you first choose **Fast** (every scored need decided from the criteria, the research, the audit and the documents, shown once as a list with a basis per line) or **Full** (recommended; every scored need asked). Both end at the same records and install block. Where the audit found something installed, `Keep — <what is installed>` is the first option; where it found nothing, `none` is never dropped. Every option quotes its migration size from the audit.
5. **Step 4, the record.** One decision record per decision, including every `none` and every keep no record carried before, with a one-sentence reason and no version. `CLAUDE.md`'s Stack table gets names only, plus the `Data layer` row.
6. **Step 5, the install block.** A chat stop (below), skipped when every answer was `none` or keep, the repo already has a linter, no database call sits outside the data layer folder and no installed library is left unused. Each migration line says `this session` or `queue line` with its count, and your approval settles which; a library your answers leave unused is a `Will remove` line.
7. **Step 6, one pass.** Only where something is replaced or moved. Every call site of one decision moves in one session, the build is confirmed, and only then is the old library removed. A migration approved as `queue line` is not started; it becomes a `docs/queue.md` line.
8. **Step 7, the floor.** For every app with a database or a remote API, whatever scored. Five refusals are written into the stack's own linter: a database client outside the data layer, a secret on its way to the client, a second library for a settled need, a cast that erases a database type, a swallowed error. The config is proven first on what must pass, then with one planted violation per refusal, and the scratch file is deleted. The `## Logic` part of `AGENTS.md` is written in the same act.
9. **Step 8, the close.** One block: needs and sources, audit findings, decisions including every `none`, the data layer folder and its basis, what was installed and removed, the floor and its baseline size, what is still `[needs verification]`. On a repo started from scratch it offers `design-settle` next.

### The data layer folder

It is measured by the audit and shown with its basis, never asked first. The `Data layer` row of `CLAUDE.md` holds its path in backticks, first in its cell; the session start reads the path from there to list the folder's functions, and prints nothing for a row it cannot parse.

| The audit found | The folder |
|---|---|
| One folder holding most database calls | That folder, as found |
| Calls scattered, no folder holding most | The folder already holding the most that is neither a page nor a component folder, with its count; the rest are the migration Step 5 prices |
| No database calls yet | The framework's own convention where it names one, else `data` under the stack's source root |

A page or component folder is never the data layer, however many calls it holds.

### Attribution at L6

A trigger chosen at L6 installs no package. Its design is copied into a migration, read through one `SECURITY DEFINER` function, and smoke-checked by writing and deleting one throwaway row. The close hands you the `Roles` line for `docs/product.md`, which is yours to add. If the tracked tables hold columns not every role may read, you are asked to filter on read (recommended) or on write.

## What it asks you

| Question | What your answer decides |
|---|---|
| Confirm the score and the `Data layer` line | Accept as read (recommended), or flip need lines or the folder |
| Fast or Full | Whether the corrections come before the decisions or after them |
| One question per scored need | The library, handwritten code or `none`, recorded with its reason |
| Filter on read or on write (L6) | Whether the audit view is narrowed or the evidence incomplete |
| The install block | What is installed, removed and migrated, the data layer move included |

## Where it stops

- **Step 0.** No PRD in either form (it points to `app-settle`), and branch `main`.
- **Step 2.** The confirmation question. All six scoring no with nothing installed skips the interview, the record and the pass; the install block still runs where the repo has no linter, because Step 7 writes its floor into one.
- **Step 5.** The install block is the one chat stop: end of turn, then your reply in chat. The data layer line is a migration like any other, priced in files and declinable; declined, those files are baselined at Step 7.

> [!NOTE]
> A dirty working tree is named and the session carries on. Committing or stashing first keeps this session's diff separable.

## What it never does

- **Open on its own initiative on a running app.** Your asking is the trigger. A session that finds the layer bleeding offers it once, through a question carrying the measured finding and a recommendation. Declining closes the matter for that session.
- **Manufacture a need.** Zero needs scoring yes, and keeping everything, are normal endings.
- **Install outside the block**, or offer a candidate that fails the admission rule: broad adoption, active maintenance, proven at scale. Unverified options are marked `unverified`.
- **Record a decision in a fourth place** beside `docs/decisions/`, `CLAUDE.md` and `AGENTS.md`. The lint config, a `docs/queue.md` line for a migration too large for the session and the audit trigger's migration file record none. No `ARCHITECTURE.md`, no `DECISIONS.md`, no audit report as a file.
- **Repair what stands when it writes the floor.** Existing violations go into the linter's baseline, which only shrinks; no rule is lowered to a warning.
- **Install a later need silently.** A need that surfaces after the session is raised to you; this skill is the only place its question is asked.

## Related

- [app-settle](app-settle.md), which writes the documents this skill scores from
- [design-settle](design-settle.md), the next session on an app with a UI
- [logic-build](logic-build.md), the rules the floor writes into the linter
- [db-ops](db-ops.md) and [gates](../concepts/gates.md), for the migrations a trigger or a data layer move involves
- [Starting an app](../guide/new-app.md) and [existing app](../guide/existing-app.md)
