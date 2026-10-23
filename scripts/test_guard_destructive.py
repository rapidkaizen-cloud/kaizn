#!/usr/bin/env python3
"""Self-check guard_destructive.py against the real Supabase MCP payload shape.

The `query` field was verified against the official supabase-community/supabase-mcp
source (execute_sql and apply_migration both use `query`, not `sql`/`statement`).
Run directly: python3 test_guard_destructive.py
"""
import json
import subprocess
from pathlib import Path

GUARD = Path(__file__).parent / "guard_destructive.py"

# `python3`, not sys.executable: this is the interpreter name hooks.json invokes, so a
# machine where only `python` resolves must fail here rather than pass a test whose
# subject never runs. The failure is the point.
PYTHON = "python3"


def run(tool_name: str, tool_input: dict, cwd: str | None = None) -> int:
    payload = json.dumps({"tool_name": tool_name, "tool_input": tool_input})
    result = subprocess.run(
        [PYTHON, str(GUARD)], input=payload, capture_output=True, text=True, cwd=cwd
    )
    return result.returncode


def demo() -> None:
    # execute_sql/apply_migration use the `query` field -> must be detected
    assert run("mcp__supabase__execute_sql", {"query": "DROP TABLE foo;"}) == 2

    guarded = (
        "DO $$ BEGIN DELETE FROM foo; IF (SELECT COUNT(*) FROM foo) != 0 THEN "
        "RAISE EXCEPTION 'mismatch'; END IF; END $$;"
    )
    assert run("mcp__supabase__apply_migration", {"query": guarded}) == 0

    # a Supabase tool carrying no SQL must not get blocked
    assert run("mcp__supabase__list_tables", {"schemas": ["public"]}) == 0

    # the same SQL arriving through the claude.ai-connected Supabase MCP, whose tools are
    # prefixed mcp__claude_ai_Supabase__ instead. This is what the mcp__.* matcher in
    # hooks.json buys: the prefix is set by whoever connects the server, not by this repo.
    assert run("mcp__claude_ai_Supabase__execute_sql", {"query": "DROP TABLE foo;"}) == 2
    assert run("mcp__claude_ai_Supabase__execute_sql", {"query": "SELECT count(*) FROM orders;"}) == 0

    # the Bash route (field `command`, shared with guard_git.py) stays closed
    assert run("Bash", {"command": 'psql -c "TRUNCATE foo;"'}) == 2
    # the PowerShell route carries the same `command` field and the same guard
    assert run("PowerShell", {"command": 'psql -c "TRUNCATE foo;"'}) == 2

    # shell vocabulary is not SQL: `update` without SET, coreutils truncate -> pass
    assert run("Bash", {"command": 'claude plugin update "raizen-hub@raizen"'}) == 0
    assert run("Bash", {"command": "sudo apt update && sudo apt upgrade -y"}) == 0
    assert run("Bash", {"command": "truncate -s 0 logs/app.log"}) == 0
    assert run("PowerShell", {"command": "claude plugin update raizen-norms@raizen"}) == 0
    # but SQL arriving through a shell still blocks
    assert run("Bash", {"command": 'psql -c "UPDATE users SET active = false;"'}) == 2

    # --- shell text is prose as often as SQL: capitals only, unless psql/supabase runs it ---

    # must pass: Tailwind's `truncate` class in a file edit, SQL words in a commit message
    assert run("Bash", {"command": "sed -i 's/flex/truncate text-sm/' src/Row.tsx"}) == 0
    assert run("Bash", {"command": "sed -i 's/flex/truncate block/' src/Row.tsx"}) == 0
    assert run("Bash", {"command": "cat > src/Row.tsx <<'EOF'\n<p className=\"truncate max-w-xs\">x</p>\nEOF"}) == 0
    assert run("PowerShell", {"command": "(Get-Content Row.tsx) -replace 'flex', 'truncate font-medium' | Set-Content Row.tsx"}) == 0
    assert run("Bash", {"command": 'git commit -m "fix: delete from queue when done"'}) == 0
    assert run("Bash", {"command": 'git commit -m "docs: when to drop table rows"'}) == 0
    assert run("Bash", {"command": 'git commit -m "update set of fixtures"'}) == 0
    assert run("Bash", {"command": "truncate logs/app.log -s 0"}) == 0
    # a path merely named after a client does not run it
    assert run("Bash", {"command": "sed -i 's/flex/truncate block/' src/lib/supabase-client.tsx"}) == 0

    # must still block: capitals anywhere in a shell, any case once psql or supabase runs
    assert run("Bash", {"command": "cat > wipe.sql <<'EOF'\nTRUNCATE leads;\nEOF"}) == 2
    assert run("Bash", {"command": 'psql -c "truncate leads;"'}) == 2
    assert run("Bash", {"command": 'psql -c "delete from leads;"'}) == 2
    assert run("Bash", {"command": 'psql -c "update leads set status = 1;"'}) == 2
    assert run("PowerShell", {"command": '& "C:\\Program Files\\PostgreSQL\\16\\bin\\psql.exe" -c "truncate leads;"'}) == 2
    assert run("Bash", {"command": "npx supabase migration new wipe && echo 'truncate leads;' >> supabase/migrations/wipe.sql"}) == 2
    assert run("mcp__supabase__execute_sql", {"query": "truncate leads;"}) == 2

    # false positives: UPDATE with a narrow WHERE, SELECT, CREATE TABLE -> pass
    assert run("mcp__supabase__execute_sql", {"query": "UPDATE users SET active = true WHERE id = 3;"}) == 0
    assert run("mcp__supabase__execute_sql", {"query": "SELECT count(*) FROM orders;"}) == 0
    assert run("mcp__supabase__execute_sql", {"query": "CREATE TABLE t (id int);"}) == 0

    # a guard must not be borrowed by a neighbour: guarded DO, then a bare DELETE
    assert run("mcp__supabase__execute_sql", {
        "query": "DO $$ BEGIN RAISE EXCEPTION 'guard'; END $$; DELETE FROM t;"
    }) == 2

    # operations approved at one stop arrive as one block with a check each, and pass
    together = (
        "DO $$ DECLARE n int; BEGIN "
        "DELETE FROM order_items WHERE order_id = 7; GET DIAGNOSTICS n = ROW_COUNT; "
        "IF n <> 12 THEN RAISE EXCEPTION 'Expected 12 rows, actual %.', n; END IF; "
        "DELETE FROM orders WHERE id = 7; GET DIAGNOSTICS n = ROW_COUNT; "
        "IF n <> 1 THEN RAISE EXCEPTION 'Expected 1 row, actual %.', n; END IF; "
        "END $$; SELECT count(*) FROM orders WHERE id = 7;"
    )
    assert run("mcp__supabase__execute_sql", {"query": together}) == 0
    assert run("Bash", {"command": f'psql "$DATABASE_URL" <<\'SQL\'\n{together}\nSQL'}) == 0

    # a subquery's WHERE must not count as the UPDATE's own WHERE
    assert run("mcp__supabase__execute_sql", {
        "query": "UPDATE users SET name = (SELECT name FROM source WHERE source.id = 1);"
    }) == 2

    # --- the [CLAUDE] carve-out: cleaning up one's own test rows needs no gate ---

    # must pass: prefix LIKE, and an exact match on a full [CLAUDE] title
    assert run("mcp__supabase__execute_sql", {
        "query": "DELETE FROM notes WHERE title LIKE '[CLAUDE]%';"
    }) == 0
    assert run("mcp__supabase__execute_sql", {
        "query": "DELETE FROM notes WHERE title = '[CLAUDE] smoke test';"
    }) == 0
    # the same cleanup arriving through Bash
    assert run("Bash", {
        "command": "psql -c \"DELETE FROM notes WHERE title LIKE '[CLAUDE]%';\""
    }) == 0
    # narrowed further by AND — still inside the prefix
    assert run("mcp__supabase__execute_sql", {
        "query": "DELETE FROM notes WHERE title LIKE '[CLAUDE]%' AND created_at < now();"
    }) == 0

    # must still block: contains, not opens-with -> reaches real rows mentioning the marker
    assert run("mcp__supabase__execute_sql", {
        "query": "DELETE FROM notes WHERE title LIKE '%[CLAUDE]%';"
    }) == 2
    # NOT inverts the target into everything the agent does not own
    assert run("mcp__supabase__execute_sql", {
        "query": "DELETE FROM notes WHERE title NOT LIKE '[CLAUDE]%';"
    }) == 2
    # OR widens back out past the prefix
    assert run("mcp__supabase__execute_sql", {
        "query": "DELETE FROM notes WHERE title LIKE '[CLAUDE]%' OR id = 1;"
    }) == 2
    # the prefix lives in a subquery: says nothing about the row being deleted
    assert run("mcp__supabase__execute_sql", {
        "query": "DELETE FROM notes WHERE id IN (SELECT id FROM src WHERE title LIKE '[CLAUDE]%');"
    }) == 2
    # no WHERE at all, whatever the table is called
    assert run("mcp__supabase__execute_sql", {"query": "DELETE FROM notes;"}) == 2
    # the carve-out is DELETE-only: it must not leak to DROP
    assert run("mcp__supabase__execute_sql", {
        "query": "DROP TABLE \"[CLAUDE] tmp\";"
    }) == 2
    # an exempt DELETE does not shelter a DROP sharing the payload
    assert run("mcp__supabase__execute_sql", {
        "query": "DELETE FROM notes WHERE title LIKE '[CLAUDE]%'; DROP TABLE orders;"
    }) == 2

    # --- comments, clients named by a path, the DROP kinds: the cases that must pass first ---

    sql = "mcp__supabase__execute_sql"

    # a `--` flag is not a comment, and a statement that is commented out is not sent
    assert run("Bash", {"command": 'psql --host=localhost -c "SELECT count(*) FROM orders;"'}) == 0
    assert run("Bash", {"command": "cat > m.sql <<'EOF'\n-- DROP TABLE old was done by hand\nCREATE TABLE t (id int);\nEOF"}) == 0
    assert run(sql, {"query": "-- DROP TABLE old\nSELECT 1;"}) == 0
    assert run(sql, {"query": "SELECT 1; -- DELETE FROM orders"}) == 0
    assert run(sql, {"query": "SELECT 1; /* DROP TABLE old */"}) == 0
    assert run(sql, {"query": "INSERT INTO log (note) VALUES ('step -- one');"}) == 0
    # what an ALTER TABLE drops without losing data
    assert run(sql, {"query": "ALTER TABLE orders DROP CONSTRAINT orders_lead_fk;"}) == 0
    assert run(sql, {"query": "ALTER TABLE orders ALTER COLUMN note DROP DEFAULT;"}) == 0
    assert run(sql, {"query": "ALTER TABLE orders ALTER COLUMN note DROP NOT NULL;"}) == 0
    # prose that only resembles a DROP statement, in a row being written
    assert run(sql, {"query": "INSERT INTO faq (q) VALUES ('can I drop user uploads or drop group chats?');"}) == 0
    # a folder named after a client runs nothing
    assert run("Bash", {"command": "ls apps/supabase && git commit -m 'delete from the queue'"}) == 0

    # must block: the flag no longer hides the SQL after it
    assert run("Bash", {"command": 'psql --host=localhost -c "DROP TABLE foo"'}) == 2
    # a `--` inside a string is data, and the statement after it is still read
    assert run(sql, {"query": "INSERT INTO log (note) VALUES ('step -- one'); DELETE FROM orders;"}) == 2
    # a client named by a path, forward slashes included
    assert run("Bash", {"command": '/usr/bin/psql -c "drop table foo"'}) == 2
    assert run("Bash", {"command": 'C:/pg/bin/psql.exe -c "drop table foo"'}) == 2
    assert run("Bash", {"command": "./node_modules/.bin/supabase migration new wipe && echo 'truncate leads;' >> wipe.sql"}) == 2
    # the DROP kinds and the renames that were not listed
    for statement in (
        "DROP MATERIALIZED VIEW daily_totals;",
        "DROP TRIGGER audit ON orders;",
        "DROP SEQUENCE orders_no_seq;",
        "DROP ROLE reporting;",
        "DROP OWNED BY reporting;",
        "ALTER INDEX orders_idx RENAME TO orders_lead_idx;",
        "ALTER VIEW open_orders RENAME TO pending_orders;",
    ):
        assert run(sql, {"query": statement}) == 2, statement
    # a column dropped without the word COLUMN
    assert run(sql, {"query": "ALTER TABLE orders DROP legacy_id;"}) == 2
    assert run(sql, {"query": "ALTER TABLE orders DROP IF EXISTS legacy_id;"}) == 2

    # the carve-out: `!=` selects every row but the marked ones
    assert run(sql, {"query": "DELETE FROM notes WHERE title != '[CLAUDE] x';"}) == 2
    assert run(sql, {"query": "DELETE FROM notes WHERE title >= '[CLAUDE] x';"}) == 2
    assert run(sql, {"query": "DELETE FROM notes WHERE title <> '[CLAUDE] x';"}) == 2
    # USING joins a table in, and the prefix is tested on that one
    assert run(sql, {"query": "DELETE FROM notes USING other WHERE other.title LIKE '[CLAUDE]%';"}) == 2

    # --- the per-repo off switch: .claude/destructive-gate.off in the project cwd ---

    import tempfile
    with tempfile.TemporaryDirectory() as td:
        # marker present -> everything passes, in that repo only
        (Path(td) / ".claude").mkdir()
        (Path(td) / ".claude" / "destructive-gate.off").write_text("why, in free text\n")
        assert run("mcp__supabase__execute_sql", {"query": "DROP TABLE foo;"}, cwd=td) == 0
    with tempfile.TemporaryDirectory() as td:
        # no marker -> the same payload still blocks (fails closed)
        assert run("mcp__supabase__execute_sql", {"query": "DROP TABLE foo;"}, cwd=td) == 2

    # --- Antigravity: the shapes 1.2.16 sends, the hook started outside the project ---

    def antigravity(name: str, args: dict, workspace: str) -> int:
        payload = json.dumps({"toolCall": {"name": name, "args": args}, "workspacePaths": [workspace]})
        return subprocess.run(
            [PYTHON, str(GUARD)], input=payload, capture_output=True, text=True, cwd=GUARD.parent.parent
        ).returncode

    def mcp(query: str) -> dict:
        return {"ServerName": "supabase", "ToolName": "execute_sql", "Arguments": {"project_id": "x", "query": query}}

    with tempfile.TemporaryDirectory() as td:
        assert antigravity("call_mcp_tool", mcp("SELECT count(*) FROM orders;"), td) == 0
        assert antigravity("call_mcp_tool", mcp(guarded), td) == 0
        assert antigravity("run_command", {"CommandLine": "git commit -m 'delete from the queue'"}, td) == 0
        assert antigravity("view_file", {"AbsolutePath": "DROP TABLE.md"}, td) == 0
        assert antigravity("call_mcp_tool", mcp("DROP TABLE foo;"), td) == 2
        assert antigravity("run_command", {"CommandLine": 'psql -c "drop table foo"'}, td) == 2

        # the off switch is looked for in the workspace, not where the hook starts
        (Path(td) / ".claude").mkdir()
        (Path(td) / ".claude" / "destructive-gate.off").write_text("why, in free text\n")
        assert antigravity("call_mcp_tool", mcp("DROP TABLE foo;"), td) == 0

    print("ok")


def switched() -> None:
    """The user's switch: `advice` lets the SQL through and hands the model the refusal,
    `off` does nothing, a value it does not know is `on`, and the repo's marker still holds."""
    import os
    import tempfile

    def call(query: str, mode: str, cwd: str | None = None) -> tuple:
        payload = json.dumps({"tool_name": "mcp__supabase__execute_sql", "tool_input": {"query": query}})
        env = {**os.environ, "CLAUDE_PLUGIN_OPTION_GUARD_DESTRUCTIVE": mode}
        result = subprocess.run([PYTHON, str(GUARD)], input=payload, capture_output=True, text=True, env=env, cwd=cwd)
        told = json.loads(result.stdout)["hookSpecificOutput"] if result.stdout else {}
        return result.returncode, result.stderr, told

    # must pass, and say nothing, under every mode
    for mode in ("on", "advice", "off"):
        assert call("SELECT count(*) FROM orders;", mode) == (0, "", {})
        assert call("DELETE FROM notes WHERE title LIKE '[CLAUDE]%';", mode) == (0, "", {})
    assert call("DROP TABLE foo;", "off") == (0, "", {})

    code, err, told = call("DROP TABLE foo;", "advice")
    assert code == 0 and err == "" and told["hookEventName"] == "PreToolUse"
    assert told["additionalContext"].startswith("ADVICE - the user switched guard_destructive to advice")
    assert "REFUSED: a destructive operation (DROP)" in told["additionalContext"]

    for mode in ("on", "maybe"):
        code, err, told = call("DROP TABLE foo;", mode)
        assert code == 2 and err.startswith("REFUSED:") and told == {}, mode

    # the repo's marker turns it off there whatever the switch says
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / ".claude").mkdir()
        (Path(td) / ".claude" / "destructive-gate.off").write_text("why\n")
        assert call("DROP TABLE foo;", "on", td) == (0, "", {})
        assert call("DROP TABLE foo;", "advice", td) == (0, "", {})

    print("ok switched")


if __name__ == "__main__":
    demo()
    switched()
