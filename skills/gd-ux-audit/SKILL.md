---
name: gd-ux-audit
description: Audit the UX of an existing game screen or flow — clarity mapping, user-flow step count, feedback gaps, affordance, cognitive load, failure types, severity-rated findings (S1–S4) with concrete fixes. Use when the user says a screen is confusing or cluttered, "players don't notice X", "too many taps/clicks", before polishing a screen, or after a playtest reveals hesitation. This skill evaluates and fixes existing UI; for brand-new screens use the project's UI design workflow if it has one.
---

# GD UX Audit

**A UX failure is the gap between what the player wants, what the interface suggests, and what the system actually does.** The telltale sign: the player has to ask "can I do X?".

Read the platform constraints in `PROJECT.md` first: orientation, input method, minimum touch/click target size, session length, UI metaphor and color palette.

## Workflow

### 1. Define the scope and read the screen
- Which screen or flow? What does the player come here to do, and where do they come from?
- Read the screen's scene/layout and scripts, the theme, sketches, and the relevant UI spec. If possible, run the game and take screenshots: auditing real visuals beats reading code.

### 2. User flow
List each Input → Navigation → Feedback → Outcome step, from entry to completion. Count the steps/actions. Mark where the player hesitates, the error branches and how they recover. *Do not apply the 3-click rule mechanically*: a clear 4-step flow beats one confusing click. Judge by predictability, hesitation and effort.

### 3. Clarity mapping
1. Pick one gameplay moment on this screen.
2. List **every signal**, both UI and environmental.
3. Rank them from most important to optional.
4. Are the important signals close to where the player is focusing?
5. Are they reinforced with color, sound or motion?
6. Are states (ready, on cooldown, danger, insufficient resources) signaled?
7. Has redundant information been removed?

### 4. Scan for 6 failure types
| Type | Example |
|---|---|
| Cognitive overload | Too many stats on one card at once |
| Unclear affordance | Something clickable doesn't look clickable (no hover/pressed state) |
| Repetition fatigue | Going through 4 menus to do one thing |
| Missing feedback | An action completes without clear confirmation |
| Hard navigation | No way back, lost context |
| Flow interruption | A popup blocks right at a tense moment |

Also watch for **invisible UX debt**: legacy systems that never got improved, UI that gets messier as content is added, tooltips compensating for bad design.

### 5. Check the 5 dimensions
- **Clarity:** the player understands what they can do and what just happened.
- **Control:** input is responsive and predictable.
- **Feedback:** every action is acknowledged, proportionate to its consequence.
- **Rhythm:** respects attention and session length.
- **Emotion:** evokes the right emotion and fantasy.

Also check: can mistakes be undone or prevented, and is the screen usable in tough conditions (tired player, small screen, one-handed play)?

### 6. Rate severity and propose fixes
- **S1 Blocker:** the player cannot complete the goal, or misunderstands and loses resources/progress.
- **S2 Major:** still completable but with noticeable hesitation, frequent misclicks, or missed important information.
- **S3 Minor:** slight friction, slowness, lack of polish.
- **S4 Polish:** improves feel or aesthetics.

Each finding includes: location (node/element path), description, failure type, severity, evidence, **a concrete fix**, and estimated effort. Fixes follow the project's code/UI standards (noted in PROJECT.md).

### 7. Output
Save to `<game_root>/docs/ux/<YYYY-MM-DD>-<screen>.md` using [templates/ux-report.md](templates/ux-report.md). When presenting: show the findings table sorted by severity first, then the top 3 things to fix now.

## Quick checklist
- [ ] Usable without instructions?
- [ ] No spots where the player hesitates or taps around at random?
- [ ] Feedback is immediate and clear?
- [ ] UI still holds up when content triples?
- [ ] No unnecessary popups stealing attention?
- [ ] UX reinforces tone, pacing and fantasy?
- [ ] Icons, colors and layout still communicate their purpose with all text removed?
