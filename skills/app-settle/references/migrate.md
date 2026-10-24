# Migrate — a legacy repo moves to the `docs/` form

Mechanical work: every sentence inside the PRD's six sections lands in the document `docs-format`'s legacy map sends its section to, **word for word**. Only headings change, to the ones the shapes name. Nothing is re-decided, improved, reworded, or translated; what looks wrong is a line in the close block.

## M1 — Read, then say whether it can move

Read in one turn: `PRD.md` whole — the session start printed only part of it — `QUEUE.md`, a root `DESIGN.md`, `CLAUDE.md`, `AGENTS.md`, and of `docs-format` both `references/legacy.md` and `references/shapes.md`. In the same turn run two searches:

- **Every other file naming the old form** — `PRD.md`, `QUEUE.md`, or the PRD by a section number: `PRD 5.7`, `PRD §5.2`, `Section 6`.
- **Every rule-test title quoting Section 3** — in the files the repo's test runner collects, and in SQL files carrying a `Rule test:` marker: a title whose words open a rule. Ignore case, a `Rule test:` marker, and a leading `<group>:`.

Print one block:

```
MIGRATE
PRD.md     : [N lines · six sections located]  or  [off-shape — the section that cannot be located]
Section 3  : [N rules — table rows and list items — in N groups]
Rule tests : [N titles quoting a Section 3 rule]
Section 4  : [N terms]
Section 5  : [ratified / partly [needs verification] / every line [needs verification] / absent / adopted-whole]
DESIGN.md  : [generated copy at the root / none]
Decisions  : [N decision lines in Section 1]
QUEUE.md   : [N lines / absent]
Names it   : [N files besides PRD.md, QUEUE.md, DESIGN.md, CLAUDE.md and AGENTS.md]
```

- **A section is located by its number**, whatever language or decoration its heading carries.
- **Section 5 is ratified when it has content and no line is `[needs verification]`.**
- **A decision line is a list item of Section 1 naming a choice and its reason**, as `legacy.md` describes it. A reason given inside the Context table is not one, and stays in the table.

**Two repos cannot move mechanically, and stay legacy for this run:**

- **Off-shape** — a section cannot be located, so its sentences have no known destination. Reshaping `PRD.md` to `legacy.md`'s shape clears it.
- **Section 5 of the adopted-whole shape** — the `docs/` form has no place for it. `design-settle` replaces it with a ratified one, and that clears it.

Name the blocker and what clears it, change nothing, and offer align or rework on the repo as it stands.

Otherwise carry on without asking: the whole move is one commit, and `git revert` undoes it.

## M2 — Move

`git mv PRD.md docs/PRD.md`, and `git mv QUEUE.md docs/queue.md` where it exists. Under the title of `docs/PRD.md` add this one line as a paragraph of its own, a blank line above and below it, and change nothing else in the file, ever:

```
Frozen YYYY-MM-DD — the legacy PRD as it stood when this repo moved to the docs/ form. History, not current truth: the living documents are listed in docs/README.md.
```

Then write the living documents from it, each under the headings `shapes.md` gives. **Match a part by what it holds** — its own heading or bold label, in whatever language, is dropped for the shape's.

| From | To | How |
|---|---|---|
| Section 1 — the Context table, the Proof profile, problem, success, non-goals | `docs/product.md` | Copied under the headings of its shape. No Proof profile in the PRD → none is written; `build-flow` reads its absence as the web default |
| Section 1 — the decision lines | `docs/decisions/`, one record per line | The choice and its reason as the outcome; `date` is today's. A non-goal naming an alternative rejected for that choice moves into the record as a considered option. A part of the shape the line gives nothing for is left out, never invented. No decision line → no folder |
| Section 2 | `docs/product.md` — Roles | Copied |
| Section 3 | `docs/rules.md` | Below |
| Section 4 | `docs/glossary.md` | Copied |
| Section 5, ratified or partly so | `DESIGN.md` | M3 |
| Section 6 | `docs/product.md` — Prohibitions | Copied |

**Everything inside a section moves.** A part its shape has no heading for — a second table, a code block, a note — stays under the shape heading its section maps to, under its own label; in Section 1 that heading is Context. A label left with nothing under it is dropped. Only what sits outside the six sections — a version line, a change log — enters no living document; it stays in `docs/PRD.md`, named in the close block.

**Section 3: each sub-section becomes a `##` group under its own heading; each table row and each list item becomes a `###` topic.**

- **A table row** → the topic is its first cell, verbatim. The other cells follow as `<column>: <cell>` lines, a `Why` column as `Why:`.
- **A list item** → its text follows whole and unchanged under its topic. The topic is the first of these it has, in the rule's own words: the opening words a rule test's title already quotes · its bold lead-in · its opening words up to the first punctuation mark — a full stop, comma, semicolon or colon before a space, an opening bracket, or a dash set off by spaces. Two items that would share a topic each run on, mark by mark, until they differ.
- **A paragraph is never a topic**: it goes under its group heading, above the group's first topic, wherever in the sub-section it stood. Name in the close block each one that moved up.
- **No `Why` column → no `Why:` line.** A reason the rule's own text gives stays in that text; none is extracted and none invented.

Two rules for the whole move:

- **A number, a term, a name leaves exactly as it arrived.**
- **Write no `docs/architecture.md`, `docs/runbook.md`, `docs/changelog.md`, `docs/guide/` or `docs/changes/`**: the PRD holds no source for them. The next `app-settle` run writes the first two from the repo (`SKILL.md`, Step 0), and the Context it leaves carries no Help row, which reads as `none`.

## M3 — `DESIGN.md`, from Section 5

The one time this skill writes `DESIGN.md`: a change of format, never of design. Read `design-settle`'s `references/design-md.md`, and the format's live spec as that file orders.

- **The body is Section 5's sub-sections under the format's headings, in the format's order**, by the table in `legacy.md`, each matched by what it holds. The headings as the format writes them; the text under them untouched, a `[needs verification]` marker included.
- **Two sub-sections under one format heading keep their own headings beneath it, as `###`.**
- **A sub-section that table sends nowhere stays a section of its own**, under its own heading, after the toolkit's two — the format keeps an unknown section.
- **A format heading Section 5 holds nothing for is left out.**
- **Write no `## Contrast`**: its rows are computed, never copied. The contrast minimums stay in Colors, where Section 5 keeps them.
- **The lines above Section 5's first sub-section are not carried** — how it was decided, that the PRD is the source. They stay in `docs/PRD.md`.
- **Frontmatter.** A generated `DESIGN.md` at the root → keep its frontmatter: its tokens are the ratified values. None → `version`, `name`, and one `omitted` entry for each of `colors`, `typography`, `rounded`, `spacing` and `components`, in the shape the live spec gives, its `reason` in the user's language: the values live in the styling files, and `design-settle` writes the tokens.
- **Never derive a token here**: one transcribed wrong becomes the norm the styling files are then measured against.
- **Run the linter `design-md.md` names — zero errors.** The file is no longer a legacy repo's generated copy, so the linter runs. An error only a design decision would clear → restore the working tree to `HEAD`, delete the files this run created, and treat the repo as one of M1's blocked ones.

**Section 5 empty, every line `[needs verification]`, or absent → write no `DESIGN.md`, and delete a generated one.** `ui-build`'s gate holds until `design-settle` runs, as it held before.

## M4 — What still names the old form

Read `scaffold.md` for the two shapes, then:

- **`CLAUDE.md`** — a line pointing at a section or at `QUEUE.md` is corrected to the document that now holds it; one pointing at the PRD as a whole takes the wording `scaffold.md`'s shape gives that part. **A block — a heading and everything under it — telling a session how to write, keep, or format the PRD is deleted whole**: `docs-format` holds those rules, and left standing it orders the next session to write a root `PRD.md` back. Name each deleted block in the close block. Nothing else in the file moves.
- **`AGENTS.md`**, where present — its `## Read first` part, and the `## UI` and `## Logic` lines naming a section, to its shape. Absent, or holding none of them → nothing is written here; align's C2 owes it.
- **`README.md`** — correct a line naming `PRD.md` or `QUEUE.md`. Add nothing.
- **The moved text itself** — a pointer to `PRD.md`, `QUEUE.md`, or a section number is corrected to the document that now holds it. A sentence that is about the PRD rather than pointing at it is reported, never reworded.
- **Every other file M1 counted** — correct a path a build or a script reads. A comment is reported by count and never edited, least of all in an applied migration.
- **Write `docs/README.md` last**, the index of what now exists: its opening sentence is the first sentence of Success, verbatim, and its History line for `PRD.md` says what the frozen line says.

## M5 — Prove, then one commit

Commit nothing until all of these hold:

- **The counts match M1** — groups, rules and topics, terms, decision lines and records, queue lines — and every role, non-goal and prohibition arrived.
- **Every rule-test title M1 found contains a `###` heading of `docs/rules.md`**, case aside.
- **`DESIGN.md` passes its linter**, where M3 wrote it.
- **No root `PRD.md` and no root `QUEUE.md` remain.**
- **The session start reads the `docs/` form**: run `scripts/session_norms.py` of the plugin folder this skill is read from, with `{"cwd": "<repo root>"}` on stdin. Its output carries a `--- docs/README.md` and a `--- docs/product.md` block, no `--- PRD.md` block, and no `is missing` note. A stale path it names is the legacy text's own — report it, never fix it here.

One fails → fix the move, never the check. Then one commit, paths named.

```
MIGRATED
Moved       : PRD.md → docs/PRD.md, frozen · QUEUE.md → docs/queue.md
Written     : docs/README.md · product.md · rules.md [N topics] · glossary.md · decisions/ [N records]
              DESIGN.md [converted, tokens kept / converted, tokens owed by design-settle / absent — design-settle owes it]
Corrected   : [CLAUDE.md · AGENTS.md · README.md · other files — N lines each]
Deleted     : [the blocks of CLAUDE.md that governed the PRD, by heading — or "none"]
Off shape   : [parts kept under their own label, and where · paragraphs moved above their group's topics — or "none"]
Not carried : [text outside the six sections, left in docs/PRD.md only — or "none"]
Reported    : [sentences about the PRD left as they were · N files with comments naming a section · stale paths — or "none"]
No Why      : [N topics with no Why: line]
Verified    : [each check above, as run]
Commit      : [hash]
```

Say what the repo owes next, and run none of it: `/kaizn:app-settle` again audits it for align, where the guide pages it owes are listed.
