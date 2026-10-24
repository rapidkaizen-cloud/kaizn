# Redesign the look

`design-settle` alone, on an app that already has a look or on one that has none yet.

Before you start: `impeccable`, `frontend-design` and `ui-ux-pro-max` are installed ([Install](../start/install.md)), and a browser MCP server is connected.

## Steps

1. **Run `/kaizn:design-settle`** — by name, because `impeccable`'s description overlaps it.
2. **Choose Fast or Full.** It is asked with the first question, on a new app and on a redesign alike.

   | | Who answers the design dialogs | The rest |
   |---|---|---|
   | Full | You, one dialog at a time | The frames, the pick, the gate and every check |
   | Fast | The skill's own recommendation, shown as one block you cancel line by line | The same, unchanged |

   `/kaizn:design-settle fast` skips the question.
3. **Read the first block.** It prints what it found: the documents, whether `DESIGN.md` is written, how many UI components exist, the platform, the design material present, and the flow it will follow.
4. **Answer the non-visual dialogs**, or in Fast cancel the lines you disagree with.
5. **Pick a direction on screen.** It draws two to four direction frames and you choose.
6. **Approve the canvas once.** Every page is built in production-grade code on a canvas; your approval promotes it into the app.
7. **Start a new session when it asks, twice** — before the pages are promoted and before they are checked. Run `/kaizn:design-settle` again and choose to continue; it costs far less than one long session.

## Where UI already exists

- **You are asked the scope first**, where the app has more than one page group: the whole app, or the groups this run redraws. Every page in scope is read, drawn, promoted and checked, so a large app is redesigned one group at a time.
- **The existing UI is audited next**, and today's look is one of the candidates.
- **Where `DESIGN.md` is already written**, you are also offered a fix of the drift only, instead of a redesign.
- **Removals are shown at a gate** before anything is taken out.

## Afterwards

`design-settle` commits once, when it closes. Where UI exists the pass runs on its own branch and the commit lands there; merging it is yours.

`DESIGN.md` is the design source, and `design-settle` is the only skill that edits it. A later session that finds it absent or finds code deviating from it stops and points you back here. Deviating code is a finding, never a new norm.

## Related

- [design-settle](../reference/design-settle.md) — every step in detail.
- [ui-build](../reference/ui-build.md) — what holds the UI to `DESIGN.md` afterwards.
