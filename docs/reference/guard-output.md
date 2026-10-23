# guard-output

Refuses a file written into the root of your output folder, or into a folder there that is not the session's own.

| | |
|---|---|
| Kind | Hook — runs by itself; it cannot ask, only pass, refuse, or print |
| Runs on Claude Code | `PreToolUse`, matcher `Write\|Edit\|MultiEdit\|NotebookEdit`, and again with matchers `Bash\|PowerShell` and `mcp__.*` |
| Runs on Antigravity | `PreToolUse`, matcher `run_command`, and again with matcher `call_mcp_tool` |
| Script | `scripts/guard_output.py` |
| Self-check | `scripts/test_guard_output.py` |

## The output folder

The reports, spreadsheets, CSVs and PDFs a session makes for you go to one folder, never into the repo, where they dirty `git status`, and never into a scratchpad, where nobody finds them again.

- **You choose it.** Claude Code asks for **Output folder** when the plugin is enabled; change it later in `/config`. Left empty, it is `Downloads/Claude` in your home folder. Antigravity has no plugin settings, so there it is always the default.
- **Each session has a folder of its own inside it**, worked out from where the session runs:

| The session runs in | Its folder |
|---|---|
| A repo's main checkout | `<repo>`, the checkout's folder name |
| A linked worktree | `<repo>-<worktree>`, beside the repo's folder and never inside it. A worktree folder already named `<repo>-...` is used as it is |
| No repo | `_general` |

- **The session is told its folder** in the `OUTPUT` block of the norms, as a full path; see [session-start](session-start.md).

## What it refuses

The message opens `REFUSED: ... is not this session's output folder.`, names the folder to write to, and lists the folders already there.

- **A name straight under the output folder** that is neither a folder already there nor the session's own: a file at the root, or a new folder such as `mockup-x`.
- **From a worktree, a new name inside its repo's folder**: a file there, or a folder named after the worktree.
- **Wherever the call carries the path**: a file path, a shell command, the text of a script being written, an MCP argument such as a screenshot's `filePath`.

## What it lets through

- **A folder already there**, the session's own among them: reading, listing and editing what it holds.
- **`_general`**, from any session.
- **From a worktree, a name its repo's folder already holds**, so what the main checkout wrote can be read.
- **A name that opens with `$`, `%`, `{`, `<` or `*`**: a variable, a placeholder or a glob, which the hook cannot know.
- **A path that only looks alike**, such as a repo under `D:/Codes`.

## What it does not reach

- **A path built at runtime**, such as `Path(out) / "x.xlsx"` or `Join-Path $root $name`.
- **A file written anywhere else** — the repo, a scratchpad. The norms carry that rule; the hook only guards the output folder.
- **Dates in names and overwriting.** The norms carry both; the hook checks neither.
- **A name cut at a space or a bracket**, which is matched by its opening: from a worktree, a new file whose name opens like one already in its repo's folder passes.
- **A folder a session left at the root before the hook existed.** It counts as a folder already there.
- **The same two names elsewhere.** The output folder is recognised by its last two names, such as `Downloads/Claude`, so it is found whichever way a path writes the home folder — and a folder with the same two names under another parent counts too.
- **On Antigravity, the tools that write a file.** Only `run_command` and `call_mcp_tool` are wired.

## Switching it

Set `guard_output` in `/config`, or ask [norms-config](norms-config.md). It holds in every repo.

- **`on`**, the default: as above.
- **`advice`**: nothing is refused. The call runs, and the session is handed what the hook would have said, beside the call's result, with an order to tell you in one line.
- **`off`**: the hook does nothing.

It switches apart from the `OUTPUT` block of the norms: turning one off leaves the other as it is. On Antigravity it is always `on`.

## Related

- [session-start](session-start.md) — the `OUTPUT` block that tells a session its folder
- [Session norms](../concepts/session-norms.md) — what the norms say, in prose
