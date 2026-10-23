# norms-config

Switch each block of the session norms, each guard and each reminder on, to advice, or off, for every repo on the machine, by answering a few questions in chat.

| | |
|---|---|
| Kind | Settings skill — runs when you ask |
| Run | `/raizen-norms:norms-config`, or ask in your own words: turn the git guard off, make the scope norm advice only, which rules are switched |
| Changes | This plugin's options under `pluginConfigs` in `~/.claude/settings.json`, and nothing else in that file |
| Source | `skills/norms-config/SKILL.md`, `scripts/norms_config.py`, `scripts/switches.py` |
| Self-check | `scripts/test_norms_config.py` |

Without it you would have to know each option's key and set it in `/config` by hand, with no word on what each rule does.

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

In sessions started after the change. The session that made it keeps the switches it started with.

## What you can rely on

- **A switch holds in every repo.** There is no switch per repo, except `.claude/destructive-gate.off`, which still turns [guard-destructive](guard-destructive.md) off in its repo whatever `guard_destructive` says.
- **A block and its guard switch apart.** `norm_git` off leaves `guard_git` refusing and holding; `guard_git` off leaves the `GIT` block telling the session to stop before a push. The same holds for `norm_output` and `guard_output`.
- **Only what you named is written.** Every other key of `settings.json` stays as it was, in its order, with its indent and its line endings — the output folder among them. An unknown switch or a mode it does not take is refused, and nothing is written.
- **The plugin is found by its id in the file**, `raizen-norms@<marketplace>`, not by a fixed marketplace name. A machine where the plugin is not enabled at user scope is refused.
- **The same switches are rows in `/config`.** You can set them there as well, and Claude Code asks for them when the plugin is enabled.
- **The rules inside the skills are not switched here**: `build-flow`, `docs-format`, `ui-build`, `db-ops` and `logic-build` hold as they are.
- **On Antigravity every rule is `on`.** That host has no plugin settings, and the skill writes nothing there.
- **It needs Claude Code 2.1.271 or later.** The switches are pickers, which an earlier version cannot load; see [Install](../start/install.md).

## Related

- [Session norms](../concepts/session-norms.md) — what each block says
- [Gates](../concepts/gates.md) — the stops the guards enforce
- [Commands](commands.md)
