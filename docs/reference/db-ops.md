# db-ops

A session reads the database before it changes it, writes schema as migration files, tests every RLS change as each role, and runs nothing destructive without a number you approved and a guard that enforces it.

| | |
|---|---|
| Kind | Rule skill — a session loads it by its description; there is no command |
| Loads when | Before writing any SQL, altering a table, creating or changing an RLS policy, or running any `DELETE`, `DROP`, `TRUNCATE` or `UPDATE` |
| Governs | Introspection, migrations, RLS and role testing, destructive operations, generated types |
| Reads | The live schema, introspected each time; `docs/decisions/` for a recorded audit trigger |
| Source | `skills/db-ops/SKILL.md`, with `references/agent-account.md` |

## What a session is held to

**The axis** (The axis). Schema has git through migration files; data does not. A dropped column is undone with a migration, a deleted row is not. The size of a change is not the criterion, because blast radius is only knowable after the fact.

**Read first, then write migrations** (Before writing any DDL). The session introspects the relevant state before it writes DDL. Schema changes are migration files in the repo, never run directly against the production database. What may run directly is `SELECT`, and role tests that end in `ROLLBACK`. A Postgres pattern the session is unsure of is checked against `supabase-postgres-best-practices`; where that skill disagrees with `db-ops`, `db-ops` wins, and an absent skill never stops the work.

**Audited tables** (A new table in a repo that audits). Applies only where `docs/decisions/` records an audit trigger. A table is created with its audit trigger in the same migration. Leaving one untracked takes your explicit answer, asked before the migration runs; silence is not that answer. The skip is recorded nowhere, because introspection shows a table without a trigger.

**A fixed order** (Mandatory order). Never reordered:

```
migration → run → introspect AFTER → regenerate types → frontend
```

Introspecting afterwards is mandatory even when the run looked successful. The result is shown as returned, never paraphrased.

**Destructive operations** (Destructive operations): `DROP`, `ALTER ... DROP COLUMN`, a rename, an `ALTER TYPE` that changes the type, `DELETE`, `TRUNCATE`, and `UPDATE` without a narrow `WHERE`. They are allowed, never without a number and a guard. The stop itself is explained in [Gates](../concepts/gates.md). Four phases:

| Phase | What happens |
|---|---|
| PRE | A `SELECT COUNT` of the rows that will be hit, and the Expected number is set |
| GATE | The `DESTRUCTIVE` block is shown and the session stops for your answer. You approve the number, not the intent. Several operations one request needs are shown at one stop, a block each with its own numbers, and only those your reply approves run |
| GUARDED EXECUTION | The statement runs inside a `DO` block that raises an exception when the count differs from the approved number, aborting the transaction. It is never sent bare. A structure-destructive operation checks the count before it acts, inside the same block. Operations approved at one stop run in one block with a check each, so one miss aborts them all |
| REPORT | Actual against Expected, the verifying `SELECT` as returned, and integrity checks where relations are touched: orphaned foreign keys, a `NOT NULL` that is violated, rows that failed to cast |

A mismatch stops the session entirely and leaves the frontend untouched.

- **The gate stands where a migration is written, not where it runs.** CI applies migration files ungated, so the session never tells you the database is protected from destructive change.
- **A repo can switch the hook off** with `.claude/destructive-gate.off`, holding one line that names why. That is your decision, never the session's, and every phase stays the norm there.

**RLS is tested as each role** (RLS). The default connection is the owner, so a query without `SET LOCAL ROLE` bypasses RLS and tests no policy. Showing `qual` and `with_check` proves only that a policy exists as written.

- **One call per role**, inside a transaction that ends in `ROLLBACK`, setting the role's JWT claims and `SET LOCAL ROLE authenticated`. A test leaves no trace.
- **The role that should see zero rows is tested too.** That negative test is what catches leaks.
- **A real user UUID is needed per role, on every RLS change.** Where none exists, the session seeds one, as the last item below describes.
- **A table created with RLS enabled gets its policy in the same operation.** With RLS and no policy, nobody can read it. A policy that must match an existing one is copied verbatim from introspection.

**Reading results** (Invocation). A step is one command up to its next stop: its statements go in one file or one call, never one call each, except the role test. A read against two servers is one command; a write reaches one server per command, so a mistake lands once. Multi-object introspection is combined into one `SELECT` where the tool returns only the last result set. A `DO` block returns zero rows, so a verifying `SELECT` follows it. `RAISE NOTICE` is not used as output.

**Types** (Types). Regenerated from the live schema after every schema change, before the frontend. An `as any` on a call missing from the types file is reported as a finding.

**A login for the session** (`references/agent-account.md`). When a session must sign in and holds no account, or the role test needs a user of a role nobody holds, it creates a Supabase Auth user by SQL. The credentials come from the session's own instructions and reach no repo file, migration or commit. It runs directly, never as a migration, and the account stays for later sessions. A magic link, OTP, OAuth, SSO or required MFA has no SQL route; you create that account.

## What you will see

- **The `DESTRUCTIVE` block**, with `Operation`, `Affected`, `Expected` and `Reversible`. `Affected` is a real count, not an estimate. A `Reversible` of no names what is lost. One block per operation, all at one stop, where a request needs several.
- **A report per role:** role · UUID · rows visible · rows expected · match or not.
- **Introspection output as returned**, after every migration and every destructive statement.
- **A question about an untracked table**, in a repo that audits, before the migration runs.

## Where it stops

- **The destructive gate.** The session waits for your answer in this session. What you approve is the number.
- **A count that differs from Expected.** The session stops and does not touch the frontend.
- **A role test that does not match.** Rows visible differ from rows expected, and the session does not move on to the frontend.
- **A table in an audited repo with no answer** on whether to track it.

## What it does not cover

- **A migration applied by CI** is not gated. Only the authoring path is.
- **Another auth service** has no SQL route for a session login. The repo's own seed script is used, or you are asked.
- **A hook switched off** removes the enforcement, never the rule.

## Related

[Gates](../concepts/gates.md) · [guard-destructive](guard-destructive.md) · [build-flow](build-flow.md) · [logic-build](logic-build.md) · [docs-format](docs-format.md)
