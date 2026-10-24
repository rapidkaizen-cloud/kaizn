# Update the plugin

A new version reaches a session only after the machine has pulled it and the host has restarted.

## On Claude Code

- **With `autoUpdate` on**, the machine picks up a new version at its next start. Nothing else is needed. The setting is described in [Install](../start/install.md).
- **Without it**, ask a session to update the plugin, or run:

  ```
  claude plugin marketplace update kaizn
  claude plugin update kaizn@kaizn
  ```

Then restart Claude Code. Nothing reaches a session before the restart.

## On Antigravity

```
agy plugin uninstall kaizn
agy plugin install https://github.com/rapidkaizen-cloud/kaizn
```

The install is a copy, and nothing refreshes it.

## Moving from raizen-norms

Until 0.106.0 the plugin was `raizen-norms`, from the marketplace `raizen`. An update in place keeps the marketplace under its old name, so move once instead:

1. **Remove the old marketplace:** `claude plugin marketplace remove raizen`. It uninstalls `raizen-norms` with it.
2. **Add the new one and install:** `claude plugin marketplace add rapidkaizen-cloud/kaizn`, then `claude plugin install kaizn@kaizn`.
3. **Turn `autoUpdate` back on**, for `kaizn` this time, as in [Install](../start/install.md). The old entry's setting left with it.
4. **In every app repo whose `.claude/settings.json` names `raizen-norms@raizen`**, change the key to `kaizn@kaizn` and commit it, so a teammate's machine enables the plugin there too.
5. **On Antigravity:** `agy plugin uninstall raizen-norms`, then install from the new URL as above.

Then restart the host.

## Check what you are running

1. **Run `/kaizn:norms-help`** in any session. The first line is the version of the copy that session loaded.
2. **Read `LAST CHANGE` on the same card**: the newest changelog entry, with its `To act on` lines — what an installed app must do because of that version.
3. **For older versions**, open `CHANGELOG.md` at the repo root.

> [!NOTE]
> `norms-help` reports the copy the session runs, not the newest one on the machine. A plugin installed at project scope updates separately from the user-scope one and falls behind — install at user scope only.

## If you change the plugin yourself

- **Every commit that changes the plugin bumps its version**, because the update compares version numbers only. `.githooks/pre-commit` refuses the commit otherwise: run `git config core.hooksPath .githooks` once per clone.
- **A version bump carries its `CHANGELOG.md` entry** in the same commit.
- **A commit reaches app sessions only after it is pushed.**

## Related

- [norms-help](../reference/norms-help.md)
- [Hosts](../concepts/hosts.md)
