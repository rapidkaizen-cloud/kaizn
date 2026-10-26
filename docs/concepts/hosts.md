# Hosts — Claude Code and Antigravity

The repo root is the plugin for both hosts: the same skills, the same norms, the same guards.

Each host reads its own manifest and its own hook file. `.claude-plugin/` and `hooks/` are Claude Code's; `plugin.json` and `hooks.json` at the root are Antigravity's.

## What differs

| | Claude Code | Antigravity |
|---|---|---|
| Install | `/plugin marketplace add`, then `/plugin install` — see [Install](../start/install.md) | `agy plugin install <repo URL>` — see [Run on Antigravity](../guide/antigravity.md) |
| Update | By itself with `autoUpdate`, or two commands | Uninstall, then install again: the install is a copy, and nothing refreshes it |
| Norms and documents | Printed at `SessionStart` | Injected before the first model call of a conversation, with the app's `CLAUDE.md` and a `HOST` block mapping the tool names |
| Where the norms run | Wherever the plugin is enabled | Every folder `agy` opens |
| The document reminder | With the result of a commit that touched no document | Before the model call that follows such a commit, once per commit — a hook there cannot hand the model text after a tool has run |
| The context reminder | At the first commit after the context passes 200k, 500k or 800k tokens | None — a hook there cannot hand the model text after a tool has run |
| A question to you | `AskUserQuestion` | `ask_question` |
| The output folder | Set with `norms-config`, which the first session on a machine runs once | None: never set |
| The [switches](../reference/norms-config.md) | Set with `norms-config`, kept in the plugin's data folder; the first session on a machine runs it once | None: every rule `on` |

## What is the same

- **A held push or merge.** The session ends its turn on the command and its commits, and runs it once when a reply typed in chat is a yes. The guard holds the command until a reply exists; reading it as a yes is the session's.
- **A refusal.** A guard that refuses stops the tool on both hosts.
- **The skills.** They are written in Claude Code's vocabulary; on Antigravity the `HOST` block is the one place the tool names are mapped.

## Switching hosts mid-work

When the working tree is dirty and the other host ran the last session in the repo, the session start prints a hand-over block: that session's last request, the answers you gave, its todo list, and the last thing it said. It is read from the other host's transcript, so it works on the same machine only.

## Related

- [What is proven](../reference/status.md) — what has run for real on each host.
- [session-start](../reference/session-start.md) — the hand-over block and the `HOST` block in detail.
