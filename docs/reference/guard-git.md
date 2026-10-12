# guard-git

Holds `git push`, `gh pr create` and `gh pr merge` until you reply in chat, and refuses a bare force push, a commit on `main` and `git add -A`.

| | |
|---|---|
| Kind | Hook — runs by itself; it cannot ask, only pass, refuse, or print |
| Runs on Claude Code | `PreToolUse`, matcher `Bash\|PowerShell` |
| Runs on Antigravity | `PreToolUse`, matcher `run_command` |
| Script | `scripts/guard_git.py` |
| Self-check | `scripts/test_guard_git.py` |

## What it does

It reads each shell command before it runs and ends in one of three ways: pass, `REFUSED:` or `HELD:`. The word opens the message the session reads.

- **A refusal has no reply that lets it through.** The session fixes the command itself.
- **A hold waits for your reply in chat.** The session ends its turn on the exact command and the commits it publishes, then runs it only on a clear yes. The full stop is in [Gates](../concepts/gates.md).
- **Quoted text is data.** A commit message or a heredoc body that mentions `gh pr create` or `git push --force` is not a call.
- **Options before the subcommand do not shake it off.** `git -c k=v push`, `git -C dir commit` and `git --no-pager push` are read like the bare spelling.

The rule behind it is the `GIT` block of the norms; see [session-start](session-start.md).

## What it refuses or holds

| Case | What happens | What lets it through |
|---|---|---|
| `git add` with `-A`, `--all`, `.` or `./` anywhere among its arguments — `git add src -A` and `git add -- .` included | `REFUSED: git add -A / git add . is not used in this repo.` | Naming the paths: `git add src/app/orders/page.tsx` |
| `git push` with `--force`, `-f` or a `+` refspec such as `+main` among its own arguments, a continued line included | `REFUSED: a bare force push.` | `--force-with-lease`, which is held like any push |
| `git commit` while HEAD is on `main`, in a repo that has a `development` branch, local or on `origin` | `REFUSED: HEAD is on main.` | Switching to `development` first |
| `git push`, `--force-with-lease` included | `HELD: a push runs only on the user's yes in chat.` | Your reply |
| `gh pr create`, `gh pr merge` | `HELD: opening or merging a pull request runs only on the user's yes in chat.` | Your reply |

A held command passes only when all four hold, read from the conversation's transcript:

1. The session's last message before your reply puts the exact command on a line of its own in backticks, or alone in a fenced block. A multi-line command can only go in a fence.
2. You typed a reply to that message, with text in it.
3. Nothing else was typed after it.
4. The command has not already run on that reply.

How the four are read:

- **The command must match.** Whitespace is collapsed, nothing else. Another branch is another command and needs its own message and reply.
- **A push the call adds to is another command.** `cd app && git push origin dev`, a pipe to `tail` or a `2>&1` after it does not match a message naming `git push origin dev`. The hold tells the session to name the push and run it alone.
- **One reply, one run.** A call of the command in either shell spends the reply once its result is in the transcript. Another message and reply grant one more run. A held attempt made before your reply spends nothing.
- **Several commands, one message.** A message that puts a push and a `gh pr create`, each on a line of its own or in a fence of its own, lets each run once on the one reply, and the run of one spends nothing of the other. Two commands sharing one fence are neither of them put. Which of them your reply covered is read by the session, not by the hook.
- **Things you did not type are ignored.** A tool result, a subagent's prompt or a note written by the host neither grants nor takes a reply back. On Antigravity only a step the user typed counts.
- **A dialog pick is no reply.** `Run` picked on a question dialog does not count.
- **A transcript that cannot be read holds the command.**

## What it lets through

- **Everyday git and gh.** `git add` with named paths, `git commit -m '...' -- <path>`, `git status`, `git fetch`, `gh pr view`, `gh release list`.
- **A commit on `main` in a repo with no `development` branch.** Refusing there would leave the session nowhere to commit.
- **A `+` inside a branch name.** `git push origin feature+search` is held, not refused as a force.
- **A flag that belongs to a later command.** `git push origin dev && rm -f x` is held as a push, not refused as a force.
- **Paths that only open like `.`.** `.gitignore` and `./src/a.ts` are named paths.
- **Commands with no `git` or `gh` in them,** such as `npm run dev`.

## What it does not reach

- **A command inside quotes.** `sh -c 'git push'` hides from it, because quoted text is blanked before any rule reads the command.
- **The meaning of your reply.** It proves the stop happened and that you replied; the session reads the words. See [Gates](../concepts/gates.md).
- **Who typed a reply is inferred on Claude Code.** Every user entry that is not a tool result, a subagent prompt or a host note is taken as typed by you. A prompt a host writes on its own would read as yours.
- **On Antigravity a result is paired to its call by position,** which holds while a step carries one call.
- **Only the shell tools are read.** The hook is wired to `Bash` and `PowerShell` on Claude Code and to `run_command` on Antigravity.

## Related

- [Gates](../concepts/gates.md) — the publishing stop as you meet it
- [session-start](session-start.md) — where the `GIT` block is printed
- [Hosts](../concepts/hosts.md) — what differs between Claude Code and Antigravity
