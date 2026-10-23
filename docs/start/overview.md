# Overview

`raizen-norms` is one plugin, for Claude Code and for Antigravity, that settles an app one layer at a time and then holds every later session to what was settled.

It has two halves. The settle skills are interviews: they decide with you what is yours to decide and write the answers into the repo. Everything else — the rule skills, the session norms, the hooks — keeps the sessions that build afterwards to those answers.

## The five parts

| Part | What it does | When it runs |
|---|---|---|
| Three settle skills — `app-settle`, `logic-settle`, `design-settle` | Decide the problem domain, the stack and the documents; the layer between database and UI; the visual direction and `DESIGN.md` | When you invoke one |
| Five rule skills — `build-flow`, `docs-format`, `ui-build`, `db-ops`, `logic-build` | Hold a building session to the build order and to the document, UI, database and logic rules | By themselves, when the work matches their description |
| Session norms | Language, scope, git, asking, decisions and the closing report — the same text in every repo | At every session start |
| Guard hooks | Refuse or hold what must not happen unasked: publishing, destructive SQL, a Supabase call aimed at another project | Before every shell command and every MCP call |
| `norms-help`, `norms-config` | The commands, these pages, the version and its last change; each norm, guard and reminder switched on, to advice, or off | When you ask |

## How a repo moves through it

1. **Settle, once per layer.** `app-settle` first, then `logic-settle`, then `design-settle`. Each one interviews you, records every answer as a decision, and writes what the next sessions read.
2. **Build, every session after.** You ask for a page; `build-flow` loads by itself and builds from the queue in `docs/queue.md`. The rule skills load when the work touches what they govern, and the hooks stand in front of the commands that cannot be taken back.
3. **Check again, whenever you want.** `app-settle` run on a settled repo audits the code against the rules and fixes what you pick, one finding per commit.

## A repo that was never settled

The plugin is installed for the whole machine, so its norms reach repos no settle skill has touched. A repo with no PRD in either form gets the norms in their `NOT SETTLED` form: no document gate, and UI built only from the components and tokens the repo already has. See [How it works](../concepts/how-it-works.md).

## Next

- [Install](install.md) — the two commands and the companion skills.
- [Quickstart](quickstart.md) — the first run on a new app or an existing one.
- [Commands](../reference/commands.md) — what to run in which situation.
