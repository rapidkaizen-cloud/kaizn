# Install

Two commands in Claude Code, one setting, and a restart. For Antigravity, see [Run on Antigravity](../guide/antigravity.md).

## Before you start

| Needs | Why |
|---|---|
| Claude Code | The host the commands below are typed into |
| `python3` | Every `kaizn` hook calls it. With only `python` on the machine the guards silently never run |
| Node.js | The companion skills install through `npx` |

## Install the plugin

```
/plugin marketplace add rapidkaizen-cloud/kaizn
/plugin install kaizn@kaizn
```

1. **Install at user scope only.** A project-scope entry updates separately and falls behind.
2. **Choose the output folder, or leave it empty.** Claude Code asks for **Output folder**: where sessions write the reports and files they make for you, one folder per repo and per worktree inside it. Empty means `Downloads/Claude` in your home folder; change it later in `/config`. See [guard-output](../reference/guard-output.md).
3. **Turn on `autoUpdate`.** In `~/.claude/settings.json`, set `"autoUpdate": true` on `kaizn` under `extraKnownMarketplaces`, so a new version reaches the machine at its next start.
4. **Restart Claude Code.**

Nothing else is asked: every rule starts `on`. The first session ends its first answer with one line naming `/kaizn:norms-config`, and a guard that refuses tells the session it can be switched; see [norms-config](../reference/norms-config.md).

## Companion skills

Required. A session missing any of them asks before continuing.

| Skill | Install | What it is for |
|---|---|---|
| `impeccable` | `npx impeccable install` | The craft rules a session reads before it writes any component, and the detector `design-settle` runs on each round |
| `frontend-design` | `/plugin` | Craft rules read before any component, beside `impeccable`'s |
| `ui-ux-pro-max` | `/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill`, then `/plugin install ui-ux-pro-max@ui-ux-pro-max-skill` | The UX floor level with `impeccable`, and the style, palette and type results `design-settle` mixes into its frames |

> [!NOTE]
> Invoke `/design-settle` by name: `impeccable`'s description overlaps it. `ui-build` forbids `ui-ux-pro-max`'s `--persist` and every script of its sub-skills.

Optional, never asked for when absent:

- **`review-animations`** — the motion floor on web Surfaces. Installed alone: `npx skills add emilkowalski/skills --skill review-animations -g -a claude-code`.
- **`apple-design`** — Apple's guideline pages `design-settle` reads for a macOS Surface: `npx skills add dickwu/apple-design-skill --skill apple-design -g -a claude-code --copy`. Then add `disable-model-invocation: true` to the frontmatter of `~/.claude/skills/apple-design/SKILL.md`: its description matches any design review, and it must never load as a reviewer. `npx skills update` drops the line; add it again.

Recommended: `npx skills add supabase/agent-skills` (Postgres guidance for `db-ops`) and `ponytail`.

> [!WARNING]
> Do not install the `supabase` plugin: it adds a second Supabase MCP server. Connect the Supabase MCP once at user scope, with no query parameters in its URL.

## Two conventions every app inherits

- **An agent account.** Sessions sign in and seed test data through it. `db-ops` creates it by SQL on Supabase Auth, taking its email and password from the session's own instructions — your `~/.claude/CLAUDE.md`, for example. The toolkit stores neither.
- **The `[CLAUDE]` prefix.** Every row a session creates for a test opens with it. Only a `DELETE` narrowed to that prefix passes `guard_destructive` unguarded; any other delete goes through the [destructive gate](../concepts/gates.md).

## Check that it loaded

- `/plugin` lists `kaizn`.
- `/kaizn:norms-help` prints the running version, the commands and the last change, in any session.
- `design-settle` prints the running build as `Skill build` in its Step 0 block.

## Next

- [Quickstart](quickstart.md) — the first run.
- [Update the plugin](../guide/update.md) — on a machine without `autoUpdate`.
