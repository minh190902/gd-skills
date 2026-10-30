#!/usr/bin/env python3
"""Static audit for Nathan Hoad Dialogue Manager (.dialogue) content in a Godot project.

Finds the narrative bugs that playtests miss:
  - flags SET but never READ          -> consequence that never pays off (choice illusion?)
  - flags READ but never SET          -> unreachable branch / typo
  - jumps (=> x) to undefined titles   -> runtime error
  - titles never jumped to             -> orphan content (unless an entry point)
  - choices with no mechanical effect  -> cosmetic choice (fine only if intentional)
  - a Choice & Consequence table (every `do` / `set` under each option)

Usage (game_root = folder containing project.godot, or any game root when flag_sources is set):
  python -I dialogue_audit.py <game_root> [--stage NAME] [--json] [--strict] [--config PATH]
  --stage filters the choice table to files whose name contains NAME (e.g. "stage_3")
Exit codes: 0 ok · 1 broken jumps (with --strict also flag problems and orphan titles) ·
2 game root missing, or no .dialogue files and no flag_sources.

Config: <game_root>/docs/design/gd.config.json, keys used here (all optional):
  "flag_set_fns":  ["set_flag"]                               function names that set a flag
  "flag_read_fns": ["check_flag", "get_flag", "get_flag_value"]
  "entry_title_patterns": ["^start$", "_intro$"]               titles entered from code
  "ignore_dirs": ["addons", ".godot", "test", "tests"]
Flags kept in code or data (any engine, no .dialogue needed), one capture group = the flag name:
  "flag_sources":       ["src/**/*.ts", "data/**/*.json"]          globs relative to the game root
  "flag_set_patterns":  ["\\\\bS\\\\.f\\\\.(\\\\w+)\\\\s*(?:[-+*/]?=(?!=)|\\\\+\\\\+|--)"]   S.f.x = 1, +=, ++ (JSON-escaped)
  "flag_read_patterns": ["\\\\bS\\\\.f\\\\.(\\\\w+)\\\\b"]
A flag also counts as READ when its name appears as a string literal in any .gd/.tres file
(registries often store flag names as data). Dynamic names ("x_%d") must be checked by hand.
"""
import argparse
import json
import re
import sys
from pathlib import Path

RE_TITLE = re.compile(r"^~\s+(\S+)")
RE_JUMP = re.compile(r"=><?\s*(\S+)")
RE_CHOICE = re.compile(r"^(\s*)-\s+(.*)$")
RE_EFFECT = re.compile(r"^\s*(?:do|set)\s+(.+)$")
RE_LITERAL = re.compile(r"\"([A-Za-z_][A-Za-z0-9_]+)\"")


def load_config(root, path):
    p = Path(path) if path else root / "docs" / "design" / "gd.config.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def short_effect(expr):
    expr = re.sub(r"^[A-Z]\w*\.", "", expr.strip())       # drop "Bridge." prefix for readability
    return expr[:70]


def parse_dialogue(path, re_set, re_read):
    titles, jumps, sets, reads, choices, effect_titles = {}, [], [], [], [], set()
    current_title, current_choice = None, None
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if raw.lstrip().startswith("#") and not raw.lstrip().startswith("#{"):
            continue
        line = raw
        if m := RE_TITLE.match(line):
            current_title, current_choice = m.group(1), None
            titles[current_title] = i
            continue
        if m := RE_CHOICE.match(line):
            indent, text = m.groups()
            current_choice = {
                "file": path.name, "line": i, "title": current_title,
                "text": re.sub(r"\s*\[if [^\]]*\]", "", text).strip()[:90],
                "conditional": "[if " in text, "indent": len(indent.expandtabs(4)),
                "effects": [], "jump": None,
            }
            choices.append(current_choice)
            for f in re_set.findall(text):          # flags in the option line itself, e.g. [if check_flag("x")]
                sets.append((f, path.name, i))
            for f in re_read.findall(text):
                reads.append((f, path.name, i))
            jm = RE_JUMP.search(text)              # inline "- option => title"
            if jm:
                jumps.append((jm.group(1), path.name, i))
                current_choice["jump"] = jm.group(1)
            continue
        if current_choice is not None and line.strip():
            ind = len(line[: len(line) - len(line.lstrip())].expandtabs(4))
            if ind <= current_choice["indent"]:
                current_choice = None
        for f in re_set.findall(line):
            sets.append((f, path.name, i))
        for f in re_read.findall(line):
            reads.append((f, path.name, i))
        if em := RE_EFFECT.match(line):
            if current_title:
                effect_titles.add(current_title)
            if current_choice is not None:
                current_choice["effects"].append(short_effect(em.group(1)))
        for j in RE_JUMP.findall(line):
            jumps.append((j, path.name, i))
            if current_choice is not None and current_choice["jump"] is None:
                current_choice["jump"] = j
    return titles, jumps, sets, reads, choices, effect_titles


def files(root, pattern, ignore):
    for p in root.rglob(pattern):
        if not ignore & set(p.relative_to(root).as_posix().split("/")[:-1]):
            yield p


def scan_code_flags(root, sources, cfg):
    """Flags kept in code or data (TS, JSON, GDScript…): every match of a set pattern is a write; a read
    pattern match that starts inside a set match is the same write, not a read."""
    set_res = [re.compile(p) for p in cfg.get("flag_set_patterns", [])]
    read_res = [re.compile(p) for p in cfg.get("flag_read_patterns", [])]
    sets, reads = [], []
    for p in sources:
        text = p.read_text(encoding="utf-8", errors="ignore")
        rel = p.relative_to(root).as_posix()
        spans = []
        for rx in set_res:
            for m in rx.finditer(text):
                spans.append((m.start(), m.end()))
                sets.append((m.group(1), rel, text.count("\n", 0, m.start()) + 1))
        for rx in read_res:
            for m in rx.finditer(text):
                if not any(a <= m.start() < b for a, b in spans):
                    reads.append((m.group(1), rel, text.count("\n", 0, m.start()) + 1))
    return sets, reads


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("--stage")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--config")
    ap.add_argument("--strict", action="store_true",
                    help="also fail on flags set-but-never-read / read-but-never-set and orphan titles")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    root = a.root.resolve()
    if not root.is_dir():
        print(f"game root not found: {root}", file=sys.stderr)
        sys.exit(2)
    cfg = load_config(root, a.config)
    ignore = set(cfg.get("ignore_dirs", ["addons", ".godot", "test", "tests"]))
    set_fns = cfg.get("flag_set_fns", ["set_flag"])
    read_fns = cfg.get("flag_read_fns", ["check_flag", "get_flag", "get_flag_value"])
    re_set = re.compile(rf"\b(?:{'|'.join(map(re.escape, set_fns))})\(\s*\"([^\"]+)\"")
    re_read = re.compile(rf"\b(?:{'|'.join(map(re.escape, read_fns))})\(\s*\"([^\"]+)\"")
    entry_res = [re.compile(p) for p in cfg.get("entry_title_patterns", ["^start$", "_intro$"])]

    dfiles = sorted(files(root, "*.dialogue", ignore))
    sources = sorted({p for g in cfg.get("flag_sources", []) for p in root.glob(g)
                      if p.is_file() and not ignore & set(p.relative_to(root).as_posix().split("/")[:-1])})
    if not dfiles and not sources:
        print(f"No .dialogue files under {root} and no flag_sources in gd.config.json", file=sys.stderr)
        sys.exit(2)
    titles, jumps, sets, reads, choices, effect_titles = {}, [], [], [], [], set()
    for f in dfiles:
        t, j, s, r, c, e = parse_dialogue(f, re_set, re_read)
        titles.update({k: (f.name, v) for k, v in t.items()})
        jumps += j; sets += s; reads += r; choices += c
        effect_titles |= e
    s, r = scan_code_flags(root, sources, cfg)
    sets += s; reads += r

    literals, dynamic = set(), []
    for p in list(files(root, "*.gd", ignore)) + list(files(root, "*.tres", ignore)):
        text = p.read_text(encoding="utf-8", errors="ignore")
        literals.update(RE_LITERAL.findall(text))
        for m in re.finditer(rf"\b(?:{'|'.join(map(re.escape, read_fns))})\(\s*\"([^\"]*%[^\"]*)\"", text):
            dynamic.append(f"{p.relative_to(root).as_posix()}: {m.group(1)}")

    set_names = {f for f, *_ in sets}
    read_names = {f for f, *_ in reads} | (literals & set_names)
    jumped = {j for j, *_ in jumps}
    entry = (literals & titles.keys()) | {t for t in titles if any(r.search(t) for r in entry_res)}

    report = {
        "files": len(dfiles), "code_files": len(sources), "titles": len(titles), "choices": len(choices),
        "flags_set": len(set_names), "flags_read": len(read_names & set_names),
        "set_never_read": sorted({f: f"{fl}:{ln}" for f, fl, ln in sets if f not in read_names}.items()),
        "read_never_set": sorted({f: f"{fl}:{ln}" for f, fl, ln in reads if f not in set_names}.items()),
        "broken_jumps": sorted({f"{j} ({fl}:{ln})" for j, fl, ln in jumps
                                if j not in titles and not j.upper().startswith("END")}),
        "orphan_titles": sorted(f"{t} ({fl}:{ln})" for t, (fl, ln) in titles.items()
                                if t not in jumped and t not in entry),
        "cosmetic_choices": [f"{c['file']}:{c['line']} [{c['title']}] {c['text']}"
                             for c in choices if not c["effects"] and c["jump"] not in effect_titles],
        "dynamic_flag_reads": dynamic,
    }
    table = [c for c in choices if not a.stage or a.stage in c["file"]]

    failed = bool(report["broken_jumps"]) or (a.strict and bool(
        report["set_never_read"] or report["read_never_set"] or report["orphan_titles"]))
    if a.json:
        report["choice_table"] = table
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(1 if failed else 0)

    print(f"# Dialogue audit — {root.name}\n")
    print(f"{report['files']} dialogue files · {report['code_files']} code files · {report['titles']} titles · {report['choices']} choices · "
          f"{report['flags_set']} flags set · {report['flags_read']} of them read\n")
    sections = [
        ("Flags SET but never READ (consequence never paid off — choice illusion?)", report["set_never_read"]),
        ("Flags READ but never SET (unreachable branch / typo)", report["read_never_set"]),
        ("Jumps to undefined titles", report["broken_jumps"]),
        ("Orphan titles (never jumped to, not an entry point)", report["orphan_titles"]),
        ("Choices with no mechanical effect", report["cosmetic_choices"]),
        ("Dynamic flag reads (format strings) — check by hand", report["dynamic_flag_reads"]),
    ]
    for head, items in sections:
        print(f"## {head} ({len(items)})")
        for it in items:
            print(f"- {' @ '.join(it) if isinstance(it, tuple) else it}")
        print()
    print("## Choice & Consequence table" + (f" — {a.stage}" if a.stage else ""))
    print("| Location | Title | Option | Cond? | Mechanical effects | → Jump |\n|---|---|---|---|---|---|")
    for c in table:
        eff = "<br>".join(c["effects"]) or ("(effects in target title)" if c["jump"] in effect_titles else "—")
        print(f"| {c['file']}:{c['line']} | {c['title']} | {c['text'].replace('|', '/')} | "
              f"{'✓' if c['conditional'] else ''} | {eff.replace('|', '/')} | {c['jump'] or ''} |")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
