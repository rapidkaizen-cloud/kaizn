# norms-config

Switch each block of the session norms, each guard and each reminder on, to advice, or off, for every repo on the machine, by answering a few questions in chat.

| | |
|---|---|
| Kind | Settings skill — runs when you ask |
| Run | `/kaizn:norms-config`, or ask in your own words: turn the git guard off, make the scope norm advice only, which rules are switched |
| Changes | `switches.json` in the plugin's data folder, `~/.claude/plugins/data/<id>/`, and nothing else |
| Source | `skills/norms-config/SKILL.md`, `scripts/norms_config.py`, `scripts/switches.py` |
| Self-check | `scripts/test_norms_config.py` |

Nothing asks about these rules when you install the plugin, because a rule is hard to judge before you meet it. You meet a guard when it refuses or holds: its message then tells the session that the rule is switchable, and the session tells you once that this skill sets it to `advice` or `off`. The first session on a machine also ends its first answer with one line naming this skill. See [session-start](session-start.md).

## The switches

Every switch starts at `on`, which is the rule as it was before switches existed.

| Switch | Rule | Modes |
|---|---|---|
| `norm_language` | The `LANGUAGE` block | `on`, `advice`, `off` |
| `norm_pointers` | The `POINTERS` block, and `NOT SETTLED` where it stands in its place | `on`, `advice`, `off` |
| `norm_scope` | The `SCOPE` block | `on`, `advice`, `off` |
| `norm_git` | The `GIT` block | `on`, `advice`, `off` |
| `norm_asking` | The `ASKING` block | `on`, `advice`, `off` |
| `norm_decisions` | The `DECISIONS` block | `on`, `advice`, `off` |
| `norm_closing` | The `CLOSING THE SESSION` block | `on`, `advice`, `off` |
| `norm_output` | The `OUTPUT` block | `on`, `advice`, `off` |
| `guard_git` | [guard-git](guard-git.md) | `on`, `advice`, `off` |
| `guard_destructive` | [guard-destructive](guard-destructive.md) | `on`, `advice`, `off` |
| `guard_output` | [guard-output](guard-output.md) | `on`, `advice`, `off` |
| `remind_docs` | [document-reminder](document-reminder.md) | `on`, `off` |
| `remind_context` | [context-reminder](context-reminder.md) | `on`, `off` |

## What each mode does

| | `on` | `advice` | `off` |
|---|---|---|---|
| A block of the norms | Printed, and binding | Printed, with `Advice only: the user has not made this block binding - weigh it.` under its heading | Not printed |
| A guard | Refuses or holds, as its page says | Lets the call through, and hands the session what it would have said, beside the call's result | Does nothing |
| A reminder | Speaks as its page says | — | Silent |

When any switch is away from `on`, the norms open with one line naming each of them and its mode, such as `SWITCHED by the user, on purpose: norm_git off, guard_git advice.` A session then reads a missing block as your choice, not as a fault. With every switch at `on` the line is not printed and nothing changes. See [session-start](session-start.md).

## How it runs

1. **It shows each switch, its mode now and what it does.**
2. **It asks which to change**, in one call of four questions: the first four blocks, the other four, the guards, the reminders. You can pick more than one in each.
3. **For each block or guard you picked, it asks which mode.** A reminder you picked flips to its other mode.
4. **It writes your answers itself** and says what changed.

A request that names the switch and the mode — "turn `guard_output` off" — is written without the questions.

## When it takes effect

- **A guard or a reminder**: from its next call, in the session that changed it too. A guard reads the file each time it runs.
- **A block of the norms**: from the next session start. The norms are printed once, when a session starts.

## What you can rely on

- **A switch holds in every repo.** There is no switch per repo, except `.claude/destructive-gate.off`, which still turns [guard-destructive](guard-destructive.md) off in its repo whatever `guard_destructive` says.
- **A block and its guard switch apart.** `norm_git` off leaves `guard_git` refusing and holding; `guard_git` off leaves the `GIT` block telling the session to stop before a push. The same holds for `norm_output` and `guard_output`.
- **One file holds every switch.** `switches.json` in the plugin's data folder lists each rule and its mode. Claude Code keeps that folder across plugin updates and deletes it when you uninstall the plugin, which sets every rule back to `on`.
- **What it cannot read counts as `on`**: a missing file, one that is not JSON, or a value a switch does not take. An unknown switch or mode you ask for is refused, and nothing is written.
- **Nothing else is touched.** `~/.claude/settings.json` and the output folder stay as they are; the output folder is the one plugin setting, in `/config`.
- **The rules inside the skills are not switched here**: `build-flow`, `docs-format`, `ui-build`, `db-ops` and `logic-build` hold as they are.
- **On Antigravity every rule is `on`.** That host gives the skill no data folder, so it says switches are not available there and writes nothing.

## Related

- [Session norms](../concepts/session-norms.md) — what each block says
- [Gates](../concepts/gates.md) — the stops the guards enforce
- [Commands](commands.md)
