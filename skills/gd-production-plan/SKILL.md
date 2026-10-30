---
name: gd-production-plan
description: Production planning for small and solo game teams — scope inventory (count every level, character, event, enemy, screen, asset, line), time estimates from measured unit costs, milestones, MoSCoW cut list, risk register, money budget and runway, and re-estimation at every gate. Use when the user asks "how long will this take", "is this scope realistic", "can I finish this alone", "plan the milestones", "what should we cut", when entering Pre-production or finishing a Vertical Slice, when milestones slip, or when the design keeps adding content without anyone counting the cost.
---

# GD Production Plan — can we actually build this?

Role: the producer who counts. Designers add; this skill adds up. Output lives in `<game_root>/docs/production/plan.md` (template: [templates/production-plan.md](templates/production-plan.md)). Read `PROJECT.md` (business targets: time and money budget, intended length, price) and `ROADMAP.md` first.

Principle: **an estimate without a measured unit cost is a guess.** Label every number MEASURED (timed on real work), ESTIMATED (reasoned), or GUESS. First-time estimates are commonly short by 1.5–3×; plan for it explicitly instead of hoping.

## When not to use
- Which stage the project is in and what its gate needs → `gd-pipeline`.
- Whether a single feature is worth keeping → `gd-feature-audit`.

## Workflow A — Scope inventory
1. Read the design docs and list every **content unit type**: levels/maps, encounters/waves, enemy types, characters, events/storylets, dialogue lines or words, items, UI screens, systems, art assets (by kind), animations, music tracks, SFX, tutorial steps, localization words.
2. Count each from the docs. Where the docs give no number, write "unknown" and ask; do not invent.
3. Split each type into **Must / Should / Could** (MoSCoW) against the pillars (`gd-core` §4 scope filters). Anything serving no pillar starts as Could.
4. Flag the 3 biggest types by total effort; they are where scope decisions matter.

## Workflow B — Estimate
1. For each unit type, find the unit cost (hours per unit, including iteration):
   - MEASURED from the vertical slice or prototype if possible (time it: build 2–3 units, take the median);
   - otherwise ESTIMATED as a range (low–high), and mark the type as a risk.
2. Total = Σ (count × unit hours) for Must + Should, then add buffers as separate lines:
   - integration and bug fixing: +30–50%;
   - polish, balance, playtest-driven rework: +20–40%;
   - non-dev work for a solo developer (marketing, community, admin, store, builds): commonly 15–30% of the week.
3. Convert to calendar: effective hours/week = planned hours × focus factor (0.6–0.8 is realistic; sick days, life, context switches). Months = total / (effective hours × 4.3).
4. Compare with the time budget and launch window in PROJECT.md. Report the gap as a single number: "plan is X months over/under budget".

## Workflow C — Cut until it fits
When the estimate exceeds the budget:
1. Cut Could items first, then reduce **counts** of the biggest unit types (fewer levels with more reuse beats fewer systems), then simplify systems, then cut whole systems (`gd-feature-audit`).
2. Never cut what the pillars and the validated core loop depend on; cut breadth before depth.
3. Quick triage for each remaining item, in order: does the core loop work without it? → move it later. Would a player notice it missing? → if not, cut. When unsure, the default answer is cut.
3. Prefer reuse multipliers: systemic content (procedural, rule-driven events, combinable parts) over hand-authored content when the team is one person.
4. Record each cut in DECISIONS.md and in the plan's cut list with the hours saved.
5. Stop when Must + Should + buffers fit within ~85% of the time budget (leave slack).

## Workflow D — Milestones
1. Milestones of 2–6 weeks. Each ends with a **playable build** and a short playtest; name each by what the player can do ("I can play chapter 1 end to end"), not by tasks.
2. Order: riskiest and most-shared work first; content that depends on unsettled systems last.
3. Map milestones onto the pipeline stages (`gd-pipeline`) and the commercial track dates (store page, festivals, launch window from `gd-go-to-market`).
4. Keep at most the current and next milestone detailed; later ones stay coarse.

## Workflow E — Risk register
Top 5–8 risks: description · likelihood (L/M/H) · impact (L/M/H) · early warning sign · mitigation · decision date. Typical solo risks: scope, art pipeline cost, burnout, a key system not fun, engine/tech unknowns, market timing, money runway. Review at every gate.

## Workflow F — Money budget and runway
1. List costs: tools and licenses, purchased or contracted assets (art, music, SFX), store fees, localization, trailer/capsule art, marketing, festival or event costs, hardware, legal/accounting.
2. List income/runway: savings, job, grants, publisher advance. Months of runway = available money / monthly burn.
3. If runway < time estimate: cut scope, find funding (publisher with the vertical slice, grants), or change the work schedule. State it plainly; this is the user's decision.
4. **Production method per asset kind, decided by Concept** (art, animation, music, SFX, voice, localization): self-made, AI-assisted, purchased or free-licensed packs (CC0), contracted, or generated in code. Write it in PROJECT.md business targets. When the money budget is zero, every plan item that assumes paying someone is a risk: list those items, propose the no-cost method, and re-estimate its unit cost with a measured sample.

## Workflow G — Re-estimate (every gate and every milestone)
1. Replace estimates with actual hours where work is done; recompute the remaining total.
2. If two milestones in a row slip by > 50%, run Workflow C before continuing.
3. Update ROADMAP.md (stage gate items "plan fits the budget") and add one line to STATE.md.

## Output rules
- Lead with the verdict: **fits / over by X months / unknown because Y**, then the table.
- Every number carries its label (MEASURED / ESTIMATED / GUESS).
- End with one recommended cut or action, not a menu.
