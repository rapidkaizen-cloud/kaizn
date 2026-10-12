# What is proven

What has run for real, on which host, and what has not. A line under "Not yet verified" is behaviour the skills describe that nobody has watched happen.

## Proven on Claude Code

All of it on paper or in throwaway copies of apps with no database, by sessions run headless or scripted through the Agent SDK, except where a line says otherwise: none ran in Orca, and none was answered by a person.

- **`design-settle`'s interview** has been simulated on an existing-UI scenario with a legacy `PRD.md`, in Full, and every decision landed.
- **`app-settle`'s migrate mode** ran twice on copies of two legacy apps, by a session that read only the skill: every sentence of the PRD's six sections arrived word for word, `DESIGN.md` linted clean, one commit each.
- **A session building a new page** ran every step on Opus at 0.87.0, in a copy of a settled app with no sign-in: `build-flow`'s todo list, its proposal with both lists and its audit offer, and all of `ui-build`'s craft material read before the page.
- **`design-settle`'s verification and close** ran on Opus at 0.87.0, on a copy of a finished run with no UI, rewound to before its close commit: the checks in a subagent with a browser, the motion read against `review-animations`, the raw values, the detector's hit, the lint floor and the fixtures' numbers fixed and checked again, `docs/queue.md` written with a line per page still on fixtures, and one commit.
- **`design-settle`'s audit under a scope** ran once at 0.90.0 in a real app on its local database, behind a sign-in, as a Sonnet subagent handed the brief, a scope of 8 page files out of 696 and an account: it read the 8 page files and none outside them, opened 7 routes — 2 inside the scope, 5 outside — wrote `places.md` by a command, 10,149 lines, and finished in 24 minutes. It took 111 calls and 23.3 million input tokens, its context growing from 45k to 350k; half of that was paid in the last 40 calls, the counts and the three files, written after the walk. Split in two subagents at 0.91.0, it ran once more on the same scope: the source in 55 calls and 10.4 million tokens, the walk in 85 calls and 10.9 million, 37 minutes together, neither reading a page file outside the scope and the walk reading none at all; it opened 6 routes and measured 118 contrast pairs where the one subagent had measured 61. Two counts differed between the runs — the files a token change touches, 793 and 616, and the stray spacings, 175 and 232 — so those rows were not read the same way twice. With the two scripts of 0.92.0 it ran a third time on that scope: the source in 58 calls and 9.9 million tokens, the walk in 70 calls and 7.9 million, 29 minutes together; the counts were copied as `audit_count.py` printed them, and `audit_measure.js` was pasted once and called from `window.name` on every later route, no page refusing `eval`. It measured 122 distinct pairs, the dark mode on one route only, and the source subagent still wrote four scripts of its own, for the rows the shipped one does not count — token health, label lengths, icon sizes.

## Proven on Antigravity

On the CLI — `agy` 1.2.16, Windows, headless, installed from this repo's URL with `agy plugin install`:

- The nine skills are listed, `hooks.json` is kept as written, the norms and the `HOST` block are injected, `git add -A` is refused, and a push is held.
- `design-settle` ran end to end at 0.70.0, Fast, on a new app with no UI, one question per headless turn: the Step 0 block, the reference search, `ui-ux-pro-max`'s generator, the install gate, frames and canvas with browser screenshots at both widths, `DESIGN.md`, the decision records, promotion, verification, and a commit with named paths.
- That run read no `impeccable` or `frontend-design` file and ran no detector. A run at 0.72.1 read `impeccable`'s craft floor and operational register and `frontend-design` before the first frame, and ran the detector in every round.

At 0.76.1 on `agy` 1.2.17, headless, installed from a folder, in a throwaway app on the `docs/` form with a bare local remote:

- The session ended its turn on the push command unprompted, a typed yes let it through once, a no with a question published nothing, and a push attempted without the stop was held.
- The document reminder arrived once after the conversation's own commit, and not after another conversation's.

Proven before 0.70.0 only, registered by path: an interactive session, and the hand-over block.

## Not yet verified

- A session building a new page on Sonnet: two sessions at 0.87.0 each dropped at least one of the todo list, the proposal's two lists and the audit offer, and neither read all of the craft material. Two rounds of tighter wording did not change that — build on Opus.
- `design-settle`'s close on the rules of 0.88.0. At 0.87.0, on Opus and on Sonnet, the structural diff failed for differences promotion itself makes, reduced motion was `not verified` because the browser tool cannot emulate it, and on Opus a fix changed pages already ratified. 0.88.0 answers the three and no session has run it; the lint floor's local plugin file alone was seen refusing its planted violations, on oxlint 1.87.0.
- The two cost cuts of 0.89.0 — `design-settle` ending its turn at two seams for a new session, and Step 8's mechanical checks in three subagents — have not run. Their saving is an estimate from one close at 0.87.0, where the one subagent's context grew from 32k to 267k tokens over 120 calls.
- The scope of 0.90.0 beyond its audit — `design-settle` asking which page groups a run redraws, the stack kept, the gate's first lines, the queue lines and the captures outside the scope — has run in no session. It was written from the size of one real app: 696 page files, where an audit of every route cannot finish.
- The three rows `audit_count.py` prints since 0.94.0 — token health, icon sizes, label lengths — have been copied by no audit, so what they save is not measured. The script alone ran on the real app of the scoped audit: the same 2,203 icon elements, 192 strings and repeats per file that audit's own scans had counted, and the one token nothing reads printed among two for the subagent to check.
- `design-settle` on Sonnet: none of three sessions printed the Step 0 block, and at the close one session at 0.87.0 wrote no queue line for the checks it could not run, left its last edits unchecked and never read the motion against `review-animations` — run it on Opus.
- `design-settle` from its first step with no UI, at 0.87.0 or later: the pass writing a `docs/queue.md` line as it promotes each page has not been seen.
- The rules of 0.85.1 to 0.87.0 on Opus: beyond one build session, `design-settle`'s Step 0 and its close, each ran on Sonnet alone.
- `design-settle` behind a sign-in, with a person: its audits walked signed out and read every signed-in route from source, the account question was asked in six sessions and no account was made, and no person has picked a frame on screen.
- In a real app with its database: database steps arriving as one command, `build-flow`'s backend batch, `logic-settle`'s migration, and a walk behind a sign-in with an account made for it.
- A dialog answered by a person: every one was answered by a script through the Agent SDK, never in Orca. No session has written `.claude/settings.json`.
- The four `logic-build` rules of 0.93.0 — uniqueness by a constraint, a returned error read at the call site, a list read paged, a test left by a bug fix — have been read by no build session. A check that refused new unused exports, type escapes, unread errors and long comments at commit was replayed over the last 100 commits of the app they came from and would have refused 51, 34 of them for a comment block alone; it was dropped, and no version shipped it.
- The UI and logic lint floors and the rule tests have never been written in a real app. `logic-settle`'s floor names ESLint alone; on another linter it has not run.
- The `docs/` form has never been bootstrapped in a real app.
- `app-settle`'s migrate mode and its align mode have never run in an app. Run migrate on a copy of a legacy app before a real one.
- Whether a cloud session installs this marketplace; until then, cloud sessions do frontend work only.
- The account-wide Supabase MCP endpoint end to end: its first-use login, and `project_id` as `guard_project_ref.py` expects.
- The document reminder after a commit: received on Antigravity only. On Claude Code no session has received it — whether a plugin's `PostToolUse` text reaches the model on an SDK host is unobserved. Both sessions that received it answered `Docs: none`, in an app with no UI; none has answered by writing a document.
- A held push passing on a chat reply: run end to end on Antigravity only. On Claude Code it is replayed against one real transcript, and no session has pushed on a chat reply there.
- A push and its pull request in one stop (0.95.0): the hook's self-check lets each run once on the one reply, on both hosts. No session has put both commands in one message.
- `norms-help`: no session has loaded it from an installed copy, on either host.
- On Antigravity: `design-settle` in Full and where UI exists — its audit subagent, its gate; `app-settle` and `logic-settle`; a question asked through `ask_question` in an interactive session; the IDE and Antigravity 2.0. `design-settle`'s `Material loaded:` line is self-reported there, and one run listed a file its transcript shows it never read. Gemini CLI is not ported.
