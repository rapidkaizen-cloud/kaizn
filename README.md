# kaizn

`kaizn` is a plugin for Claude Code and Antigravity. Three interview skills decide with you an app's scope and stack, its logic layer and its look, and write the answers into the repo; rule skills, session norms and guard hooks hold every later session to those answers.

The name is *kaizen*, Japanese for continuous improvement, without its `e`: every command below spells it `kaizn`.

## Install

Claude Code:

```
/plugin marketplace add rapidkaizen-cloud/kaizn
/plugin install kaizn@kaizn
```

Antigravity:

```
agy plugin install https://github.com/rapidkaizen-cloud/kaizn
```

Requirements and companion skills: [Claude Code](docs/start/install.md), [Antigravity](docs/guide/antigravity.md).

## Use

In an empty folder, run `/kaizn:app-settle`, then `/kaizn:logic-settle` and `/kaizn:design-settle` in the repo it creates. After that, ask for a page; the rule skills load by themselves.

An app that already exists: [Quickstart](docs/start/quickstart.md). Every command: [Commands](docs/reference/commands.md).

## Documentation

<https://rapidkaizen-cloud.github.io/kaizn/>, or the same pages under [`docs/`](docs/README.md). What changed: [CHANGELOG.md](CHANGELOG.md). In a session: `/kaizn:norms-help`.
