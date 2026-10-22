# BACKEND — what the backend chain adds

Read this before the first page of a backend batch, or of an app that never split its work. A UI batch does not need it.

## The rule test, before the wiring

Write the rule test from the rule, against the enforcement point, while the page cannot yet vouch for it — a test written to agree with running code agrees with its bugs. A page implementing no rule has no such step. A repo with no test runner raises it once under `logic-build` and records what stays unproven as `Prove: <topic>` lines in the queue.

## Wiring a page built in a UI batch

The query must return the contract type. Three rules, and the first is the one broken quietly:

- **No `as any`, no `as unknown as`, no widening a type to make it fit** — a cast hides a decision that belongs to the user.
- **A query that cannot satisfy the contract changes the contract**, and the page it belongs to goes back into `docs/queue.md` — a stated decision, never a side effect of wiring.
- **Replace the mocked session; never leave it beside the real one.** Two sources of role is one too many.

## The page spec, after the walk

Every page this batch wires leaves one Playwright Test spec, because a walk is paid for again in every session and a spec replays it for nothing. A Proof profile that is not the web writes none, and the close says so.

- **Three tests in `e2e/<page>.spec.ts`**, or where the repo's Playwright config already collects: the flow the walk just finished, as the page's role; then `failed` and `empty`, the page's reads answered by `page.route` with an error and with no rows, asserting what `contract.md`'s cases ask of those states. A page that reads nothing keeps the first test alone.
- **`page.route` stands in for the database in those two tests only**, because they test the page, not the read.
- **A read the browser never makes — rendered on the server — cannot be answered by `page.route`**: write its two tests as `test.fixme`, titled with the read, so the gap prints in every run.
- **Launch Chrome as Playwright does by default — headless, on its own temporary profile — with `channel: 'chrome'`.** Never `connectOverCDP`, and never `launchPersistentContext` on the user's profile, because the user's own Chrome holds their work.
- **Point `baseURL` at the dev server the session started for the walk**, never at one it did not start.
- **Sign in with the walk's account through environment variables the spec names**, and write a saved `storageState` only to a git-ignored path, because it holds a live session.
- **A write the flow makes lands on a row named `[CLAUDE] …` that the test deletes after itself, or is answered by `page.route`**, because the database a spec reaches may hold real data.
- **A write that sends anything out — an e-mail, a webhook, a message, through a trigger or an edge function — is always answered by `page.route`**, because a sent message cannot be taken back.
- **Run the spec before the page's commit, and fix a failure in the page**, never by loosening an assertion to match it.
- **Run the whole suite once before the session's last commit**, because a page this session changed can break another page's spec: a failure this session caused is fixed now, any other becomes a `docs/queue.md` line.
- **No Playwright in the repo → raise it once, bundled with the page's Section 4 questions**: install `@playwright/test` as a dev dependency, recommended, with no browser download, because `channel: 'chrome'` runs the installed Chrome · carry on unproven, one `docs/queue.md` line per page, `Prove: <page> spec`.

## Retiring a page's canvas file

`src/design-canvas/<page>` still standing means the design session ratified this page and left the file for comparison. After the wiring walk passes at both widths:

1. Put the real page beside its canvas file and fix what silently diverged.
2. **Propose the deletion at a chat stop** — naming the page and inviting the side-by-side look — and delete only on the user's granted confirmation (`design-settle`'s canvas lifecycle: never delete unasked).
3. Propose it in this same session: kept past its verified page, the file becomes a second source of values.

The last page file to go takes the canvas index route, its foundations board, its CSS, and `.design-audit/` with it.
