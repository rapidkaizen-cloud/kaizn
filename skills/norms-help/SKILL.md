---
name: norms-help
description: Help for the kaizn skills — which command to run in which situation, where each guide page is, the version this session runs and its latest changelog entry. Use when the user asks for help with these skills, which command to run, how something they do works, what version they are, or what changed.
---

# norms-help — the commands, the pages, the version

**Run `python3 <plugin folder>/scripts/norms_help.py` and relay what it prints as one card, in the user's language.** The plugin folder is the one this skill is read from, two levels above this file — never another copy, because a machine keeps one folder per installed version and the script reports the folder it sits in.

- **Keep every command, file name and the version number as printed**, and the entry's `To act on` lines word for word; act on one only when the user asks.
- **The version is its number and that one changelog entry, nothing more**: no install date, no path, no comparison with origin, no older entry.
- **A question comes with the request → answer it from the page `PAGES` names for it**, read from the plugin folder, and name the file. No page covers it → answer from `skills/<name>/SKILL.md` there and say that no page does.
- **Neither covers it → say so.** Never answer from what an older version did.
