# Run on a Pro plan

Four settings of your own machine that decide how many 5-hour windows a `design-settle` run takes on a Pro plan; `kaizn` can change none of them for you.

One redesign of the proof app took 8 windows of a Pro plan: about $182 at API prices, a window running out at $12–23. These steps cut what every call carries before `kaizn` adds anything.

## Steps

1. **Measure what a session starts with.** Open a new session in the app repo and run `/context`. In the proof app every call started at 56k–67k tokens before any work: the system prompt, the skill listing, the tool definitions of every MCP server and the session-start hooks. `kaizn`'s own part was under 5k. Aim for about 30k.
2. **Turn off what that repo does not use.** Plugins in `/plugin`, MCP servers in `/mcp`. A server's tool definitions ride every call, used or not; one reverse-engineering server alone carried about 200 tools there. The connectors of your claude.ai account load into Claude Code too: set `"ENABLE_CLAUDEAI_MCP_SERVERS": "false"` under `env` in `~/.claude/settings.json` to keep them out, and remove the line when a session needs one.
3. **Turn off ECC's GateGuard**, where the `ecc` plugin is installed: set `"ECC_GATEGUARD": "off"` under `env` in `~/.claude/settings.json`. In the proof app it refused 172 writes and commands over 11 sessions, each refusal one more call at the full context, and every refused file was written again. You lose its read-before-you-write reminder; `kaizn`'s own guards keep running.
4. **Run no other session on the same account during a redesign.** Every session, every machine and claude.ai draw on the same window: in the proof app other work used part of the windows the redesign ran out of.
5. **Read the quota.** `design-settle` prints it at Step 0 and at its close, on Claude Code. Any other time: `claude -p "/usage"`. It shows the window and the week as a percent, and what drove them on this machine — the share used above 150k tokens of context, with several sessions running at once, and by each skill, plugin and MCP server. It does not count other machines or claude.ai.

## Related

- [Redesign the look](redesign.md) — the run these steps prepare.
- [context-reminder](../reference/context-reminder.md) — the note that offers a new session as the context grows.
