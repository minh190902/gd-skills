---
name: gd-status
description: Project compass — know where a game project stands and keep it written down. Use at the START of a work session ("let's continue", "what should we do today", "where are we", "where were we"; in any language), at the END of a session or after finishing a task, when switching tasks, when the user asks what's done/next/blocked, or when progress docs look stale compared to git history. Maintains docs/design/STATE.md as the single one-page source of truth.
---

# GD Status — project compass

The problem to avoid: after a few weeks you no longer know where you are, and the docs say one thing while the code does another. The fix is **a single page** that is always correct, `<design_dir>/STATE.md`, together with a decision log and a system map. Design dir: see the convention in `gd-core`; if it does not exist yet, set it up per `gd-core` section 1.

| File | Answers the question | Who updates it |
|---|---|---|
| `STATE.md` | Where are we, what's next, what's still undecided? (≤ 1 page) | This skill, at the end of each session |
| `DECISIONS.md` | Why is the game the way it is? | `gd-design-review`, `gd-unstuck` when a decision is made |
| `SYSTEMS.md` | Which systems exist, and which system touches which variable? | `gd-design-review` after each change |
| The project's PROGRESS / CHANGELOG (if any) | What has been finished (history) | Archived when a milestone closes |

## Start of session — "where are we?"
1. Read STATE.md and PROJECT.md.
2. Check for **drift**: run `git log --since=<STATE's last-updated date>` and `git status`. Are there commits or changes not recorded in STATE? Any changes outside the current focus?
3. Answer in ≤ 8 lines:
   - **Milestone:** … · **Focus:** …
   - **Last time:** …
   - **Next:** (the first item in "Next")
   - **Still undecided:** …
   - **Drift:** (if any)
4. Ask the user whether to take the next item or change direction. If changing direction, run the new idea through `gd-design-review` first.

## End of session / task finished
1. Remove finished work from "In progress". Add one line to the "Session log": date · what was done · commit.
2. Update "Next" (≤ 5, by priority), "Open questions" and "Parking lot".
3. Record any new decision in DECISIONS.md. If systems changed, run `system_map.py` and update SYSTEMS.md.
4. Keep STATE ≤ 1 page: the session log keeps only the 5 most recent lines; older lines move to the project's history file.
5. Update the `Updated:` date at the top of the file.

## Rules for staying lean
- **One milestone at a time**, with a testable "done" criterion.
- **At most 2 items in progress.** To start a 3rd, finish or defer one first.
- **Ideas that pop up mid-task are not done right away**: write them to the parking lot, and run them through `gd-design-review` if they need evaluation.
- When closing a milestone: review the parking lot and choose the next milestone together with the user.
- When old docs contradict STATE, STATE wins; note the drift so it can be cleaned up later.
