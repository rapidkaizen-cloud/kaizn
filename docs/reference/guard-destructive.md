# guard-destructive

Refuses destructive SQL that arrives without a guard — a `DO` block that aborts the transaction when the row count misses the number you approved.

| | |
|---|---|
| Kind | Hook — runs by itself; it cannot ask, only pass, refuse, or print |
| Runs on Claude Code | `PreToolUse`, matcher `Bash\|PowerShell`, and again with matcher `mcp__.*` |
| Runs on Antigravity | `PreToolUse`, matcher `run_command`, and again with matcher `call_mcp_tool` |
| Script | `scripts/guard_destructive.py` |
| Self-check | `scripts/test_guard_destructive.py` |

## What it does

It reads the SQL a tool call carries and checks its shape. It cannot know whether you agreed, so it relies on the guard needing a number that only your answer gives. The stop you meet is in [Gates](../concepts/gates.md).

- **It reads the SQL fields.** `query`, `sql` and `statement` on an MCP tool, `command` on a shell tool. A call with none of them passes at once. The MCP matcher is wide because the server name is chosen by whoever connects it.
- **Comments are not read; strings are.** `/* ... */` and `-- ...` are removed first, and a `--` inside a quoted string is data. In a shell command only a line that opens with `-- ` is a comment, because `--` there is usually a flag.
- **Each statement is judged alone.** Statements split at `;`, except inside `$$ ... $$` or `$tag$ ... $tag$`, so a whole `DO` block stays one statement.
- **A guard is not shared.** A guarded `DO` block followed by a bare `DELETE FROM t;` leaves the `DELETE` refused.
- **Letter case depends on the route.** Over MCP the SQL words match in any case. In a shell command they match in capitals only, unless the command runs `psql` or `supabase`, which makes any case match — by name or by a path, such as `/usr/bin/psql` or `./node_modules/.bin/supabase`.

## What it refuses or holds

A statement counts as guarded when it holds a `DO $` block with `RAISE EXCEPTION`. Without one:

| Case | Label in the message | What lets it through |
|---|---|---|
| `DROP` followed by `TABLE`, `FOREIGN TABLE`, `COLUMN`, `SCHEMA`, `DATABASE`, `TYPE`, `DOMAIN`, `FUNCTION`, `PROCEDURE`, `POLICY`, `INDEX`, `VIEW`, `MATERIALIZED VIEW`, `SEQUENCE`, `TRIGGER`, `EXTENSION`, `ROLE` or `OWNED` | `DROP` | The guard |
| `TRUNCATE` followed by a table name, with or without `TABLE` or `ONLY` | `TRUNCATE` | The guard |
| `DELETE FROM` | `DELETE` | The guard, or the `[CLAUDE]` carve-out below |
| `ALTER TABLE ... DROP` of a column, with or without the word `COLUMN` | `ALTER ... DROP COLUMN` | The guard |
| `ALTER ... RENAME` on a `TABLE`, `INDEX`, `VIEW`, `MATERIALIZED VIEW`, `SEQUENCE`, `SCHEMA`, `FUNCTION`, `PROCEDURE`, `POLICY`, `TRIGGER`, `ROLE`, `DATABASE` or `DOMAIN` | `RENAME` | The guard |
| `ALTER TYPE` | `ALTER TYPE` | The guard |
| `UPDATE ... SET` with no `WHERE`, or a `WHERE` opening with `true` or `1 = 1` | `UPDATE without a narrow WHERE` | A narrower `WHERE`, or the guard |

The message opens `REFUSED: a destructive operation (<label>) was sent without a guard.` and gives the order: count first and set the Expected number, show the `DESTRUCTIVE` block — one per operation where the request needs several — and stop once for your answer, then run wrapped in a `DO` block with `RAISE EXCEPTION`, followed by a verifying `SELECT` in the same call.

A `WHERE` inside a subquery is not the statement's own `WHERE`: `UPDATE users SET name = (SELECT name FROM source WHERE source.id = 1);` is refused.

## What it lets through

- **A `DELETE` narrowed to rows opening with `[CLAUDE]`.** These are the test rows the session made itself. The `WHERE` must read `LIKE '[CLAUDE]...'` or `= '[CLAUDE]...'`, and may be narrowed further with `AND`.
- **The carve-out fails closed.** `OR`, `NOT` or `USING` outside parentheses, a comparison other than a lone `=` such as `!=`, a `'%[CLAUDE]%'` match, a prefix that appears only inside parentheses such as a subquery, and a `DELETE` with no `WHERE` all go back to needing a guard.
- **The carve-out is `DELETE` only.** A `DROP` in the same payload, or on a table named `"[CLAUDE] tmp"`, is still refused.
- **Several operations in one `DO` block.** Operations you approved at one stop arrive as one block with a check each, and the hook reads that block as one guarded statement.
- **Narrow `UPDATE`, `SELECT`, `CREATE TABLE`.**
- **An `ALTER TABLE` that drops no data**: a `CONSTRAINT`, a `DEFAULT`, `NOT NULL`, an `IDENTITY`, a generated `EXPRESSION`.
- **Shell words that are not SQL.** `claude plugin update ...`, `apt update`, `truncate -s 0 logs/app.log`, a `truncate` class edited by `sed`, a commit message saying "delete from queue".
- **Tools that carry no SQL field,** and SQL that sits in a comment.

## What it does not reach

- **The logic of the guard.** It looks for `DO $` and `RAISE EXCEPTION` in the statement. That the exception compares against the number you approved is not checked.
- **Lowercase SQL that reaches the database another way** than `psql` or `supabase`, such as a `.sql` file written by heredoc or `node -e`.
- **Ordinary string literals.** A `;` inside `'...'` still splits a statement, and parentheses inside a string are dropped when the hook looks for a `WHERE`.
- **Anything outside the table.** Only the forms listed there are read. A `DROP` of a kind it does not list — `USER`, `GROUP`, `RULE`, `SERVER` among them — passes, because those two words are common in ordinary text and SQL arrives with text in it.
- **A shell command continued onto a line that opens with `-- "<sql>"`.** That line is read as a comment.
- **SQL that does not pass through the wired tool calls.** [Gates](../concepts/gates.md) lists what that leaves out.

## Switching it

Set `guard_destructive` in `/config`, or ask [norms-config](norms-config.md). It holds in every repo.

- **`on`**, the default: as above.
- **`advice`**: nothing is refused. The SQL runs, and the session is handed what the hook would have said, beside the call's result, with an order to tell you in one line.
- **`off`**: the hook does nothing.
- **On Antigravity** it is always `on`.

A repo can also turn the hook off alone, with a file at `.claude/destructive-gate.off` in the project directory, whatever the switch says. Its presence is the decision and its content is free text naming why. That is your decision, never the session's.

- **It is per repo.** Other repos keep the gate, because the plugin's hooks load into every app repo at once.
- **Deleting the file turns the gate back on.**
- **On Antigravity** the file is looked for in the workspace, not where the hook starts.

## Related

- [Gates](../concepts/gates.md) — the destructive stop as you meet it
- [db-ops](db-ops.md) — the rule behind it
