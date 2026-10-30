#!/usr/bin/env python3
"""Who writes / reads which gameplay state — a dependency map for a Godot (GDScript) or a
TypeScript/JavaScript game (web engines such as Phaser, PixiJS, three.js; also Cocos, Excalibur).

State variables = top-level `var`s of the *state owner* scripts (e.g. a GameState autoload) and of
*instance owner* classes (e.g. HeroData resources, matched as `<anything>.<field>`).
For every script — and every .dialogue file through its `Autoload.func(` calls — the tool finds
direct and indirect writes/reads, following calls such as
`DialogueBridge.change_tyranny(5)` -> `GameState.change_tyranny()` -> writes `tyranny_score`.

Usage (game_root = folder containing project.godot, or package.json / tsconfig.json):
  python -I system_map.py <game_root>                     # full map (markdown)
  python -I system_map.py <game_root> --impact loyalty    # who touches one variable
  python -I system_map.py <game_root> --impact shop       # blast radius of a system (substring)
  python -I system_map.py <game_root> --snapshot before.json
  python -I system_map.py <game_root> --diff before.json  # edges added/removed since snapshot
  python -I system_map.py <game_root> --json              # machine-readable map (state, writers, readers)
Exit codes: 0 ok · 1 no state found / query matched nothing · 2 game root missing.

Config: <game_root>/docs/design/gd.config.json (or --config PATH), keys used here:
  "state_owners":    {"GameState": "scripts/game_state.gd"}   (default: autoloads with >= 5 vars)
  "instance_owners": {"HeroData": "scripts/data/hero_data.gd"} (default: none)
  "save_systems":    ["SaveLoadManager"]                       (default: names containing "save")
  "ignore_dirs":     ["addons", ".godot", "test", "tests"]  (default; TS adds node_modules, dist, build)
  "language":        "gdscript" | "ts"   (default: detected from project.godot / package.json)
TypeScript/JavaScript: an owner is an interface, type or class name, mapped to the file declaring it
  ("state_owners": {"GameState": "src/core/types.ts"}); its fields are the state variables. Code reaches
  the state through aliases: every name annotated with the owner type (`S: GameState`) in a file, plus
  "state_aliases": {"GameState": ["state", "this.state"]}. Instance owners match `<anything>.<field>`.
  A system is one source file (*.test.* / *.spec.* files are skipped); calls follow function names
  that are unique across the project.
Heuristic (regex, not a parser): an instance field name shared with another class can create false
edges. Treat output as evidence to verify, not truth.
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

MUTATORS = (r"(?:append|push_back|push_front|erase|clear|remove_at|insert|pop_back|pop_front|"
            r"sort|sort_custom|assign|merge|resize|fill)")
# bulk rewrites (new game / save / load) would make every caller look like a writer of everything
BULK = re.compile(r"^_?(reset|load|save|auto_?save|delete_?save|new_?game|restore|deserialize|"
                  r"serialize|from_?dict|to_?dict|from_?json|to_?json|apply_?save)\w*$", re.I)
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


# ---------- TypeScript / JavaScript profile ----------
TS_EXT = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".mts")
TS_SKIP_FILE = re.compile(r"\.(test|spec)\.[mc]?[jt]sx?$|\.d\.ts$")
TS_MUTATORS = (r"(?:push|pop|shift|unshift|splice|sort|reverse|fill|copyWithin|set|delete|clear|add)")
TS_ASSIGN = r"\s*(?:[+\-*/%]|\*\*|\?\?|\|\||&&|<<|>>)?=(?!=)"
TS_KEYWORDS = {"if", "for", "while", "switch", "catch", "return", "function", "typeof", "new", "await",
               "super", "import", "export", "constructor", "delete", "void", "yield", "else", "do"}
RE_TS_FUNC = re.compile(
    r"^[ \t]*(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s*\*?\s*(\w+)\s*[<(]"
    r"|^[ \t]*(?:export\s+)?(?:const|let|var)\s+(\w+)\s*(?::[^=\n]+)?=\s*(?:async\s+)?"
    r"(?:function\b|\([^)\n]*\)?|\w+\s*=>|<)"
    r"|^[ \t]+(?:(?:public|private|protected|static|async|override|readonly|get|set)\s+)*"
    r"(\w+)\s*\([^;\n]*\)\s*(?::\s*[^{;\n]+)?\{\s*$", re.M)


def ts_strip_comments(text):
    text = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    return re.sub(r"(?<![:\\'\"`])//[^\n]*", "", text)


def ts_split_funcs(text):
    marks = []
    for m in RE_TS_FUNC.finditer(text):
        name = next(g for g in m.groups() if g)
        if name not in TS_KEYWORDS:
            marks.append((m.start(), name))
    funcs = {"<top>": text[: marks[0][0]] if marks else text}
    for i, (pos, name) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        funcs[name] = funcs.get(name, "") + text[pos:end]
    return funcs


def ts_fields(text, owner):
    """Top-level members of `interface Owner {…}`, `type Owner = {…}` or `class Owner {…}`."""
    m = re.search(rf"\b(?:interface|class)\s+{owner}\b[^{{]*\{{|\btype\s+{owner}\b[^=]*=\s*\{{", text)
    if not m:
        return []
    depth, i, body = 1, m.end(), []
    while i < len(text) and depth:
        c = text[i]
        depth += c == "{"
        depth -= c == "}"
        body.append(c if depth == 1 else ("\n" if c == "\n" else " "))
        i += 1
    fields = re.findall(r"^\s*(?:(?:public|private|protected|readonly|static|declare)\s+)*"
                        r"(\w+)\s*[?!]?\s*[:=;(]", "".join(body), re.M)
    return [f for f in dict.fromkeys(fields) if f != "constructor"]


def detect_language(root, cfg):
    if cfg.get("language"):
        return cfg["language"].lower()
    if (root / "project.godot").exists():
        return "gdscript"
    if (root / "package.json").exists() or (root / "tsconfig.json").exists():
        return "ts"
    return "gdscript"


def build_ts(root, cfg):
    ignore = set(cfg.get("ignore_dirs", ["test", "tests"])) | {"node_modules", "dist", "build", ".git"}
    texts, sysname = {}, {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in ignore and not d.startswith("."))
        for name in sorted(filenames):
            p = Path(dirpath) / name
            if p.suffix in TS_EXT and not TS_SKIP_FILE.search(name):
                rel = p.relative_to(root).as_posix()
                texts[rel] = ts_strip_comments(p.read_text(encoding="utf-8", errors="ignore"))
    stems = defaultdict(list)
    for rel in texts:
        stems[Path(rel).stem].append(rel)
    for rel in texts:   # a system is a file: its stem, or parent/stem when two files share a stem
        stem = Path(rel).stem
        sysname[rel] = stem if len(stems[stem]) == 1 else "/".join(Path(rel).with_suffix("").parts[-2:])

    state_owners = cfg.get("state_owners") or {}
    inst_owners = cfg.get("instance_owners", {})
    save_cfg = cfg.get("save_systems")
    for name, rel in {**state_owners, **inst_owners}.items():
        if rel not in texts:
            sys.exit(f"owner file not found: {rel} (check gd.config.json)")
    state = {}
    for name, rel in {**state_owners, **inst_owners}.items():
        fields = ts_fields(texts[rel], name)
        if not fields:
            sys.exit(f"no interface/type/class '{name}' with fields in {rel} (check gd.config.json)")
        for v in fields:
            state.setdefault(v, name)
    inst_names = set(inst_owners)
    extra_alias = cfg.get("state_aliases", {})

    # a module-level `export let S: GameState` is an alias in every file that imports S
    exported = {o: {m.group(1) for t in texts.values() for m in re.finditer(
        rf"^export\s+(?:let|const|var)\s+(\w+)\s*:\s*(?:Readonly<\s*)?{o}\b", t, re.M)} for o in state_owners}

    def aliases(text, owner):
        found = set(re.findall(rf"(?<![\w.])(\w+)\s*[?!]?\s*:\s*(?:Readonly<\s*)?{owner}\b", text))
        found |= set(re.findall(rf"(?<![\w.])(?:const|let|var)\s+(\w+)\s*=\s*[^;\n]*\bas\s+{owner}\b", text))
        for group in re.findall(r"\bimport\s*(?:type\s*)?\{([^}]*)\}\s*from", text):
            for item in group.split(","):
                parts = item.split()
                if parts and parts[0] in exported[owner]:
                    found.add(parts[-1])           # `S` or `S as state`
        return found | set(extra_alias.get(owner, []))

    def direct(text_aliases, body):
        w, r = set(), set()
        for v, o in state.items():
            if o in inst_names:
                head = r"(?<=[\w)\]])\??\."
            else:
                names = text_aliases.get(o)
                if not names:
                    continue
                head = r"(?<![\w.])(?:%s)\??\." % "|".join(re.escape(a) for a in sorted(names))
            chain = r"(?:\??\.\w+|\[[^\]\n]*\])*"
            pw = (rf"{head}{v}\b{chain}(?:{TS_ASSIGN}|\s*(?:\+\+|--)|\.{TS_MUTATORS}\()"
                  rf"|(?:\+\+|--|\bdelete\s+){head}{v}\b")
            if re.search(pw, body):
                w.add(v)
            elif re.search(rf"{head}{v}\b", body):
                r.add(v)
        # free calls only: `x.push(` is a method, not a call to some helper that happens to be named push
        calls = {m.group(1) for m in re.finditer(r"(?<![\w$.])(\w+)\s*(?:<[^>()\n]*>)?\s*\(", body)}
        return w, r, calls - TS_KEYWORDS

    fn = {}
    for rel, t in texts.items():
        al = {o: aliases(t, o) for o in state_owners}
        for f, body in ts_split_funcs(t).items():
            if not BULK.match(f):                  # new game / load / reset rewrite everything
                fn[(sysname[rel], f)] = list(direct(al, body))
    by_name = defaultdict(set)
    for key in fn:
        if key[1] != "<top>":
            by_name[key[1]].add(key)

    def is_save(name):
        return name in save_cfg if save_cfg is not None else "save" in name.lower()

    def resolve(s, call):
        if BULK.match(call):
            return []
        if (s, call) in fn:                        # same file first
            return [(s, call)]
        owners = by_name.get(call, set())
        return list(owners) if len(owners) == 1 and not is_save(next(iter(owners))[0]) else []

    def propagate(same_file, rounds):
        """Merge callee effects into callers: same-file calls until stable, cross-file calls `rounds` hops.
        Each cross-file round reads the previous round's result, so the hop count is exact."""
        for _ in range(10_000 if same_file else rounds):
            before = {k: (set(w), set(r)) for k, (w, r, _) in fn.items()}
            changed = False
            for key, (w, r, calls) in fn.items():
                for c in calls:
                    for tgt in resolve(key[0], c):
                        if tgt == key or (tgt[0] == key[0]) != same_file:
                            continue
                        tw, tr = before[tgt]
                        if not (tw <= w and tr <= r):
                            w |= tw
                            r |= tr
                            changed = True
            if not changed:
                return

    # A long call chain (UI -> dispatcher -> rules) would make every caller a writer of everything,
    # so cross-file calls count only `call_depth` hops (default 1: the file and the functions it calls).
    propagate(True, 0)
    propagate(False, int(cfg.get("call_depth", 1)))
    propagate(True, 0)

    writes, reads = defaultdict(set), defaultdict(set)
    for (s, f), (w, r, _) in fn.items():
        writes[s] |= w
        reads[s] |= r
    for s in list(writes):
        reads[s] -= writes[s]
    systems = {s for s in writes.keys() | reads.keys() if not is_save(s) and (writes[s] or reads[s])}
    return state, writes, reads, systems, state_owners, inst_owners


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("--config")
    ap.add_argument("--impact")
    ap.add_argument("--snapshot")
    ap.add_argument("--diff")
    ap.add_argument("--json", action="store_true", help="print the map as one JSON object")
    ap.add_argument("--language", choices=["gdscript", "ts"], help="override detection")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    root = a.root.resolve()
    if not root.is_dir():
        print(f"game root not found: {root}", file=sys.stderr)
        sys.exit(2)
    cfg = load_config(root, a.config)
    lang = a.language or detect_language(root, cfg)
    if lang == "ts":
        state, writes, reads, systems, so, io = build_ts(root, cfg)
    else:
        if not (root / "project.godot").exists():
            print(f"warning: no project.godot in {root}", file=sys.stderr)
        state, writes, reads, systems, so, io = build(root, cfg)
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

    if a.json:
        print(json.dumps({"tool": "system_map", "schema": 1, "root": root.as_posix(), "language": lang,
                          "owners": {**so, **io},
                          "state": {v: {"owner": state[v], "writers": sorted(writers[v]),
                                        "readers": sorted(readers[v]), "contested": len(writers[v]) >= 4}
                                    for v in sorted(state)},
                          "systems": {s: {"writes": sorted(writes[s]), "reads": sorted(reads[s])}
                                      for s in sorted(systems)}},
                         ensure_ascii=False, indent=1))
        return

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
          f"({'incl. dialogues; ' if lang == 'gdscript' else ''}save systems hidden)\n")
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
