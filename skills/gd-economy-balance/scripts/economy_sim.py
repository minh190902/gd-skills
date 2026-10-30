#!/usr/bin/env python3
"""Monte Carlo simulator for a stage-based resource economy (sources -> pool -> sinks), plus curve checks.

Three commands:
  sim     python -I economy_sim.py sim model.json [--runs 2000] [--seed 1] [--json] [--strict]
  curve   python -I economy_sim.py curve 150 200 250 300 350 450 550 700 1000 [--band 1.1 1.3] [--strict]
  growth  python -I economy_sim.py growth --base 10 --rate 1.15 --levels 50 [--json]

Exit codes: 0 ok · 1 flags found with --strict (death spiral, no tension, spikes) · 2 bad input.

Model JSON (all amounts per stage cycle; [min, max] = uniform random, number = fixed):
{
  "currency": "gold",
  "start": 300,
  "stages": [
    {"name": "stage_0",
     "sources": {"combat_reward": 150, "loot": [100, 200]},
     "sinks": [
        {"name": "salary",  "amount": [200, 300], "mandatory": true},
        {"name": "repair",  "amount": [50, 100],  "mandatory": false, "priority": 1},
        {"name": "shop",    "amount": [50, 200],  "mandatory": false, "priority": 2}
     ]}
  ]
}
Mandatory sinks are paid first (shortfall = "deficit"); optional sinks are bought in priority
order only if affordable. Each stage may also set "repeat": N to clone it N times.

Reads to look for:
  deficit%      share of runs that cannot cover mandatory costs at that stage (pillar "tight" vs broken)
  optional%     share of optional purchases affordable (≈30-70% = real choices; ~100% = no tension)
  end p10/p50/p90  gold carried into next stage (growing p50 = inflation / hoarding)
curve: ratio of each tier to the previous one against a band (default ×1.1–×1.3 around the ×1.2 rule).
growth: an exponential cost curve cost(n) = base × rate^n — how fast it doubles and where it explodes.
"""
import argparse
import json
import math
import random
import statistics
import sys


class BadInput(Exception):
    pass


def draw(v, rng):
    if isinstance(v, (list, tuple)):
        if len(v) != 2 or v[0] > v[1]:
            raise BadInput(f"range must be [min, max] with min <= max, got {v}")
        return rng.uniform(v[0], v[1])
    return float(v)


def expand(stages):
    out = []
    for s in stages:
        if "name" not in s:
            raise BadInput(f"every stage needs a name: {s}")
        for k in range(int(s.get("repeat", 1))):
            out.append({**s, "name": s["name"] if k == 0 else f"{s['name']}#{k + 1}"})
    return out


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))]


def sim(model, runs, seed):
    if not isinstance(model.get("stages"), list) or not model["stages"]:
        raise BadInput("model needs a non-empty 'stages' list")
    rng = random.Random(seed)
    stages = expand(model["stages"])
    stats = [{"end": [], "deficit": 0, "opt_bought": 0, "opt_total": 0, "income": [],
              "spent": {}} for _ in stages]
    for _ in range(runs):
        pool = float(model.get("start", 0))
        for i, st in enumerate(stages):
            s = stats[i]
            income = sum(draw(v, rng) for v in st.get("sources", {}).values())
            pool += income
            s["income"].append(income)
            short = False
            for sink in st.get("sinks", []):
                if not sink.get("mandatory"):
                    continue
                cost = draw(sink["amount"], rng)
                paid = min(cost, pool)
                short |= paid < cost
                pool -= paid
                s["spent"][sink["name"]] = s["spent"].get(sink["name"], 0) + paid
            s["deficit"] += short
            for sink in sorted((k for k in st.get("sinks", []) if not k.get("mandatory")),
                               key=lambda k: k.get("priority", 99)):
                cost = draw(sink["amount"], rng)
                s["opt_total"] += 1
                if pool >= cost:
                    pool -= cost
                    s["opt_bought"] += 1
                    s["spent"][sink["name"]] = s["spent"].get(sink["name"], 0) + cost
            s["end"].append(pool)

    rows, flags = [], []
    for st, s in zip(stages, stats):
        total_spent = sum(s["spent"].values()) or 1
        top = max(s["spent"].items(), key=lambda kv: kv[1], default=("-", 0))
        deficit = 100 * s["deficit"] / runs
        opt = 100 * s["opt_bought"] / s["opt_total"] if s["opt_total"] else None
        rows.append({"stage": st["name"], "income_p50": statistics.median(s["income"]),
                     "end_p10": pct(s["end"], .1), "end_p50": pct(s["end"], .5), "end_p90": pct(s["end"], .9),
                     "deficit_pct": deficit, "optional_pct": opt,
                     "top_sink": top[0], "top_sink_pct": 100 * top[1] / total_spent})
        if deficit > 25:
            flags.append(f"{st['name']}: deficit {deficit:.0f}% — death spiral risk (need catch-up / negative feedback)")
        if opt is not None and opt > 90 and deficit < 5:
            flags.append(f"{st['name']}: optional {opt:.0f}% affordable, no deficit — economy NOT tight here")
    ends = [statistics.median(s["end"]) for s in stats]
    if len(ends) > 2 and all(b > a for a, b in zip(ends, ends[1:])):
        flags.append("median carry-over grows every stage — hoarding/inflation; add sinks or scale costs")
    return rows, flags


def print_sim(model, runs, rows, flags):
    print(f"# Economy sim — {runs} runs, currency={model.get('currency', 'gold')}, start={model.get('start', 0)}\n")
    print("| Stage | income p50 | end p10 | end p50 | end p90 | deficit% | optional% | top sink |")
    print("|---|---|---|---|---|---|---|---|")
    for r in rows:
        opt = f"{r['optional_pct']:.0f}%" if r["optional_pct"] is not None else "—"
        print(f"| {r['stage']} | {r['income_p50']:.0f} | {r['end_p10']:.0f} | {r['end_p50']:.0f} | "
              f"{r['end_p90']:.0f} | {r['deficit_pct']:.0f}% | {opt} | {r['top_sink']} ({r['top_sink_pct']:.0f}%) |")
    print("\nFlags:")
    for f in flags:
        print(f"- {f}")


def curve(values, lo, hi):
    rows = [{"tier": 1, "value": values[0], "ratio": None, "tag": None}]
    for i in range(1, len(values)):
        if values[i - 1] <= 0:
            raise BadInput("curve values must be positive")
        r = values[i] / values[i - 1]
        rows.append({"tier": i + 1, "value": values[i], "ratio": r,
                     "tag": "ok" if lo <= r <= hi else ("SPIKE" if r > hi else "flat")})
    g = (values[-1] / values[0]) ** (1 / (len(values) - 1)) if len(values) > 1 else None
    return rows, g


def print_curve(rows, g, lo, hi):
    print(f"| Tier | Value | ×prev | vs ×{lo:g}–×{hi:g} band |\n|---|---|---|---|")
    for r in rows:
        if r["ratio"] is None:
            print(f"| 1 | {r['value']:g} | — | — |")
        else:
            print(f"| {r['tier']} | {r['value']:g} | ×{r['ratio']:.2f} | {r['tag']} |")
    if g:
        print(f"\nGeometric mean growth ×{g:.3f} per tier (rule of thumb ×1.2; jumps above the band only at "
              f"deliberate scale leaps)")


def growth(base, rate, levels):
    """cost(n) = base × rate^n. Bands from common practice: ×1.07–1.15 for upgrades bought many times,
    ×1.5–3 only for rare, few-level purchases."""
    if base <= 0 or rate <= 1 or levels < 1:
        raise BadInput("growth needs base > 0, rate > 1, levels >= 1")
    doubling = math.log(2) / math.log(rate)
    marks = sorted({1, 5, 10, 20, 50, 100, levels} & set(range(1, levels + 1)) | {levels})
    rows = [{"level": n, "cost": base * rate ** n, "x_level0": rate ** n} for n in marks]
    warnings = []
    if rate >= 1.5 and levels > 20:
        warnings.append(f"rate ×{rate:g} over {levels} levels: the last level costs ×{rate ** levels:,.0f} the first; "
                        f"keep steep rates for rare purchases with few levels")
    if rate < 1.05:
        warnings.append(f"rate ×{rate:g} barely grows: costs double only every {doubling:.0f} levels; "
                        f"income growth will outrun it (check with the sim)")
    return {"base": base, "rate": rate, "levels": levels, "doubles_every": doubling, "rows": rows,
            "warnings": warnings}


def print_growth(r):
    print(f"# Cost curve — cost(n) = {r['base']:g} × {r['rate']:g}^n\n")
    print(f"Doubles every {r['doubles_every']:.1f} levels.\n")
    print("| Level | Cost | × level 0 |\n|---|---|---|")
    for row in r["rows"]:
        print(f"| {row['level']} | {row['cost']:,.0f} | ×{row['x_level0']:,.1f} |")
    print("\nFlags:")
    for w in r["warnings"]:
        print(f"- {w}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a1 = sub.add_parser("sim")
    a1.add_argument("model")
    a1.add_argument("--runs", type=int, default=2000)
    a1.add_argument("--seed", type=int, default=1)
    a2 = sub.add_parser("curve")
    a2.add_argument("values", type=float, nargs="+")
    a2.add_argument("--band", type=float, nargs=2, default=[1.1, 1.3], metavar=("LO", "HI"))
    a3 = sub.add_parser("growth")
    a3.add_argument("--base", type=float, required=True)
    a3.add_argument("--rate", type=float, required=True)
    a3.add_argument("--levels", type=int, default=50)
    for p in (a1, a2, a3):
        p.add_argument("--json", action="store_true")
        p.add_argument("--strict", action="store_true", help="exit 1 when any flag is raised")
    a = ap.parse_args()
    try:
        if a.cmd == "sim":
            try:
                with open(a.model, encoding="utf-8") as f:
                    model = json.load(f)
            except (OSError, ValueError) as e:
                raise BadInput(f"cannot read model {a.model}: {e}")
            rows, flags = sim(model, a.runs, a.seed)
            out = {"tool": "economy_sim", "command": "sim", "runs": a.runs, "seed": a.seed, "stages": rows,
                   "flags": flags}
            if not a.json:
                print_sim(model, a.runs, rows, flags)
        elif a.cmd == "curve":
            rows, g = curve(a.values, *a.band)
            flags = [f"tier {r['tier']}: ×{r['ratio']:.2f} {r['tag']}" for r in rows if r["tag"] == "SPIKE"]
            out = {"tool": "economy_sim", "command": "curve", "band": a.band, "tiers": rows,
                   "geometric_growth": g, "flags": flags}
            if not a.json:
                print_curve(rows, g, *a.band)
        else:
            out = growth(a.base, a.rate, a.levels)
            flags = out["warnings"]
            out = {"tool": "economy_sim", "command": "growth", **out, "flags": flags}
            if not a.json:
                print_growth(out)
    except BadInput as e:
        print(f"bad input: {e}", file=sys.stderr)
        sys.exit(2)
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    sys.exit(1 if a.strict and flags else 0)


if __name__ == "__main__":
    main()
