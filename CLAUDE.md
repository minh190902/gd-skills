# CLAUDE.md — gd-skills (source repo for the skill set)

This is the **source** repo for the `gd-*` skills. It is not a game. When editing:

- Skills live in `skills/<name>/SKILL.md`. Frontmatter: `name` matches the folder name; `description` in English, at most 1024 characters, no `<` or `>`, stating clearly **when to use** it (triggers). Content in English. Keep each SKILL.md under 500 lines; move long details into `references/` or `templates/`.
- **Never write anything specific to one game** into a skill. Game-specific information lives in that game's design dir (PROJECT.md, gd.config.json). Keep illustrative examples generic.
- Write script paths in SKILL.md as `<skill_dir>/scripts/...`. When another skill refers to one, name the skill (e.g. "system_map.py from gd-design-review"). Never hard-code `.claude/skills/...`, because the path differs when installed as a plugin.
- Scripts use only the Python standard library (Python 3.10+, the oldest version CI tests), run with `python -I`, and print UTF-8. Every new behavior needs a fixture and a test in `tests/`.
- Script contract (agents and hooks rely on it): `script.py TARGET [--json] [--strict] [--config PATH]`; exit 0 = no problems, 1 = problems found (some only with `--strict`), 2 = target missing or the wrong kind of project. Text output names `path:line` and how to fix; `--json` prints one object with a `tool` key. Configuration lives in the game's `gd.config.json`, documented in the script's docstring.
- Every SKILL.md has a "When not to use" section naming the sibling skills; every bundled file is linked from its SKILL.md; a new skill is added to the gd-core routing table and the README table (the validator checks all of this).
- Write files from Python with `write_bytes(text.encode("utf-8"))` or `newline="\n"`: `Path.write_text` writes CRLF on Windows.
- All files use LF (enforced by `.gitattributes`). On Windows, when writing files from Python, use `newline="\n"`.
- Before committing: `python tools/validate.py && python -m unittest discover -s tests && claude plugin validate .`
- Releasing a new version: bump the version in `.claude-plugin/plugin.json` and `marketplace.json` (both places), then add an entry to CHANGELOG.md.
