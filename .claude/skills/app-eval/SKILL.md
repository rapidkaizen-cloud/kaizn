---
name: app-eval
description: Evaluate an app that was built under these skills in order to find defects in the toolkit itself — traces what the user finds wrong in the result back to the rule that produced it, and reports findings rather than fixing anything. Runs in the raizen-toolkit repo with the app repo added as a working directory, and never modifies the app. Use when the user is dissatisfied with something an app under these skills produced, or wants a toolkit-improvement pass over a finished batch.
---

# app-eval — the app is the evidence, the toolkit is the defendant

Every gate in this toolkit measures an app against itself. `build-flow` judges a page against the proving page *of the same app*; the session audit checks accessibility, states, and click paths — none of which fail in an app that is merely bland. So an app can pass every gate, session after session, and still come out worse than it should be.

This skill is the only thing that looks at the finished result and asks whether the rules produced it. It changes no code. Its output is findings.

## 0 — Where this runs

**In this repo, with the app repo added as a working directory.** Not in the app repo.

Two reasons, and the second is the one that matters:

- **The installed plugin copy drifts from this repo.** `raizen-norms` needs a version bump and `/plugin update` before a change reaches a machine, so a session in an app repo reads rules that may already be fixed here. A trace against the wrong text is a void trace.
- **An agent inside a ruleset is the worst judge of that ruleset.** A session in an app repo has the `raizen-norms` block printed and the guards live: it is being *governed* by the thing under review, and it reads every constraint as the definition of correct. Here the skills are text under review instead. That posture is the whole method — without it this skill reproduces, one level up, exactly the self-referential bar described above.

The primary working directory is not this repo → **STOP** and say so. The `raizen-norms` session block is no signal either way — its hook is installed globally and prints in every session, this one included.

**Nothing in the app repo is written, moved, or deleted.** Fixing the app and fixing the toolkit are separate jobs, and the second may never quietly do the first. A defect worth fixing in the app is reported as a finding, and `app-settle`'s align mode is what acts on it — in the app repo, in another session.

No hook pins a Supabase call to the app's project. Name the project ref explicitly before any database read, and read only.

## 1 — The input is mandatory

**No input from the user → do not run.**

This is mechanical, not a courtesy. The user's dissatisfaction is the only signal from outside the app. Without it there is nothing to measure against, and the run collapses into listing whatever differs from product-type convention — taste presented as evidence.

Refusing is not the same as demanding a brief. The user often feels something is wrong well before they can name it, and helping them name it is part of the job. Ask three questions **in one turn**:

1. **Which page or screen** brings on the feeling → this points at the evidence
2. **Compared to what** — another product, an earlier version, a picture in their head → this is the external bar
3. **What did you expect to see instead** → this is the target

Question 2 may be answered *I don't know, it just feels off*. Then propose candidates the way `design-settle`'s reference search does — real products of this app's type, with links — and let the user point at one. A reference the user selects is evidence; a reference invented on their behalf is not.

The input may be a complaint or a direction — *"I want this app to feel more like X"* is as usable as *"this looks dead"*.

**The input sets the scope, never the verdict.** A run that can only ever confirm the user's complaint is a yes-machine. Concluding *the complaint is real, and the cause is a decision you took yourself in the `design-settle` interview* is a legitimate outcome, and so is *the complaint does not reproduce*.

## 2 — What is read

| Source | Where |
|---|---|
| The rules under review | This repo. The source, never the installed plugin |
| The app: routes, components, styling files, the design-system route | The app repo working directory |
| What the app was supposed to be | Its documents, `DESIGN.md` above all — through `docs-format`'s legacy map where the app has a root `PRD.md` |
| What was built when, and what is still owed | `git log`, and `git log` of its queue file |
| What happened while it was built | The app's session transcripts under `~/.claude/projects/<app-slug>/` |
| The external bar | The reference the user pointed at, plus product-type research run live |

The app is **run**, not only read. Screenshot the pages named in the input at the two widths `DESIGN.md` fixes. A judgement about how a screen feels, made from source alone, is a guess.

Transcripts are the one source that shows a rule failing without leaving a trace in the code: a session that worked around a rule, or took a default because no route existed. Read them for the pages in scope.

## 3 — Depth is uneven, and the report says so

A deep sweep of the whole toolkit surface costs hours and mostly returns nothing.

- **What the user named** → deep, all the way to the rule that caused it
- **Everything else** → one shallow pass, recording only what is anomalous
- **The report states which parts got which**

And it carries a **Not checked** section, always, even where the answer is *nothing*. Silence reads as *checked and fine*, and that is where context is lost without anyone noticing.

## 4 — Every finding names the rule

> A finding that cannot name the rule behind it is not a finding. It is a note, and it is reported as one.

*"This dashboard is boring"* names nothing. What follows is a finding:

> Every card carries the library's default padding and radius, in 12 of 14 pages, because `ui-build`'s Library defaults test can only be satisfied by a line in `DESIGN.md`, and `DESIGN.md` holds no line about visual emphasis. The rule has no route to an intentional departure.

Each finding carries five things, and none is optional:

1. **The symptom** — which pages, how many, what is on screen
2. **The rule traced** — skill and section, quoted
3. **The evidence** — code quoted inline, screenshots, counts
4. **The user's own words**, verbatim and unparaphrased
5. **What changes if the rule changes** — including which other apps it would reach

Point 4 exists because the sentence that started the run is the thing most easily lost. Paraphrased into the skill's own vocabulary, it stops being the user's complaint.

Then one of three verdicts, and every finding gets exactly one:

| Verdict | What it means | Where it goes |
|---|---|---|
| **The rule caused it** | Following the rule produces this result | A toolkit patch |
| **The rule allowed it; the session did not take the route** | A route existed and went unused | An app fix, not a toolkit one — *unless* the route is buried deep enough that no session finds it, which is a weaker toolkit finding, marked as such |
| **The rule is right; `DESIGN.md` is too thin** | The rule correctly refused, because nothing ever authorised the departure | Upstream: the `design-settle` interview never asked the question |

The third is the one most often mistaken for the first. A rule refusing correctly is not a defective rule — the defect is that nothing upstream could ever have granted permission. Patching the refusing rule there loosens a constraint that was doing its job.

**One app is one hypothesis.** State how many apps a finding was observed in. A pattern seen once may be that app's own history; the same pattern in a second app is the toolkit.

## 5 — Counter-evidence is required

The report carries a section naming **where the rule under attack did its job**: drift it prevented, inconsistency it caught, a decision it kept from being retaken per session.

Without it a report only ever shows failures, and the reflex is to loosen everything. Most of the tightness here is correct — operational apps trade expressiveness for consistency on purpose. A patch made without seeing what the rule was protecting buys one page's freedom with every later page's drift.

## 6 — The report

**Length is not the constraint.** One test decides what belongs:

> Can the toolkit patch be decided from this report, without opening the app repo again?

Concise means no line that changes no decision. Complete means every finding carries what deciding it takes. Both hold at once, so neither is traded for the other.

Shape: findings first, decidable in one read; raw evidence in an appendix behind them. That separation is what buys both properties — not compression.

**The report stands alone.** Quote code inline; a path on its own is dead the moment the report is read anywhere else. Describe each screenshot in words as well as linking it, because the image file may not survive.

Delivered twice, one job each:

- **Inline, in full** — this is what gets read and decided here
- **`~/.claude/raizen-evals/<app>-<YYYY-MM-DD>/`** — `report.md` plus the screenshots, which have to be files. Outside both repos: the app repo keeps only `docs-format`'s closed list, and this repo does not need a second copy of a decision its commit messages already record

## 7 — This skill does not patch the toolkit

The output is findings. Whether an instruction changes is the user's decision, taken after reading them.

Two reasons it stops here. A skill that both finds the defect and writes the fix stops arguing with itself about whether the defect is real. And an instruction changed here reaches every app that installs the plugin — that blast radius is not something a run should acquire by momentum.

When a patch is agreed, the rule the repo already holds applies: name what would be lost if the change did not exist, and pay for added lines with removed ones. Every line here costs context in every session, including the ones that never need it.
