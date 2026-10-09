# Game Map — detailed reference

Source: gamedesign.guide/theory (CC BY 4.0), paraphrased.

## Player layer

**Chain:** Context → Need → Conflict/Gap → Motivation → Intention → Behavior.

| Element | Question |
|---|---|
| Context | Who plays, in what mood, where, for how long, on what device? |
| Need | What gap do they want to fill? |
| Conflict | What creates tension? |
| Motivation | What directs their energy? |
| Intention | What are they *trying* to do? |
| Behavior | What do they *actually* do? |

**Gap types** (no gap = no reason to play; tune the gap size to steer motivation): lack of recognition → leaderboards; stress relief → combat; boredom → short levels; curiosity/mastery → deeper patterns; mood maintenance → relaxing loops; belonging → group play; **control → sandbox/management**; sensory novelty → procedural.

**Context profile:** Geography, Demographics, Emotional goal, Gaming history, Session pattern, Device setup, Preferred features, **Implication** (what to prioritize). Example: mobile players with 10–15 minute sessions → prioritize clarity, cut dead time, split content into modules.

**Need → strategy:** Progression ↔ Competence (visible feedback, fair failure); Economy ↔ Control/Stability (predictable rewards, clear resource roles); Narrative ↔ Purpose/Belonging (consequences, symbols); UX ↔ Safety/Clarity; Social ↔ Relatedness.

**Conflict types:** Personal, Systemic (scarcity, timers, fog), Social, Moral (dilemmas), Cognitive. Strongest when layered: system + emotion + identity. *If the player cannot perceive or affect the conflict, it becomes grind.*

Mechanic → hidden conflict: countdown → urgency; dialogue choice → moral tension; resource trade → sacrifice; hidden role → trust/suspicion; procedural map → missing information.

### Motivation models

| Model | Components | Use for |
|---|---|---|
| SDT | Competence, Autonomy, Relatedness | Core loop, onboarding |
| Quantic Foundry | Action, Social, Mastery, Achievement, Immersion, Creativity | Segmenting features/content |
| Bartle | Achiever, Explorer, Socializer, Killer | Online/social (crude for single-player) |
| Big Five | Openness→sandbox, Conscientiousness→strategy/sim… | Personas, difficulty, tone |
| Flow | Challenge≈skill, clear goals, immediate feedback | Challenge curve, bosses |

**Framework → loop recipe (7 steps):** pick ONE framework → write a 1-line tension ("The player lacks…") → map each motive to 1 design lever → prototype a micro-loop that surfaces the motive ~every 30s → measure KPIs (time-to-first-action, retry rate, session length) → adjust 1 knob per sprint → stop when improvement plateaus.

Extrinsic (XP, loot) is the kindling; intrinsic (curiosity, mastery, meaning) is the fuel. **Overjustification:** is the mechanic still fun without the reward? If retention relies on frustration → the design is serving compulsion.

**Fogg B=MAP:** behavior happens when Motivation, Ability and Prompt are present together. To diagnose bad behavior: *"Which system made this behavior profitable or hard to counter?"*

**Cognitive load:** intrinsic (task complexity — manage it), extraneous (bad UI — eliminate it), germane (learning effort — nurture it). Techniques: progressive disclosure, UI hierarchy, chunking, contextual tutorials. *Structure beats minimalism.*

**Frustration:** productive = constructive ("almost had it") / exploratory (hidden trick); destructive = punitive (lost without knowing why) / accidental (action ≠ intention). Break points: Intention→Behavior ("don't know what to do"), Behavior→Action ("input didn't register"), Action→Feedback ("unfair"), Feedback→Learning ("whatever"). *Good systems make failure informative; bad systems make failure personal.*

## Structure layer

- **Rule** = a condition that allows/forbids/triggers; **Mechanic** = a verb the player uses, built from rules + objects. Rules (atoms) → mechanics (molecules) → systems (ecosystems).
- **Mechanic spec:** Name (verb), Rules, Objects, Input, State checks, Action logic, Output/Feedback, Edge cases.
- **Input / Output / Feedback:** Output = state change (system); Feedback = sensory presentation (player). Perceived fairness depends on I/O quality more than on balance.
- **Game state:** Data (HP=42) ≠ State ("wounded") ≠ Feedback (red flash). Write an *Input → Required State → Result* table; model an FSM with entry/exit + a cue for each state transition. Overlapping booleans → use an enum/FSM.
- **Action logic:** check conditions → apply result → update state → fire event (SFX/anim) → chain the next state/cooldown. *"Action logic defines the truth. Feedback defines the feeling."*
- **Goal / Challenge / Reward** share 3 levers: **When** (timing, rhythm), **Where** (location), **What** (type, form). Challenge ≠ difficulty; it is purposeful tension. Reward loop: Action → Reward → Reinforcement → Re-engagement → Mastery → Deeper reward.

## Cognition layer

UX has 5 aspects: Clarity, Control, Feedback, Rhythm, Emotion. The detailed process is in `gd-ux-audit`.

## Dynamics layer

- Every loop must give the player: something to do **now**, a **next** goal, and a reason to **come back later**.
- Loop scale: Core (seconds–minutes), Mid (minutes–hours), Meta (days–weeks), Emergent (player-created).
- Positive feedback (rewards success, accelerates) vs negative (limits runaway leaders, catch-up).
- Good progression gives the player *more choices*; bad progression = the same gameplay with bigger numbers.
- Regulators in detail: `gd-pacing-progression`, `gd-economy-balance`.

## Perception layer

- **Player fantasy** = Role + Power + Responsibility + Emotion; one fantasy type must dominate (Power, Nurture, Escape, Identity, Survival, Mystery).
- **Theme** must be statable in 1 sentence and felt through actions, not cutscenes. If you can swap the theme without breaking anything → the theme is too shallow.
- **Feedback:** immediate, clear, layered, **proportional to consequence** (boss death > grunt death), consistent.
- **Game feel:** feedback within ~100–200 ms of input (text/turn-based games can accept ≥150 ms but need an immediate cue).
- Narrative & emotion arc in detail: `gd-narrative-design`, `gd-pacing-progression`.
