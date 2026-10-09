---
name: gd-pacing-progression
description: Pacing, progression and onboarding design — level/stage tension maps, complexity curve (when each mechanic or system is introduced), difficulty curve, emotion arc across a chapter, FTUE/tutorial flow, unlock schedules, session length. Use when planning a new chapter or batch of levels, deciding when to unlock a system, designing or reviewing the tutorial or first 15 minutes, "the mid-game is boring", "too much at once", "players quit early", or reordering content.
---

# GD Pacing & Progression

The four regulators of the Dynamics layer: **Progression** (intentional change over time), **Complexity curve** (difficulty to learn plus difficulty to play), **Pacing** (rhythm of tension and release), and **Balance** (see `gd-economy-balance`). Complexity is not difficulty. Read `PROJECT.md` for session length and platform constraints.

## Workflow A — Pacing map of a chapter / stage sequence

1. **Inventory each stage** (from level config/data and narrative content): number of waves or challenges, new enemies, new characters, mechanics or systems *appearing for the first time*, major choices, estimated duration.
2. **Build a pacing table** using [templates/pacing-map.md](templates/pacing-map.md): each row is a stage or a 10–15 minute slice. Columns: new mechanic · tension (L/M/H) · complexity (L/M/H) · target emotion · breathing room/reward · surprise. Energy color code: 🔴 high · 🔵 calm · 🟡 reward.
3. **Check pacing patterns:**
   - Contrast exists: never sustained maximum tension.
   - Each new mechanic follows Learn → Try → Rest.
   - Setup before payoff: a threat or mystery is planted before it is resolved.
   - A lull before a big clash.
   - Rewards interleaved between pressure sections.
   - Each stage has at least one quiet moment.
4. **Diagnose problems:** flat pacing → boredom; constant tension → exhaustion; too dense → paralysis; weak mid-game → players quit.
5. **Propose** reordering, moving unlock timing, or adding breathing room, with concrete changes to data/content.

## Workflow B — Complexity curve (system unlock schedule)

1. Split the game into **3 acts**. For each act, note which new mechanics or systems appear and how they interact with existing ones.
2. 7 rules for introducing mechanics:
   - One mechanic at a time.
   - Build on what the player has already mastered.
   - Introduce it while the player still has capacity to spare.
   - Spread evenly across acts.
   - Teach in context.
   - Schedule breathing room.
   - Trim overlap in the late game.
3. Mark rest points and peak points (where many systems overlap, bosses).
4. Optional: a **false peak**, i.e. add a new layer right when the player thinks they have seen everything.
5. The output is a `System · Current unlock · Proposed unlock · How it's taught · Reason` table, then check whether the existing tutorial matches this schedule. Take the system list from SYSTEMS.md.

## Workflow C — FTUE / first 15 minutes

Standard rhythm: **Hook** (visuals, theme or story) → **teach one core action** → a simple challenge using that action → **immediate reward** → reveal the core loop → hint at what the player could become.

Checklist:
- [ ] Does the player know what to do in the first 10 seconds?
- [ ] Does the main action appear right away?
- [ ] Is the full core loop visible within the first 5–10 minutes?
- [ ] Is there a reward before asking the player to commit?
- [ ] Can the player feel the tone and fantasy described in PROJECT.md?
- [ ] Does the tutorial teach through action, isolate each concept before mixing, allow skipping, and fit the tone?
- [ ] *"If the player forgets they are in a tutorial, you did it right."*

How to check: describe the first 15 minutes in 3-minute slices, rate each low/medium/high, and mark breathing room, surprises, mechanic transitions, and at least one quiet moment.

## Progression
- Types: stats, spatial, story, mechanical, cosmetic, systemic. Structures: linear, branching, modular, cyclical, dynamic.
- **Good progression gives the player more choices.** Bad progression is the same playstyle with bigger numbers. Each level-up should open a new *choice*, not just add stats.
- Checklist: is growth clear? are there milestones to look forward to? does it change core play? is the pacing balanced? are there multiple layers? does it support the theme?
- Milestone map: plot milestones per stage, then look for stretches longer than 2 stages with no milestone.

## Sessions
Each stage should fit one typical play session (noted in PROJECT.md) and have a natural stopping point, with a save at that point. Consider splitting any stage that exceeds about 1.5× the session length.
