# Commands

What to run in which situation. Five skills have a command; the rest load by themselves.

| Situation | Run |
|---|---|
| New app, empty directory | `/raizen-norms:app-settle`, then in the new repo `/raizen-norms:logic-settle` and `/raizen-norms:design-settle` |
| Running app | `/raizen-norms:app-settle` — it reads the repo and runs the one mode it owes next: documents it, migrates a root `PRD.md` to `docs/`, then audits the code against the rules and fixes what you pick, one finding per commit. Ask it for a change and it reworks the decisions instead. Then the other two |
| Only the look or the logic layer | `/raizen-norms:design-settle` or `/raizen-norms:logic-settle` alone |
| Which command to run, what version this is, what changed | `/raizen-norms:norms-help`, or ask in your own words |
| A norm, a guard or a reminder turned off, to advice only, or back on | `/raizen-norms:norms-config`, or ask in your own words |

`design-settle` asks Fast or Full with its first question, on a new app and a redesign alike. Fast answers every design dialog with its recommendation in one block you cancel line by line; the frames, the pick, the gate and every check run as in Full. `/raizen-norms:design-settle fast` skips the question.

## No command needed

| Skill | Loads when a session |
|---|---|
| `build-flow` | Starts a page or a feature, or decides what to build next — in every app session |
| `docs-format` | Writes, edits or proposes a change to a document of the app |
| `ui-build` | Creates or edits a component, touches a styling value, or writes user-facing text |
| `db-ops` | Writes SQL, alters a table, changes an RLS policy, or runs a `DELETE`, `DROP`, `TRUNCATE` or `UPDATE` |
| `logic-build` | Writes a query, a server action, a route handler, an edge function, or an environment variable |

## Things you never type

A session never hands you a command to run. Updating the plugin, committing, pushing, running a migration: ask for it, and the session runs it — after your reply, where it is a [gate](../concepts/gates.md).
