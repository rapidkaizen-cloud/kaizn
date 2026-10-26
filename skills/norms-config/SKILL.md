---
name: norms-config
description: Switch the kaizn session-norm blocks, guards and reminders on, to advice, or off, and set the output folder, for every repo on this machine — shows each rule, its mode now and what it does, asks which to change, and writes the answers itself. Use when the user wants a norm, a guard or a reminder of these skills turned off, made advisory or back on, asks which ones are switched, or wants the files sessions make for them written to another folder.
---

# norms-config — the switches of the norms and the hooks

**Run `python3 <plugin folder>/scripts/norms_config.py --data "${CLAUDE_PLUGIN_DATA}" show`.** The plugin folder is the one this skill is read from, two levels above this file. It prints, from the one switches file of this machine, each switch's key, its mode now, the modes it takes and what it does, then the output folder now.

**The folder after `--data` above opens with `$` → this host did not fill it in (Antigravity): tell the user in their language that switches are not available on this host, run nothing, and stop.** The script refuses such a folder too.

1. **Show one table in the user's language**: switch, mode now, what it does in one plain line, and `output_dir` last with its folder, or Claude Code's own behaviour where none is set. Keep every key, mode and path as printed.
2. **The request already names the switch and the mode, or the folder → write it** (step 4) without asking.
3. **Otherwise ask through AskUserQuestion, in two rounds.**
   - **Round one**, one call of four multi-select questions, each with "boleh pilih lebih dari satu" in its text, one option per switch, its mode now in the label and what it does in the description: `norm_language`, `norm_pointers`, `norm_scope`, `norm_git` · `norm_asking`, `norm_decisions`, `norm_closing`, `norm_output` · `guard_git`, `guard_destructive`, `guard_output`, `output_dir` · `remind_docs`, `remind_context`.
   - **Round two**, one single-select question per picked block, guard or `output_dir`, at most four per call: a block's or a guard's options are the modes it is not in now. Describe a block's mode as `on` printed and binding, `advice` printed but not binding, `off` not printed; a guard's as `on` refuses, `advice` lets every such call through in every repo and warns the session, `off` does nothing in every repo. `output_dir` always has two: Claude Code's own behaviour, no folder, files land where Claude Code puts them; and a folder of the user's own, one folder per repo and per worktree inside it.
   - **A picked reminder flips** to its other mode, unasked. **A folder of their own is asked in chat as a full path**, unless they typed it under Other. Nothing picked → write nothing and say so.
4. **Write every answer in one call**: `python3 <plugin folder>/scripts/norms_config.py --data "${CLAUDE_PLUGIN_DATA}" set <key>=<mode> ...`, the folder as `"output_dir=<full path>"` or `output_dir=none`. It refuses an unknown key or mode, or a folder that is not a full path, and writes nothing; read its message and ask again. Never hand the user a command.
5. **Say what changed and when it applies**: a guard's or a reminder's switch, and the folder `guard_output` guards, from its next call, in this session too; a block of the norms, and the folder the `OUTPUT` block names, from the next session start. Files already in the old folder stay there.

- **A block and its guard switch apart**: `norm_git` and `guard_git`, `norm_output` and `guard_output`. Say so when the user moves one of a pair.
- **`.claude/destructive-gate.off` in a repo still turns `guard_destructive` off there**, whatever its switch says.
- **Only these thirteen and the output folder are set here.** The rules inside the skills are not.
