---
name: simulate
description: Run the interview of any settle skill — app-settle, logic-settle, design-settle, or the chain of them — for real, against an app repo, a described scenario, or a test scenario this skill proposes, without executing anything — every question asked as the live skill would ask it, and after each answer the decision it produces and where the flow goes next, so the user can see whether the flow lands where their answers meant it to. Skips every printed block and every build step; installs nothing, writes nothing, draws nothing. Runs in the kaizn repo. Use to check a flow's decisions before running it in an app repo, or to test a skill change by answering its interview end to end. Also runs alone on request — a background subagent answers from a brief it writes first — to evaluate a skill with no one answering.
---

# simulate — the interview for real, the work on paper

What the user cannot see by reading a skill is whether their answers land where they meant them to: which decision a tick records, what it switches on, where the flow goes because of it. This skill runs the interview itself — the same questions, in the same order, with options invented for the target the same way — and after every answer states the decision and the direction. Nothing else runs.

## 0 — Where this runs, and what it touches

**In this repo, against the source under `skills/`, never the installed plugin copy.**

The target is one of three: a real app repo added as a working directory — read-only: `ls`, `grep`, `git log`, reading files; `npx impeccable detect <path>` where the skill would run it — a scenario in words, or **a scenario this skill proposes** (below). A scenario missing what the skill's first step reads (document form, `DESIGN.md`, UI present, platform, kind of app, who uses it, what is installed) is completed in **one** AskUserQuestion before the interview starts.

**Nothing is written, installed, drawn, or run.** No file in the target, no report file here, no `npm install`, no dev server, no canvas. The primary working directory is not this repo → **STOP**.

## 1 — The input

1. **Which skill**, or the chain `app-settle → logic-settle → design-settle`, each skill's decisions feeding the next as the live chain would.
2. **The target** — a repo path, a scenario in words, or none: then this skill proposes one.
3. **Who answers** — the user, or no one when the user asks for a run they do not answer: then section 6.

### Proposed scenarios

No target, or the user asks for one → offer **three or four test scenarios in one AskUserQuestion**, each a real kind of app with a platform, a primary role, a register, and a repo state — and each chosen to trip a **different set of the skill's switches**, named in its description: *template Next.js admin, no PRD, shadcn installed — trips: reading from code, UI exists, Keep candidate, audit, gate* · *fresh repo after app-settle, no UI — the shortest path* · *a written `DESIGN.md`, 40 components, drift only — trips: fix-or-redesign, findings gate* · *public landing page with a brand hex — trips: first-visit register, brand palette as constraint, no data table*. The recommended one is the scenario covering the switches no earlier simulation in this session has exercised. The picked scenario is written out as the facts the skill's first step reads, shown once, and the interview starts from it. At the close, name the switches this run never tripped and the scenario that would.

## 2 — What is read

The skill's `SKILL.md` whole, from this repo, before the first question; **each reference when the flow reaches the step that reads it** — a file the live run would not open, for a switch that is off, is not opened. The skills a step defers to, in `kaizn` or outside it — `ui-ux-pro-max`'s brand voice reference at the copy-voice dialog — where the step reads them and as far as it reads them; one not installed → the option carries `would read <skill>`. From the target, **only what the live skill would read at that step, in that order** — the router at the audit, not at Step 0; a fact read early produces a question the live run could not have asked, and is a defect of the simulation to report.

Where the skill says *verify live* or *research*, the result is not invented: the option carries `would verify live` and the interview goes on.

## 3 — What is skipped, and what replaces it

| The live skill would | This skill does |
|---|---|
| Print a block — preconditions, audit, frame inventory, close | Skip it. State only the switches it sets, in one line: `UI exists: yes → audit runs, Keep candidate offered, gate at Step 6` |
| Stop in chat on a block the user must read — the install block, the gate | Show the block **reduced to its decision lines** — each line's recommendation and alternatives, the gate's diff and removals — and ask the same approval in chat |
| Report cancellable lines — assumptions, ratified values, derived decisions | List the lines, then one multi-select: *which of these do you want to change?* — a cancelled line opens the dialog the skill defines for it |
| Draw frames, build a canvas, promote pages | Describe, do not draw: each candidate's name, the axis it explores, its motivation and trade-off lines, the proving page and why — never a palette, pairing or signature, which the live skill withholds before the pick — then ask the pick as the live skill asks it |
| Install, run, verify | State `would run:` in one line and move on |
| Ask a question | **Ask it, for real**, through AskUserQuestion, with the options the skill's own rule produces for this target, labels in the user's words, one marked as the skill marks it |

## 4 — After every answer

One block, short, before the next question:

- **Decision recorded** — what the answer becomes: a `DESIGN.md` line, a decision record, an install line, an anchor, a switch, a `[needs verification]`
- **Switched on / off** — every step, dialog, or check this answer turns on or off, with the condition named as the skill names it
- **Next** — where the flow goes, and why
- **Not fired** — conditionals of this step the target did not trip, with the fact that kept each off, in one line

**Options are invented per target under the skill's own rules** — reference products for this app, engine dialogs only where a trigger fired, frame candidates composed from the direction answer, each naming its source. A simulation that reuses an earlier run's options has tested nothing.

## 5 — The close: did the answers land

At the end, one table: **question · your answer · decision recorded · where it lands**. Then the check the whole run exists for:

- **Matches** — the decision says what the answer meant.
- **Mismatch** — the answer meant one thing and the rule recorded another; the rule is quoted and the gap named. *You ticked a direction but did not stress it, and the canvas was not measured against it — that is the rule, not an error.* *You answered "no charts" and an engine line still appeared — that is a finding.*
- **Undecided** — answers the flow never read, and facts the flow needed that no answer or source supplied.

Findings about the skill itself — a step reference that resolves nowhere, a condition with no behavior, a question with no recommendation, two rules that contradict on this target — are listed apart, each quoting the rule. **No patching**: a change here reaches every app repo on the next version bump, and it is the user's call after reading.

Three lines close the output: what a live run would additionally need (installs, credentials, capture tooling, a committed base, a non-`main` branch) · what could not be simulated (pixels, live verification) · that a live run invents different taste options — the shape was tested, not the content.

## 6 — Self-run: the brief answers

The user asks for a run they do not answer → this section replaces every AskUserQuestion and every chat stop above; sections 2 to 5 hold as written.

**The session launches and relays; it never reads the skill.** One background subagent per scenario, on a cheaper model than the session's (`sonnet` on Claude Code), handed this file's path, the skill, the target, and the switches to trip where the user named any. No subagent → run it here and say so.

The subagent, in this order:

1. **Writes the brief before opening the skill** — who the person is, the kind of app, and what they want from it in five to eight plain sentences: from the scenario's words, from a repo target's `README.md` alone, or invented where there is no target. No sentence uses the skill's words, describes the repo state, or serves a switch handed over — because a want written after the rule is read bends to the rule.
2. Reads what section 2 names, then fixes the repo state around the brief's app: the target's own, or with no target one that trips the switches handed over, else the one *Proposed scenarios* would recommend, counting what `docs/queue.md` names as not exercised. A fact no target supplies is fixed now where the skill's first step reads it and chosen at its own step where a later one does, each marked `assumed`.
3. Prints each question as it would be asked — text, options, the marked one — then the answer and the brief's sentence that gives it; an answer no option holds goes under `Other`, in the brief's words. No sentence gives it → `brief silent`, and the marked option is taken; none marked → the first; a chat stop → approval; a question with no options → no answer, and what it would fill stays `[needs verification]`. A cancellable line is cancelled only where a sentence of the brief contradicts it.
4. Trips a switch handed over by the repo state where state trips it, by the answer where an answer does — given in the call, never as an invocation argument unless handed over as one — printed `aimed`.
5. Adds one line to section 4's block, **Uncovered**: each reply the question's options or its chat stop allow — ticks that conflict, a blanket option ticked beside others, a partial approval, a refusal — that the step's rules give no behavior for; never free text where options are offered, and none listed twice. Each is a finding; none is taken.
6. Checks section 5's `Mismatch` against the brief alone, never against why it picked: a line the skill answered itself is judged like an answer, an `aimed` answer is not.

Nothing is written here either: the report is the subagent's last message. Before relaying it, the session greps every rule a finding quotes and drops the finding whose quote is not in the file.

The close gains a fourth line: the answerer had read the rule, so a question a person would misread was not found.
