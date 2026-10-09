---
name: gd-economy-balance
description: Economy and balance design — resource sources/sinks, currency flow, upkeep and cost tuning, tier/cost curves, unit/enemy stat scaling, "is this too easy/hard/strong", dominant strategies. Use when changing gameplay numbers in data/resources, designing a new currency/cost/reward, reviewing difficulty or power curves, or checking whether the economy matches the design intent in PROJECT.md. Includes economy_sim.py (Monte Carlo economy per stage + ×1.2 curve check).
---

# GD Economy & Balance

Balance is *"making every choice worth considering"*: a dynamic equilibrium that depends on perception and changes over time. The goal is not to make everything equal. Read `PROJECT.md` for the design intent, e.g. a "harsh" or "generous" economy, because that is the yardstick for judging the numbers.

## Tools
`<skill_dir>` is the directory containing this skill.
```bash
python -I <skill_dir>/scripts/economy_sim.py sim <model.json> --runs 2000   # Monte Carlo: sources → pool → sinks, per stage
python -I <skill_dir>/scripts/economy_sim.py curve 150 200 250 300 350       # compare growth between tiers against the ×1.2 rule
```
Model format: see the script's docstring and [examples/sample_model.json](examples/sample_model.json). That example is for illustration only; **always use numbers taken from the real code**. Save the project's model under `<game_root>/docs/balance/` so it can be rerun later.

## Workflow

### 1. Define the balance question
Write it as one sentence, e.g. "In the mid-game, does the player have to drop one expense every stage?" or "Is a rare unit always better than 2 common units?". Pick the **balance type**: mathematical, perceived, strategic, or experiential.

### 2. Take real numbers from code, don't guess
Find every source, sink and formula in data/Resources and code. Record them as a **Source · Pool · Sink · Scarcity type** table, each number with its file:line. `system_map.py --impact <currency>` (part of gd-design-review) lists every system that changes a given currency.

### 3. Model it
- **Economy:** write a JSON model and run `sim`. Read 3 metrics:
  - `deficit%`: the rate of being unable to pay mandatory costs.
  - `optional%`: the rate of being able to afford optional sinks.
  - The amount of currency carried into the next stage (p50).

  Starting point for a "harsh but fair" economy: deficit 5–20% on hard stages, optional 30–70%, and carry-over that does not grow steadily across every stage. This is a starting point for playtesting, not the truth.
- **Curves:** run `curve` for each tier sequence (rewards, prices, HP, power). The rule of thumb is roughly ×1.2 growth per tier. Jumps larger than ×1.3 should only be intentional (new chapter, boss encounter).
- **Power and choice:** write formulas and a tier table with columns cost · power · efficiency (power/cost). See [references/balance-math.md](references/balance-math.md) for diminishing returns, soft caps, sources/sinks, feedback loops.

### 4. Check for dominant strategies
- **Compare two competing options:** for each option, note power, limits and playstyle. Is any option practically mandatory? Is any option useless?
- List **positive feedback** loops (rich get richer) and **negative feedback** loops (catch-up mechanics). Flag any loop that could spiral out of control or be exploited.
- Prefer soft counters over hard blocks.

### 5. Propose changes
Build a table: Parameter · Old value · New value · File · Reason · Sim result before/after. **Change only one parameter group at a time** so the impact is measurable. Rerun the sim to prove the change hits the goal. Write to `<game_root>/docs/balance/<YYYY-MM-DD>-<topic>.md`. Major changes go through `gd-design-review` and are recorded in DECISIONS.md.

### 6. Validate
Spreadsheet numbers are only hypotheses. Playtesting is needed to confirm them (`gd-playtest`, Balance goal category). If a formula changes, add or update tests.

## Checklist
- [ ] Every core option is worth choosing in *some context*
- [ ] No option is mandatory
- [ ] Can be countered with skill or planning
- [ ] Rewards are proportional to effort
- [ ] Still fair when the player fails (there is a way out of a losing spiral)
- [ ] Every source has a matching sink; carry-over does not inflate
- [ ] Numbers come from code with file:line, and the sim was rerun after changes
- [ ] Monetization does not break pillars: no pay-to-win, odds are disclosed
