---
name: gd-feature-spec
description: Write a buildable design spec for a new game feature, mechanic or system BEFORE implementing it (Intention → Functionality → Parameters, state table, edge cases, dependencies, KPIs, validation plan). Use when the user asks to add/design/plan a feature, start a new sprint item, "build feature X", "add system Y" (in any language), or when a request to code a gameplay feature has no spec yet. Produces a spec file under docs/specs that maps to data resources and code.
---

# GD Feature Spec

Goal: a spec that **devs can implement without asking back, designers can challenge, and QA can test edge cases from**. Don't write a novel: about 1 page is enough for a prototype; write it out in full once the system has stabilized.

## Process

### 0. Gather context (required)
- Read `PROJECT.md` and `SYSTEMS.md` in the design dir (convention in `gd-core`).
- Has the idea been through `gd-design-review`? If not, run the review first.
- Grep the related code and data: is there already a system doing something similar? **If an existing system already covers about 70% of the need, propose extending it instead of adding a new one.**
- Read the related GDD/PRD (location listed in PROJECT.md).

### 1. Intention (why it exists)
- **Player problem** the feature solves (which need/gap in the Game Map)? Why *now*?
- **Pillar** it serves (at least 1; if none, stop and flag it as scope creep).
- **Desired experience** in 1 sentence, and the **behavior** you want to encourage.
- **Fantasy check:** does the feature strengthen or weaken the player fantasy in PROJECT.md?

### 2. Functionality (how it works)
- **Interaction loop** in the form `Action → Feedback → Gain/Spend/Unlock`, connected to the meta loop.
- **Feature block** for each action: *Goal · Conditions · Player input · System response · Edge cases*.
- **State table:** `Input → Required state → Result`. With 3 or more states, use an FSM and note entry/exit and a cue for each transition. Avoid overlapping booleans.
- **Action logic** in order: check conditions → apply result → update state → emit event/signal → chain to the next step or a cooldown.
- **Feedback** at 3 levels (small / standard / big), with intensity proportional to the consequence, and where it is shown on screen.
- **Failure conditions**, and how failure teaches the player something instead of punishing them for no reason.
- **Rule transparency:** what the player can see, and what is deliberately hidden.

### 3. Parameters (numbers)
Parameter table with: starting value, unit, valid range, and **where it lives in code/data** (Resource, config). Do not hard-code numbers in logic. For parameters that scale by tier, use the ×1.2/tier rule as a starting point (see `gd-economy-balance`).

### 4. Dependencies & risks
- A **System · Change type · Risk level** table: new signals/events, save/load, dialogue, UI.
- Run `system_map.py --impact` (part of gd-design-review) for each state variable touched, and **write the list of affected readers into the spec**.
- **Save/Load:** any state that needs to persist must be serialized, with a migration for old saves.
- **Narrative hooks:** flags or bridge functions so dialogue can react to the feature.
- **Intent vs actual impact:** how could players optimize away the design intent?

### 5. Validation
- **KPIs / signals:** measurable, relevant, time-bound. If there is no telemetry yet, use playtest observation and unit tests for the logic.
- **Hypothesis · How to test · Threshold · Fallback.**
- **Iteration plan:** v0.1 (rough prototype, proves the feel) → v0.3 → v0.6 → v1.0.
- **Test cases to write**, at least one test per edge case.

### 6. Write the file and hand off
- Save to `<game_root>/docs/specs/<feature-kebab>.md` following [templates/feature-spec.md](templates/feature-spec.md). Changelog at the top of the file, tagged `WIP`/`Final`, with an "Open questions" section.
- Finish with an **implementation task list** following the project's coding standards (listed in PROJECT.md), then ask the user whether to start.

## Quality checklist
- [ ] Solves a defined problem, tied to a pillar
- [ ] Intention, Functionality and Parameters kept separate
- [ ] Every input has an output and feedback; edge cases handled (spam, insufficient resources, object deleted mid-action, save/load mid-action)
- [ ] Does not duplicate an existing system, or explains why
- [ ] Readers of shared state are listed and checked
- [ ] Parameters live in data/config and have valid ranges
- [ ] Impact on UX (cognitive load on the platform), economy and balance assessed
- [ ] Has a validation plan and an iteration plan
- [ ] Devs can implement without asking; QA can write tests

**Tip:** use the spec itself as the prompt for generating code. If the generated code needs a lot of fixing, the spec is missing something.
