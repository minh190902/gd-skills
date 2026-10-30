---
name: gd-prototype
description: Plan, build and judge a game prototype that answers one design question — prototype brief, timebox, throwaway vs keep, greybox, instrumenting, keep/kill/refactor criteria written before building, targeted self-test sessions, bot or simulation runs on the real rules, rule switches with a parity baseline, and the keep-means-rewrite rule. Use when the user wants to prototype a mechanic or core loop, "is this fun", "just get something playable", greybox or paper-prototype an idea, test a rule change in a living prototype, decide whether to keep or kill a prototype, or is in the Find the Fun stage. Not for the playtest plan with outside testers (gd-playtest) or the full spec of a validated feature (gd-feature-spec).
---

# GD Prototype — answer one question, cheaply, then decide

The output of a prototype is a **decision** (keep / kill / refactor), not a product. Optimize for how fast you learn. Most prototypes fail in one of three ways: they test everything at once, they never get a written kill criterion, or the spike quietly becomes the shipping code.

Design dir convention: see `gd-core`. Stage context: `gd-pipeline` (this skill does the work of stage 2, Find the Fun, and the prototype parts of stage 3, Validate).

## When not to use
- Playtests with other people (plan, criteria, tester types, triage) → `gd-playtest`.
- A feature that already passed its prototype and needs a buildable spec → `gd-feature-spec`.
- Tuning numbers in an economy model → `gd-economy-balance` (this skill only says when a bot run is the right test).

## Workflow A — Before building: the brief

Copy [templates/prototype-brief.md](templates/prototype-brief.md) to `<game_root>/docs/prototypes/<YYYY-MM-DD>-<name>.md` and fill it **before writing code**:

1. **One question**, as close to yes/no as possible: *"Is choosing which of two failing districts to save each turn tense, not tedious?"* Two questions → two prototypes. The riskiest question of the project (ROADMAP gate 2) comes first.
2. **Core verb**: the one action the player repeats. Everything else is stubbed.
3. **Throwaway or keep** — decide now. Throwaway: hard-code freely, delete after. Keep: still rough, but names and folders you can grow. Default to throwaway.
4. **Timebox**: 30–90 minutes for a mechanic spike, a few sessions for a core-loop prototype. When it runs out, judge what exists.
5. **Medium**: the cheapest that answers the question — paper, spreadsheet, HTML page, greybox in an engine. Fun questions need real-time feel only when the verb is about feel.
6. **Keep / kill / refactor criteria**, written and dated now, as observable signals (examples in the template). Criteria written after playing get bent to fit the result.

## Workflow B — Build

- **Greybox everything the question does not depend on**: shapes for art, built-in fonts, no menus, no save system, no audio unless the question is about audio.
- **Instrument for the question**: on-screen debug values for what you are judging (timings, resources per turn, decisions per minute), and a log or a copyable run report so a session can be reviewed later.
- **Fixed seeds** for anything random, recorded in every test log, so a surprising run can be replayed.
- **Contain it**: a separate folder or project that the real game never imports.

## Workflow C — Test it yourself, then with bots

1. **Self-play log** (`docs/playtest/<date>-selftest.md`): after each session, what was fun, what was boring, what you changed, the seed and build. Gate 2 asks for about ten sessions.
2. **Targeted sessions**: build start points that jump straight to the part under test (a debug start, a prepared save, a URL parameter). Ten full replays of content you already know measure your boredom with the content, not the loop.
3. **Familiarity fatigue vs loop fatigue**: being bored after several replays is normal for the person who made it. Tell them apart by what changed: if decisions per minute drop in the parts you know by heart, it is familiarity; if you stop caring even in a fresh targeted scenario, it is the loop. Strangers in Validate answer this better than you can.
4. **Bots and simulations on the real rules** (different strategies such as optimizer, newcomer, random; many seeds; a table per run) measure **balance and exploits, never fun**. Use them to find dominant strategies, death spirals and pacing numbers; use people for feel and interest.
5. **AI agents as testers** can report clarity problems (what was unclear, where they got stuck) on a text or screenshot build. They cannot judge fun or taste; treat them like a blind internal tester.

## Workflow D — Change rules in a living prototype

When the prototype has become the place where rules evolve (common in Find the Fun):
- Put each rule change behind a **switch** (a config flag) so the old and new rule can both run.
- Keep a **parity baseline**: a frozen copy of the earlier version, or recorded runs on fixed seeds, and a test that the switch-off path still matches it. Without it, you cannot tell whether a change made the game better or just different.
- Compare old vs new with the same seeds and bot strategies, then with a person.
- Record the switch and its result in DECISIONS.md; remove dead switches when a rule is settled.

## Workflow E — Decide

Judge against the criteria written in the brief, not against how much work went in:

| Verdict | When | Next |
|---|---|---|
| **Keep** | the keep signal appeared without explaining the game | Write the full spec (`gd-feature-spec`); **rewrite** in the real project — a keep authorizes a rewrite, not a copy of the spike |
| **Refactor** | one variable is clearly off (too slow, window too tight) | Narrow the question, retune, test again within a new timebox |
| **Kill** | the verb only works after explanation, or needs systems far beyond the prototype, or art is being added to hide a flat verb | Log the lesson in DECISIONS.md and move on |

Exception to the rewrite rule: a deliberately throwaway web or desktop build may serve as the Validate build if it is clearly labeled a prototype; it still does not become production code.

## Rules
- The question decides the scope. A feature that does not serve the question is cut; when unsure, the default answer is cut.
- Feature triage while building: does the loop work without it? → later. Would a tester notice it missing? → if not, cut. Under 30 minutes and needed for the question? → do it.
- Polish hides problems. No final art, no juice, no menus until the verb proves itself.
- One outside player without coaching tells you more than an hour of self-play. Do it as soon as the loop runs end to end (`gd-playtest`).
