# Document mode — the documents of an app that never had them

## D1 — Read the stack, do not ask it

Launch the subagent on `repo-read.md`, mode document, and report the STACK block it returns. Everything in it is readable, so none of it is a question.

Rows that come out `not readable` stay that way. They are asked at D3 only where they change what the documents must say — a hosting platform nobody can name does not.

## D2 — The story, then state your reading, then STOP

Run the interview of `SKILL.md`. **The reading may draw on the code, and it must say which parts did**: separate what was measured from what was inferred, so the user knows what they are correcting.

**A correction that contradicts a measurement is written by what it states**: what the app is meant to do — a rule, a role's limit — as the user said it; what exists — a version, a host, a file — as measured. The losing side is a `Findings` line at D6.

## D3 — Six themes, and one rule that outranks the rest

**Three themes are partly readable and three leave no trace at all.** Roles, rule *values*, and terms came back from D1. Nothing readable is asked as though unknown — it is **shown and confirmed**:

> *"The code caps approvals at 5,000,000 for the `supervisor` role — `rls/approvals.sql:14`. What is that number for?"*

- **The problem before the app, how the work was done then, and the non-goals exist nowhere in the repo**: ask them openly, with no options, in one message where they are independent.
- **The rule that outranks everything else here is the reason behind every number** (`SKILL.md`): the code gave every value and will never give one reason. A recorded ignorance is worth more than a plausible fiction, because the next session knows not to trust it.
- **Confirm the Locale row here, though it was measured**: a half-translated UI measures as whichever half is larger.

## D4 — Summary, then STOP

One message: app name · Surface/Data/Deploy as read · roles · key business rules **with their reasons** · domain terms · non-goals · every row still `not readable`.

## D5 — Write

After the approval, read `prd-structure.md` and `scaffold.md` in one turn. Write `docs/PRD.md` and seed the living documents as `prd-structure.md` states, with these differences:

| Where | Difference from bootstrap mode |
|---|---|
| Stack | Recorded **as found**, each line a measurement naming its file, and no decision record seeded — nobody chose from a list. The Surface row and Proof profile are still written, measured rather than chosen |
| Prohibitions | Only those the user states now. A prohibition inferred from code is not a prohibition, it is a habit |
| `docs/architecture.md`, `docs/runbook.md` | Written from D1's block, each sentence a measurement naming its file. What the repo does not show — a backup, a restore, who decides in an outage — is `[needs verification]`, never asked |
| Help row | `guide pages` where `docs/guide/` holds pages, `in-app` with its route where a page renders them, else `none` — read, never asked |

Then the rows `scaffold.md` marks Both:

- **`CLAUDE.md`** to its shape, filled from D1. Already present → **do not overwrite.** Add only the missing rows and report what was left alone.
- **A `CLAUDE.md` that imports `AGENTS.md`** — an `@AGENTS.md` line, as a framework's template ships it — **is asked once through AskUserQuestion**: remove the import line, recommended, because `AGENTS.md` is written for agents never handed the norms and may restate one; or keep it. Kept → write `AGENTS.md`'s opening line without its claim that Claude Code does not read the file, which the import makes false.
- **`AGENTS.md`** to its shape. The `## UI` and `## Logic` parts hold their bootstrap lines — no `DESIGN.md` exists here and no data layer folder has been named; `design-settle` and `logic-settle` each fill their own part. Already present → **do not overwrite**; add the parts it lacks under their own headings and report what was left alone.
- **`README.md` at the root** — already present → **do not overwrite**; report it untouched.
- **A file already at a path this mode writes under `docs/`** → do not overwrite it; report it and ask where it goes before writing.
- **`.claude/settings.json`** enabling `raizen-norms`. Already present with other plugins → add the key, keep the rest.
**No scaffold, no `git init` on an existing repo, no host config, no CI workflow** — they already exist or the user decided against them.

Commit the new files, paths named.

## The stack is not on trial — in this mode

**Document mode reports; it does not migrate, and it does not re-litigate.** Say a finding once, in the close block, one line each, and only where it is concrete:

| A finding | Not a finding |
|---|---|
| The library is unmaintained, or has had a supply-chain event | The rubric would have recommended something else |
| A version is past end-of-life for security fixes | A newer framework exists |
| **A norm can never apply here** — a database with no row-level security makes the `db-ops` role test meaningless | You would have picked differently |

- **Never report the right-hand column.** The rubric filters options for a **new** repo, where choosing costs nothing; this repo already paid, and *Not ready* there means no path is written for it, not that it is wrong.
- **Never soften the third row.** It says a guarantee this toolkit makes does not hold in this repo, and the user is entitled to know which one and why.
- **The trial the user wants is rework mode**, in a later session, once these documents exist to judge any change against.

## D6 — Close

One block:

```
Written    : docs/PRD.md · docs/README.md · product.md · rules.md · glossary.md
             README.md [new / untouched] · CLAUDE.md [new / N rows added]
             AGENTS.md [new / N parts added] · .claude/settings.json
Not read   : [rows still unreadable]
Unverified : [what carries [needs verification]]
Findings   : [concrete stack findings, and D2's corrections that met a measurement — or "none"]
DESIGN.md  : absent — design-settle writes it
```

Then the next sessions, in this order:

```
/logic-settle   — the logic layer as it stands: what is installed, what is
                  missing, what is the wrong tool. Keeping everything is a
                  valid ending.
/design-settle  — audits the styling, then puts every visual decision to you:
                  ratify what the code already does, or decide otherwise.
/app-settle     — again, once these documents exist: it audits the code against
                  the rules and fixes what you pick, one commit per finding. Ask
                  it for a change instead, and it re-opens business rules, scope,
                  or stack.
Until DESIGN.md exists, any session will refuse to write a UI component.
```

`logic-settle` runs first because the promoted pages carry loading, empty, and failed states, and those belong to the data layer.

Do not run any of them now. Close by reminding the user that `raizen-norms` becomes active only once the next session starts in this repo.
