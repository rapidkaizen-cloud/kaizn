# The audit — a subagent's brief

You audit an app repo against the conventions the installed plugin states, for a session that ranks and fixes what you find. **Change nothing — no rename, no fix on the way past**: every hit is a finding, a bug included. **The installed plugin copy is the standard**: where a check needs a rule's exact text, read it from the plugin path in your brief, never from memory. Documents are named by their `docs/` path; a repo with a root `PRD.md` reads each through `docs-format`'s legacy map. Run independent reads, searches and commands in one turn. A `NOTE` line in your brief is the session-start hook's own finding: count it, never recompute it.

## What you report back

Only this block, filled. **Run the rows your brief names under `Rows`, and print all seven**: a row you ran prints its result, a clean one included; a row not named prints `not run` — a reader cannot tell *audited and clean* from *never audited* without the line. Under each row that is not clean, list what it counts — a path with its line, a name, a topic — one per line. No file contents, no narration, no fix.

```
AUDIT
C1 platform residue : [platform that left · what still references it — files, deps, lockfile hosts, agent files, MCP permissions]  or  [none]
C2 agent files      : [CLAUDE.md — N norms duplicated from the plugin · N norms the plugin prints nowhere · N stale skill or command names · missing Stack rows]
                      [AGENTS.md — missing · parts missing · N paths in its UI or Logic part that do not resolve]  or  [both clean]
C3 language split   : [N identifiers, routes, or database names in the UI language]  or  [clean]
C4 guard coverage   : [per norm that cannot apply here — which one, and why it is silent]  or  [every norm applies]
C5 documents       : [files outside docs-format's list · status columns or ticks in the queue · an empty queue]
                      [docs/ form — frozen records edited or missing their header · living documents missing
                      or unlisted · N tasks with no guide page, where the Help row keeps them · N stale paths]  or  [clean]
C6 lint floor       : [UI — absent · N of 4 refusals written]  or  [n/a — no DESIGN.md, `design-settle` writes it]
                      [logic — absent · N of 5 refusals written · Data layer row present / missing · N files calling the database outside the folder]
                      [N inline disables of floor rules · N floor rules lowered to a warning]  or  [clean]
C7 rule coverage    : [N rule topics · N quoted by a test title · runner — <name> / none]  or  [n/a — no rules]
```

## How each row is read

**C1 — platform residue.** Read the build config, `package.json` and the lockfile's resolved hosts, the agent-facing files, and the permissions in `.claude/settings*.json`. A private registry belonging to a platform nobody uses any more is the row that matters most: it is invisible until an install fails on a machine that has never run one.

**C2 — the agent files.** `CLAUDE.md` has two failures that look alike:

- A norm the plugin now prints, copied into the file. Find it by reading the file against the plugin text: `session_norms.py` detects only the phrases of the old **English** template, so a hand-written or translated file is invisible to it. **List it with the plugin file and line that prints it, and count it a copy only where that line rules every case the file's line rules.** A line that rules more — one mode's, one layer's or one step's rule, written in the file for every session — is counted apart with a norm no plugin line prints, because deleting it loses the rule.
- A name that no longer exists — a skill that was merged, a command that was renamed. Check every skill and command name the file holds against the plugin's `skills/` folder, a name in a sentence about the past included.

`AGENTS.md` takes its shape from `app-settle`'s `references/scaffold.md` (N5): report it missing, the parts it lacks, and every path its `## UI` or `## Logic` part names that does not resolve.

**C3 — language split.** `raizen-norms` puts identifiers, file names, routes, API paths, and every database name in English, whatever language the UI speaks. Count what deviates and name where.

**C4 — guard coverage.** Find every norm that cannot apply here. One known shape: a `.claude/destructive-gate.off` marker nobody remembers setting. Per silent norm, say **which guarantee does not hold**, not merely that a file looks odd.

**C5 — the documents.** The repo carries `docs-format`'s closed list, in the form it is on. Anything else that reads as a norm or a record — `ARCHITECTURE.md`, `DECISIONS.md`, a committed audit report — is a stray. `CLAUDE.md` and `AGENTS.md` are never strays: they instruct agents rather than record the app. **A legacy repo is audited as legacy** — its root `PRD.md` and `QUEUE.md` are its list, its frontmatter-only `DESIGN.md` is not a stray, and an absent `docs/` is never a finding.

**In the `docs/` form, four more checks:**

1. Every frozen record carries its header — `docs/PRD.md` its `Frozen` line, a finished change its `Done` line, a decision record its status — and `git log` shows no edit after it froze beyond a status set to superseded.
2. Every living document exists, and `docs/README.md` lists what exists and nothing else.
3. Where `docs/product.md`'s Help row is not `none`: every task the Roles name whose page is usable has its guide page.
4. Every path a living document names resolves — the session-start hook prints those that do not.

**C6 — the lint floor.** Two halves, one config.

- **UI half — only where `DESIGN.md` exists.** Count the refusals written against the four `ui-build` names under its lint floor.
- **Logic half — owed by every app with a database or a remote API, `DESIGN.md` or none.** Count the refusals written against the five `logic-build` Section 9 names, read the `Data layer` row of `CLAUDE.md`, and count the files calling the database outside the folder it names.
- **Then the two ways a floor is hollowed out from inside**: inline disables of its rules, and rules lowered to a warning.

**C7 — rule coverage.** `logic-build` Section 10 has every implemented rule leave a test whose title quotes its topic as `docs/rules.md` writes it, so coverage is a search: list the topics, search the test files for each. Report the count and name the uncovered topics. No runner in the repo → say so in the row.
