# Balance math — reference formulas

The ×1.2 section, two-option audit and bottom-up framework come from gamedesign.guide (CC BY 4.0). The remaining formulas are standard industry knowledge (Schreiber & Romero, *Game Balance*), since the site only names them without giving formulas.

## Tier growth
- **Geometric (default):** `value_n = base × r^(n−1)`, r ≈ 1.2. Level 6 ≫ level 1, but 5 vs 6 is still a fair fight.
- **Linear:** `value_n = base + k·(n−1)` — use when you want each step to matter less over time (relative growth rate decreases).
- **Polynomial:** `value_n = a·n^p` (p 1.5–2.5) — a common XP curve.
- Cost should grow slightly faster than power → efficiency (power/cost) declines slightly per tier, creating a choice between "upgrade the old" and "buy the new".

## Diminishing returns & soft cap
- **Hyperbolic:** `effect = x / (x + K)` → 50% effect when x = K; never reaches 100%. Good for dodge %, damage reduction %, crit chance.
- **Soft cap:** `effect = x` when x ≤ C; `C + (x − C)·d` when x > C (d ≈ 0.3–0.5).
- **Log:** `effect = a·ln(1 + x/b)` — grows fast at first, then slows.

## Damage formula
- Subtractive: `dmg = atk − def` → high def can fully negate damage (needs a minimum floor, e.g. `max(dmg, atk·0.1)`).
- Ratio: `dmg = atk × K/(K + def)` → never 0, each point of def has diminishing value. With K = the "standard" def for that tier, 50% reduction.
- Time-to-kill: `TTK = HP / DPS`. Balance roles by TTK, not by individual stats.

## Economy (Source → Pool → Sink)
- **Faucet/sink ratio** per stage = total income / total mandatory spending. <1 → debt (death spiral without catch-up); ≈1.0–1.3 → harsh; >1.5 → abundant, the "harsh" pillar loses its effect.
- **Inflation:** median carry-over rises steadily each stage → add meaningful sinks (long-term investment, cosmetics, base upgrades) or scale costs.
- **Catch-up (negative feedback):** loans, cheap heroes, relief side quests — avoid letting one lost stage lose the whole game.
- **Snowball (positive feedback):** win → reward → stronger → win. Needs a cap or upkeep cost (salary is a natural upkeep cost).

## Sample tier table
| Tier | Cost | Power | Efficiency (P/C) | Notes |
|---|---|---|---|---|

## Bottom-up framework
Atomic unit (1 attack, 1 gold) → resource exchange → system economy → progression pacing → emergent strategy. Balance bottom-up; verify top-down through playtesting.

## Deliberate imbalance
Allowed when the ecosystem can absorb it (a strong weapon with a cost/risk, an SSR hero with an expensive salary). Document it as intentional.

## Balance doc (when a full document is needed)
Exec summary · System overview (flow + key variables) · Player model (archetypes, difficulty curve, reward pacing) · Balance per system (formulas, values, goals) · Math models & cost curves · Analytics/A-B · Feedback loops · Asymmetry & meta (pick rate, counters, buff/nerf log) · Tools · Simulation guidance.
