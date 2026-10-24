# CLAUDE.md — repo kaizn

This repo is not an application. Its root is the plugin that governs other repos, so a mistake here spreads to every app.

## Language

All files in this repo — `SKILL.md`, references, templates, README — are written in English, so they work for anyone who installs them.

Reply language is not fixed. Follow whichever language the user writes in.

## Rules

Skills and norms here are read by other agents, not by humans. Write them as direct instructions, not as observations.

Keep every rule short. One rule is one imperative sentence. Give its reason in one clause, only when an agent would otherwise break the rule. Cut any paragraph that argues, defends, or restates. State each rule in one file only; other files point to it by name.

Change a rule only for a finding seen in two sessions or in a real app, because one session's miss is as often the session as the rule; a finding seen once is a line of `docs/reference/status.md`.

Do not add a skill to `kaizn` without naming what would be lost if it did not exist. Every skill pays a context cost in every session through its description, including the sessions that never use it.

Hooks block without being able to ask. A new hook must first be tested against the cases that **should pass**, not only the ones that must be refused. A hook that is too strict costs more than no hook.

This plugin ships no templates. What a new app repo gets is written by `app-settle` for that repo's answers — never a stock file, which is a decision taken before its question was asked and goes stale without anyone re-reading it. Whatever a skill here tells a session to write lands in app repos that may not be private, so a rule that produces a file must never produce a secret in it: name the variable, never its value.

## Proof runs

A proof run tests a hook or a script on a throwaway copy of an app in the scratchpad. Never run one to judge a skill: a skill's findings come from its use in a real app, read with `app-eval`, because a copy answered by a script shows the copy's faults. Write only the public client values into the copy's `.env` — the URL and the publishable key; never copy the real `.env`. A server key reaches the copy only by the user's own hand: a key created for the run and revoked after it. Without one, report every server route `not verified — no server key in the proof copy`.

Write `the proof app`, never the app's name, a client, a person, or a domain, in any file or commit message of this repo, because anyone who installs the plugin reads its history.

## docs/

Write `docs/` for the people who install the plugin, never for agents: a rule stays in its skill and is not restated there.

A commit that changes what a user meets — a question, a stop, a command, a file a skill writes — corrects that feature's page under `docs/` in the same commit, or writes the page where it has none.

Put a page in the group its reader comes for: `start/` to begin, `concepts/` to understand, `guide/` to finish one task in numbered steps, `reference/` for one page per skill, hook and command.

List every page in `docs/README.md` under its group, because that file is the index on GitHub, the site's home and its sidebar, and what `norms-help` prints: a page it does not list is in none of them.

Write a page in GitHub-flavored Markdown only — no frontmatter, no `:::` container, no include — and open it with its `# ` title and one lead sentence, because the same file is read on GitHub, on the site and by a session.

Keep `docs/queue.md` only while it holds an edit this toolkit still owes — delete it with its last item — because the `SessionStart` hook injects it into every session here and stays silent when it is absent.

Write a rule no session has run as a line of `docs/reference/status.md`, never as a queue line, because a queue of runs owed refills with every edit.

Keep `CHANGELOG.md` at the root and the commands a user runs in `docs/reference/commands.md`, because `norms-help` prints the first's top entry and the second whole from an installed copy.

Never add `docs/PRD.md`: it switches this repo's sessions to the norms of an app.

## Git

Commit, push, and open a PR by the `GIT` block of `scripts/session_norms.py`, as an app repo does.

A commit that changes the plugin — `skills/`, `scripts/`, `hooks/` or a manifest — bumps its `version` in the same commit, because `/plugin update` compares version numbers only; `.githooks/pre-commit` refuses it otherwise, so run `git config core.hooksPath .githooks` once per clone.

A commit that bumps the version adds that version's entry to `CHANGELOG.md`, in English and in Keep a Changelog form, naming every rename or removal an installed app must act on; `.githooks/pre-commit` refuses the bump without it, and warns when the plugin changed and no page under `docs/` did.

A commit reaches app sessions only after it is pushed to `origin`, and the user decides every push.
