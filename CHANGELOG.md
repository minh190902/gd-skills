# Changelog

Format based on [Keep a Changelog](https://keepachangelog.com/), versioning per [SemVer](https://semver.org/).

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
