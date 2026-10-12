---
name: db-ops
description: Rules for touching the database — introspection, migrations, RLS and role testing, destructive operations. Use before writing any SQL, altering a table, creating or changing an RLS policy, or running any DELETE, DROP, TRUNCATE, or UPDATE.
---

# db-ops — rules for touching the database

Documents are named by their `docs/` path; a repo with a root `PRD.md` reads each through `docs-format`'s legacy map.

## What a load costs — two rules

- **Run independent reads, searches and commands in one turn** — parallel calls, or one chained command — because every extra model call re-reads the whole session. Nothing is chained past a STOP.
- **Never re-read what the session start printed.** The database's state is not in it: introspect wherever a rule below says to, every time.

## The axis

Schema has git through migration files; **data does not**. A `DROP COLUMN` can be undone with a new migration — a deleted row cannot.

The size of the change is not the criterion: blast radius is only knowable after the fact.

## Before writing any DDL

**Introspect the relevant state first** — DDL written without reading the current state is a guess.

**Check a Postgres pattern you are not certain about** — indexes, column types, constraints, the shape of an RLS policy — against the `supabase-postgres-best-practices` skill before writing it into a migration file. Disagreement → `db-ops` wins: a general Postgres rule never overrides a rule of this file — the mandatory order, the destructive gate, and role testing included. That skill is not installed → continue without it, do not stop.

Schema changes are written as **migration files in the repo**, not run directly against the production database. What may be run directly: `SELECT`, and role tests that end in `ROLLBACK`.

## A new table in a repo that audits

Applies only when `docs/decisions/` records an audit trigger.

**A new table is created with its audit trigger in the same migration**, never in a follow-up: the period it ran untracked has no history, and no later migration brings that back.

**Leaving a table untracked takes an explicit answer from the user, asked before the migration runs** — silence is not that answer. State what the table holds and ask; a lookup of provinces or a cache of computed totals is fair to leave out, and the user is the one who says so. Never track everything by reflex either: a table tracked without thought is the same failure as a table skipped without thought.

Record the skip nowhere — introspection shows a table without a trigger.

## Mandatory order

```
migration → run → introspect AFTER → regenerate types → frontend
```

Never reordered — reversing it produces `as any` patches that become permanent technical debt.

**Introspecting afterwards is mandatory, including when the execution looked successful.** Show the result as-is, never paraphrased: the user is the one checking it, and "succeeded" without the read-back is a claim without evidence.

## Destructive operations

`DROP` · `ALTER ... DROP COLUMN` · rename · `ALTER TYPE` that changes the type · `DELETE` · `TRUNCATE` · `UPDATE` without a narrow `WHERE`.

They are allowed. What is not allowed is doing them **without a number** and **without a guard**.

**This gate stands where a migration is written, not where it runs.** CI applies whatever migration files reach it, ungated. So never tell the user the database is protected from destructive change — the authoring path is. A destructive migration written by hand reaches production with nothing in its way.

**A repo may switch the enforcing hook off — the user's decision, never the agent's.** A marker file at `.claude/destructive-gate.off` (content: one line naming why) disables the hook for that repo alone; deleting it turns enforcement back on. Every phase below remains the norm even there — the marker removes the enforcement, not the rule.

**Phase 1 — PRE.** `SELECT COUNT` for the rows that will be hit. Set the **Expected** number: how many rows should be deleted or changed. That number goes straight into the guard condition.

**Phase 2 — GATE, STOP.**

```
DESTRUCTIVE
Operation  : [what]
Affected   : [real number from SELECT COUNT — not an estimate]
Expected   : [how many should be deleted/changed — becomes the guard]
Reversible : [yes/no — if no, name what is lost permanently]
```

Then **STOP** and wait for the user's answer in this session. The user approves the **number**, not the intent. The approved number is what goes into the guard, with no adjustment of your own.

**Several destructive operations one request needs share one STOP**: one block per operation, in the order they run, each with its own numbers. Run only the operations the reply approves.

**Phase 3 — GUARDED EXECUTION.** Never sent bare. The hook will refuse it, and that refusal is correct.

Row-destructive:

```sql
DO $$
DECLARE n int;
BEGIN
  DELETE FROM <table> WHERE <predicate>;
  GET DIAGNOSTICS n = ROW_COUNT;
  IF n <> <Expected> THEN
    RAISE EXCEPTION 'Expected <Expected> rows, actual %. Aborted.', n;
  END IF;
END $$;
SELECT <query proving the resulting state>;
```

Structure-destructive operations have no meaningful `ROW_COUNT`, so their guard is a check **before** the operation inside the same block:

```sql
DO $$
DECLARE n int;
BEGIN
  SELECT count(*) INTO n FROM <table> WHERE <column> IS NOT NULL;
  IF n <> <Expected> THEN
    RAISE EXCEPTION 'Expected <Expected> rows affected, actual %. Aborted.', n;
  END IF;
  ALTER TABLE <table> DROP COLUMN <column>;
END $$;
SELECT <query proving the resulting state>;
```

The exception aborts the whole transaction, so the verifying SELECT never runs and zero data is lost.

**Operations approved at one STOP run in one `DO` block, each with its own check against its own Expected**: one miss aborts them all, where a block each leaves the earlier ones committed.

**Phase 4 — REPORT.** Actual versus Expected, plus the SELECT output as-is. Include integrity checks when relations are touched: orphaned FKs, `NOT NULL` now violated, rows that failed to cast.

Aborted by the guard, or an integrity check that fails → **stop entirely, do not touch the frontend.**

## RLS — role testing is mandatory

RLS fails **silently**: no error, just leaked data or missing data.

**The default connection is the owner, so RLS is bypassed.** A query without `SET LOCAL ROLE` tests no policy at all; it only tests whether data exists. The result looks reasonable and proves nothing.

Showing `qual` and `with_check` only proves the policy **exists as written**, not that its predicate is **correct** — a predicate that is valid SQL but wrong in logic survives any amount of careful reading.

Test pattern, one call per role — the claims and role names are Supabase's; on another Postgres, set the role and the session settings its own policies read:

```sql
BEGIN;
  SELECT set_config('request.jwt.claims',
    '{"sub":"<uuid of a user with this role>","role":"authenticated"}', true);
  SET LOCAL ROLE authenticated;
  SELECT <query representing this role's real access>;
ROLLBACK;
```

`ROLLBACK` makes this test free of side effects.

**Also test the role that should see zero rows.** The negative test is what catches leaks; the positive one only proves the data arrives.

A real user UUID is needed per role, on **every** RLS change, not once. None exists yet → seed one first (`references/agent-account.md`).

Report per role: role · UUID · rows visible · rows expected · match or not. Mismatch → stop, do not move on to the frontend.

**Writing policies:** multi-table predicates with overlapping column names → fully qualify them. A policy that must be identical to an existing one → copy the predicate verbatim from introspection, do not rewrite it from memory. A new table → RLS enabled and its policy in the same operation; a table with RLS enabled and no policy is readable by nobody.

## An account for the session

**A session that must sign in to the app and holds no account for it reads `references/agent-account.md` before creating one** — a login inserted by SQL, never by a migration.

## Invocation

**A step is one command up to its next STOP**: every statement of the step in one file or one call, never one call per statement — the role test alone keeps its call per role. **A read spans environments in that command**: the same introspection against two servers is two lines of it. **A write reaches one environment per command**, so a mistake lands once.

Multi-object introspection is combined into **one SELECT** (`json_build_object` or `UNION ALL`) when the tool in use only returns the last result set. `DO $$ ... $$` returns zero rows — its success is invisible, so always follow it with a verifying SELECT.

`RAISE NOTICE` often does not get through. Do not use it as output; `RAISE EXCEPTION` to abort, `SELECT` to report.

## Types

Regenerate after every schema change, before touching the frontend. The source is the live schema, not memory.

An `as any` cast on a call that is absent from the types file: **a finding to report**, not a pattern to imitate.
