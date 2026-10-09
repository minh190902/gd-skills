#!/usr/bin/env python3
"""Who writes / reads which gameplay state — a dependency map for a Godot (GDScript) project.

State variables = top-level `var`s of the *state owner* scripts (e.g. a GameState autoload) and of
*instance owner* classes (e.g. HeroData resources, matched as `<anything>.<field>`).
For every script — and every .dialogue file through its `Autoload.func(` calls — the tool finds
direct and indirect writes/reads, following calls such as
`DialogueBridge.change_tyranny(5)` -> `GameState.change_tyranny()` -> writes `tyranny_score`.

Usage (game_root = folder containing project.godot):
  python -I system_map.py <game_root>                     # full map (markdown)
  python -I system_map.py <game_root> --impact loyalty    # who touches one variable
  python -I system_map.py <game_root> --impact shop       # blast radius of a system (substring)
  python -I system_map.py <game_root> --snapshot before.json
  python -I system_map.py <game_root> --diff before.json  # edges added/removed since snapshot

Config: <game_root>/docs/design/gd.config.json (or --config PATH), keys used here:
  "state_owners":    {"GameState": "scripts/game_state.gd"}   (default: autoloads with >= 5 vars)
  "instance_owners": {"HeroData": "scripts/data/hero_data.gd"} (default: none)
  "save_systems":    ["SaveLoadManager"]                       (default: names containing "save")
  "ignore_dirs":     ["addons", ".godot", "test", "tests"]  (default)
Heuristic (regex, not a parser): an instance field name shared with another class can create false
edges. Treat output as evidence to verify, not truth.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

MUTATORS = (r"(?:append|push_back|push_front|erase|clear|remove_at|insert|pop_back|pop_front|"
            r"sort|sort_custom|assign|merge|resize|fill)")
# bulk rewrites (new game / save / load) would make every caller look like a writer of everything
BULK = re.compile(r"^_?(reset|load|save|auto_save|delete_save|new_game|restore|deserialize|"
                  r"serialize|from_dict|to_dict|apply_save)\w*$")
RE_FUNC = re.compile(r"^(?:static\s+)?func\s+(\w+)\s*\(", re.M)
RE_VAR = re.compile(r"^(?:@export[^\n]*?\s)?var\s+(\w+)", re.M)


def load_config(root, path):
    p = Path(path) if path else root / "docs" / "design" / "gd.config.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def strip_comments(text):
    out = []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            out.append("")
            continue
        m = re.search(r"\s#[^\"']*$", line)        # trailing comment with no quote after '#'
        out.append(line[:m.start()] if m else line)
    return "\n".join(out)


def split_funcs(text):
    marks = [(m.start(), m.group(1)) for m in RE_FUNC.finditer(text)]
    funcs = {"<top>": text[: marks[0][0]] if marks else text}
    for i, (pos, name) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        funcs[name] = funcs.get(name, "") + text[pos:end]
    return funcs


def autoloads(root):
    names = {}
    pg = root / "project.godot"
    if pg.exists():
        sec = False
        for line in pg.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("["):
                sec = line.strip() == "[autoload]"
            elif sec and "=" in line:
                k, v = line.split("=", 1)
                path = v.strip().strip('"').lstrip("*").replace("res://", "")
                names[path] = k.strip()
    return names


def build(root, cfg):
    ignore = set(cfg.get("ignore_dirs", ["addons", ".godot", "test", "tests"]))
    auto = autoloads(root)
    texts, sysname = {}, {}
    for p in root.rglob("*.gd"):
        rel = p.relative_to(root).as_posix()
        if ignore & set(rel.split("/")[:-1]):
            continue
        t = strip_comments(p.read_text(encoding="utf-8", errors="ignore"))
        texts[rel] = t
        cn = re.search(r"^class_name\s+(\w+)", t, re.M)
        sysname[rel] = auto.get(rel) or (cn.group(1) if cn else p.stem)

    state_owners = cfg.get("state_owners")
    if state_owners is None:   # default: autoload scripts that hold real state
        state_owners = {n: rel for rel, n in auto.items()
                        if rel in texts and len(RE_VAR.findall(texts[rel])) >= 5}
    inst_owners = cfg.get("instance_owners", {})
    save_cfg = cfg.get("save_systems")
    for name, rel in {**state_owners, **inst_owners}.items():
        if rel not in texts:
            sys.exit(f"owner file not found: {rel} (check gd.config.json)")
    owner_of_file = {rel: n for n, rel in {**state_owners, **inst_owners}.items()}

    state = {}                    # var -> owner name
    for name, rel in {**state_owners, **inst_owners}.items():
        for v in RE_VAR.findall(texts[rel]):
            state.setdefault(v.lstrip("_"), name)
    inst_names = set(inst_owners)

    def direct(rel, body):
        w, r, calls = set(), set(), set()
        own = owner_of_file.get(rel)
        if own:
            body = RE_VAR.sub("", body)    # a declaration is neither a read nor a write
        for v, o in state.items():
            if o == own:
                pw = rf"(?<![\w.])_?{v}(?:\[[^\]\n]*\])?\s*(?:[+\-*/]?=(?!=)|\.{MUTATORS}\()"
                pr = rf"(?<![\w.])_?{v}\b"
            elif o in inst_names:
                pw = rf"\w\.{v}(?:\[[^\]\n]*\])?\s*(?:[+\-*/]?=(?!=)|\.{MUTATORS}\()"
                pr = rf"\w\.{v}\b"
            else:
                pw = rf"\b{o}\.{v}(?:\[[^\]\n]*\])?\s*(?:[+\-*/]?=(?!=)|\.{MUTATORS}\()"
                pr = rf"\b{o}\.{v}\b"
            if re.search(pw, body):
                w.add(v)
            elif re.search(pr, body):
                r.add(v)
        calls |= {(m.group(1), m.group(2)) for m in re.finditer(r"\b([A-Z]\w+)\.(\w+)\s*\(", body)}
        calls |= {("*", m.group(1)) for m in re.finditer(r"[a-z_]\w*\.(\w+)\s*\(", body)}
        calls |= {("self", m.group(1)) for m in re.finditer(r"(?<![\w.])(\w+)\s*\(", body)}
        return w, r, calls

    fn = {}
    for rel, t in texts.items():
        for f, body in split_funcs(t).items():
            fn[(sysname[rel], f)] = list(direct(rel, body))
    by_method = defaultdict(set)
    for (s, f) in fn:
        by_method[f].add(s)

    def is_save(name):
        return name in save_cfg if save_cfg is not None else "save" in name.lower()

    def resolve(s, call):
        cls, m = call
        if BULK.match(m) or is_save(cls):
            return []
        if cls == "self":
            return [(s, m)] if (s, m) in fn else []
        if cls == "*":   # instance call: only methods unique to one instance owner
            owners = by_method[m] & inst_names
            return [(next(iter(owners)), m)] if len(owners) == 1 and len(by_method[m]) == 1 else []
        return [(cls, m)] if (cls, m) in fn else []

    changed = True
    while changed:
        changed = False
        for key, (w, r, calls) in fn.items():
            for c in calls:
                for tgt in resolve(key[0], c):
                    if tgt == key:
                        continue
                    tw, tr, _ = fn[tgt]
                    if not (tw <= w and tr <= r):
                        w |= tw
                        r |= tr
                        changed = True

    writes, reads = defaultdict(set), defaultdict(set)
    for (s, f), (w, r, _) in fn.items():
        writes[s] |= w
        reads[s] |= r
    for p in root.rglob("*.dialogue"):
        rel = p.relative_to(root).as_posix()
        if ignore & set(rel.split("/")[:-1]):
            continue
        name = f"dialogue:{p.stem}"
        t = p.read_text(encoding="utf-8", errors="ignore")
        for cls, m in set(re.findall(r"\b([A-Z]\w+)\.(\w+)\s*\(", t)):
            if (cls, m) in fn:
                writes[name] |= fn[(cls, m)][0]
                reads[name] |= fn[(cls, m)][1]
    for s in list(writes):
        reads[s] -= writes[s]
    systems = {s for s in writes.keys() | reads.keys() if not is_save(s)}
    return state, writes, reads, systems, state_owners, inst_owners


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("--config")
    ap.add_argument("--impact")
    ap.add_argument("--snapshot")
    ap.add_argument("--diff")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    root = a.root.resolve()
    if not (root / "project.godot").exists():
        print(f"warning: no project.godot in {root}", file=sys.stderr)
    state, writes, reads, systems, so, io = build(root, load_config(root, a.config))
    if not state:
        sys.exit("no state variables found — set state_owners in docs/design/gd.config.json")

    edges = sorted({f"W {s} {v}" for s in systems for v in writes[s]} |
                   {f"R {s} {v}" for s in systems for v in reads[s]})
    if a.snapshot:
        Path(a.snapshot).write_text(json.dumps(edges, indent=0), encoding="utf-8")
        print(f"snapshot: {len(edges)} edges -> {a.snapshot}")
        return
    if a.diff:
        old = set(json.loads(Path(a.diff).read_text(encoding="utf-8")))
        new = set(edges)
        print("# System map diff\n")
        for title, items in (("Added", sorted(new - old)), ("Removed", sorted(old - new))):
            print(f"## {title} ({len(items)})")
            for e in items:
                k, s, v = e.split(" ", 2)
                print(f"- {'writes' if k == 'W' else 'reads '} `{v}` ← {s}")
            print()
        return

    writers, readers = defaultdict(set), defaultdict(set)
    for s in systems:
        for v in writes[s]:
            writers[v].add(s)
        for v in reads[s]:
            readers[v].add(s)

    if a.impact:
        q = a.impact
        if q in state:
            W, R = sorted(writers[q]), sorted(readers[q])
            print(f"# Impact: `{q}` ({state[q]})\n")
            print(f"**Writers ({len(W)}):** {', '.join(W) or '—'}\n")
            print(f"**Readers ({len(R)}):** {', '.join(R) or '—'}\n")
            print("Changing this variable's meaning/range affects every reader; "
                  "a new writer must respect every other writer's assumptions.")
            return
        match = sorted(s for s in systems if q.lower() in s.lower())
        if not match:
            sys.exit(f"no variable or system matches '{q}'")
        for s in match:
            print(f"# Impact: system `{s}`\n")
            print("| Var it WRITES | Other writers | Readers affected |\n|---|---|---|")
            for v in sorted(writes[s]):
                print(f"| {v} | {', '.join(sorted(writers[v] - {s})) or '—'} | "
                      f"{', '.join(sorted(readers[v] - {s})) or '—'} |")
            print("\n| Var it READS | Written by |\n|---|---|")
            for v in sorted(reads[s]):
                print(f"| {v} | {', '.join(sorted(writers[v] - {s})) or '—'} |")
            print()
        return

    owners = ", ".join(f"{k} ({v})" for k, v in {**so, **io}.items())
    print(f"# System map — {root.name}\n")
    print(f"Owners: {owners} · {len(state)} state vars · {len(systems)} systems "
          f"(incl. dialogues; save systems hidden)\n")
    print("| Variable | Owner | #W | Writers | #R | Readers |\n|---|---|---|---|---|---|")
    for v in sorted(state, key=lambda x: (-len(writers[x]), x)):
        if not writers[v] and not readers[v]:
            continue
        flag = " ⚠" if len(writers[v]) >= 4 else ""
        print(f"| {v}{flag} | {state[v]} | {len(writers[v])} | {', '.join(sorted(writers[v]))} | "
              f"{len(readers[v])} | {', '.join(sorted(readers[v]))} |")
    unused = sorted(v for v in state if not writers[v] and not readers[v])
    print("\n⚠ = 4+ writers (contested: a new writer must agree on meaning/range with all others).")
    print(f"\nDeclared but untouched outside owner/save: {', '.join(unused) or '—'}")


if __name__ == "__main__":
    main()
