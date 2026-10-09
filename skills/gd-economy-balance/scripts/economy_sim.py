#!/usr/bin/env python3
"""Monte Carlo simulator for a stage-based resource economy (sources -> pool -> sinks).

Two commands:
  sim    python -I economy_sim.py sim model.json [--runs 2000] [--seed 1]
  curve  python -I economy_sim.py curve 150 200 250 300 350 450 550 700 1000

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
"""
import argparse
import json
import random
import statistics
import sys


def draw(v, rng):
    if isinstance(v, (list, tuple)):
        return rng.uniform(v[0], v[1])
    return float(v)


def expand(stages):
    out = []
    for s in stages:
        for k in range(int(s.get("repeat", 1))):
            out.append({**s, "name": s["name"] if k == 0 else f"{s['name']}#{k + 1}"})
    return out


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))]


def sim(model, runs, seed):
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

    cur = model.get("currency", "gold")
    print(f"# Economy sim — {runs} runs, currency={cur}, start={model.get('start', 0)}\n")
    print("| Stage | income p50 | end p10 | end p50 | end p90 | deficit% | optional% | top sink |")
    print("|---|---|---|---|---|---|---|---|")
    for st, s in zip(stages, stats):
        total_spent = sum(s["spent"].values()) or 1
        top = max(s["spent"].items(), key=lambda kv: kv[1], default=("-", 0))
        opt = 100 * s["opt_bought"] / s["opt_total"] if s["opt_total"] else float("nan")
        print(f"| {st['name']} | {statistics.median(s['income']):.0f} | {pct(s['end'], .1):.0f} | "
              f"{pct(s['end'], .5):.0f} | {pct(s['end'], .9):.0f} | {100 * s['deficit'] / runs:.0f}% | "
              f"{opt:.0f}% | {top[0]} ({100 * top[1] / total_spent:.0f}%) |")
    print("\nFlags:")
    for st, s in zip(stages, stats):
        d = 100 * s["deficit"] / runs
        opt = 100 * s["opt_bought"] / s["opt_total"] if s["opt_total"] else None
        if d > 25:
            print(f"- {st['name']}: deficit {d:.0f}% — death spiral risk (need catch-up / negative feedback)")
        if opt is not None and opt > 90 and d < 5:
            print(f"- {st['name']}: optional {opt:.0f}% affordable, no deficit — economy NOT tight here")
    ends = [statistics.median(s["end"]) for s in stats]
    if len(ends) > 2 and all(b > a for a, b in zip(ends, ends[1:])):
        print("- median carry-over grows every stage — hoarding/inflation; add sinks or scale costs")


def curve(values):
    print("| Tier | Value | ×prev | vs ×1.2 rule |\n|---|---|---|---|")
    for i, v in enumerate(values):
        if i == 0:
            print(f"| 1 | {v:g} | — | — |")
            continue
        r = v / values[i - 1]
        tag = "ok" if 1.1 <= r <= 1.3 else ("SPIKE" if r > 1.3 else "flat")
        print(f"| {i + 1} | {v:g} | ×{r:.2f} | {tag} |")
    if len(values) > 1:
        g = (values[-1] / values[0]) ** (1 / (len(values) - 1))
        print(f"\nGeometric mean growth ×{g:.3f} per tier (rule of thumb ×1.2; jumps >×1.3 only at deliberate scale leaps)")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a1 = sub.add_parser("sim"); a1.add_argument("model"); a1.add_argument("--runs", type=int, default=2000)
    a1.add_argument("--seed", type=int, default=1)
    a2 = sub.add_parser("curve"); a2.add_argument("values", type=float, nargs="+")
    a = ap.parse_args()
    if a.cmd == "sim":
        with open(a.model, encoding="utf-8") as f:
            sim(json.load(f), a.runs, a.seed)
    else:
        curve(a.values)


if __name__ == "__main__":
    main()
