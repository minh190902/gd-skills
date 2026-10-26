#!/usr/bin/env python3
"""Install the gd-* skills into a repo (or globally) and optionally set up a game's design dir.

  python tools/install.py --target <repo>                     # copy skills to <repo>/.claude/skills/
  python tools/install.py --global                            # copy skills to ~/.claude/skills/
  python tools/install.py --target <repo> --init <game_root>  # + create <game_root>/docs/design/
                                                              #   and add the rules block to <repo>/CLAUDE.md
  python tools/install.py --target <repo> --agents            # + copy skills to <repo>/.agents/skills/ too
  add --dry-run to print what would happen.

Updating: re-run the same command. gd-* skill folders are replaced entirely (no stale files);
existing design docs (PROJECT/STATE/DECISIONS/SYSTEMS/gd.config.json) are never overwritten;
the rules block between <!-- gd-skills:begin/end --> is replaced in place.

One rules file for every agent: when <repo>/CLAUDE.md imports AGENTS.md (a line "@AGENTS.md") and
<repo>/AGENTS.md exists, the rules block goes into AGENTS.md (read by Codex and other agents, and by
Claude Code through the import) and any old block in CLAUDE.md is removed. Otherwise it goes into CLAUDE.md.
--agents keeps a copy of the skills in .agents/skills for agents that read that folder, so they never
run an older hand-copied version.
"""
import argparse
import json
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"
TEMPLATES = SKILLS / "gd-core" / "templates" / "project"
BEGIN, END = "<!-- gd-skills:begin -->", "<!-- gd-skills:end -->"


def version():
    return json.loads((REPO / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]


def write_lf(path: Path, text: str):
    with open(path, "w", encoding="utf-8", newline="\n") as f:   # Path.write_text(newline=) needs 3.10
        f.write(text)


def act(dry, msg, fn=None):
    print(("[dry-run] " if dry else "") + msg)
    if not dry and fn:
        fn()


def install_skills(dest: Path, dry: bool):
    for src in sorted(p for p in SKILLS.iterdir() if p.is_dir() and p.name.startswith("gd-")):
        out = dest / src.name
        if out.exists():
            act(dry, f"replace {out}", lambda o=out: shutil.rmtree(o))
        act(dry, f"copy    {src.name} -> {out}",
            lambda s=src, o=out: shutil.copytree(s, o, ignore=shutil.ignore_patterns("__pycache__", "*.pyc")))
    act(dry, f"write   {dest / '.gd-skills-version'} ({version()})",
        lambda: (dest / ".gd-skills-version").write_text(version() + "\n", encoding="utf-8"))


def has_import(text: str, name: str) -> bool:
    """True when a CLAUDE.md line imports the file (Claude Code `@path` import)."""
    return any(line.strip() in (f"@{name}", f"@./{name}") for line in text.splitlines())


def init_project(target: Path, game_root: Path, dry: bool):
    design = game_root / "docs" / "design"
    fresh = not (design / "PROJECT.md").exists()
    act(dry, f"mkdir   {design}", lambda: design.mkdir(parents=True, exist_ok=True))
    for f in sorted(TEMPLATES.iterdir()):
        if f.name == "CLAUDE.snippet.md":
            continue
        out = design / f.name
        if out.exists():
            print(f"keep    {out} (exists)")
        else:
            act(dry, f"create  {out}", lambda s=f, o=out: shutil.copyfile(s, o))
    rel = os.path.relpath(design, target).replace(os.sep, "/")
    block = (TEMPLATES / "CLAUDE.snippet.md").read_text(encoding="utf-8").replace("{{DESIGN_DIR}}", rel).strip()
    claude, agents = target / "CLAUDE.md", target / "AGENTS.md"
    claude_text = claude.read_text(encoding="utf-8") if claude.exists() else ""
    rules = agents if agents.exists() and has_import(claude_text, "AGENTS.md") else claude
    if rules == agents and BEGIN in claude_text and END in claude_text:
        stripped = claude_text[: claude_text.index(BEGIN)].rstrip() + "\n" + claude_text[claude_text.index(END) + len(END):].lstrip("\n")
        act(dry, f"remove  gd-skills block from {claude} (it lives in AGENTS.md now)", lambda: write_lf(claude, stripped))
    text = rules.read_text(encoding="utf-8") if rules.exists() else ""
    if BEGIN in text and END in text:
        new = text[: text.index(BEGIN)] + block + text[text.index(END) + len(END):]
        msg = f"update  gd-skills block in {rules}"
    else:
        new = (text.rstrip() + "\n\n" if text.strip() else "") + block + "\n"
        msg = f"append  gd-skills block to {rules}"
    act(dry, msg, lambda: write_lf(rules, new))
    if fresh:
        print(f"\nNext: open the game in Claude Code and ask it to fill {rel}/PROJECT.md and gd.config.json "
              f"(skill gd-core, section 1).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--target", type=Path, help="repo root to install into (.claude/skills)")
    g.add_argument("--global", dest="glob", action="store_true", help="install into ~/.claude/skills")
    ap.add_argument("--init", type=Path, metavar="GAME_ROOT", help="also create GAME_ROOT/docs/design")
    ap.add_argument("--agents", action="store_true", help="also copy the skills to <target>/.agents/skills")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    target = Path.home() if a.glob else a.target.resolve()
    if not a.glob and not target.is_dir():
        sys.exit(f"target not found: {target}")
    dest = target / ".claude" / "skills"
    print(f"gd-skills {version()} -> {dest}")
    act(a.dry_run, f"mkdir   {dest}", lambda: dest.mkdir(parents=True, exist_ok=True))
    install_skills(dest, a.dry_run)
    if a.agents:
        if a.glob:
            sys.exit("--agents needs --target")
        shared = target / ".agents" / "skills"
        print(f"gd-skills {version()} -> {shared}")
        act(a.dry_run, f"mkdir   {shared}", lambda: shared.mkdir(parents=True, exist_ok=True))
        install_skills(shared, a.dry_run)
    if a.init:
        if a.glob:
            sys.exit("--init needs --target (the repo whose CLAUDE.md gets the rules block)")
        init_project(target, a.init.resolve(), a.dry_run)


if __name__ == "__main__":
    main()
