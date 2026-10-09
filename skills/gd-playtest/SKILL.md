---
name: gd-playtest
description: Plan playtests and turn playtest feedback into decisions — test goals, metrics, tester types, observation script, capture setup, triage, decision log, and insight-to-action tickets. Use when the user wants to test a build, prepare questions for testers, has playtest notes/recordings/feedback to process, "people said X", wants to decide what to fix next from feedback, or asks whether an analysis is actionable.
---

# GD Playtest & Iteration

*The biggest trap: collecting feedback you can't act on.* Goal: from a complete build → documented decisions within 72 hours.

## Workflow A — Plan a playtest

1. **Goal ≤ 2 sentences**, pick 1–2 categories:

   | Category | Question | Measured signal |
   |---|---|---|
   | Feel & Flow | Does the core action feel good? Is the loop readable? | Time to mastery, input error rate |
   | Balance | Are challenges fair? Do resources create tension? | Stages/waves lost, end-of-stage resources, character deaths |
   | Clarity | Do players understand what happens and why? | Tutorial skip rate, number of questions/hesitations |
   | Emotion | Do they feel the highs and lows? | Self-report per beat |
   | Retention hook | Do they want another session? | Return-intent score 1–5 |

2. **Test type** (small & frequent first): team internal → blind internal (hasn't seen the game) → friends/family → focus group → closed alpha → public demo.
3. **Pick testers** (3–5 people, mixed types): *blind* (onboarding) · *careful explorer* (over-explains) · *optimizer* (exploits) · *chaos agent* (system limits).
4. **Prepare capture** — check before testing: phone screen recording, think-aloud, event logs (if possible: add temporary logs for key events: stage start/end, resources, character deaths, dialogue choices), a 5-question survey tied to the goal.
5. **Observation script** for the facilitator: *never explain during the test*; don't fix mid-session; note silences, sighs, long pauses.
6. Output: `<game_root>/docs/playtest/<YYYY-MM-DD>-plan.md` using [templates/playtest.md](templates/playtest.md) (Plan section). Record the build/commit hash and changelog.

## Workflow B — Process results

1. **Record surprises** first, then separate **symptoms** (got lost) from **causes** (missing guidance).
2. **Read behavioral signals:**

   | Behavior | Usually means |
   |---|---|
   | Long pause | Friction or overload |
   | Repeating an action | Unclear feedback / broken affordance |
   | Missing the obvious | Poor visual hierarchy |
   | No reaction | Flat pacing |
   | Laughing at the wrong moment | Contradiction or emergent play |
   | Backtracking | Unclear goal |
   | Skipping | Boredom or distrust |
   | Sudden silence | Tension peak (good) or lost interest |

   *"The player is never wrong. If they misunderstand the system, the system communicated it wrong."* But don't overreact to one person — look for patterns across sessions.
3. **Think in systems:** which action triggers it, how the system responds, which layer of the Game Map is broken.
4. **Group & triage:** by pillar and severity → **Critical / Important / Nice-to-have** (parking lot). Fixes estimated at >1 day → prototype spike first.
5. **Decision log:** Problem · Proposed change · Owner · Deadline · Pillar served · How to validate in the next test.
6. Turn each decision into a ticket (add to the project backlog if the user agrees; important decisions → DECISIONS.md) and call the appropriate skill: UX → `gd-ux-audit`, numbers → `gd-economy-balance`, story → `gd-narrative-design`, features → `gd-feature-spec`/`gd-feature-audit`.

## Insight → Action (applies to EVERY analysis)
Pattern ("skips dialogue after 10s") → ask why → check context (onboarding or endgame) → hypothesis → next step (try a shortened version) → track impact.

An analysis is only actionable if it answers at least one of: *what to change, what to keep, what to test, what to cut/postpone, what is likely to break/delight*. Final test: **can it be written as a sprint ticket?** If not → it's still commentary.

Data warning: a few people on Discord, gut feeling, streamer opinions, an 8-person test = *signal*, not *data*. Correlation ≠ causation.

## Suggested cadence
Monday build + test · Wednesday decide · Friday implement.

## Checklist
- [ ] Goal ≤ 2 sentences
- [ ] Build number + changelog shared
- [ ] Capture checked beforehand
- [ ] Triaged within 48 hours
- [ ] Every action tied to a pillar
- [ ] Next test scheduled
