#!/usr/bin/env python3
"""Install the gd-* skills into a repo (or globally) and optionally set up a game's design dir.

  python tools/install.py --target <repo>                     # copy skills to <repo>/.claude/skills/
  python tools/install.py --global                            # copy skills to ~/.claude/skills/
  python tools/install.py --target <repo> --init <game_root>  # + create <game_root>/docs/design/
                                                              #   and add the rules block to <repo>/CLAUDE.md
  add --dry-run to print what would happen.

Updating: re-run the same command. gd-* skill folders are replaced entirely (no stale files);
existing design docs (PROJECT/STATE/DECISIONS/SYSTEMS/gd.config.json) are never overwritten;
the CLAUDE.md block between <!-- gd-skills:begin/end --> is replaced in place.
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
    claude = target / "CLAUDE.md"
    text = claude.read_text(encoding="utf-8") if claude.exists() else ""
    if BEGIN in text and END in text:
        new = text[: text.index(BEGIN)] + block + text[text.index(END) + len(END):]
        msg = f"update  gd-skills block in {claude}"
    else:
        new = (text.rstrip() + "\n\n" if text.strip() else "") + block + "\n"
        msg = f"append  gd-skills block to {claude}"
    act(dry, msg, lambda: claude.write_text(new, encoding="utf-8", newline="\n"))
    if fresh:
        print(f"\nNext: open the game in Claude Code and ask it to fill {rel}/PROJECT.md and gd.config.json "
              f"(skill gd-core, section 1).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--target", type=Path, help="repo root to install into (.claude/skills)")
    g.add_argument("--global", dest="glob", action="store_true", help="install into ~/.claude/skills")
    ap.add_argument("--init", type=Path, metavar="GAME_ROOT", help="also create GAME_ROOT/docs/design")
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
    if a.init:
        if a.glob:
            sys.exit("--init needs --target (the repo whose CLAUDE.md gets the rules block)")
        init_project(target, a.init.resolve(), a.dry_run)


if __name__ == "__main__":
    main()
