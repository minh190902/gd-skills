---
name: gd-game-analysis
description: Analyze or deconstruct a reference game (or an open-source game repo) and extract actionable lessons for our projects — core loop, systems, progression/economy, UX/FTUE, narrative, monetization, market fit, and system-level comparison/benchmark between games. Use when the user shares a game, store page, video, review set or repo to study ("analyze game X", "what can we learn from Y", "compare with Z"; in any language), when researching competitors, or when writing documents like "Cultivation Simulator Analysis.md".
---

# GD Game Analysis

The purpose is not to summarize someone else's game, but to **extract decisions for our own game**. Every analysis ends with recommendations that can become tickets, tied to the pillars of the target project.

## Process

### 1. Define the question & target project
Which of our games is the analysis for? What is the specific question ("how do they handle long-term consequences?", "how do they keep the economy tight?")? Read `PROJECT.md` in the target game's design dir (convention in `gd-core`).

### 2. Gather sources — choose the right lens
| Lens | Gives insight into | How |
|---|---|---|
| Play / watch gameplay | Behavior | Note repeated actions, stopping points, hesitation, emotions, immersion breaks |
| Reviews (Steam, store, Reddit) | Emotion | Tag: pacing, feedback, economy, tone, expectations. Negative reviews are often the most valuable |
| MDA | Cause and effect | Mechanics → Dynamics → Aesthetics (8 kinds of fun: Challenge, Fantasy, Narrative, Discovery, Expression, Fellowship, Submission, Sensation) |
| AERM | Business sustainability | Acquisition, Engagement, Retention, Monetization |
| Diagrams | Systems | Mind map, decision/state flowchart, resource flow diagram |
| Source code (open-source repo) | Implementation | Read the main loop, data model, how consequences are stored & read |

Use WebSearch/WebFetch for store pages, wikis and reviews; use the Explore agent for large repos.

### 3. 7 questions for analyzing any game
1. What does the player do most of the time? (core loop — draw it as Action → Feedback → Progress)
2. Which systems reinforce or break the loop?
3. Where and how does the game teach?
4. When does tension rise/fall, and why?
5. Which feedback is memorable, satisfying, or confusing?
6. How do theme, mechanics and pacing connect?
7. Would you keep playing, and what pulls you back?

### 4. Feature breakdown (for features worth learning from)
Purpose · Core fit · Mental model · Feedback · Failure modes · Scalability · System hooks. *Understand why it works, in what context, for whom* — don't copy features without their context.

### 5. Comparison (when there are ≥2 games)
Compare **systems and outcomes, not feature lists**, across 7 dimensions: Core loop · Cognitive load · Progression · Onboarding · Emotional hook · Monetization · Presentation. Ask: what constraints do they share? How do they solve the same problem differently? What is absent, and why? Intent vs impact?

Red flags of lazy comparison: copying because a competitor has it; undefined "polished"; copying a hit while dropping its context; comparing across genres/budgets without nuance; comparing visuals only.

### 6. Turn it into action for the target project
For each lesson:
| Lesson | Evidence (source) | Applies to (our system/file) | Proposed change | Pillar | Effort | Risk |
Classify: **Apply now / Experiment (prototype) / Note (not a fit right now, and why)**. At most ~5–7 prioritized recommendations — few but solid.

### 7. Output
Save to `<game_root>/docs/analysis/<game-kebab>.md` (or repo-level `docs/analysis/` if the analysis is shared across several games) following [templates/deconstruction.md](templates/deconstruction.md). Put the "Key takeaways" section and the action table **at the top** of the file.

## Checklist
- [ ] Clear analysis question & target project
- [ ] Analyzes systems, does not just list features
- [ ] Knows *why* it works, and for whom
- [ ] Covers emotion and UX, not just mechanics
- [ ] Every recommendation has evidence, is tied to our files/systems, and can become a ticket
- [ ] States explicitly what is deliberately *not* applied
