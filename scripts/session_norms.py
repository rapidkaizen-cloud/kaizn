#!/usr/bin/env python3
"""Print the session norms, then the files a session must not start without.

SessionStart hook on Claude Code: stdout is added to the session context. Antigravity
has no such event, so the same script runs as its PreInvocation hook - before every
model call - and hands the same text over once per conversation, as an injected step.

Everything printed here holds in every app repo, so it lives in the plugin rather
than in an app's CLAUDE.md — changing it then reaches every app through a plugin
update instead of an edit in N repositories. An app's CLAUDE.md keeps only what the
plugin cannot know: its stack, its locale, the rules that belong to that app alone,
and the two gates that must survive the plugin being absent.

Each block prints as the user's switch for it says (`switches.py`): whole, marked as
advice, or not at all. The norms then open with one line naming every rule the user moved
away from `on`, so that a missing block reads as their choice rather than a fault. Nothing
asks for a switch up front; the first session on a machine is told once, after its task,
where the rules are switched.

The documents are injected rather than pointed at. A pointer is obeyed by judgement,
and the sessions that skip it are exactly the narrow ones where its prohibitions still
apply. A repo with a root `PRD.md` is on the legacy form and gets `QUEUE.md` and the
sections of `PRD.md` that `docs/product.md` holds in the other; a repo with `docs/PRD.md`
gets the `docs/` form's block and the three living documents `docs-format` names — never
the frozen ones. A repo with neither gets the `NOT SETTLED` block and its queue, kept at
the root or under `docs/`.

Claude Code replaces a hook's stdout over 10,000 characters with its first 2,000 and a
file path nobody is told to read, which cut the norms off after `LANGUAGE` in every repo
whose documents made the output longer. So the output stays under `BUDGET`: the norms
and the notes always, then each document whole where it fits and named with an order to
read it where it does not, then the listings, cut where the room ends. A pointer that
arrives beats a document that does not. A document that is only named still gets its
prohibitions printed where they fit: sessions on a cheaper model skipped the read, and
the prohibitions are what a narrow session breaks.

The two inventories — components, and the data layer's functions — are printed for
the same reason. `ui-build` orders a listing
of the components folder before any element is written, and a skill is loaded by
judgement — a session that never loads it hunts for `Pagination`, misses `Pager`, and
writes it a second time. It is printed here rather than from a PreToolUse hook on
Write because that hook's additionalContext lands beside the tool result: after the
file is already written.
"""
import contextlib
import io
import json
import os
import re
import sys
from pathlib import Path

import guard_output
import handoff
import host
import remind_docs
import switches

HEAD = """\
SESSION NORMS (kaizn)

These hold in every app repo. The app's CLAUDE.md holds what is true of that app
alone; where the two disagree about a norm, this one is the newer.

"""

LANGUAGE = """\
LANGUAGE
The user's language and the repo's language are two different things. `PRD.md` is
printed or named below in the user's language, and it is the longest thing you will
read this session - do not let it decide the language of what you write.
  The user's language : chat, `PRD.md`, `QUEUE.md`, commit messages, pull
                        requests, and the strings the app puts on screen
  English, always     : comments, identifiers, file names, URL routes, API
                        endpoint paths, and every name in the database - tables,
                        columns, views, enum types, functions, policies, and
                        migration file names
  Decided per case    : enum values. They are stored data rather than a name, so
                        weigh readability against rewriting every existing row,
                        and map them to English keys at the boundary either way.
A route is an identifier the user happens to see - the menu label above it is the
thing written for them. A PRD term that names a thing in the code is translated on
the way in: a PRD that says "view kandidat" becomes `lead_candidates`, never
`lead_kandidat`. Existing code in the other language is a finding to report, not a
licence to match it.

"""

POINTERS = """\
POINTERS - read before touching
  Starting a page, or deciding what to build next : skill `build-flow`
  `PRD.md`                                        : skill `docs-format`
  UI, components, styling tokens                  : skill `ui-build`
  Schema, RLS, migrations                         : skill `db-ops`
  Queries, actions, handlers, keys, env vars      : skill `logic-build`
  Which command to run, the version, what changed : skill `norms-help`
Skills load by judgement rather than by rule, and a new component triggers no file
read at all - so the components and the data-layer functions this repo already has
are listed at the end of this block, wherever it has any. Do not write new UI without
reading `ui-build` first, do not write a query without reading `logic-build` first,
and do not write a key or an environment variable without its Section 1.

"""

SCOPE = """\
SCOPE
Only what was asked. No refactor, no rename, no "while I'm here" outside scope.
Do not emit documentation that was not explicitly requested. `PRD.md` and `QUEUE.md`
are the only documents maintained in an app repo: `PRD.md` holds intent, `QUEUE.md`
holds what is not built yet.

"""

GIT = """\
GIT
Before anything else: `git fetch`, then check the branch position. Where the repo has a
`development` branch: HEAD on `main` -> stop, and behind `origin/development` -> stop
and ask to run `git pull --ff-only`.

Committing is part of finishing, not a separate request:
  - A scope item that is finished is committed in the same turn, without asking first.
  - Name the paths explicitly, in `git add` and again in `git commit -- <paths>`: a
    path staged before you never rides along. `git add -A` and `git add .` are refused.
  - The message states why, not only what - the diff already shows the what.
  - Paths that changed outside SCOPE are findings reported to the user, never
    committed along.

Do not commit when you stop for one of the three legitimate stops in `build-flow`
Section 6 - the `db-ops` destructive gate, a role test that misses, a business rule
absent from the PRD. Leave the working tree dirty and report the stop instead. So at
the end of a session: a clean tree means finished, a dirty tree means something is
waiting on the user.

`main` never receives a direct commit while `development` exists. A push, or the merge
of a pull request, is a chat stop, never an AskUserQuestion - a dialog gets clicked
before it is read. End the turn on a message with the exact command in backticks on a
line of its own and, under it, every commit it publishes as `- ` bullets: short hash
and subject. Run it only on a clear yes, in whatever words - a question, a condition or
another instruction is not a yes. Answer a question and wait: a push stays open for the
yes that follows, a merge is put again in the answer. `guard_git` holds both until the
stop has a reply, and one stop covers one run. Open a pull request only when asked; it
needs no stop.

"""

ASKING = """\
ASKING
A decision that is the user's is asked through AskUserQuestion, or answered in chat at
a hard stop; then you run it yourself. Never hand the user a command to type - only
what needs their own hands: a browser login, a dashboard, a key rotation, a payment.
A block or a table a skill orders printed is printed whole: a brevity mode set by
another plugin shortens prose, never that.

"""

DECISIONS = """\
DECISIONS
An answer carrying two or more decisions, options, or recommendations closes with one
table: question - options - recommendation. An answer that only explains, with nothing
for anyone to choose, does not get one; a table where no decision is due only teaches
the reader to skip past every other table.
The recommendation column is never left out, and it names its trade-off. A
recommendation without a trade-off has not finished being thought through - no solution
is free, and where the price has not been found, say that it has not been found.
This comes before the work, while it can still change the plan. The block below is the
report afterwards, and neither replaces the other.

"""

CLOSING = """\
CLOSING THE SESSION
Report per scope item: what changed, or "UNTOUCHED". A scope item that did not change
is flagged. Then this block, always, even where the answer is "none":
  - Which page is usable now, and at which route
  - Which other pages were touched by spread
  - Which defaults you decided yourself
  - Unfinished steps, written as `QUEUE.md` lines rather than as sentences
  - What the user must do by hand
  - Which branch you are on and what you committed
  - PRD: written this session, and what needs the user's decision
A missing block is ambiguous between "none" and "forgot".
"""

# The blocks in the order they print, each under the switch the user sets for it.
BLOCKS = [
    ("norm_language", LANGUAGE),
    ("norm_pointers", POINTERS),
    ("norm_scope", SCOPE),
    ("norm_git", GIT),
    ("norm_asking", ASKING),
    ("norm_decisions", DECISIONS),
    ("norm_closing", CLOSING),
]

# Every block on: what a session gets where the user switched nothing.
NORMS = HEAD + "".join(text for _, text in BLOCKS)

# Printed after the norms in every form and on every host, with the folder worked out for
# this session, because the session is the one place that knows its checkout.
OUTPUT = """\

OUTPUT
A file made for the user to open or pass on - a report, a spreadsheet, a CSV, a PDF -
goes to this session's own folder, never into the repo, a scratchpad or the root of the
output folder:
  {folder}
Working files - scripts, raw data, screenshots - stay where the work is. Name a file for
what it holds, with no date, and never overwrite one: a name already taken gets `-v2`,
`-v3`. Give the user the full path. `guard_output` refuses any other folder there.
"""

# The block above is the legacy form's, printed byte for byte where a root `PRD.md`
# exists. The `docs/` form differs only where the block names a document.
DOCS_FORM = [
    (
        "`PRD.md` is\nprinted or named below in the user's language, and it is the longest thing you will\n"
        "read this session - do not let it decide the language of what you write.\n",
        "The `docs/`\nfiles are printed or named below in the user's language - do not let them decide\n"
        "the language of what you write.\n",
    ),
    (
        "  The user's language : chat, `PRD.md`, `QUEUE.md`, commit messages, pull\n"
        "                        requests, and the strings the app puts on screen\n",
        "  The user's language : chat, `docs/`, the prose of `DESIGN.md` and `README.md`,\n"
        "                        commit messages, pull requests, and the strings the\n"
        "                        app puts on screen\n",
    ),
    ("A PRD term that names", "A term that names"),
    ("a PRD that says", "a glossary that says"),
    (
        "  `PRD.md`                                        : skill `docs-format`\n",
        "  `docs/`, `DESIGN.md`, `README.md`               : skill `docs-format`\n",
    ),
    (
        "Do not emit documentation that was not explicitly requested. `PRD.md` and `QUEUE.md`\n"
        "are the only documents maintained in an app repo: `PRD.md` holds intent, `QUEUE.md`\n"
        "holds what is not built yet.\n",
        "Write no document outside the closed list in `docs-format`, and keep every listed\n"
        "one true in the commit that changes what it says. A commit that changes how the\n"
        "app behaves carries its `docs/changelog.md` entry, in a new file where the repo has\n"
        "none. `docs/queue.md` holds what is not built yet.\n",
    ),
    (
        "absent from the PRD. Leave the working tree dirty and report the stop instead. So at\n"
        "the end of a session: a clean tree means finished, a dirty tree means something is\n"
        "waiting on the user.\n",
        "absent from `docs/rules.md`. Leave the working tree dirty and report the stop\n"
        "instead. So at the end of a session: a clean tree means finished, a dirty tree\n"
        "means something is waiting on the user.\n",
    ),
    ("written as `QUEUE.md` lines", "written as `docs/queue.md` lines"),
    (
        "  - PRD: written this session, and what needs the user's decision\n",
        "  - Docs: which files of `docs-format`'s list this session changed, or `none` and\n"
        "    why, and what needs the user's decision\n",
    ),
]

# The living documents a `docs/` repo gets at every session start. The frozen ones —
# `docs/PRD.md`, `docs/changes/`, the decision records — are history and never printed.
LIVING = [
    ("docs/README.md", "the index"),
    ("docs/product.md", "context, roles, prohibitions"),
    ("docs/queue.md", "what is not built yet"),
]
# Living documents whose named paths are checked. Frozen records may name paths that are
# gone on purpose, `changelog.md` is dated history, and the queue names files not built yet.
PATH_CHECKED = ["README.md", "product.md", "rules.md", "glossary.md", "architecture.md", "runbook.md"]
LINK = re.compile(r"\]\(([^)\s]+)\)")
TICKED = re.compile(r"`([^`\s]+)`")
FILE_EXT = re.compile(r"\.(md|mdx|[cm]?[jt]sx?|json|toml|ya?ml|s?css|sql|py|dart|kt|swift|vue|svelte|astro|html|sh)$")
STALE_MAX = 20


def docs_norms(text: str = NORMS) -> str:
    for old, new in DOCS_FORM:
        text = text.replace(old, new)
    return text


# A repo with a PRD in neither form has never been through `app-settle`. It is handed the
# block without the two sections that rest on what `app-settle` writes, and this one in
# the place of `POINTERS`: a gate that points at a document nobody wrote stops work the
# user never put under these skills.
NOT_SETTLED = """\
NOT SETTLED
This repo has neither a root `PRD.md` nor `docs/PRD.md`: `app-settle` has not run here,
and the documents the build skills measure code against do not exist.
  - `build-flow` and `docs-format` do not apply.
  - Read `ui-build` before writing UI, `db-ops` before SQL, and `logic-build` before a
    query, a key or an environment variable. A rule of theirs that reads `docs/` or
    `DESIGN.md` has nothing to read here and does not apply.
  - Build UI only from the components and tokens this repo already has, and write no new
    styling value. A repo with no UI yet is not bound by this.
  - In an app repo, say once, when the work is done, that `app-settle` has not run here.
  - Which command to run, the version, what changed: skill `norms-help`.

"""

# Applied after `DOCS_FORM`: what the docs form says of documents this repo does not have.
UNSETTLED_FORM = [
    (
        " The `docs/`\nfiles are printed or named below in the user's language - do not let them decide\n"
        "the language of what you write.\n",
        "\n",
    ),
    (
        "Write no document outside the closed list in `docs-format`, and keep every listed\n"
        "one true in the commit that changes what it says. A commit that changes how the\n"
        "app behaves carries its `docs/changelog.md` entry, in a new file where the repo has\n"
        "none. `docs/queue.md` holds what is not built yet.\n",
        "Do not emit documentation that was not explicitly requested.\n",
    ),
    (
        "one of the three legitimate stops in `build-flow`\nSection 6 - the `db-ops` destructive "
        "gate, a role test that misses, a business rule\nabsent from `docs/rules.md`. Leave the "
        "working tree dirty and report the stop\ninstead. So at the end of a session: a clean "
        "tree means finished, a dirty tree\nmeans something is waiting on the user.\n",
        "the `db-ops` destructive gate or a role test that misses.\n"
        "Leave the working tree dirty and report the stop instead. So at the end of a session:\n"
        "a clean tree means finished, a dirty tree means something is waiting on the user.\n",
    ),
    (
        "This comes before the work, while it can still change the plan. The block below is the\n"
        "report afterwards, and neither replaces the other.\n",
        "This comes before the work, while it can still change the plan.\n",
    ),
]


def unsettled_norms() -> str:
    text = docs_norms(HEAD + LANGUAGE + NOT_SETTLED + SCOPE + GIT + ASKING + DECISIONS)
    for old, new in UNSETTLED_FORM:
        text = text.replace(old, new)
    return text.rstrip("\n") + "\n"


UNSETTLED_BLOCKS = [
    (key, NOT_SETTLED if key == "norm_pointers" else text) for key, text in BLOCKS if key != "norm_closing"
]

# Printed under the heading of a block the user switched to `advice`.
ADVICE = "Advice only: the user has not made this block binding - weigh it.\n"


def switched_block(key: str, text: str) -> str:
    """A block as the user's switch for it says: whole, marked as advice, or nothing."""
    mode = switches.mode(key)
    if mode == switches.OFF:
        return ""
    if mode == switches.ADVICE:
        lead = len(text) - len(text.lstrip("\n"))
        heading, _, body = text[lead:].partition("\n")
        return text[:lead] + heading + "\n" + ADVICE + body
    return text


def switched_line() -> str:
    """One line naming every rule the user moved away from `on`, so that a missing block or
    a quiet hook reads as their choice rather than a fault. Nothing when none moved."""
    moved = switches.switched()
    if not moved:
        return ""
    return (
        "SWITCHED by the user, on purpose: "
        + ", ".join(f"{key} {mode}" for key, mode in moved.items())
        + ".\n\n"
    )


def norms(blocks: list, *forms: list) -> str:
    """The norms as this session gets them: each block worded for the repo's form, then
    printed as its switch says. Every switch on, this is `NORMS`, `docs_norms()` or
    `unsettled_norms()` exactly - each replacement lies inside one block."""
    out = HEAD + switched_line()
    for key, text in blocks:
        for form in forms:
            for old, new in form:
                text = text.replace(old, new)
        out += switched_block(key, text)
    return out.rstrip("\n") + "\n"


# Sections that used to be rendered into an app's CLAUDE.md and are now owned by this
# plugin. A repo bootstrapped before a move still carries the old copy, and the two
# then contradict each other silently. Detection is by a phrase distinctive to the old
# template — add a line here whenever a section is retired.
STALE = [
    ("then check the branch position", "the git paragraph under 'Before touching anything'"),
    ("Uncommitted :", "the GIT block under 'Closing a session'"),
    ("Pointers — read before touching", "the Pointers table"),
    ("Read `PRD.md` at the start of a session", "the 'read PRD.md' line - the hook injects it now"),
    ("Only what was asked", "the Scope section"),
    ("Report per scope item", "the closing report"),
]

# A PRD past this length means `docs-format` has leaked and the file is accumulating
# status. The size is said out loud; what is printed never depends on it.
PRD_LINES_WARN = 400

# A legacy PRD is printed as the `docs/` form prints `docs/product.md`: context, roles,
# prohibitions. Sections 3-5 — rules, glossary, design system — are named with their
# line range instead, the read the `docs/` form already asks for: printed whole they
# were most of what every model call in the repo re-read, and Section 5 put the old
# look in front of a `design-settle` session that must draw blind to it.
PRD_SECTION = re.compile(r"^## (\d+)\..*$", re.M)
PRD_UNPRINTED = {"3", "4", "5"}


def prd_printed(text: str) -> str:
    marks = list(PRD_SECTION.finditer(text))
    if [m.group(1) for m in marks] != ["1", "2", "3", "4", "5", "6"]:
        return text  # off-shape: a prohibition that cannot be located is never cut
    out = [text[: marks[0].start()]]
    for mark, after in zip(marks, marks[1:] + [None]):
        end = after.start() if after else len(text)
        if mark.group(1) not in PRD_UNPRINTED:
            out.append(text[mark.start() : end])
            continue
        first = text.count("\n", 0, mark.start()) + 1
        last = text.count("\n", 0, end)
        out.append(
            f"{mark.group(0)}\n\nNot printed. Read `PRD.md` lines {first}-{last} before "
            "writing or changing anything this section governs.\n\n"
        )
    return "".join(out)


def prd_ranges(text: str) -> str:
    """The line ranges of the sections `prd_printed` prints, for a PRD too long to print."""
    marks = list(PRD_SECTION.finditer(text))
    if [m.group(1) for m in marks] != ["1", "2", "3", "4", "5", "6"]:
        return ""
    spans = []
    for mark, after in zip(marks, marks[1:] + [None]):
        if mark.group(1) in PRD_UNPRINTED:
            continue
        first = 1 if mark is marks[0] else text.count("\n", 0, mark.start()) + 1
        last = text.count("\n", 0, after.start() if after else len(text))
        if spans and spans[-1][1] + 1 == first:
            spans[-1][1] = last
        else:
            spans.append([first, last])
    return " and ".join(f"{a}-{b}" for a, b in spans)


# Claude Code's cap on a hook's plain stdout, and what this script allows itself under
# it. The gap is room for the closing lines of parts that had to be cut.
LIMIT = 10_000
BUDGET = 9_500
MORE_COMPONENTS = "... more components than a session start carries - list the `components` folders before writing UI.\n"
MORE_DATA = "... more of the data layer than a session start carries - list the folder `CLAUDE.md` names before writing a query.\n"
MORE_HANDOVER = "... the hand-over is cut here: a session start carries no more.\n"


def size(text: str) -> int:
    # a Windows stdout writes `\r\n` for every line, and the host may count both
    return len(text) + text.count("\n")


def captured(fn, *args) -> str:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        fn(*args)
    return out.getvalue()


def fit(text: str, room: float, more: str) -> str:
    """A listing whole where it fits, else cut at a line and closed with `more`."""
    if size(text) <= room:
        return text
    kept = ""
    for line in text.splitlines(keepends=True):
        if size(kept + line + more) > room:
            break
        kept += line
    # six lines are a listing's own heading: with no entry under them, say only `more`
    return (kept if kept.count("\n") > 6 else "\n") + more


# Printed in the first session on a machine, on Claude Code alone: a user cannot judge a rule
# before meeting it, so nothing asks up front, and this line is where the switches are named.
FIRST = """\

FIRST SESSION ON THIS MACHINE
End your first answer, once the user's task is done, with one line in the user's language:
these rules can be adjusted with `/kaizn:norms-config`. Do not stop or ask about it
before the task.
"""
# Written into the plugin's data folder once `FIRST` was printed; kept across updates.
ONBOARDED = "onboarded"


def first_session() -> str:
    """`FIRST` where the plugin's data folder holds no marker yet, which it then gets. A
    marker that cannot be written leaves the line out, so that it never repeats."""
    folder = os.environ.get("CLAUDE_PLUGIN_DATA", "").strip()
    if not folder:
        return ""
    marker = Path(folder) / ONBOARDED
    try:
        if marker.exists():
            return ""
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text("The first session here was told where the switches are.\n", encoding="utf-8")
    except OSError:
        return ""
    return FIRST


# The norms and the skills are written in Claude Code's vocabulary. A session on another
# host gets this block after them, and it is the only place the two are mapped.
HOST_ANTIGRAVITY = """\

HOST - Antigravity
The norms above and every skill name Claude Code's tools. Use this host's own:
  AskUserQuestion            : `ask_question`
  the Bash, PowerShell tools : `run_command`
  a subagent, the Agent tool : `invoke_subagent`
  loading a skill            : read its `SKILL.md` with `view_file`, then the files it
                               names - nothing is loaded until it is read
  an `mcp__server__tool`     : `call_mcp_tool` with that server and tool
  a `claude mcp add` line    : the same server in `~/.gemini/config/mcp_config.json`
The guards the norms and the skills name run here as this plugin's hooks, unseen
until one refuses.
The installed plugin is the folder these skills are read from; its version is in
its `.claude-plugin/plugin.json`.
`frontend-design` has no installer for this host. Where Claude Code holds it at
`~/.claude/plugins/marketplaces/claude-plugins-official/plugins/frontend-design/skills/frontend-design/SKILL.md`
it is present, unlisted as it is: read it there.
Write the todo list `build-flow` requires in chat, since this host has no tool for one.
`CLAUDE.md` is printed below, because this host does not load it.
This host loads `AGENTS.md`, which was written for a session without these norms -
where the two disagree, these norms hold.
"""

MARK = NORMS.splitlines()[0]


def printed(transcript: str) -> bool:
    """True when this conversation was already handed the norms."""
    try:
        with open(transcript, encoding="utf-8", errors="replace") as f:
            return any(MARK in line for line in f)
    except OSError:
        return False


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


PROHIBITIONS = re.compile(r"^## Prohibitions[ \t]*$", re.M)
SECTION = re.compile(r"^## ", re.M)


def prohibitions(rel: str, text: str) -> str:
    """The prohibitions section of the two documents that hold one, else nothing."""
    if rel == "PRD.md":
        marks = list(PRD_SECTION.finditer(text))
        if [m.group(1) for m in marks] != ["1", "2", "3", "4", "5", "6"]:
            return ""
        return text[marks[-1].start() :].strip()
    if rel != "docs/product.md":
        return ""
    mark = PROHIBITIONS.search(text)
    if not mark:
        return ""
    after = SECTION.search(text, mark.end())
    return text[mark.start() : after.start() if after else len(text)].strip()


def document(root: Path, rel: str, what: str, room: float) -> str:
    """A document whole where it fits the room left, else named with an order to read it
    and, where they fit, its prohibitions."""
    text = read(root / rel)
    if not text:
        return ""
    head = f"\n--- {rel} — {what} ---\n\n"
    lines = text.count("\n") + 1
    warning = ""
    if rel == "PRD.md" and lines > PRD_LINES_WARN:
        warning = (
            f"\nWARNING: PRD.md is {lines} lines. Past ~{PRD_LINES_WARN} it is "
            "carrying status rather than intent — read `docs-format` and say so to "
            "the user.\n"
        )
    whole = head + (prd_printed(text) if rel == "PRD.md" else text) + "\n" + warning
    if size(whole) <= room:
        return whole
    ranges = prd_ranges(text) if rel == "PRD.md" else ""
    order = (
        f"Read lines {ranges} - context, roles, prohibitions - before the first edit of\n"
        "this session, and each other section before changing what it governs."
        if ranges
        else "Read it before the first edit of this session."
    )
    named = f"{head}Not printed: no room left at session start. {order}\n"
    part = prohibitions(rel, text)
    kept = f"{named}Its prohibitions bind whether or not it is read:\n\n{part}\n"
    return (kept if part and size(kept + warning) <= room else named) + warning


# Where components live, by the folder name every stack in the rubric converges on.
# ponytail: a name heuristic, not a declared path. A repo keeping its shared set under
# another name is listed as nothing; read the path from the app's own files when one does.
UI_DIRS = {"components", "widgets"}
PRUNE = {"node_modules", "dist", "build", "out", "target", "vendor", "coverage", "design-canvas"}
SKIP_FILES = (".test.", ".spec.", ".stories.")
INVENTORY_MAX = 60  # files listed; the rest are counted, so the cost per session is bounded
INVENTORY_DEPTH = 5  # how deep a components folder is looked for, not how deep one is read

# Capitalised names only: a variants helper or a hook is not a component, and listing
# it buries the ones that are.
JS_DECLARED = re.compile(r"export\s+(?:default\s+)?(?:async\s+)?(?:function|const|class)\s+([A-Z]\w*)")
JS_BRACED = re.compile(r"export\s*\{([^}]*)\}")
NAMES = {
    ".tsx": None,
    ".jsx": None,
    ".vue": "stem",
    ".svelte": "stem",
    ".astro": "stem",
    ".dart": re.compile(r"class\s+([A-Z]\w*)\s+extends\s+\w*Widget\b"),
    ".kt": re.compile(r"@Composable(?:\s+@?\w+(?:\([^)]*\))?)*?\s+fun\s+([A-Z]\w*)"),
    ".swift": re.compile(r"struct\s+([A-Z]\w*)\s*:[^{]*\bView\b"),
}


def component_names(path: Path) -> list:
    rule = NAMES[path.suffix]
    if rule == "stem":
        return [path.stem]
    text = read(path)
    if rule is not None:
        return rule.findall(text)
    names = JS_DECLARED.findall(text)
    for group in JS_BRACED.findall(text):
        for item in group.split(","):
            # `Dialog as Trigger` exports Trigger; `type Props` exports no component
            name = item.split(" as ")[-1].strip()
            if name[:1].isupper() and " " not in name:
                names.append(name)
    # `IMPORT_STEPS` is capitalised and is a constant
    return [n for n in dict.fromkeys(names) if not n.isupper()]


def component_files(root: Path) -> list:
    found = []
    for cur, dirs, files in os.walk(root):
        rel = Path(cur).relative_to(root)
        inside = any(part.lower() in UI_DIRS for part in rel.parts)
        dirs[:] = [
            d for d in dirs
            if not d.startswith(".") and d not in PRUNE
            and (inside or d.lower() in UI_DIRS or len(rel.parts) < INVENTORY_DEPTH)
        ]
        if inside:
            found += [
                rel / f for f in files
                if Path(f).suffix in NAMES and not any(s in f for s in SKIP_FILES)
            ]
    return sorted(found, key=lambda p: (len(p.parts), p.as_posix()))


def inventory(root: Path) -> None:
    try:
        files = component_files(root)
    except OSError:
        return
    if not files:
        return
    sys.stdout.write(
        "\n--- Components already in this repo - reuse before writing a new one ---\n\n"
        "A listing, not the rule: `ui-build` is still read before any UI is written, and\n"
        "the file holding the shared set is still read whole.\n\n"
    )
    for rel in files[:INVENTORY_MAX]:
        names = component_names(root / rel)
        sys.stdout.write(rel.as_posix() + (": " + ", ".join(names) if names else "") + "\n")
    if len(files) > INVENTORY_MAX:
        sys.stdout.write(f"... {len(files) - INVENTORY_MAX} more files - list the folder.\n")


# The data layer is read from the row `logic-settle` writes into the app's Stack table,
# never guessed from a folder name: `lib`, `services`, `data`, and `api` all occur, and a
# wrong guess lists utilities as if they were queries. No row → nothing is printed.
DATA_ROW = re.compile(r"^\|\s*Data layer\s*\|\s*([^|]+)\|", re.I | re.M)
DATA_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs"}
DATA_MAX_FILES = 40
DATA_MAX_NAMES = 12
FN_DECLARED = re.compile(r"export\s+(?:async\s+)?(?:function\s+|const\s+)([A-Za-z_]\w*)")


def function_names(path: Path) -> list:
    # ponytail: JS and TS only. Another language lists its files by name; add its
    # declaration pattern here when an app on that stack has a data layer to list.
    if path.suffix not in DATA_SUFFIXES:
        return []
    text = read(path)
    names = FN_DECLARED.findall(text)
    for group in JS_BRACED.findall(text):
        for item in group.split(","):
            name = item.split(" as ")[-1].strip()
            if name and " " not in name:
                names.append(name)
    return [n for n in dict.fromkeys(names) if not n.isupper()]


def data_layer(root: Path) -> None:
    row = DATA_ROW.search(read(root / "CLAUDE.md"))
    if not row:
        return
    cell = row.group(1).strip()
    ticked = re.search(r"`([^`]+)`", cell)
    rel = (ticked.group(1) if ticked else cell.split()[0]).strip("/\\")
    folder = (root / rel).resolve()
    if root.resolve() not in folder.parents:
        return
    if not folder.is_dir():
        sys.stdout.write(
            f"\nNOTE: the Data layer row of CLAUDE.md names `{rel}`, and no such folder "
            "exists. The lint floor scoped to it guards nothing. Tell the user.\n"
        )
        return
    files = sorted(
        (
            p.relative_to(root) for p in folder.rglob("*")
            if p.is_file() and not p.name.endswith(".d.ts")
            and not any(s in p.name for s in SKIP_FILES)
            and not any(part in PRUNE or part.startswith(".") for part in p.relative_to(root).parts)
        ),
        key=lambda p: (len(p.parts), p.as_posix()),
    )
    if not files:
        return
    sys.stdout.write(
        f"\n--- Data layer of this repo ({rel}) - call what exists before writing a query ---\n\n"
        "A listing, not the rule: `logic-build` is still read before a query, an action,\n"
        "or a handler is written, and no database call is written outside this folder.\n\n"
    )
    for path in files[:DATA_MAX_FILES]:
        names = function_names(root / path)
        shown = names[:DATA_MAX_NAMES]
        if len(names) > DATA_MAX_NAMES:
            shown.append(f"+{len(names) - DATA_MAX_NAMES}")
        sys.stdout.write(path.as_posix() + (": " + ", ".join(shown) if shown else "") + "\n")
    if len(files) > DATA_MAX_FILES:
        sys.stdout.write(f"... {len(files) - DATA_MAX_FILES} more files - list the folder.\n")


def named_paths(doc: Path, root: Path) -> list:
    """Paths a living document names that do not exist: link targets resolved from the
    document's folder, backticked paths from the repo root."""
    # ponytail: a shape heuristic — a backticked token with a slash or a known file
    # extension. A backticked `and/or` reads as a path; widen the skip list when one shows up.
    text = read(doc)
    missing = []
    for target in LINK.findall(text):
        target = target.split("#")[0]
        if not target or "://" in target or target.startswith(("mailto:", "/")):
            continue
        if not (doc.parent / target).exists():
            missing.append(target)
    for token in TICKED.findall(text):
        if token.startswith(("/", "~", "$", "-", "http", "@")) or any(c in token for c in "<>*{}()=:"):
            continue
        if not re.search(r"[A-Za-z]", token):
            continue  # `09/2026/0001` is a document number, `1/2` a fraction
        if token == "DESIGN.md":
            continue  # absent until `design-settle` writes it, and the Proof profile names it from bootstrap
        first = token.split("/")[0]
        if "/" not in token and not FILE_EXT.search(token):
            continue
        if "." in first.lstrip(".") and "/" in token:
            continue  # a host name, not a folder
        if not (root / token).exists():
            missing.append(token)
    return list(dict.fromkeys(missing))


def stale_paths(root: Path) -> None:
    docs = root / "docs"
    files = [docs / name for name in PATH_CHECKED] + sorted((docs / "guide").glob("**/*.md"))
    found = []
    for doc in files:
        if doc.is_file():
            found += [f"{doc.relative_to(root).as_posix()}: `{p}`" for p in named_paths(doc, root)]
    if not found:
        return
    sys.stdout.write(
        "\nNOTE: these living documents name paths that do not exist:\n"
        + "".join(f"  - {line}\n" for line in found[:STALE_MAX])
        + (f"  ... {len(found) - STALE_MAX} more\n" if len(found) > STALE_MAX else "")
        + "A commit that moved them should have corrected the document (`docs-format`,\n"
        "same commit). Tell the user, and correct them in this session's scope.\n"
    )


def stale_note(root: Path) -> None:
    text = read(root / "CLAUDE.md")
    if not text:
        return
    found = [label for phrase, label in STALE if phrase in text]
    if not found:
        return
    sys.stdout.write(
        "\nNOTE: CLAUDE.md still carries sections now owned by kaizn:\n"
        + "".join(f"  - {label}\n" for label in found)
        + "Tell the user to delete them; the plugin version above is authoritative.\n"
    )


def emit(root: Path, payload: dict) -> None:
    on_antigravity = payload.get("host") == host.ANTIGRAVITY
    queue = "what is not built yet"
    notes = ""
    if (root / "PRD.md").is_file():
        text, files = norms(BLOCKS), [("PRD.md", "intent and prohibitions"), ("QUEUE.md", queue)]
    elif (root / "docs" / "PRD.md").is_file():
        text, files = norms(BLOCKS, DOCS_FORM), list(LIVING)
        for rel in ("docs/README.md", "docs/product.md"):
            if not (root / rel).is_file():
                notes += f"\nNOTE: {rel} is missing. `app-settle` seeds it from docs/PRD.md - tell the user.\n"
        notes += captured(stale_paths, root)
    else:
        # No PRD in either form: an empty directory, an app not documented yet, or a repo
        # that is not an app. Its queue is still printed, from the root or from `docs/`.
        text, files = norms(UNSETTLED_BLOCKS, DOCS_FORM, UNSETTLED_FORM), [("QUEUE.md", queue), ("docs/queue.md", queue)]
    notes += captured(stale_note, root)
    text += switched_block("norm_output", OUTPUT.format(folder=guard_output.folder(str(root))))
    # Antigravity takes the text as an injected step, which no such cap cuts.
    room = float("inf") if on_antigravity else BUDGET
    if on_antigravity:
        text += HOST_ANTIGRAVITY
        files.append(("CLAUDE.md", "what is true of this app alone"))
    else:
        text += first_session()
    out = text
    room -= size(text) + size(notes)
    for rel, what in files:
        text = document(root, rel, what, room)
        out += text
        room -= size(text)
    out += notes
    for listing, more in ((inventory, MORE_COMPONENTS), (data_layer, MORE_DATA)):
        text = captured(listing, root)
        text = fit(text, room, more) if text else ""
        out += text
        room -= size(text)
    note = handoff.note(root, payload.get("host") or host.CLAUDE, payload.get("transcript_path") or "")
    out += fit(note, room, MORE_HANDOVER) if note else ""
    sys.stdout.write(out)


def main() -> None:
    # On Windows stdout defaults to the ANSI codepage, which mangles anything the PRD
    # writes outside it — an em dash, a currency symbol, Indonesian quotation marks.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    payload = host.read_payload()
    root = Path(payload.get("cwd") or ".")
    if payload.get("host") != host.ANTIGRAVITY:
        emit(root, payload)
        sys.exit(0)

    # PreInvocation fires before every model call. The norms go in before the first call
    # of a conversation that has not been handed them: the first call of a turn is the
    # only one that checks, and the transcript is what remembers across turns.
    transcript = payload.get("transcript_path") or ""
    if payload.get("invocationNum"):
        # A later call of a turn follows a tool: the one moment this host lets a hook say
        # what `remind_docs` says after a commit on Claude Code. Never a reason to fail -
        # this runs before every model call.
        try:
            text = remind_docs.unasked(transcript)
        except Exception:
            text = ""
        if text:
            json.dump({"injectSteps": [{"userMessage": text}]}, sys.stdout)
        sys.exit(0)
    if printed(transcript):
        sys.exit(0)
    text = io.StringIO()
    with contextlib.redirect_stdout(text):
        emit(root, payload)
    # A user-role step stays in the conversation; an `ephemeralMessage` is gone after one call.
    json.dump({"injectSteps": [{"userMessage": text.getvalue()}]}, sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
