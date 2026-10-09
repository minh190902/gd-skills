#!/usr/bin/env python3
"""Validate the skills repo: frontmatter, names, descriptions, links, line endings, scripts, versions.

  python tools/validate.py        # exit 1 on any error
"""
import json
import py_compile
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TEXT_EXT = {".md", ".py", ".json", ".txt", ".yml", ".yaml"}
errors, warnings = [], []


def err(msg):
    errors.append(msg)


def check_skill(d: Path):
    sk = d / "SKILL.md"
    if not sk.exists():
        return err(f"{d.name}: missing SKILL.md")
    raw = sk.read_bytes()
    text = raw.decode("utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return err(f"{d.name}: SKILL.md must start with LF '---' frontmatter")
    fm = dict(re.findall(r"^(\w[\w-]*):\s*(.*)$", m.group(1), re.M))
    name, desc = fm.get("name", ""), fm.get("description", "")
    if name != d.name:
        err(f"{d.name}: frontmatter name '{name}' != folder name")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        err(f"{d.name}: name must be lowercase letters, digits, hyphens (≤64)")
    if not desc:
        err(f"{d.name}: missing description")
    elif len(desc) > 1024:
        err(f"{d.name}: description {len(desc)} chars > 1024")
    elif re.search(r"[<>]", desc):
        err(f"{d.name}: description must not contain '<' or '>'")
    body_lines = text.count("\n")
    if body_lines > 500:
        warnings.append(f"{d.name}: SKILL.md has {body_lines} lines (keep < 500; move detail to references/)")
    for link in re.findall(r"\]\(([^)#]+)\)", text):
        if "://" in link:
            continue
        if not (d / link).exists():
            err(f"{d.name}: broken link '{link}'")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    (REPO / "tests" / "out").mkdir(parents=True, exist_ok=True)
    skills = sorted(p for p in (REPO / "skills").iterdir() if p.is_dir())
    for d in skills:
        check_skill(d)
    for p in REPO.rglob("*"):
        if ".git" in p.parts or not p.is_file() or p.suffix not in TEXT_EXT:
            continue
        if b"\r\n" in p.read_bytes():
            err(f"{p.relative_to(REPO)}: CRLF line endings (use LF)")
        if p.suffix == ".py":
            try:
                py_compile.compile(str(p), doraise=True, cfile=str(REPO / "tests" / "out" / "pyc.tmp"))
            except py_compile.PyCompileError as e:
                err(f"{p.relative_to(REPO)}: {e.msg}")
        if p.suffix == ".json":
            try:
                json.loads(p.read_text(encoding="utf-8"))
            except ValueError as e:
                err(f"{p.relative_to(REPO)}: invalid JSON ({e})")
    plugin = json.loads((REPO / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    market = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    versions = {plugin["version"], market["metadata"]["version"], *(p["version"] for p in market["plugins"])}
    if len(versions) != 1:
        err(f"version mismatch between plugin.json and marketplace.json: {sorted(versions)}")
    if f"## [{plugin['version']}]" not in (REPO / "CHANGELOG.md").read_text(encoding="utf-8"):
        err(f"CHANGELOG.md has no entry for {plugin['version']}")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(skills)} skills checked · {len(errors)} errors · {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
