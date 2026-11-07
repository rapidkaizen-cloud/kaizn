# CONTRACT — the UI batch's stand-in for a backend

Read this before the first page of a UI batch. A backend batch does not need it.

A UI batch builds pages with no database behind them, and invented data is always well formed — no nulls, short strings, five tidy rows — so a page approved against it breaks the day real data arrives. The contract writes the data's shape down before a page is shaped around it.

## The two files

```
src/contracts/<page>.ts            types only, no runtime
src/contracts/<page>.fixtures.ts   the six cases
```

The contract holds three things: the data the page reads, the actions it fires, and the role of whoever is reading — an input like any other, because role handling patched in later is where leaks live.

**A page imports from its contract and from nothing else that carries data.** During a UI batch, no file under `src/pages` may import the database client or the generated database types. One grep at the close of the session, and a hit is a finding:

```
grep -rE "lib/supabase|database\.types" src/pages
```

## The six cases

A page is not accepted until all six render without the layout breaking. They are a closed floor — a checklist, not a judgement; a page adds a named case only for a form branch or a busy state it shows:

| Case | What it proves |
|---|---|
| `loading` | A skeleton shaped like the result, not a spinner |
| `empty` | The empty state says why it is empty and what comes next |
| `single` | One row does not leave the layout stranded |
| `bulk` | 500+ rows — pagination, scrolling, column widths, and the density `DESIGN.md` asked for |
| `messy` | Null in every nullable field, the longest string that really occurs, the widest number |
| `failed` | The failure sits next to its cause, with a way to retry |

`bulk` and `messy` are the two usually skipped and the two that catch the most.

**Fixtures are copied from the document the app replaces, not invented** — a spreadsheet, an export, a paper form. Its rows are the fixture: real column widths, real name lengths, real edge cases, and figures whose correct answer the user already knows. Where no real document can be used, say so in the session and name what was substituted.

**A fixture carries no person and no secret**: replace every name, phone number, e-mail, address, identity or account number and free-text value with an invented one of the same length and format, and keep every figure, date, code and status as it stands — the file is committed.

## Switching cases

Two switches — one for the fixture case, one for the role — reachable without a rebuild, and no tooling beyond them. On the web they are two search params; elsewhere they are whatever the **Cases** line of the Proof profile in `docs/product.md` names:

```
?fixture=messy
?role=approver
```

No Storybook, no mock server, no fixture generator, on any platform. Reach for more only when two switches stop being enough.

## The walk — in a subagent

**Hand the walk of a page's cases to one subagent on a cheaper model than the session's** (`sonnet` on Claude Code): a walk is dozens of browser calls, and each one made here re-reads the whole session.

- **Brief it with** the address of the dev server this session started, the page's route and the proving page's, the two switches and the values to walk, the two widths of `SKILL.md` Section 4, and the browser rule of its Section 5.
- **It changes no file and returns only** one line per case — `renders`, or what broke with the console error beside it — and the paths of the screenshots it saved: the `bulk` case at both widths, and the proving page at the desktop width.
- **Read the screenshots and judge them here**, as `SKILL.md` Section 5 orders — the judgement is never the subagent's.
- **A case that broke is fixed here, then walked again alone.**
- **No subagent → say so and walk here.**

## What a contract does not cover

Behaviour that crosses screens — editing a figure on one page and watching another page change — cannot be proven by fixtures. It is verified in the backend batch, and stated as a limit rather than faked with in-memory state.

## The page copy count

The UI chain's step before lint; a backend batch renders no copy. Group every string the page renders into three classes and print one line each, longest and median, in words:

- `Action` — buttons, links, menu and tab items. Text naming what happens.
- `Name` — field labels, column headers, badges, headings. Text naming a thing.
- `Explanation` — helper text, empty and error states, tooltips, dialog bodies, toasts.

```
/visits
Action       longest 2 · median 2
Name         longest 4 · median 2
Explanation  longest 8 · median 6
```

- **Cut every string over its cap before the commit.** The caps bind tenth-use pages (`ui-build`, Writing — copy caps); a first-visit page group is counted only.
- **No limit is set here and no count is a finding** — the count puts drift where the user sees it before the page is accepted, and the fix comes from `ui-build`'s `Writing` rules. A median far below its longest is one string that ran away; a median close to it is the whole page drifting.
- **Count from the source**: the strings are there, so the count needs no browser and survives a session with no capture tooling.
