# Genre levers — the knobs that usually decide balance

Starting points to check a design against, not rules. Every number here is a common practice or rule of thumb; replace it with the project's measured values as soon as there are any. Use the matching section together with the general method in SKILL.md.

## Wave / tower defense
- **Enemy HP vs player income.** HP per wave grows geometrically (about ×1.1–1.2 per wave) while income grows roughly linearly. HP slower than income and damage → the game trivializes after a few waves; much faster → a wall. The player should *almost* afford the answer to each wave.
- **Leaks cost twice:** lives *and* the bounty the enemy would have paid. If leaking only costs lives, letting enemies through is sometimes optimal.
- **Refund on sell** around 70% keeps experimenting cheap without making rebuilds free.
- **Counters over raw stats:** fast, armored, flying and swarm enemies each beat a different build; one build that beats all of them is a dominant strategy.
- **Targeting priority** (first, last, strongest, weakest, closest) often changes play more than damage numbers.
- **Telegraph the next wave** so a hard counter feels fair.
- **"Can this lane hold" math** (damage per second × time in range ≥ enemy HP) ignores enemies overlapping in range; treat it as an upper bound and confirm with a simulation.
- **Rhythm:** spike → breather → spike, never a monotonic ramp (see `gd-pacing-progression`).

## RPG stats and combat
- **Stacking percent bonuses:** decide per layer whether bonuses add (+20% and +30% → ×1.5) or multiply (×1.2 × 1.3 = ×1.56). Add within a layer, multiply between layers, and write the order down.
- **Mitigation** as `defense / (defense + K)` (K about 100 at the scale of early stats) never reaches 100% and gives diminishing returns per point.
- **Variance** around ±10% on damage and a critical multiplier around ×1.5 keep fights readable; wider ranges make planning pointless.
- **Round once**, at the very end of a formula; rounding mid-formula creates breakpoints players will find.
- **XP curves:** linear, quadratic, or exponential with growth about 1.2–1.5 per level. Set a target *time per level* first, then derive the curve from expected XP per minute.

## Roguelike loot and runs
- Give "nothing" and common results most of the weight in drop tables; rare items stay rare only if the common outcome is frequent.
- Gate strong items behind a minimum depth so early runs cannot roll the late game.
- Keep **run state** (resets on death) separate from **profile state** (meta-progression) in data and in the save.
- Meta-progression that makes runs much easier shortens the game; prefer unlocks that widen options over flat power.

## Card games
- **Every threat needs an answer** somewhere in the card pool; a threat with no answer decides games.
- **Mana or energy curve:** count cards per cost; a deck that cannot play anything on early turns feels broken regardless of power.
- **Power budget:** price each effect (damage, draw, tempo) in a shared unit so new cards can be costed against existing ones.

## Survival / crafting
- **The ladder:** each loop (gather → craft → survive) should unlock the next tier; when a tier unlocks nothing new, the game turns into a grind.
- **Threats arrive about when the tools to answer them unlock.** Earlier is unfair, much later is boring.
- Need-decay rates must leave room for the player's own goals between refills; a meter that empties in a couple of minutes turns the game into chores.

## Idle, prestige and cost curves
- **Exponential costs** `cost(n) = base × rate^n`: rates about ×1.07–1.15 for upgrades bought many times, ×1.5–3 only for rare purchases with few levels. A steep rate over many levels explodes (×1.5 over 50 levels ≈ 637 million× the first price). Check with `economy_sim.py growth`.
- **Prestige / new-game-plus loops:** each loop should take only a little longer than the previous one (about ×1.2–1.5). With a bonus that adds `p` per prestige and a target growth `r`, the wait ratio between loops is about `r × (1 + k·p) / (1 + (k+1)·p)`: it starts near `r / (1 + p)` and climbs toward `r`.
- **Offline earnings** at a fraction (about 25–50%) of active income, with a cap (about 8–12 hours), reward returning without making active play pointless.
- **Shown odds equal rolled odds:** build the odds display and the roll from the same weight list; apply luck or pity by producing a new list, never by changing the roll in secret.

Sources: common indie practice and genre playbooks, including awesome-gamedev-agent-skills (gamedev-skills, Apache-2.0) — see the repo's NOTICE.md.
