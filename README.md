# gd-skills — Game Design Skills for Claude Code

[![CI](https://github.com/minh190902/gd-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/minh190902/gd-skills/actions/workflows/ci.yml) ![version](https://img.shields.io/badge/version-0.3.0-blue) ![license](https://img.shields.io/badge/license-MIT-green)

A set of 16 skills that make Claude Code (and other agents that read Agent Skills) work like a **small game studio with a process** — a producer, a designer and a marketing lead:
- **walks you through the whole pipeline**, from idea to launch, one step at a time, with written gates between stages (works for first-time developers);
- **challenges ideas** with evidence instead of nodding along by default;
- **stops a new feature from breaking the logic of another**, using a map of who writes/reads state;
- **untangles things** when you feel overwhelmed;
- **always knows where the project stands.**

It also includes workflows for prototyping (one question, keep/kill criteria), writing specs, auditing systems, narrative design, economy balancing, pacing, UX, playtests and analyzing reference games.

The method is based on [Game Design Guide](https://gamedesign.guide) (CC BY 4.0, see [NOTICE.md](NOTICE.md)). The bundled tools read **Godot 4 / GDScript**, **TypeScript / JavaScript** (web engines such as Phaser, PixiJS, three.js) and **Nathan Hoad Dialogue Manager** files, and story flags kept in any code; the workflows work with any engine.

## Skills

| Skill | Use when |
|---|---|
| `gd-pipeline` | "What do I do next?", "guide me", are we doing it right: stage, gates, one step at a time (ROADMAP.md) |
| `gd-core` | General design questions; setting up a design dir for a new game; routing to other skills |
| `gd-status` | Start/end of a session: "where are we, what's next" (STATE.md) |
| `gd-design-review` | **Every time an idea comes up**: checks impact and conflicts, raises objections with severity |
| `gd-unstuck` | When confused: splits the problem, finds the blocking decision, picks the next step |
| `gd-prototype` | "Is it fun?": one-question prototype, keep/kill criteria written first, targeted self-tests, bots for balance |
| `gd-feature-spec` | Writing a spec before coding |
| `gd-feature-audit` | Keep, merge or cut features; overlap matrix |
| `gd-narrative-design` | Choice and consequence, flag payoffs, character arcs |
| `gd-economy-balance` | Sources/sinks, value curves, economy simulation |
| `gd-pacing-progression` | Pacing, unlock schedule, FTUE |
| `gd-ux-audit` | Screen audits, S1–S4 severity |
| `gd-playtest` | Test plans, result triage, decision log |
| `gd-game-analysis` | Deconstructing reference games and extracting action items |
| `gd-production-plan` | Scope, time estimates, milestones, cut list, risks, budget |
| `gd-go-to-market` | Positioning, Steam page, wishlists, demo/festival, launch, publisher, business setup |

## Installation

Requirements: Claude Code, Python 3.9+ (standard library only).

### Option 1: Plugin marketplace (Claude Code)
```
/plugin marketplace add minh190902/gd-skills
/plugin install gd-skills@gd-skills
```
Skills will be named like `gd-skills:gd-core`. Then open your game and ask Claude to "set up the design dir for this game" (per Section 1 of `gd-core`).

### Option 2: Copy into the game repo (recommended for teams)
This keeps the skills in the game repo's git, so the whole team uses the same version.
```bash
git clone https://github.com/minh190902/gd-skills
python gd-skills/tools/install.py --target <game_repo> --init <game_dir>
```
- `--target`: the repo receiving the skills, copied to `<repo>/.claude/skills/gd-*`.
- `--init`: creates `<game_dir>/docs/design/` from the templates (without overwriting existing files) and inserts the rules block into the repo's `CLAUDE.md`.
- `--global`: installs into `~/.claude/skills/` for use in every project.
- `--dry-run`: only prints what would be done.

**Updating:** `git pull`, then rerun the same command. The `gd-*` folders are fully replaced; your design docs are kept intact.

## Each game has a design dir

```
<game_root>/docs/design/
├── PROJECT.md      # identity, fantasy, pillars, core loop, platform constraints, risks
├── STATE.md        # where we are, next, open questions, parking lot (≤ 1 page)
├── ROADMAP.md      # pipeline stage, gate checklists, commercial/business tracks, stage debt
├── DECISIONS.md    # settled decisions and their rationale
├── SYSTEMS.md      # purpose of each system + auto-generated dependency map
└── gd.config.json  # configuration for the tools
```
The skills are shared; the data lives in each game. In a monorepo with several games, each game has its own design dir.

`gd.config.json` (all keys are optional):
```json
{
  "state_owners":    {"GameState": "scripts/game_state.gd"},
  "instance_owners": {"HeroData": "scripts/data/hero_data.gd"},
  "save_systems":    ["SaveLoadManager"],
  "flag_set_fns":    ["set_flag"],
  "flag_read_fns":   ["check_flag", "get_flag"]
}
```
For a TypeScript game: `"state_owners": {"GameState": "src/core/types.ts"}` (an interface, type or class). Story flags kept in code: `flag_sources`, `flag_set_patterns`, `flag_read_patterns`. Docs limits and translated STATE headings: `"docs": {...}`. Each script's docstring lists its keys.

## Tools

```bash
# Who writes/reads which state variable; blast radius; before/after comparison of an edit
python -I skills/gd-design-review/scripts/system_map.py <game_root> [--impact gold] [--snapshot f | --diff f]
# Flags set but never read, flags read but never set, broken jumps, orphan titles, choice & consequence table
python -I skills/gd-narrative-design/scripts/dialogue_audit.py <game_root> [--stage ch1] [--json]
# Per-stage economy simulation; ×1.2 curve check; exponential cost curve
python -I skills/gd-economy-balance/scripts/economy_sim.py sim model.json | curve 100 120 150 | growth --base 10 --rate 1.15
# STATE one page, decision index, STATE/ROADMAP stage agreement (--fix regenerates the index)
python -I skills/gd-core/scripts/docs_check.py <game_root> [--fix] [--strict]
```
Every script takes `--json` and exits 0 (ok), 1 (problems found; some only with `--strict`), 2 (target missing or wrong kind), so they can run in pre-commit hooks and CI.
The scripts are regex-based, not full parsers: treat their output as evidence to check, not as ground truth. Limitations are documented in each script's docstring.

## Usage examples

- *"I want to add a troop morale system that lowers loyalty after a defeat."* → `gd-design-review` lists every system writing/reading `loyalty`, flags conflicts with other systems that also touch loyalty, raises 🔴/🟠/🟡 objections and concludes Go / Park / Reject.
- *"I'm so confused, I don't know whether to do combat or story first."* → `gd-unstuck`.
- *"I've never made a game. What do I do next?"* → `gd-pipeline` finds the stage from ROADMAP.md and answers with one step: why, how, done when.
- *"How long will this take me alone?"* → `gd-production-plan`.
- *"When should I open the Steam page?"* → `gd-go-to-market`.
- *"Let's continue."* → `gd-status` reads STATE.md, compares it with git, and suggests the next task.
- *"Do the player's choices actually matter?"* → `gd-narrative-design`, workflow B.

## Other agents

The skills are plain `SKILL.md` folders (the Agent Skills format), so other agents load them too. `install.py --agents` also copies them to `<repo>/.agents/skills/`, the shared folder read by Codex, Gemini CLI, Antigravity, GitHub Copilot and Cursor. Other per-agent folders: Cursor `.cursor/skills/`, Windsurf `.windsurf/skills/`, Cline `.cline/skills/`, Kiro `.kiro/skills/`, Copilot `.github/skills/`; Claude Code `.claude/skills/`. Keep one rules file (`AGENTS.md`, imported by `CLAUDE.md`) so every agent follows the same workflow.

## Engine skills (complementary)

gd-skills owns the **design process**: stages, decisions, reviews, balance, playtests. For engine APIs and implementation (Godot nodes, Phaser scenes, save systems, shaders, Steam/itch uploads), pair it with an engine skill set such as [awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills). Install only the engine and the few discipline skills you use: skills with overlapping triggers (UI/UX, level design, dialogue) compete with `gd-ux-audit`, `gd-pacing-progression` and `gd-narrative-design`.

## Repo structure

```
gd-skills/
├── .claude-plugin/          # plugin.json + marketplace.json (Claude Code plugin)
├── .github/workflows/ci.yml # validate + tests (one cheap Linux job)
├── skills/                  # 16 gd-* skills (SKILL.md + references/ templates/ scripts/)
│   └── gd-core/templates/project/   # design dir skeleton for each game
├── tools/
│   ├── install.py           # install into a repo / globally, initialize the design dir
│   └── validate.py          # frontmatter, boundaries, links, orphan files, routing coverage, LF, JSON, version
├── tests/
│   ├── fixtures/mini_game/  # small Godot game with planted bugs
│   ├── fixtures/mini_web/   # small TypeScript game with planted bugs
│   └── test_tools.py
├── CHANGELOG.md · CLAUDE.md (contributor conventions) · LICENSE · NOTICE.md
```

## Development

```bash
python tools/validate.py                  # frontmatter, boundaries, links, orphans, routing coverage, LF, JSON, version
python -m unittest discover -s tests -v   # regression tests against small Godot and TypeScript fixtures
claude plugin validate .                  # Claude Code manifest check
```
Contributor conventions: see [CLAUDE.md](CLAUDE.md). Change history: [CHANGELOG.md](CHANGELOG.md).

## License

Code and skill content: [MIT](LICENSE). The method paraphrased from gamedesign.guide is under CC BY 4.0, credited in [NOTICE.md](NOTICE.md).
