# The interview and the record — Steps 3 and 4

Options are assembled and verified as `logic-rubric.md` rules, on the criteria of each need's file.

## The mode — one question, before any need

Ask it right after the score is confirmed: two options, with a recommendation.

| Mode | What is asked | For whom |
|---|---|---|
| **Fast** | Nothing. Every scored need is decided from the rubric's criteria, the research, the audit, and the documents' reading, then shown once as a list to correct | An app that must ship today, or needs whose platform answer nobody disputes |
| **Full** | Every scored need, batched — sequential only across a real dependency | **Recommended.** The interview is at most six questions, and each answer is a dependency the repo carries for years |

- **Exactly one need scored → skip this question and ask that need directly.**
- **Consequence, said in the question:** both modes end at the same records and the same install block — the only difference is where the correction happens, before the decisions or after them.
- **Fast is never silent.** Report every decision on one line with its basis:

```
L1 cache → <researched standard>  (criteria: several list screens share server rows; verified live)
L3 dates → Intl built-in          (platform ladder: format-only, no date arithmetic)
```

- **Fast skips the questions, never the verification**: a candidate it chooses is verified live first, and "none" or *keep* still wins wherever the ladder and the audit say they do. The user may cancel any line; a cancelled line opens that question normally.

## Running the interview

- **Batch the questions in L-number order**, up to four per call, several calls per turn. A need whose options or recommendation read an earlier answer (a family already chosen shifting a later recommendation) waits for that answer; independent needs travel together.
- **Reconcile after every batch**: two answers that collide go back as one question naming both, never resolved silently.
- **Each question carries more than two options, one marked recommendation, and a one-sentence consequence per option** — the same contract as the `design-settle` interview.
- **The story bends the options.** The need file's criteria filter and re-rank: an Edge runtime reorders L2, a realtime mention extends L1, a two-screen app moves the recommendation to handwritten. Read the story from the documents, not from the rubric.
- **Accept an answer outside the options.** A library the user names is verified the same way and used; state its consequence if known, or say you do not know it.
- **Quote every option's migration size from the audit** — `Replace with X — 31 call sites` beside `Keep — 0`.

## Two rules that read the audit, per need

**The audit found nothing for this need → the "none" option is never dropped** — *handwritten*, *platform built-in*, or *not yet*, whichever the need file names. It is the recommendation whenever the platform already covers the need or the app is too small for the library to pay for itself; its place in the list is the ladder's (`logic-rubric.md`).

**The audit found something → that is always an option, written first even when it is not the recommendation** — `Keep — <what is installed>`, or `Keep — handwritten, N sites`. It does not count toward the "more than two options" requirement.

- **Keeping an installed library is the recommendation, unless the audit produced a concrete finding against it.** A concrete finding is one of three, and the list is closed:

| Concrete finding | Not a finding |
|---|---|
| Unmaintained, or a fresh supply-chain event or advisory | Research ranks another candidate higher |
| Past end-of-life for security fixes | A newer option exists |
| **It blocks a norm** — something in `kaizn` cannot hold while this library stands | You would have picked differently |

- **A finding exists → the replacement may be recommended, and the finding is its one-sentence consequence.** State the finding, never a preference.
- **Against handwritten code, the need file's recommendation rule decides**, *keep* still written first — the closed list names library failures, so it never indicts handwritten code.

## Step 4 — Record

| Where | What |
|---|---|
| `docs/decisions/` | One record per decision, to `docs-format`'s shape: the candidates offered as considered options with their consequences — one never verified marked `unverified` — **the choice, and its one-sentence reason** |
| `CLAUDE.md` Stack table | One row per library: name only. Plus the `Data layer` row (`SKILL.md`, Hard limits) |

- **Keep the reason to one sentence, and versions out entirely** — the lockfile always knows *what*, never *why*, and a version turns every bump into a document edit.
- **A decision that replaces an earlier one supersedes its record.**
- **Record every "none", and every *keep* no record carried before**, so a later session that finds handwritten fetching can tell a decision from an accident.
- **Record a library that belongs to a family with its family** — `TanStack Query — TanStack ecosystem` — because `design-settle` reads the decision records when assembling UI options.
- **A trigger chosen at L6 is recorded as `need-attribution.md` rules.**

Then `install.md`, unless Step 5's skip condition holds (`SKILL.md`, the steps table) — then `floor.md`.
