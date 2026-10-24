#!/usr/bin/env python3
"""Self-check session_norms.py: the two listings, the two document forms, and that they stay quiet.

Components are found by folder name; the data layer is read from the `Data layer` row
of the app's CLAUDE.md. The quiet cases come first on purpose. Both listings are paid
for in every session of every app repo, so a repo with nothing to list must add
nothing — a listing that appears where it should not costs more than one that is missing.
Run directly: python3 test_session_norms.py
"""
import importlib.util
import json
import os
import subprocess
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent / "session_norms.py"
MARK = "Components already in this repo"
DATA_MARK = "Data layer of this repo"

# `python3`, not sys.executable: this is the interpreter name hooks.json invokes, so a
# machine where only `python` resolves must fail here rather than pass a test whose
# subject never runs. The failure is the point.
PYTHON = "python3"


def run(root: Path, data: Path | str | None = None, **options: str) -> str:
    """The hook's output for `root`. Its data folder is a fresh one holding `options` as
    the user's switches and the first session's marker, so that a case sees only what it
    sets - unless `data` names the folder, or `""` hands the hook none."""
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PLUGIN_DATA"}
    with tempfile.TemporaryDirectory() as tmp:
        if data is None:
            (Path(tmp) / "switches.json").write_text(json.dumps(options), encoding="utf-8")
            (Path(tmp) / "onboarded").write_text("", encoding="utf-8")
            data = tmp
        if data:
            env["CLAUDE_PLUGIN_DATA"] = str(data)
        result = subprocess.run(
            [PYTHON, str(SCRIPT)],
            input=json.dumps({"cwd": str(root)}),
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
    assert result.returncode == 0, result.stderr
    return result.stdout


def write(root: Path, rel: str, text: str = "") -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        # quiet: an empty repo gets the norms and nothing else, its output folder among them
        out = run(root)
        assert "SESSION NORMS" in out and "\nOUTPUT\n" in out and "`guard_output` refuses" in out
        assert MARK not in out

        # quiet: a repo with code but no components folder
        write(root, "src/lib/date.ts", "export const Format = 1\n")
        write(root, "PRD.md", "# PRD - Demo\n")
        out = run(root)
        assert "# PRD - Demo" in out
        assert MARK not in out

        # quiet: components that live only where nobody should be sent looking
        write(root, "node_modules/lib/components/Thing.tsx", "export function Thing() {}\n")
        write(root, "src/design-canvas/components/Draft.tsx", "export function Draft() {}\n")
        write(root, ".next/components/Built.tsx", "export function Built() {}\n")
        assert MARK not in run(root)

        # listed: the one shared file, by its exported names — capitalised only, so a
        # variants helper or a hook does not read as a component
        write(
            root,
            "src/components/ui.tsx",
            "export function Button() {}\n"
            "export const Pager = () => null\n"
            "export const buttonVariants = {}\n"
            "export const PAGE_SIZES = [10, 50]\n"
            "export function usePager() {}\n",
        )
        # listed: the copy-in library shape, names exported in one trailing brace
        write(
            root,
            "src/components/ui/dialog.tsx",
            "function Dialog() {}\nfunction DialogTrigger() {}\n"
            "export { Dialog, DialogTrigger as Trigger, dialogVariants }\n",
        )
        # listed: a feature-local folder, which is where duplicates hide
        write(root, "src/features/leads/components/LeadCard.tsx", "export default function LeadCard() {}\n")
        # listed by file name: a single-file component format
        write(root, "src/components/StatusChip.vue", "<template/>\n")
        # not listed: tests and stories sitting beside the components
        write(root, "src/components/ui.test.tsx", "export function Fake() {}\n")
        write(root, "src/components/ui.stories.tsx", "export function Story() {}\n")

        out = run(root)
        assert MARK in out
        assert "src/components/ui.tsx: Button, Pager" in out
        assert "buttonVariants" not in out and "usePager" not in out and "PAGE_SIZES" not in out
        assert "src/components/ui/dialog.tsx: Dialog, Trigger" in out
        assert "src/features/leads/components/LeadCard.tsx: LeadCard" in out
        assert "src/components/StatusChip.vue: StatusChip" in out
        assert "Fake" not in out and "Story" not in out
        assert "Thing" not in out and "Draft" not in out and "Built" not in out
        # the inventory comes last, after the documents it must not push out of view
        assert out.index("# PRD - Demo") < out.index(MARK)

    # native surfaces: the platform axis has broken quietly three times already
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "lib/widgets/pager.dart", "class Pager extends StatelessWidget {}\nclass _State {}\n")
        write(
            root,
            "app/src/main/java/ui/components/Chips.kt",
            "@Composable\nfun StatusChip() {}\n\n@Composable\nprivate fun Dot() {}\n\nfun helper() {}\n",
        )
        write(root, "App/Components/Badge.swift", "struct Badge: View {}\nstruct Model: Codable {}\n")
        out = run(root)
        assert "lib/widgets/pager.dart: Pager" in out
        assert "Chips.kt: StatusChip, Dot" in out and "helper" not in out
        assert "Badge.swift: Badge" in out and "Model" not in out

    # capped: a large app gets the shallowest files and a count, never the whole tree
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for i in range(90):
            write(root, f"src/components/deep/nested/C{i:02}.tsx", f"export function C{i:02}() {{}}\n")
        write(root, "src/components/Shell.tsx", "export function Shell() {}\n")
        out = run(root)
        assert "src/components/Shell.tsx: Shell" in out
        assert "31 more" in out
        assert "C89" not in out

    # the data layer: read from the row `logic-settle` writes, never guessed from a name —
    # `lib`, `services`, `data`, and `api` all occur, and `lib` holds far more than queries
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        stack = "## Stack\n\n| Aspect | Choice |\n|---|---|\n| Database | Supabase |\n"

        # quiet: code that calls the database, but no app file declaring where it lives
        write(root, "src/lib/leads.ts", "export async function getLeads() {}\n")
        assert DATA_MARK not in run(root)

        # quiet: a Stack table with no Data layer row — nobody settled it yet
        write(root, "CLAUDE.md", stack)
        assert DATA_MARK not in run(root)

        # said out loud: a row pointing at a folder that is not there is a stale pointer,
        # and the lint floor's globs are wrong in the same way
        write(root, "CLAUDE.md", stack + "| Data layer | `src/data` — every database call |\n")
        out = run(root)
        assert DATA_MARK not in out
        assert "Data layer row" in out and "src/data" in out

        # listed: functions by name; types, constants, and tests are not functions to call
        write(root, "CLAUDE.md", stack + "| Data layer | `src/lib` — every database call |\n")
        write(
            root,
            "src/lib/leads.ts",
            "export type Lead = {}\nexport interface Row {}\n"
            "export const PAGE_SIZE = 50\n"
            "export async function getLeads() {}\n"
            "export const approveLead = async () => {}\n"
            "function internal() {}\nexport { internal as archiveLead }\n",
        )
        write(root, "src/lib/leads.test.ts", "export function fake() {}\n")
        write(root, "src/lib/many.ts", "".join(f"export function fn{i:02}() {{}}\n" for i in range(20)))
        out = run(root)
        assert DATA_MARK in out and "src/lib" in out
        assert "src/lib/leads.ts: getLeads, approveLead, archiveLead" in out
        assert " Lead," not in out and " Row" not in out and "PAGE_SIZE" not in out
        assert "fake" not in out
        assert "fn11, +8" in out and "fn12" not in out

        # a path that climbs out of the repo is not followed
        write(root, "CLAUDE.md", stack + "| Data layer | `../outside` |\n")
        assert DATA_MARK not in run(root)

    forms()
    limit()
    print("ok")


def limit() -> None:
    """Claude Code replaces a hook's stdout over 10,000 characters with its first 2,000, so
    the norms themselves stop arriving. What fits is printed as before - those cases come
    first - and what does not is named or cut, never allowed to push the output over."""
    spec = importlib.util.spec_from_file_location("session_norms", SCRIPT)
    norms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(norms)

    def sized(out: str) -> int:
        return len(out) + out.count("\n")  # as a Windows stdout writes it

    # the fixed text leaves room for a repo's own: the three forms of the norms alone
    for text in (norms.NORMS, norms.docs_norms(), norms.unsettled_norms()):
        assert sized(text) < norms.BUDGET - 3000, sized(text)
        assert "`norms-help`" in text and "git commit -- <paths>" in text
        assert "A block or a table a skill orders printed is printed whole" in text

    shaped = (
        "# PRD\nintro\n\n## 1. Konteks\nctx\n\n## 2. Roles\nrole-body\n\n"
        "## 3. Business Rules\n" + "rule-line\n" * 40 + "\n## 4. Glossary\nterm-body\n\n"
        "## 5. Design System\nhex-body\n\n## 6. Larangan\n"
    )

    # unchanged: a PRD that fits is printed, with its queue and its listing whole
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "PRD.md", shaped + "never-x\n")
        write(root, "QUEUE.md", "- Legacy page\n")
        write(root, "src/components/Shell.tsx", "export function Shell() {}\n")
        out = run(root)
        assert "never-x" in out and "- Legacy page" in out and "Shell.tsx: Shell" in out
        assert "Not printed:" not in out and "session start carries" not in out

        # too long: the PRD is named by the lines of its printed sections, the norms
        # arrive whole, and what is small is still printed
        long = shaped + "never-x\n" * 900
        write(root, "PRD.md", long)
        out = run(root)
        assert sized(out) <= norms.LIMIT, sized(out)
        assert out.startswith(norms.NORMS) and "CLOSING THE SESSION" in out
        lines = long.splitlines()
        rules, last = lines.index("## 3. Business Rules"), lines.index("## 6. Larangan") + 1
        assert f"Read lines 1-{rules} and {last}-{len(lines)} - context, roles, prohibitions" in out
        assert "never-x" not in out and "WARNING: PRD.md is" in out
        assert "- Legacy page" in out and "Shell.tsx: Shell" in out

        # too long, Section 6 short: the prohibitions are printed under the order to read
        write(root, "PRD.md", shaped.replace("ctx\n", "ctx-line\n" * 900) + "never-z\n")
        out = run(root)
        assert sized(out) <= norms.LIMIT and "Not printed: " in out
        assert "## 6. Larangan\nnever-z" in out and "ctx-line" not in out

        # too long and off-shape: no section can be located, so the order is to read it
        write(root, "PRD.md", "# PRD\n" + "never-x\n" * 2000)
        out = run(root)
        assert sized(out) <= norms.LIMIT and "Read it before the first edit" in out

    # docs form: the one document that does not fit is named, the others are printed
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "docs/PRD.md", "# PRD - Frozen\n")
        write(root, "docs/README.md", "# Index\n")
        write(root, "docs/product.md", "# Product\n" + "context-line\n" * 900)
        write(root, "docs/queue.md", "- Import page\n")
        out = run(root)
        assert sized(out) <= norms.LIMIT and out.startswith(norms.docs_norms())
        assert "--- docs/product.md — context, roles, prohibitions ---\n\nNot printed: " in out
        assert "context-line" not in out and "# Index" in out and "- Import page" in out

        # its prohibitions are printed all the same, and nothing after them
        write(
            root,
            "docs/product.md",
            "# Product\n" + "context-line\n" * 900 + "\n## Prohibitions\n\n- never-y\n\n## Later\nlater-line\n",
        )
        out = run(root)
        assert sized(out) <= norms.LIMIT and "Not printed: " in out
        assert "## Prohibitions\n\n- never-y\n" in out and "- Import page" in out
        assert "context-line" not in out and "later-line" not in out

        # prohibitions too long to fit are named with the rest, never cut
        write(root, "docs/product.md", "# Product\n\n## Prohibitions\n\n" + "- never-y\n" * 900)
        out = run(root)
        assert sized(out) <= norms.LIMIT and "never-y" not in out and "Not printed: " in out

    # a listing is cut where the room ends and says so; one with no room says only that
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "docs/queue.md", "- A line of the queue\n" * 120)
        for i in range(60):
            write(root, f"src/components/Component{i:02}.tsx", f"export function AVeryLongComponentName{i:02}() {{}}\n")
        out = run(root)
        assert sized(out) <= norms.LIMIT, sized(out)
        assert "Component00.tsx" in out and "Component59.tsx" not in out
        assert norms.MORE_COMPONENTS in out

        # a queue sized to leave less room than the listing's own heading takes
        output = norms.OUTPUT.format(folder=norms.guard_output.folder(str(root)))
        room = norms.BUDGET - sized(norms.unsettled_norms() + output)
        write(root, "docs/queue.md", "- A line of the queue\n" * ((room - 150) // 23))
        out = run(root)
        assert sized(out) <= norms.LIMIT, sized(out)
        assert "- A line of the queue" in out and MARK not in out and norms.MORE_COMPONENTS in out


def forms() -> None:
    """The two document forms, and the repo with neither. The legacy repo comes first: the
    four running apps are legacy, and their session start must not move."""
    spec = importlib.util.spec_from_file_location("session_norms", SCRIPT)
    norms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(norms)
    # every replacement must hit, or the docs form silently prints a legacy line
    for old, _ in norms.DOCS_FORM:
        assert old in norms.NORMS, old
    for old, _ in norms.UNSETTLED_FORM:
        assert old in norms.docs_norms(), old

    # legacy: a root PRD.md keeps the legacy block and documents, whatever docs/ holds
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "PRD.md", "# PRD - Legacy\n")
        write(root, "QUEUE.md", "- Legacy page\n")
        write(root, "docs/PRD.md", "# PRD - Stray\n")
        write(root, "docs/product.md", "# Product - Stray\n")
        out = run(root)
        assert out.startswith(norms.NORMS)
        assert "--- PRD.md — intent and prohibitions ---" in out and "- Legacy page" in out
        assert "Stray" not in out and "NOTE" not in out and "NOT SETTLED" not in out

        # legacy, off-shape: a PRD whose six sections cannot be located is printed whole
        off = "# PRD\n\n## 1. Context\nctx\n\n## 3. Business Rules\nrule-body\n\n## Prohibitions\nnever-x\n"
        write(root, "PRD.md", off)
        out = run(root)
        assert "rule-body" in out and "never-x" in out and "Not printed" not in out

        # legacy, in shape: context, roles and prohibitions printed; rules, glossary and
        # design system named by line range, whatever language the headings are in
        shaped = (
            "# PRD\nintro\n\n## 1. Konteks\nctx\n\n## 2. Roles\nrole-body\n\n"
            "## 3. Business Rules\nrule-body\n### Timing\nmore-rules\n\n## 4. Glossary\nterm-body\n\n"
            "## 5. Design System\nhex-body\n\n## 6. Larangan\nnever-x\n"
        )
        write(root, "PRD.md", shaped)
        out = run(root)
        assert "intro" in out and "ctx" in out and "role-body" in out and "never-x" in out
        assert "rule-body" not in out and "more-rules" not in out
        assert "term-body" not in out and "hex-body" not in out
        lines = shaped.splitlines()
        first, last = lines.index("## 3. Business Rules") + 1, lines.index("## 4. Glossary")
        assert f"## 3. Business Rules\n\nNot printed. Read `PRD.md` lines {first}-{last} " in out
        assert "## 4. Glossary\n\nNot printed." in out and "## 5. Design System\n\nNot printed." in out

    # neither form: `app-settle` has not run, so the block says so and drops the sections
    # resting on what it writes; a root QUEUE.md when present, and nothing said about
    # documents that were never seeded
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "QUEUE.md", "- Toolkit line\n")
        out = run(root)
        assert out.startswith(norms.unsettled_norms()) and "- Toolkit line" in out and "NOTE" not in out
        assert "\nNOT SETTLED\n" in out and "\nGIT\n" in out and "\nASKING\n" in out
        assert "POINTERS" not in out and "CLOSING THE SESSION" not in out
        assert "named below" not in out and "block below" not in out and "closed list" not in out
        assert "docs/rules.md" not in out and "Section 6" not in out

    # ... and a queue kept under docs/ with no PRD beside it is printed the same way
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "docs/queue.md", "- Toolkit line\n")
        write(root, "docs/guide/gates.md", "# Not injected\n")
        out = run(root)
        assert out.startswith(norms.unsettled_norms()) and "--- docs/queue.md" in out
        assert "- Toolkit line" in out and "Not injected" not in out and "NOTE" not in out

    # docs form: the three living documents, never the frozen ones
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "docs/PRD.md", "# PRD - Frozen\n")
        write(root, "docs/changes/2026-01-01-import.md", "# Change - Frozen\n")
        write(root, "docs/decisions/0001-stack.md", "# Decision - Frozen\n")
        write(root, "docs/README.md", "# Index\n- [product.md](product.md)\n- [rules.md](rules.md#approval)\n")
        write(root, "docs/product.md", "# Product - Living\nRuns from `package.json`, data in `src/data`.\n")
        write(root, "docs/rules.md", "# Rules - Not injected\n")
        write(root, "docs/queue.md", "- Import page — writes `src/contracts/import.ts`\n")
        write(root, "package.json", "{}\n")
        write(root, "src/data/leads.ts", "export async function getLeads() {}\n")
        out = run(root)
        assert out.startswith(norms.docs_norms()) and "NOT SETTLED" not in out
        assert "--- docs/README.md — the index ---" in out and "# Product - Living" in out
        assert "- Import page" in out
        assert "Frozen" not in out and "Not injected" not in out
        assert "`PRD.md` and `QUEUE.md`" not in out and "`docs/queue.md` lines" in out
        # quiet: every named path resolves, and the queue may name files not built yet
        assert "NOTE" not in out

        # said out loud: a moved file and a dead link, and nothing that only looks like a path
        write(
            root,
            "docs/product.md",
            "# Product\nData in `src/data/gone.ts`. See [the guide](guide/missing.md).\n"
            "Not paths: `/help`, `https://x.dev/a.ts`, `api.example.com/v1`, `docs/changes/<date>-<slug>.md`,"
            " `lead_candidates`, [site](https://x.dev), `Intl.DateTimeFormat`, `09/2026/0001`.\n"
            # the Proof profile names it from bootstrap, before `design-settle` writes it
            "Screenshots at the widths `DESIGN.md`'s Layout fixes.\n",
        )
        write(root, "docs/guide/approve-a-request.md", "# Approve\nOpen `src/pages/gone.tsx`.\n")
        out = run(root)
        assert "docs/product.md: `src/data/gone.ts`" in out and "docs/product.md: `guide/missing.md`" in out
        assert "docs/guide/approve-a-request.md: `src/pages/gone.tsx`" in out
        for fake in ("/help", "x.dev", "api.example.com", "<date>", "lead_candidates", "Intl.", "09/2026", "DESIGN.md"):
            assert f"`{fake}" not in out.split("NOTE:")[1], fake

    # docs form, half seeded: the missing living document is named, not skipped in silence
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "docs/PRD.md", "# PRD - Frozen\n")
        out = run(root)
        assert "docs/product.md is missing" in out and "docs/README.md is missing" in out
        assert "queue.md is missing" not in out


def antigravity() -> None:
    """Antigravity runs the script before every model call, from the folder holding
    hooks.json: it must hand the norms over once per conversation and stay silent after."""

    def call(root: Path, invocation: int, transcript: str = "") -> str:
        payload = {"invocationNum": invocation, "workspacePaths": [str(root)], "transcriptPath": transcript}
        result = subprocess.run(
            [PYTHON, str(SCRIPT)], input=json.dumps(payload), capture_output=True,
            text=True, encoding="utf-8", cwd=SCRIPT.parent.parent,
        )
        assert result.returncode == 0, result.stderr
        return result.stdout

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "app"
        write(root, "docs/PRD.md", "# PRD - Frozen\n")
        write(root, "docs/README.md", "# Index\n")
        write(root, "docs/product.md", "# Product\n")
        write(root, "CLAUDE.md", "# App\n## Locale\nOn screen: Indonesian\n")

        # quiet: every model call after the first of a turn
        assert call(root, 3) == ""

        # quiet: a later turn of a conversation that was already handed the norms
        seen = Path(tmp) / "seen.jsonl"
        seen.write_text(json.dumps({"type": "USER_INPUT", "content": "SESSION NORMS (raizen-norms)\n..."}) + "\n", encoding="utf-8")
        assert call(root, 0, str(seen)) == ""

        # the first call: one injected user-role step, and nothing else on stdout
        fresh = Path(tmp) / "fresh.jsonl"
        fresh.write_text(json.dumps({"type": "USER_INPUT", "content": "build the page"}) + "\n", encoding="utf-8")
        steps = json.loads(call(root, 0, str(fresh)))["injectSteps"]
        assert len(steps) == 1 and list(steps[0]) == ["userMessage"]
        text = steps[0]["userMessage"]
        assert text.startswith("SESSION NORMS") and "# Product" in text
        assert "HOST - Antigravity" in text and "`ask_question`" in text and "loading a skill" in text
        assert "claude-plugins-official/plugins/frontend-design" in text
        # this host does not load CLAUDE.md, so the app's own facts are handed over too
        assert "On screen: Indonesian" in text

        # no cap cuts an injected step, so a long document is still handed over whole
        write(root, "docs/product.md", "# Product\n" + "context-line\n" * 900)
        long = Path(tmp) / "long.jsonl"
        long.write_text(json.dumps({"type": "USER_INPUT", "content": "build the page"}) + "\n", encoding="utf-8")
        text = json.loads(call(root, 0, str(long)))["injectSteps"][0]["userMessage"]
        assert text.count("context-line") == 900 and "Not printed:" not in text
        write(root, "docs/product.md", "# Product\n")

        # Claude Code is told nothing about another host, and loads CLAUDE.md itself
        out = run(root)
        assert "HOST - Antigravity" not in out and "On screen: Indonesian" not in out

    print("ok antigravity")


def switched() -> None:
    """The user's switches: a block on is printed as before, `advice` is printed with one
    line under its heading, `off` is not printed, and one line names what moved."""
    spec = importlib.util.spec_from_file_location("session_norms", SCRIPT)
    norms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(norms)

    # every switch on, the blocks are each form's text exactly: each replacement lies in one block
    assert norms.norms(norms.BLOCKS) == norms.NORMS
    assert norms.norms(norms.BLOCKS, norms.DOCS_FORM) == norms.docs_norms()
    assert norms.norms(norms.UNSETTLED_BLOCKS, norms.DOCS_FORM, norms.UNSETTLED_FORM) == norms.unsettled_norms()
    every = {key: "on" for key in norms.switches.RULES}

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "PRD.md", "# PRD - Demo\n")
        plain = run(root)

        # unchanged: every switch spelled `on`, or set to a value nobody offered
        assert run(root, **every) == plain and run(root, norm_git="maybe", guard_git="") == plain
        assert "SWITCHED" not in plain

        # off: the block is gone, the others and the documents stay, and the line says why
        out = run(root, norm_git="off", norm_closing="off")
        assert "\nGIT\n" not in out and "CLOSING THE SESSION" not in out and "git commit -- <paths>" not in out
        assert "\nLANGUAGE\n" in out and "\nSCOPE\n" in out and "\nOUTPUT\n" in out and "# PRD - Demo" in out
        assert out.startswith(norms.HEAD + "SWITCHED by the user, on purpose: norm_git off, norm_closing off.\n\nLANGUAGE\n")

        # advice: the block whole, one line under its heading
        out = run(root, norm_language="advice", norm_output="advice")
        assert "\nLANGUAGE\n" + norms.ADVICE + "The user's language and" in out
        assert "\nOUTPUT\n" + norms.ADVICE + "A file made for the user" in out
        assert out.replace(norms.ADVICE, "").replace(
            "SWITCHED by the user, on purpose: norm_language advice, norm_output advice.\n\n", ""
        ) == plain

        # a guard or a reminder moved away from on: every block printed, and the line names it
        out = run(root, guard_git="advice", remind_docs="off")
        assert "SWITCHED by the user, on purpose: guard_git advice, remind_docs off.\n" in out
        assert out.replace("SWITCHED by the user, on purpose: guard_git advice, remind_docs off.\n\n", "") == plain

        # the output block and the pointers, in each form that prints them
        assert "\nOUTPUT\n" not in run(root, norm_output="off")
        assert "\nPOINTERS - read before touching\n" not in run(root, norm_pointers="off")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root, "docs/PRD.md", "# PRD - Frozen\n")
        write(root, "docs/product.md", "# Product\n")
        write(root, "docs/README.md", "# Index\n")
        out = run(root, norm_scope="off", norm_decisions="advice")
        assert "\nSCOPE\n" not in out and "closed list in `docs-format`" not in out
        assert "\nDECISIONS\n" + norms.ADVICE in out and "# Product" in out

    # unsettled: `norm_pointers` covers the NOT SETTLED block that stands in its place
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        assert "\nNOT SETTLED\n" in run(root)
        out = run(root, norm_pointers="off")
        assert "NOT SETTLED" not in out and "\nSCOPE\n" in out
        assert "\nNOT SETTLED\n" + norms.ADVICE in run(root, norm_pointers="advice")
        # everything off: the heading and the line remain, and the output stays well formed
        out = run(root, **{key: "off" for key in every})
        assert out.startswith(norms.HEAD + "SWITCHED by the user, on purpose: norm_language off")
        assert "\nLANGUAGE\n" not in out and "\nOUTPUT\n" not in out and "\n\n\n" not in out

    print("ok switched")


def first() -> None:
    """The first session on a machine is told once, after its task, where the rules are
    switched: on Claude Code, where a data folder holds no marker yet."""
    spec = importlib.util.spec_from_file_location("session_norms", SCRIPT)
    norms = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(norms)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "app"
        write(root, "PRD.md", "# PRD - Demo\n")
        plain = run(root)
        assert "FIRST SESSION" not in plain
        # no data folder handed over: what every session got before
        assert run(root, data="") == plain

        data = Path(tmp) / "plugins" / "data" / "raizen-norms-raizen"
        out = run(root, data=data)
        assert out.count("\nFIRST SESSION ON THIS MACHINE\n") == 1 and "`/raizen-norms:norms-config`" in out
        assert out.replace(norms.FIRST, "") == plain and (data / "onboarded").is_file()
        # once: the next session on the machine is not told again
        assert run(root, data=data) == plain
        # the user's switches do not count as having been told
        other = Path(tmp) / "other"
        write(other, "switches.json", json.dumps({"guard_git": "advice"}))
        assert "FIRST SESSION" in run(root, data=other)
        # a data folder that cannot hold the marker: no line, never a failed hook
        write(Path(tmp), "a-file", "x")
        assert run(root, data=Path(tmp) / "a-file" / "data") == plain

        # Antigravity: never, and no marker written
        fresh = Path(tmp) / "fresh.jsonl"
        fresh.write_text(json.dumps({"type": "USER_INPUT", "content": "build the page"}) + "\n", encoding="utf-8")
        unseen = Path(tmp) / "agy-data"
        payload = {"invocationNum": 0, "workspacePaths": [str(root)], "transcriptPath": str(fresh)}
        result = subprocess.run(
            [PYTHON, str(SCRIPT)], input=json.dumps(payload), capture_output=True, text=True, encoding="utf-8",
            cwd=SCRIPT.parent.parent, env={**os.environ, "CLAUDE_PLUGIN_DATA": str(unseen)},
        )
        text = json.loads(result.stdout)["injectSteps"][0]["userMessage"]
        assert result.returncode == 0 and text.startswith("SESSION NORMS") and "FIRST SESSION" not in text
        assert not unseen.exists()

    print("ok first")


if __name__ == "__main__":
    demo()
    antigravity()
    switched()
    first()
