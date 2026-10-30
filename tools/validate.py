#!/usr/bin/env python3
"""Validate the skills repo: frontmatter, names, descriptions, boundaries, links, orphan files,
cross-skill references, routing coverage, line endings, scripts, versions.

  python tools/validate.py              # exit 1 on any error
  python tools/validate.py --root DIR   # validate another copy (used by the tests)
"""
import argparse
import json
import py_compile
import re
import sys
import tempfile
from pathlib import Path

TEXT_EXT = {".md", ".py", ".json", ".txt", ".yml", ".yaml"}
SKILL_ENTRIES = {"SKILL.md", "SOURCES.md", "references", "templates", "scripts", "examples", "agents"}
RE_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RE_BOUNDARY = re.compile(r"^(## When not to use|\*\*When not to use)", re.M)
RE_GD_NAME = re.compile(r"(?<![\w/-])(gd-[a-z0-9]+(?:-[a-z0-9]+)*)(?![\w-])")
RE_BACKTICK_PATH = re.compile(r"`((?:references|templates|scripts|examples)/[^`\s*<>]+)`")


class Validator:
    def __init__(self, repo):
        self.repo = repo
        self.errors, self.warnings = [], []

    def err(self, msg):
        self.errors.append(msg)

    def check_skill(self, d, names):
        sk = d / "SKILL.md"
        if not sk.exists():
            return self.err(f"{d.name}: missing SKILL.md")
        text = sk.read_bytes().decode("utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            return self.err(f"{d.name}: SKILL.md must start with LF '---' frontmatter")
        keys = re.findall(r"^(\w[\w-]*):", m.group(1), re.M)
        if sorted(keys) != ["description", "name"]:
            self.err(f"{d.name}: frontmatter must have exactly name and description, found {keys}")
        fm = dict(re.findall(r"^(\w[\w-]*):\s*(.*)$", m.group(1), re.M))
        name, desc = fm.get("name", ""), fm.get("description", "")
        if name != d.name:
            self.err(f"{d.name}: frontmatter name '{name}' != folder name")
        if not RE_NAME.fullmatch(name) or len(name) > 64:
            self.err(f"{d.name}: name must be lowercase words joined by single hyphens (≤64)")
        if not desc:
            self.err(f"{d.name}: missing description")
        elif len(desc) > 1024:
            self.err(f"{d.name}: description {len(desc)} chars > 1024")
        elif re.search(r"[<>]", desc):
            self.err(f"{d.name}: description must not contain '<' or '>'")
        elif not re.search(r"\bUse (when|whenever|EVERY time|at)\b", desc):
            self.err(f"{d.name}: description must say when to use the skill ('Use when …')")
        if text.count("\n") > 500:
            self.err(f"{d.name}: SKILL.md has {text.count(chr(10))} lines (max 500; move detail to references/)")
        if not RE_BOUNDARY.search(text):
            self.err(f"{d.name}: no 'When not to use' section naming the sibling skills to use instead")

        for entry in d.iterdir():
            if entry.name not in SKILL_ENTRIES and entry.name != "__pycache__":
                self.err(f"{d.name}: unexpected entry '{entry.name}' (allowed: {', '.join(sorted(SKILL_ENTRIES))})")
        for link in re.findall(r"\]\(([^)#\s]+)\)", text):
            if "://" not in link and not (d / link).exists():
                self.err(f"{d.name}: broken link '{link}'")
        for line in text.splitlines():
            if set(RE_GD_NAME.findall(line)) - {d.name}:
                continue                          # the path belongs to the other skill named on this line
            for rel in RE_BACKTICK_PATH.findall(line):
                if not (d / rel).exists():
                    self.err(f"{d.name}: path `{rel}` does not exist")
        for other in set(RE_GD_NAME.findall(text)) - names:
            self.err(f"{d.name}: mentions unknown skill '{other}'")

        # every bundled file is reachable from SKILL.md (by its path, a parent folder link, or its file name)
        for f in d.rglob("*"):
            rel = f.relative_to(d).as_posix()
            if not f.is_file() or rel in ("SKILL.md", "SOURCES.md") or "__pycache__" in rel:
                continue
            parents = [rel.rsplit("/", k)[0] + "/" for k in range(1, rel.count("/") + 1)]
            if not any(p in text for p in [rel, f.name] + parents[:-1]):
                self.err(f"{d.name}: '{rel}' is not referenced from SKILL.md (orphan file)")

    def check_coverage(self, names):
        core = self.repo / "skills" / "gd-core" / "SKILL.md"
        if core.exists():
            routing = core.read_text(encoding="utf-8").split("## 2. Routing", 1)[-1]
            for n in sorted(names - {"gd-core"}):
                if f"`{n}`" not in routing:
                    self.err(f"gd-core routing does not mention `{n}`")
        readme = self.repo / "README.md"
        if readme.exists():
            text = readme.read_text(encoding="utf-8")
            for n in sorted(names):
                if f"`{n}`" not in text:
                    self.err(f"README.md does not list `{n}`")
            m = re.search(r"A set of (\d+) skills", text)
            if m and int(m.group(1)) != len(names):
                self.err(f"README.md says {m.group(1)} skills, repo has {len(names)}")

    def check_files(self):
        out = Path(tempfile.gettempdir()) / "gd-skills-validate.pyc"
        for p in self.repo.rglob("*"):
            if ".git" in p.parts or "node_modules" in p.parts and "fixtures" not in p.parts:
                continue
            if not p.is_file() or p.suffix not in TEXT_EXT:
                continue
            if b"\r\n" in p.read_bytes():
                self.err(f"{p.relative_to(self.repo)}: CRLF line endings (use LF)")
            if p.suffix == ".py":
                try:
                    py_compile.compile(str(p), doraise=True, cfile=str(out))
                except py_compile.PyCompileError as e:
                    self.err(f"{p.relative_to(self.repo)}: {e.msg}")
            if p.suffix == ".json":
                try:
                    json.loads(p.read_text(encoding="utf-8"))
                except ValueError as e:
                    self.err(f"{p.relative_to(self.repo)}: invalid JSON ({e})")

    def check_versions(self):
        plugin_p = self.repo / ".claude-plugin" / "plugin.json"
        market_p = self.repo / ".claude-plugin" / "marketplace.json"
        if not plugin_p.exists() or not market_p.exists():
            return self.err("missing .claude-plugin/plugin.json or marketplace.json")
        plugin = json.loads(plugin_p.read_text(encoding="utf-8"))
        market = json.loads(market_p.read_text(encoding="utf-8"))
        versions = {plugin["version"], market["metadata"]["version"], *(p["version"] for p in market["plugins"])}
        if len(versions) != 1:
            self.err(f"version mismatch between plugin.json and marketplace.json: {sorted(versions)}")
        changelog = self.repo / "CHANGELOG.md"
        if not changelog.exists() or f"## [{plugin['version']}]" not in changelog.read_text(encoding="utf-8"):
            self.err(f"CHANGELOG.md has no entry for {plugin['version']}")

    def run(self):
        skills = sorted(p for p in (self.repo / "skills").iterdir() if p.is_dir())
        names = {d.name for d in skills}
        for d in skills:
            self.check_skill(d, names)
        self.check_coverage(names)
        self.check_files()
        self.check_versions()
        return len(skills)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    v = Validator(ap.parse_args().root.resolve())
    count = v.run()
    for w in v.warnings:
        print(f"WARN  {w}")
    for e in v.errors:
        print(f"ERROR {e}")
    print(f"{count} skills checked · {len(v.errors)} errors · {len(v.warnings)} warnings")
    sys.exit(1 if v.errors else 0)


if __name__ == "__main__":
    main()
