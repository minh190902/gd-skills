# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/), versioning per [SemVer](https://semver.org/).

## [0.3.0] - 2026-10-30

Fit for non-Godot games and lessons from using the skills on a real project; ideas from awesome-gamedev-agent-skills (Apache-2.0) adapted in our own words.

### Added
- `gd-prototype`: one-question prototype brief, throwaway vs keep, timebox, instrumenting, keep/kill/refactor criteria written and dated before building, targeted self-test sessions, familiarity vs loop fatigue, bots and AI agents as testers (what each can and cannot judge), rule switches with a parity baseline, keep-means-rewrite. Template `prototype-brief.md`.
- `docs_check.py` (gd-core): STATE one page (size, long lines, in-progress and session-log counts, headings configurable for any language), duplicate decision IDs, generated decision index (`--fix`, keeps a translated header), Supersedes links, STATE vs ROADMAP stage drift.
- `system_map.py`: TypeScript/JavaScript profile (interfaces/types/classes as owners; aliases from annotations, `as` casts, imports of an exported state binding, config; `call_depth` hops, default 1; method calls never resolve to free helpers; reset/load functions and test files skipped), `--json`, `--language`.
- `dialogue_audit.py`: story flags kept in any code or data (`flag_sources`, `flag_set_patterns`, `flag_read_patterns`), with or without `.dialogue` files.
- `economy_sim.py growth` (exponential cost curves: doubling interval, explosion warning), `curve --band`, `--json` on every command.
- Decision cards (gd-core `references/decision-cards.md`), used by gd-pipeline gate reviews and gd-unstuck; ROADMAP template "Pending decisions".
- gd-economy-balance `references/genre-levers.md`: tower defense, RPG stats, roguelike loot, card games, survival/crafting, idle/prestige; bot harness on the real rules.
- gd-playtest: go/no-go criteria dated before the first tester, non-human testers table, seeds and run report codes, blind human scoring for taste choices.
- gd-ux-audit: relayouts start from reference-game lineages; measurable floors (text size, contrast, touch targets, flashing, localization room, feedback size).
- gd-pacing-progression: sawtooth rules and beats as data, Introduce → Develop → Twist → Test, unlock reachability check.
- gd-narrative-design: structure cost (linear → full routes), apply choice effects on the choice, Workflow D canon lint.
- gd-production-plan: production method per asset kind decided by Concept, no-budget risk check, cut triage.
- Steam timing traps and itch.io draft advice in steam-notes; README sections on other agents and complementary engine skill sets.

### Changed
- Every skill has a "When not to use" section naming the sibling skill.
- Check-script contract for every script: `--json`, `--strict` where it applies, exit 0 ok / 1 problems / 2 target missing. `dialogue_audit.py` now exits 1 on broken jumps.
- `tools/validate.py`: frontmatter must be exactly name + description; description must say when to use; "When not to use" required; unknown `gd-*` names, orphan files, unresolved backticked paths, routing and README coverage, README skill count; SKILL.md over 500 lines is an error; `--root` for tests.
- Gate 2 counts targeted self-test sessions; Pre-production adds an art bible, an asset manifest and blind style scoring; DECISIONS template carries the generated index; STATE names the history file; rules block runs `docs_check.py` and routes prototypes.

## [0.2.1] - 2026-10-26

### Added
- `tools/install.py --agents`: also install the skills into `<target>/.agents/skills`, so agents that read that folder never run an older hand-copied version.
- The rules block goes into `AGENTS.md` when `CLAUDE.md` imports it (`@AGENTS.md`); an old block in `CLAUDE.md` is removed. One rules file for Claude Code, Codex and other agents.

## [0.2.0] - 2026-10-12
### Added
- `gd-pipeline`: 10-stage studio pipeline (Spark → Launch) with written gates, commercial and business tracks, stage debt, gate review verdicts, and a beginner "guide me" mode that gives one step at a time. Glossary for first-time developers.
- `gd-production-plan`: scope inventory, estimates labeled MEASURED / ESTIMATED / GUESS, buffers, MoSCoW cut workflow, milestones, risk register, money runway, re-estimation; template.
- `gd-go-to-market`: positioning, hook tests, store page timing and checklist, audience building, demos and festivals, launch plan and checklist, business setup (name, store account, tax, licenses, disclosures, publisher); dated Steam notes; marketing plan template.
- Design dir template `ROADMAP.md`; `Stage:` line in STATE.md; "Business targets" section in PROJECT.md.

### Changed
- `gd-core` routes to the new skills and sets up ROADMAP.md; `gd-status` reports the stage and ticks gate items; `gd-design-review` checks stage fit; the CLAUDE.md rules block adds the stage rule.

## [0.1.0] - 2026-10-09
### Added
- 12 `gd-*` skills: core (router + project setup), status, design-review, unstuck, feature-spec, feature-audit, narrative-design, economy-balance, pacing-progression, ux-audit, playtest, game-analysis.
- Per-game design dir convention: `docs/design/{PROJECT,STATE,DECISIONS,SYSTEMS}.md` and `gd.config.json`.
- Tools: `system_map.py` (who writes/reads state, impact, diff), `dialogue_audit.py` (Dialogue Manager), `economy_sim.py` (Monte Carlo + ×1.2 curve).
- `tools/install.py` (install into a repo or globally, initialize the design dir, insert the rules block into CLAUDE.md), `tools/validate.py`, regression tests with a small Godot fixture.
- Minimal GitHub Actions CI (one Ubuntu job on Python 3.9, path-filtered, cancel-in-progress, 5-minute cap), `.editorconfig`, `.gitignore`, `.gitattributes` (LF).

### Fixed
- `install.py` crashed on Python 3.9 (`Path.write_text(newline=)` requires 3.10).
