#!/usr/bin/env python3
"""Block destructive SQL sent bare.

What is enforced here is SHAPE, not permission. A hook cannot ask, so it does not
know whether the user agreed. What it checks: whether the destructive operation
arrives wrapped in a DO block with RAISE EXCEPTION as its guard, per statement —
one destructive statement without a guard of its own is still blocked even when
another statement in the same payload is guarded.

A guard can only be written once the Expected number exists, and the Expected
number is only born from a gate the user answered. So enforcing the shape is
enough to enforce that the gate happened.

One carve-out: a DELETE narrowed to the `[CLAUDE]` prefix — the test rows the
agent created itself — passes unguarded, because its blast radius is already
fixed to rows the agent owns. See claude_test_delete for what disqualifies it.

One off switch, per repo and never per plugin: a marker file at
`.claude/destructive-gate.off` in the project directory disables this guard for
that repo alone. The file's presence is the decision; its content is free text
naming why. This exists because the plugin's hooks load into every app repo at
once — an app that legitimately needs the gate gone (heavy schema iteration,
bulk re-imports) must not take the gate away from the apps holding production
data. Deleting the marker file turns the gate back on.

Exit 0 = pass, exit 2 = block.
"""
import os
import re
import sys

import host

GATE_OFF_MARKER = os.path.join(".claude", "destructive-gate.off")

DESTRUCTIVE = [
    # A DROP statement, by the kind of object it names. A kind is listed only where the two
    # words are rare in prose: SQL arrives with text in it, and `drop user` or `drop group`
    # in an inserted sentence must pass.
    (r"\bDROP\s+(TABLE|FOREIGN\s+TABLE|COLUMN|SCHEMA|DATABASE|TYPE|DOMAIN|FUNCTION|PROCEDURE|"
     r"POLICY|INDEX|VIEW|MATERIALIZED\s+VIEW|SEQUENCE|TRIGGER|EXTENSION|ROLE|OWNED)\b", "DROP"),
    # `TRUNCATE` followed by an identifier (optionally TABLE/ONLY) is SQL; coreutils
    # `truncate -s 0 file` is followed by a flag and must pass.
    (r"\bTRUNCATE\s+(TABLE\s+|ONLY\s+)?[\"A-Za-z_]", "TRUNCATE"),
    (r"\bDELETE\s+FROM\b", "DELETE"),
    # The word COLUMN is optional in SQL, so the column is whatever follows DROP that is not
    # one of the things an ALTER TABLE drops without losing data.
    (r"\bALTER\s+TABLE\b.*\bDROP\s+(?!(?:CONSTRAINT|DEFAULT|NOT|IDENTITY|EXPRESSION)\b)", "ALTER ... DROP COLUMN"),
    (r"\bALTER\s+(TABLE|INDEX|VIEW|MATERIALIZED\s+VIEW|SEQUENCE|SCHEMA|FUNCTION|PROCEDURE|POLICY|"
     r"TRIGGER|ROLE|DATABASE|DOMAIN)\b.*\bRENAME\b", "RENAME"),
    (r"\bALTER\s+TYPE\b", "ALTER TYPE"),
]

# "query" = the real field of Supabase MCP execute_sql/apply_migration (not a guess,
# see test_guard_destructive.py); "command" = the Bash field. "sql"/"statement" as a net.
SQL_KEYS = ("query", "sql", "command", "statement")

# Shell text is prose as often as SQL — a commit message saying "delete from the queue",
# Tailwind's `truncate` class in a file edit. So in a shell command the SQL words match
# in capitals only, unless psql or supabase runs it. Residual ceiling: lowercase SQL
# reaching the database another way (a .sql file written by heredoc, `node -e`) passes.
# A client named by a path runs as a bare one does: `/usr/bin/psql`, `C:/pg/bin/psql.exe`,
# `./node_modules/.bin/supabase`. A folder named `supabase` runs nothing, so after a `/`
# that word counts only where the folder before it is a `bin`.
SQL_CLIENT = re.compile(r"(?:(?<![\w.@-])psql|(?:(?<![\w./@-])|(?<=bin/))supabase)(\.exe)?(?![\w./-])")

# The hooks.json matcher is deliberately mcp__.* (not mcp__supabase__.*): the server
# name in the user's MCP config is chosen by whoever connects it, outside this repo's control.
# Widening is safe because SQL_KEYS above comes up empty for non-SQL tools -> main()
# exits 0 on its first line, with no effect on other MCP tools.
DOLLAR_TAG = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)?\$")

# A string literal that OPENS with the marker: `LIKE '[CLAUDE]%'`, `= '[CLAUDE] smoke'`.
# In Postgres LIKE only % and _ are special, so `[` here is a literal bracket, not a class.
# The `=` stands alone: in `!=` it selects every row but the marked ones.
CLAUDE_SCOPED = re.compile(r"(?:\bLIKE\b|(?<![!<>=])=)\s*'\[CLAUDE\][^']*'", re.I)

# A quoted string, a block comment, a line comment - tried in that order, so a `--` inside
# a string is data: blanking the rest of its line would hide the statement after it.
COMMENT = re.compile(r"'(?:[^']|'')*'|/\*.*?\*/|--[^\n]*", re.S)


def read_sql() -> tuple[str, bool]:
    """The SQL-bearing text, and whether it arrived as a shell command."""
    ti = host.read_payload().get("tool_input")
    if not isinstance(ti, dict):
        return "", False
    parts = [str(ti[k]) for k in SQL_KEYS if k in ti and ti[k]]
    return "\n".join(parts), "command" in ti


def strip_comments(sql: str, shell: bool) -> str:
    """Blank SQL comments and nothing else, so that a commented-out statement passes.

    In a shell command `--` is a flag or the end of options far more often than a comment,
    and blanking from `--host=localhost` on would hide the SQL after it. There only a line
    that opens with `-- ` is a comment, the way one stands in a heredoc. Residual ceiling:
    a command continued onto a line that opens with `-- "<sql>"` is read as one."""
    def blank(found: re.Match) -> str:
        text = found.group(0)
        if text.startswith("'"):
            return text
        if shell and text.startswith("--"):
            line_start = sql.rfind("\n", 0, found.start()) + 1
            opens_line = not sql[line_start:found.start()].strip()
            if not (opens_line and text[2:3] in ("", " ", "\t")):
                return text
        return " "

    return COMMENT.sub(blank, sql)


def split_statements(sql: str) -> list[str]:
    """Split on ';', aware of dollar-quoting ($$...$$ / $tag$...$tag$).
    A semicolon inside a dollar-quoted block is not a separator, so a whole DO
    block (with its RAISE EXCEPTION) stays one statement. Not aware of ordinary
    string literals ('...') — a semicolon inside one still separates."""
    statements = []
    start = pos = 0
    n = len(sql)
    while pos < n:
        m = DOLLAR_TAG.match(sql, pos)
        if m:
            tag = m.group(0)
            close = sql.find(tag, pos + len(tag))
            pos = close + len(tag) if close != -1 else n
            continue
        if sql[pos] == ";":
            statements.append(sql[start:pos])
            pos += 1
            start = pos
            continue
        pos += 1
    tail = sql[start:pos]
    if tail.strip():
        statements.append(tail)
    return statements


def has_guard(stmt: str) -> bool:
    up = stmt.upper()
    return "RAISE EXCEPTION" in up and re.search(r"\bDO\s+\$", up) is not None


def strip_parens(s: str) -> str:
    """Drop balanced parenthesized content (nested included), so that a WHERE
    belonging to a subquery is not counted as the outer statement's WHERE. A
    mitigation, not a guarantee: not aware of string literals, so parentheses
    inside a string get stripped too."""
    out = []
    depth = 0
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif depth == 0:
            out.append(ch)
    return "".join(out)


def claude_test_delete(stmt: str) -> bool:
    """A DELETE narrowed to rows whose text starts with the literal `[CLAUDE]`
    marker — the throwaway rows the agent created to test with. Cleaning those up
    is the agent's own mess, so it does not need a gate the user must answer.

    Strict on purpose, and fails closed — anything it cannot read as prefix-narrow
    goes back to needing a guard:
      - OR and NOT can widen the target back out past the prefix.
      - USING joins another table in, and the prefix may be tested on that one.
      - A subquery's WHERE says nothing about the row being deleted, so
        strip_parens removes it before the prefix is looked for.
      - '%[CLAUDE]%' (contains) would reach real rows that merely mention the
        marker; only a literal opening with `[CLAUDE]` counts.
    """
    m = re.search(r"\bDELETE\s+FROM\b(.*)$", stmt, flags=re.S | re.I)
    if not m:
        return False
    body = strip_parens(m.group(1))
    if not re.search(r"\bWHERE\b", body, flags=re.I):
        return False
    if re.search(r"\b(OR|NOT|USING)\b", body, flags=re.I):
        return False
    return CLAUDE_SCOPED.search(body) is not None


def bare_update(stmt: str, flags: int) -> bool:
    """UPDATE without a WHERE, or with a WHERE that is always true.

    Only a real SQL UPDATE counts, and SQL requires SET: without it the word is
    shell vocabulary (`claude plugin update`, `apt update`) and must pass. Nothing
    is lost by requiring SET — an UPDATE without SET is invalid SQL and destroys
    nothing."""
    for m in re.finditer(r"\bUPDATE\b(.*?)(;|$)", stmt, flags=flags):
        body = strip_parens(m.group(1))
        if not re.search(r"\bSET\b", body, flags=flags):
            continue
        if not re.search(r"\bWHERE\b", body, flags=flags):
            return True
        if re.search(r"\bWHERE\s+((?i:true)|1\s*=\s*1)\b", body, flags=flags):
            return True
    return False


def block(op: str) -> None:
    sys.stderr.write(
        "REFUSED: a destructive operation ({op}) was sent without a guard.\n\n"
        "The order is:\n"
        "  1. SELECT COUNT first, and set the Expected number.\n"
        "  2. Show the DESTRUCTIVE block (operation - affected - Expected - reversible), one "
        "per operation where the request needs several, then STOP once and wait for the "
        "user's answer in this session.\n"
        "  3. Execute wrapped in a DO block: RAISE EXCEPTION when the row count misses "
        "Expected, followed by a verifying SELECT in the same call.\n\n"
        "The exception aborts the whole transaction, so zero data is lost when the "
        "number does not match.\n".format(op=op)
    )
    sys.exit(2)


def main() -> None:
    text, shell = read_sql()

    # Reading the payload leaves the project directory as cwd on either host, so this
    # scopes to one repo.
    if os.path.exists(GATE_OFF_MARKER):
        sys.exit(0)

    sql = strip_comments(text, shell)
    if not sql.strip():
        sys.exit(0)
    flags = re.S if shell and not SQL_CLIENT.search(sql) else re.I | re.S

    for stmt in split_statements(sql):
        if not stmt.strip() or has_guard(stmt):
            continue

        # Per label, not per statement: a DROP sitting in the same statement as an
        # exempt DELETE is still blocked on its own account.
        exempt_delete = claude_test_delete(stmt)

        for pattern, label in DESTRUCTIVE:
            if label == "DELETE" and exempt_delete:
                continue
            if re.search(pattern, stmt, flags=flags):
                block(label)

        if bare_update(stmt, flags):
            block("UPDATE without a narrow WHERE")

    sys.exit(0)


if __name__ == "__main__":
    main()
