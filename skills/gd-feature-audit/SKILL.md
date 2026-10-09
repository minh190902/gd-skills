---
name: gd-feature-audit
description: Audit existing game features/systems for purpose, core-loop fit, overlap, scalability and whether they should be kept, deepened, merged, reworked or cut. Use when the user asks "is feature X worth it", "why does nobody use X", "too many systems", "simplify the game", "review our systems" (in any language), before a refactor/sprint planning, or after several systems were added in a row. Includes an overlap matrix for systems that affect the same variables.
---

# GD Feature Audit

*"If removing it changes nothing, it's noise."* Goal: decide **Keep / Deepen / Merge / Rework / Cut** for each feature, based on evidence in the code and design docs, not on gut feeling.

## Process

### 1. Define the scope and gather evidence
- Auditing one feature, or a cluster (e.g. every system that touches a character's "mood")?
- Read `PROJECT.md` and `SYSTEMS.md`. Run `system_map.py` (part of gd-design-review) to see which variables each system writes/reads.
- For each feature, find: logic files, data/Resources, signals, where it appears in the UI, dialogue hooks, whether it is saved, whether it has tests. Record full paths.
- Read the description in the GDD/PRD to learn the *intent*, then compare it with the *reality* in the code.

### 2. 7-step analysis for each feature

| Step | Question |
|---|---|
| **Purpose** | What player problem does it solve? Which pillar does it serve? |
| **Core fit** | Which phase of the core loop does it attach to? Does it change the player's decisions? |
| **Mental model** | What does the player *think* it does? Does that match reality? Can they even see it? |
| **Feedback** | How does using it feel? Where does feedback appear? Any friction? |
| **Failure modes** | What happens when it breaks, is abused, ignored, or misunderstood? |
| **Scalability** | Is it still useful in the late game, or only meaningful early on? |
| **System hooks** | Which systems depend on it? What breaks if it is removed? |

### 3. Red flags
- Isolated systems, not connected to any other system.
- **Overlapping functions**: several mechanics limiting the same thing.
- **Conflicting motivations**: the story encourages one behavior while the mechanics reward the opposite (ludonarrative dissonance).
- Players use it a lot at first, then abandon it.
- Big impact, but players don't notice it.
- Tooltips are carrying the weight of a weak design.

### 4. Lifecycle
Introduction (is it taught meaningfully?) → Growth (does it deepen, have variations?) → Integration (does it connect to other systems?) → End of role (is it useless in the late game?). *Good features scale, transform, or retire gracefully.*

### 5. Overlap matrix (when auditing 2 or more systems)
Rows are systems, columns are **affected variables or behaviors** (from `system_map.py`). Mark cells where 2 or more systems act on the same thing. For each overlapping column:
- Can the player tell which cause is responsible? If not, consider **Merge** (combine into one system with multiple input sources) or **Rework** (separate the roles clearly).
- Count the number of status indicators a single screen must display, then assess cognitive load within the platform constraints.

### 6. Verdicts and actions
Each feature gets a **Keep / Deepen / Merge / Rework / Cut** verdict, with a 1–2 sentence reason and evidence (file:line). Every verdict other than Keep must come with **an action that can be written as a ticket**: what to do, in which file, how success is measured, save-compatibility risk. Prioritize using an impact × effort matrix.

## Output
Save to `<game_root>/docs/audits/<YYYY-MM-DD>-<scope>.md` following [templates/feature-audit.md](templates/feature-audit.md). When presenting, put the verdict table first and the details after. **Never delete code on your own**: the audit only recommends. Once the user approves, record it in DECISIONS.md, then use `gd-feature-spec` for the rework.

## Per-feature checklist
- [ ] Serves a clear player goal
- [ ] Integrated with the core loop
- [ ] Scales, grows, and rewards mastery
- [ ] The player *feels* it, not just *sees* it
- [ ] Removing it breaks something (if not, it's noise)
