---
name: gd-core
description: Game design lens, project setup and router for the gd-* skills. Use whenever a request involves game design thinking rather than pure coding — brainstorming a mechanic or system, "should we add X", "why is this not fun", choosing between design options, defining pillars or the core loop, writing a 1-pager/concept — and when a game has no docs/design/PROJECT.md yet (set it up). Routes to gd-status, gd-design-review, gd-unstuck, gd-feature-spec, gd-feature-audit, gd-narrative-design, gd-economy-balance, gd-pacing-progression, gd-ux-audit, gd-playtest, gd-game-analysis.
---

# GD Core — design lens, project setup, routing

The shared foundation for every `gd-*` skill. Based on the **Game Map** model from gamedesign.guide (see [SOURCES.md](SOURCES.md)).

## 1. Project conventions (every gd-* skill relies on these)

Each game has a **design dir**: `<game_root>/docs/design/` (game_root = the folder containing `project.godot`, or the game's root for other engines).

| File | Role |
|---|---|
| `PROJECT.md` | Identity, fantasy, pillars, core loop, platform constraints, data locations, known risks. **Read it before giving any design opinion.** |
| `STATE.md` | Where we are, what's next, open questions, parking lot (`gd-status`) |
| `DECISIONS.md` | Settled decisions and their rationale (`gd-design-review`, `gd-unstuck`) |
| `SYSTEMS.md` | Purpose of each system + map of who writes/reads state (`gd-design-review`) |
| `gd.config.json` | Configuration for the scripts (state owners, flag functions…) |

Skill output docs live next to the design dir: `<game_root>/docs/{specs,audits,narrative,balance,ux,playtest,analysis}/`.

**Finding the design dir:** search for `**/docs/design/PROJECT.md`. With several games (monorepo), pick the game matching the file/folder under discussion; if unclear, ask.

**No design dir yet → set it up:**
1. Create `<game_root>/docs/design/`, then copy the files in [templates/project/](templates/project/) into it (skip `CLAUDE.snippet.md`). Do not overwrite existing files.
2. Fill in `PROJECT.md` from the GDD/README/code. Where information is missing, write "TODO — ask the user"; do not invent.
3. Adjust `gd.config.json` to the actual code: state owners (autoloads holding state), instance owners (Resources such as HeroData), names of the set/check flag functions.
4. Run `system_map.py` (part of gd-design-review) to fill the auto-generated part of SYSTEMS.md. Write the "Purpose" section from the header comment of each file.
5. Fill in STATE.md from recent `git log` and existing TODOs.
6. Offer to add `templates/project/CLAUDE.snippet.md` to the repo's CLAUDE.md (replacing `{{DESIGN_DIR}}`) so the rules are always applied.

## 2. Routing

| The user wants to… | Use |
|---|---|
| Start/end a session, "where are we", "what's next" | `gd-status` |
| Propose an idea, change gameplay / story / a system | `gd-design-review` (**always run before building**) |
| Untangle confusion, too many questions, doesn't know where to start | `gd-unstuck` |
| Design a new feature before coding | `gd-feature-spec` |
| Evaluate an existing feature: keep, merge or cut | `gd-feature-audit` |
| Story, choice & consequence, dialogue, quests | `gd-narrative-design` |
| Currency, prices, rewards, stats, difficulty in numbers | `gd-economy-balance` |
| Pacing, unlock order, tutorial/FTUE, difficulty curve | `gd-pacing-progression` |
| A confusing or cluttered screen/flow, missing feedback | `gd-ux-audit` |
| Plan a test, process feedback | `gd-playtest` |
| Analyze a reference game / competitor | `gd-game-analysis` |
| An open design question that fits no category yet | Continue with this skill (Sections 3–5) |

Typical chain: design-review → feature-spec → economy-balance → playtest → status.

## 3. Game Map — 5 layers for thinking about any problem

| Layer | Question | Components |
|---|---|---|
| **Player** | Why does the player act? | Context → Need → Conflict/Gap → Motivation → Intention → Behavior; cognitive load, flow, frustration |
| **Structure** | What is possible? | Rules, game objects, mechanics (Input→State→Action logic→Output), goals/challenges/rewards |
| **Cognition** | Can the player understand and act? | UX, UI, clarity mapping, affordance, tutorial |
| **Dynamics** | How does the system behave over time? | Core / meta / emergent loop; regulators: progression, complexity curve, pacing, balance |
| **Perception** | How is the system *felt*? | Setting, theme, narrative, game feel, emotion arc, player fantasy, feedback |

Layer details, motivation models (SDT, Quantic Foundry, Flow, B=MAP) and gap types: [references/game-map.md](references/game-map.md).

**Diagnosis:** go from Player to Perception, find the *first* layer that breaks and fix it at that layer. Don't fix a Cognition problem by adding a new system (Structure layer).

## 4. Five questions for every proposal

1. Which player need/motivation is tied to which specific mechanic?
2. Do the rules, goals and rewards fit together?
3. Does the UX/UI keep cognitive load low, within the platform constraints in PROJECT.md?
4. Can the loops and regulators tune challenge rhythm and depth?
5. Does the presentation amplify emotion and the player fantasy?

Two scope filters: **a feature that serves no pillar is scope creep**, and **a system that serves neither autonomy, competence nor relatedness is suspect**.

## 5. Designing backward from the experience

1. Write the desired experience in 1 sentence.
2. List the *verbs* that let the player feel it.
3. Define rules, inputs, goals and rewards so those verbs matter.
4. Build loops with escalating and releasing tension.
5. Set system outputs and consequence triggers.
6. Attach the expression: visuals, audio, text, symbols.
7. Design feedback that reinforces the emotional flow.

## 6. Pillars, 1-pager, concept doc

Use when creating a new game or redefining pillars: [references/pillars-and-concept.md](references/pillars-and-concept.md).

## 7. Working principles

- **A doc must help someone implement, test or challenge it.** Write each system in 3 layers: Intention → Functionality → Parameters.
- **Prototype the risky part first.** A minimal spec of about 1 page, build a rough version, observe, then write the full spec.
- **Analysis must lead to action:** end with concrete changes that can be written as sprint tickets.
- **Recommend one option**; don't ramble through a list.
- Write design docs in the language the user works in, keeping standard English game-design terms.
