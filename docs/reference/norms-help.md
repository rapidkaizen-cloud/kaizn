# norms-help

Ask any session for help with these skills, and get one card: the version, the commands, these pages, and the last change.

| | |
|---|---|
| Kind | Help skill — runs when you ask |
| Run | `/kaizn:norms-help`, or ask in your own words: which command to run, what version this is, what changed |
| Changes | Nothing |
| Source | `skills/norms-help/SKILL.md`, `scripts/norms_help.py` |

## The card

It is printed in your language. Commands, file names and the version number stay as written.

| Part | Holds | Taken from |
|---|---|---|
| Version | The number of the copy this session runs | The plugin's manifest |
| Commands | What to run in which situation, and which skills need no command | `docs/reference/commands.md` |
| Pages | Every page of these docs, and what it holds | `docs/README.md` |
| Last change | The newest changelog entry, with what it asks you to act on | `CHANGELOG.md` |

Nothing on the card is written for the card alone: each part is printed as its file holds it, so the card cannot disagree with these pages.

## Asking a question with it

Ask "how does the push stop work" and the session answers from the page that covers it, and names the file. Where no page does, it answers from the skill itself and says that no page does. Where neither covers it, it says so.

## What you can rely on

- **The version is its number and that one changelog entry.** Whether a newer version exists is not checked. [Update the plugin](../guide/update.md) says how a newer one arrives.
- **The card is about the copy the session loaded**, not the newest one on the machine. A machine keeps one folder per installed version, and the newest is not always the one a session loaded.
- **Nothing is changed.** A `To act on` line is shown word for word, and acted on only when you ask.

## Related

- [Commands](commands.md)
- [Update the plugin](../guide/update.md)
