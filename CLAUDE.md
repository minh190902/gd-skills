# CLAUDE.md — gd-skills (source repo for the skill set)

This is the **source** repo for the `gd-*` skills. It is not a game. When editing:

- Skills live in `skills/<name>/SKILL.md`. Frontmatter: `name` matches the folder name; `description` in English, at most 1024 characters, no `<` or `>`, stating clearly **when to use** it (triggers). Content in English. Keep each SKILL.md under 500 lines; move long details into `references/` or `templates/`.
- **Never write anything specific to one game** into a skill. Game-specific information lives in that game's design dir (PROJECT.md, gd.config.json). Keep illustrative examples generic.
- Write script paths in SKILL.md as `<skill_dir>/scripts/...`. When another skill refers to one, name the skill (e.g. "system_map.py from gd-design-review"). Never hard-code `.claude/skills/...`, because the path differs when installed as a plugin.
- Scripts use only the Python standard library, run with `python -I`, and print UTF-8. Every new behavior needs a fixture and a test in `tests/`.
- All files use LF (enforced by `.gitattributes`). On Windows, when writing files from Python, use `newline="\n"`.
- Before committing: `python tools/validate.py && python -m unittest discover -s tests && claude plugin validate .`
- Releasing a new version: bump the version in `.claude-plugin/plugin.json` and `marketplace.json` (both places), then add an entry to CHANGELOG.md.
