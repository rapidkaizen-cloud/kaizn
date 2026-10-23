# How it works

Settle, then hold: three interviews decide what is yours to decide, and everything else keeps later sessions to the answers.

## Settle — decided with you, once per layer

| Skill | Settles | Run it |
|---|---|---|
| [`app-settle`](../reference/app-settle.md) | The problem domain, the stack, the documents that record them — and existing code brought back onto the installed rules | First, in an empty directory or in a running app |
| [`logic-settle`](../reference/logic-settle.md) | The layer between database and UI: server-state cache, boundary validator, date handling, error reporting, scheduled jobs, change attribution, the one folder every database call lives in, and the lint floor that holds the layer there | After `app-settle`, before `design-settle` |
| [`design-settle`](../reference/design-settle.md) | The visual direction and the component library, written into `DESIGN.md` | Before the first UI component is written, and whenever you want a redesign |

A settle skill runs only when you invoke it. Each answer you give is written into the repo; a decision is recorded once under `docs/decisions/` and never edited afterwards.

## Hold — every session after

| What holds | How |
|---|---|
| [Session norms](session-norms.md) | Printed at every session start, the same text in every repo |
| The app's documents | `docs/README.md`, `docs/product.md` and `docs/queue.md` are printed at every session start, so a session reads them without being told. One too long to fit is named there instead, with an order to read it |
| Rule skills | `build-flow`, `docs-format`, `ui-build`, `db-ops` and `logic-build` load by their descriptions when the work touches what they govern |
| Hooks | Stand in front of the commands that cannot be taken back, and refuse or hold them whatever the session intends. See [Gates](gates.md) |

Each block of the norms, each guard and each reminder can be switched to advice or off, for every repo at once: see [norms-config](../reference/norms-config.md).

## What loads when

| Part | Loaded |
|---|---|
| `app-settle`, `logic-settle`, `design-settle` | When invoked |
| `build-flow`, `docs-format`, `ui-build`, `db-ops`, `logic-build` | By their descriptions |
| `norms-help` | When asked for help, which command to run, the version, or what changed |
| `norms-config` | When asked to switch a norm, a guard or a reminder on, to advice, or off |
| Session norms, guard hooks | Every session where the plugin is enabled — installed at user scope, that is every folder on the machine. `app-settle` writes the `enabledPlugins` line into each app repo |

## A repo that was never settled

A repo with neither a root `PRD.md` nor `docs/PRD.md` has never been through `app-settle`, and the documents the build skills measure code against do not exist. Its sessions get the norms in their `NOT SETTLED` form:

- **`build-flow` and `docs-format` do not apply.** There is no queue to build from and no document list to keep.
- **`ui-build`, `db-ops` and `logic-build` still apply**, without the rules that read `docs/` or `DESIGN.md`.
- **UI is built only from the components and tokens the repo already has**, and no new styling value is written. A repo with no UI yet is not bound by this.
- **The session says once**, when the work is done, that `app-settle` has not run there.

## Related

- [Overview](../start/overview.md)
- [Documents](documents.md) — what an app repo keeps, and what gets it written.
- [session-start](../reference/session-start.md) — exactly what is printed, and when.
