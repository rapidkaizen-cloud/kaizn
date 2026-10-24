# Start a new app

From an empty directory to the first page built, in three interviews and one request.

Before you start: the plugin and its [companion skills](../start/install.md) are installed, and a browser MCP server is connected — `design-settle` uses it for every screenshot and browser check.

## Steps

1. **Open Claude Code in an empty directory.**
2. **Run `/kaizn:app-settle`.** It reads the directory and reports the mode it found: empty means bootstrap. It interviews you about the problem domain and the stack, writes the documents, scaffolds the app and runs `git init`. See [app-settle](../reference/app-settle.md).
3. **Open the new repo and run `/kaizn:logic-settle`.** It settles the layer between the database and the UI, and the one folder every database call lives in. See [logic-settle](../reference/logic-settle.md).
4. **Run `/kaizn:design-settle`.** Its first question asks Fast or Full. It then draws two to four direction frames, you pick one on screen, and it builds a canvas of every page that you approve once. `/kaizn:design-settle fast` skips the first question. See [design-settle](../reference/design-settle.md).
5. **Ask for the first page.** `build-flow` loads by itself and builds from `docs/queue.md`. A finished page is committed in the same turn and reported with its route. See [build-flow](../reference/build-flow.md).
6. **Reply when it asks to publish.** A push waits for your answer in chat. See [Gates](../concepts/gates.md).

> [!NOTE]
> `logic-settle` and `design-settle` each commit what they wrote when they close. One that stopped before its close leaves the working tree dirty, and `app-settle`'s migrate and align modes stop on a tree that is not clean.

## What the repo holds afterwards

| File | Holds |
|---|---|
| `docs/` | The app's documents, for the developer and the agent: the index, the product, the rules, the glossary, the architecture map, the runbook, the changelog, the queue, one record per decision |
| `DESIGN.md` | The design system — written by `design-settle` alone |
| `README.md` | What the app is and how to run it |
| `CLAUDE.md`, `AGENTS.md` | Instructions for agents; they record nothing about the app |

The full list, and what gets each one written: [Documents](../concepts/documents.md).

## If something goes wrong

- **The directory is not empty, but holds no application code and no PRD** — a stray `README`, a `.git` and nothing else. `app-settle` stops and asks whether to continue there or move. It overwrites nothing.
- **The branch is `main`.** A session never works on `main`. Where no `development` branch exists, `app-settle` offers to create it from `main` and switch to it.
- **A companion skill is missing.** The session asks before continuing, and names what is lost without it.

## Related

- [Quickstart](../start/quickstart.md)
- [Bring in an existing app](existing-app.md)
