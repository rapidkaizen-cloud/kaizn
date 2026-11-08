# DELEGATE — work written by an agent outside this session

Read this before the first brief handed to another agent to write code — Antigravity, another CLI, another model. The session that hands the work out keeps every decision; the writer only writes.

## Before the first brief

- **Print `External writer : <agent · model · quota left>` and check it**, because a writer out of quota writes nothing: quota unknown → write `unknown`; none left → wait for its reset rather than launch a run that cannot finish.
- **Write the brief to a file and hand the writer its path, never its text on a command line**, because shell quoting breaks a long brief.

## The brief

- **Name files and line ranges; paste no code**, because the writer reads the repo itself and pasted code goes stale.
- **Name the rules the work answers to by file and section** — `DESIGN.md`, `ui-build`'s floor, the canvas file a page is promoted from — never restated.
- **End it with the scan the work's own step runs, as commands the writer runs clean before it reports done** — the detector on every route it touched, each `?fixture=` case opened with no console error, every contrast pair it drew computed, a grep for each pattern the floors forbid, the type check, the lint command, the tests. `scripts/verify_pages.js` of this plugin, by its absolute path and one page per `?fixture=` case, answers the console errors, contrast and width in one command. A command it cannot run is reported as such, never skipped.

## Its result

- **Review it in one subagent on a cheaper model than the session's** (`sonnet` on Claude Code), handed the brief's path and the diff's commit range: it runs the brief's scan again, reads the diff against the brief, and returns pass or the failed items, each with its file and line. Read the verdict, never the diff whole.
- **Merge every failed item into one fix brief, and give a brief two runs at most** — its first and one fix — because a third run of one brief costs more than fixing it here.
