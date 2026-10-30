#!/usr/bin/env python3
"""Keep a game's design dir lean and consistent: STATE.md stays one page, DECISIONS.md has unique IDs
and an up-to-date index, STATE and ROADMAP agree on the stage.

Usage (target = the game root or the design dir itself):
  python -I docs_check.py <target>                  # report; exit 1 on errors
  python -I docs_check.py <target> --strict         # warnings also fail (use in pre-commit / CI)
  python -I docs_check.py <target> --fix            # (re)generate the decision index in DECISIONS.md
  python -I docs_check.py <target> --json           # one JSON object instead of text

Exit codes: 0 no errors · 1 errors (or warnings with --strict) · 2 target missing / not a design dir.

Config: "docs" object in <design_dir>/gd.config.json (or --config PATH), every key optional:
  "state_max_bytes": 12000          STATE.md size limit (about one printed page)
  "line_max": 600                   longest allowed line in STATE.md
  "in_progress_headings": ["In progress"]   heading(s) of the in-progress section (any language)
  "in_progress_max": 2
  "session_log_headings": ["Session log"]
  "session_log_max": 5
  "decision_index_min": 15          suggest an index once DECISIONS.md has this many entries
Decision headings follow the template: "### D-012 · Short title · *Active* (YYYY-MM-DD)".
"""
import argparse
import json
import re
import sys
from pathlib import Path

DEFAULTS = {
    "state_max_bytes": 12000, "line_max": 600,
    "in_progress_headings": ["In progress"], "in_progress_max": 2,
    "session_log_headings": ["Session log"], "session_log_max": 5,
    "decision_index_min": 15,
}
RE_DECISION = re.compile(r"^###\s+(D-\d+)\s*·\s*(.+?)\s*·\s*\*([^*]+)\*(?:\s*\((\d{4}-\d{2}-\d{2})[^)]*\))?", re.M)
RE_BEGIN = re.compile(r"^<!-- index:begin[^\n]*-->$", re.M)
RE_END = re.compile(r"^<!-- index:end -->$", re.M)
DEFAULT_BEGIN = "<!-- index:begin (generated from the ### D-xxx entries; run docs_check.py --fix) -->"
RE_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+\S")
RE_STAGE = re.compile(r"\*\*(?:Current stage|Stage)[^*]*:\*\*\s*(\d+)")


class Report:
    def __init__(self, root):
        self.root, self.errors, self.warnings, self.notes = root, [], [], []

    def add(self, kind, path, line, msg, fix):
        rel = path.relative_to(self.root).as_posix() if path.is_absolute() else str(path)
        getattr(self, kind).append({"path": rel, "line": line, "message": msg, "fix": fix})


def find_design_dir(target):
    for d in (target, target / "docs" / "design"):
        if (d / "STATE.md").is_file() or (d / "DECISIONS.md").is_file():
            return d
    return None


def load_config(design_dir, path):
    p = Path(path) if path else design_dir / "gd.config.json"
    cfg = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
    return {**DEFAULTS, **cfg.get("docs", {})}


def section_lines(lines, headings):
    """(first line number, lines) of the first '## <heading>' section, or (None, [])."""
    pat = re.compile(r"^##\s+(?:%s)\b" % "|".join(re.escape(h) for h in headings), re.I)
    for i, line in enumerate(lines):
        if pat.match(line):
            body = []
            for nxt in lines[i + 1:]:
                if nxt.startswith("## "):
                    break
                body.append(nxt)
            return i + 1, body
    return None, []


def check_state(design_dir, cfg, rep):
    path = design_dir / "STATE.md"
    if not path.is_file():
        return rep.add("warnings", path, 0, "STATE.md is missing", "copy it from gd-core templates/project/")
    raw = path.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    if len(raw) > cfg["state_max_bytes"]:
        rep.add("warnings", path, 0, f"{len(raw):,} bytes, over {cfg['state_max_bytes']:,} (one page)",
                "move history to the project's history file, decisions to DECISIONS.md, details to topic docs")
    for n, line in enumerate(lines, 1):
        if len(line) > cfg["line_max"]:
            rep.add("warnings", path, n, f"line is {len(line)} characters (max {cfg['line_max']})",
                    "split it, or point to the doc that holds the detail")
    for key, limit, what in (("in_progress_headings", "in_progress_max", "items in progress"),
                             ("session_log_headings", "session_log_max", "session log lines")):
        start, body = section_lines(lines, cfg[key])
        count = sum(1 for line in body if RE_ITEM.match(line) and not line.strip().endswith(("- ", "1.")))
        if start and count > cfg[limit]:
            rep.add("warnings", path, start, f"{count} {what} (max {cfg[limit]})",
                    "finish or defer items" if "progress" in key else "move older lines to the history file")
    return lines


def check_decisions(design_dir, cfg, rep, fix):
    path = design_dir / "DECISIONS.md"
    if not path.is_file():
        return set()
    text = path.read_text(encoding="utf-8")
    entries, seen = [], set()
    for m in RE_DECISION.finditer(text):
        did, title, status, date = m.groups()
        line = text.count("\n", 0, m.start()) + 1
        if did in seen:
            rep.add("errors", path, line, f"duplicate decision ID {did}", "renumber the newer entry")
        seen.add(did)
        entries.append((did, title, status.split(" — ")[0].split(",")[0].strip(), date or ""))
    for m in re.finditer(r"Supersedes\s+(D-\d+)", text):
        if m.group(1) not in seen:
            rep.add("warnings", path, text.count("\n", 0, m.start()) + 1,
                    f"supersedes {m.group(1)}, which has no entry", "fix the ID")

    begin, end = RE_BEGIN.search(text), RE_END.search(text)
    rows = [f"| {d} | {t} | {s} | {dt} |" for d, t, s, dt in entries]
    index = "\n".join([begin.group(0) if begin else DEFAULT_BEGIN, "",
                       "| ID | Decision | Status | Date |", "|---|---|---|---|", *rows, "", "<!-- index:end -->"])
    if begin and end and end.start() > begin.start():
        # compare only the decision rows, so a translated header or intro line in the block is kept
        block = text[begin.start():end.end()].split("\n")
        at = [i for i, line in enumerate(block) if re.match(r"^\|\s*D-\d+", line)]
        if [block[i] for i in at] == rows:
            return seen
        if fix:
            block = block[:at[0]] + rows + block[at[-1] + 1:] if at else index.split("\n")
            new = text[:begin.start()] + "\n".join(block) + text[end.end():]
        else:
            rep.add("errors", path, text.count("\n", 0, begin.start()) + 1,
                    "decision index is out of date", "run docs_check.py --fix")
            return seen
    elif fix and entries:
        first = re.search(r"^###\s+D-", text, re.M)
        new = text[:first.start()] + index + "\n\n" + text[first.start():]
    else:
        if len(entries) >= cfg["decision_index_min"]:
            rep.add("notes", path, 0, f"{len(entries)} decisions and no index",
                    "run docs_check.py --fix to add a generated index at the top")
        return seen
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new)
    rep.add("notes", path, 0, "decision index regenerated", "commit DECISIONS.md")
    return seen


def check_stage(design_dir, state_lines, rep):
    road = design_dir / "ROADMAP.md"
    if not road.is_file() or not state_lines:
        return
    a = RE_STAGE.search("\n".join(state_lines))
    b = RE_STAGE.search(road.read_text(encoding="utf-8"))
    if a and b and a.group(1) != b.group(1):
        rep.add("warnings", design_dir / "STATE.md", 0,
                f"STATE says stage {a.group(1)}, ROADMAP says stage {b.group(1)}",
                "update the stage line in the stale file (ROADMAP wins after a gate review)")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("target", type=Path, help="game root or design dir")
    ap.add_argument("--config")
    ap.add_argument("--fix", action="store_true", help="regenerate the decision index")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="warnings also fail")
    ap.add_argument("--max-issues", type=int, default=50)
    args = ap.parse_args()

    design_dir = find_design_dir(args.target.resolve())
    if not design_dir:
        print(f"not a design dir (no STATE.md or DECISIONS.md): {args.target}", file=sys.stderr)
        sys.exit(2)
    cfg = load_config(design_dir, args.config)
    rep = Report(design_dir)
    state_lines = check_state(design_dir, cfg, rep)
    check_decisions(design_dir, cfg, rep, args.fix)
    check_stage(design_dir, state_lines, rep)

    issues = [("ERROR", i) for i in rep.errors] + [("WARNING", i) for i in rep.warnings] + \
             [("NOTE", i) for i in rep.notes]
    shown = issues[:args.max_issues]
    if args.json:
        print(json.dumps({"tool": "docs_check", "schema": 1, "root": design_dir.as_posix(),
                          "files_checked": [p for p in ("STATE.md", "DECISIONS.md", "ROADMAP.md")
                                            if (design_dir / p).is_file()],
                          "error_count": len(rep.errors), "warning_count": len(rep.warnings),
                          "note_count": len(rep.notes), "errors": rep.errors, "warnings": rep.warnings,
                          "notes": rep.notes, "truncated": len(shown) < len(issues)},
                         ensure_ascii=False, indent=1))
    else:
        for kind, i in shown:
            print(f"{kind} {i['path']}:{i['line']}: {i['message']}\n  fix: {i['fix']}")
        print(f"Summary: {len(rep.errors)} errors, {len(rep.warnings)} warnings, {len(rep.notes)} notes")
    sys.exit(1 if rep.errors or (args.strict and rep.warnings) else 0)


if __name__ == "__main__":
    main()
