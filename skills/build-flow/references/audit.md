# The audit — a subagent's brief

You audit the pages one building session built or changed, for that session, which fixes what you find. **Change nothing**: every hit is a finding. Run only the passes your brief names, over the commit range and the routes it gives. Run independent reads, searches and commands in one turn.

## What you report back

Only findings, one per line — `<pass> · <file>:<line> or <route> · <what is wrong>` — and `<pass> : clean` for a pass that found none. No file contents, no narration, no fix.

## The passes

| Pass | What it looks for |
|---|---|
| Accessibility | contrast, visible focus, keyboard reachability, every control paired with a label, images given alternatives — the ratios and the state list are `impeccable`'s craft floor Verify list, loaded per `ui-build`; the touch-target floor is `impeccable`'s too — its audit and adapt playbooks on the web, its iOS and Android references on those platforms — read for the number, never recalled. A surface needing tighter than its platform floor is a `DESIGN.md` line the user ratifies |
| Interaction polish | hover, active, focus, disabled and empty states present; hit area no smaller than the control it belongs to; spacing and radius matching the proving page |
| Click path | per handler — does the final state match what the control's label promises, and does any later call undo what an earlier one just did |
| Platform conventions | the shell affordances this Surface's users expect and no design decision produces — window chrome and menus, context menu and the gesture that opens it, system back, safe areas and insets, file and permission dialogs |

- **Use the skills that cover a pass** — `accessibility`, `make-interfaces-feel-better`, `click-path-audit` in the `ecc` plugin. Without them the rows above are the whole checklist: the audit never depends on a plugin being installed.
- **Open the browser as `SKILL.md` Section 5 drives every browser step.**
- **No browser tooling, or no dev server address in your brief → say so in the report and judge from the source.**
