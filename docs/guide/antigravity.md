# Run on Antigravity

One command in a terminal, once per machine, and every folder `agy` opens runs under the norms and the guards. For Claude Code, see [Install](../start/install.md).

## Before you start

| Needs | Why |
|---|---|
| The Antigravity CLI, `agy` | The host the command below is typed into. The IDE and Antigravity 2.0 are not verified: see [What is proven](../reference/status.md) |
| `python3` | Every `kaizn` hook calls it. There, a hook that cannot start blocks every command |

## Install the plugin

```
agy plugin install https://github.com/rapidkaizen-cloud/kaizn
```

The copy lands in `~/.gemini/config/plugins/kaizn`.

> [!WARNING]
> - **Install it for the machine, never through a repo's `.agents/plugins.json`.** Registered per folder, the plugin loaded a minute after an interactive conversation began, and that conversation ran unguarded.
> - **Never run `agy plugin import` on this plugin.** It replaces `hooks.json` with Claude Code's, which Antigravity cannot parse, and every guard goes silent.

## Companion skills

Required: the same three as on Claude Code, where [Install](../start/install.md) says what each is for. A session missing one asks before continuing.

| Skill | Install |
|---|---|
| `impeccable` | Copy the folder that holds its `SKILL.md` to `~/.gemini/config/skills/impeccable/` |
| `frontend-design` | Nothing on a machine with Claude Code: the `HOST` block sends the session to Claude Code's own copy, as current as Claude Code keeps it. Without Claude Code, copy its folder to `~/.gemini/config/skills/frontend-design/` |
| `ui-ux-pro-max` | Copy the folder that holds its `SKILL.md` to `~/.gemini/config/skills/ui-ux-pro-max/` |

> [!NOTE]
> A skill is found only as a folder of its own under `~/.gemini/config/skills/`. Under `~/.gemini/antigravity-cli/skills/`, or as a link to a folder elsewhere, it is never listed.

`design-settle` also needs a browser MCP server, for every screenshot and browser check. Absent, it asks.

## Check that it loaded

- `agy plugin list` names `kaizn`, with `skills` and `hooks` as its components.

## Update

```
agy plugin uninstall kaizn
agy plugin install https://github.com/rapidkaizen-cloud/kaizn
```

The install is a copy, and nothing refreshes it.

## Headless runs

A headless run (`agy -p`) cannot be asked for permission, and a skill file sits outside the workspace.

1. **Allow the plugin folder to be read**, in `~/.gemini/antigravity-cli/settings.json`, or the run stops at the first skill it reads:

   ```json
   {"permissions": {"allow": ["read_file(C:/Users/<you>/.gemini/config/plugins/kaizn)"]}}
   ```

2. **For a headless `design-settle` run, allow all of these**, or the turn ends with no output at the first one missing:

   | Permission | On |
   |---|---|
   | `read_file` | The plugin, the skills folder, Claude Code's `frontend-design` folder, the repo |
   | `write_file` | The repo |
   | `command(*)` | Every command — `command(git)` does not cover `git status` |
   | `read_url(*)` | Every URL |
   | `mcp(<browser server>/*)` | The browser MCP server |
   | `execute_url(*)` | The browser opening a page |

3. **Refuse what must never run through `deny`**, which does not end the turn.
4. **Continue the conversation with `--conversation <id>`.** A dev server started in a headless turn dies when the turn ends.

## Related

- [Hosts](../concepts/hosts.md) — what differs from Claude Code, and switching hosts mid-work.
- [What is proven](../reference/status.md) — what has run for real on Antigravity.
