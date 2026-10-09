<!-- gd-skills:begin -->
## Game design workflow (gd-* skills)

Design docs for this game: `{{DESIGN_DIR}}` (PROJECT, STATE, DECISIONS, SYSTEMS, gd.config.json).

1. Start of a design/gameplay session: read `{{DESIGN_DIR}}/STATE.md` (skill `gd-status`); report drift between git and STATE.
2. The user proposes an idea or a gameplay/story/system change → run `gd-design-review` before writing code. Challenge with evidence and never agree by default. The user decides; record the decision in DECISIONS.md.
3. The user is confused or overwhelmed → `gd-unstuck`.
4. Before changing code that writes shared state (see "Danger zones" in SYSTEMS.md) → run `system_map.py --impact` and check every reader.
5. After editing dialogue → run `dialogue_audit.py`; leave no broken jumps and no new read-but-never-set flags.
6. End of a session or task → update STATE.md (and DECISIONS / SYSTEMS when they changed). New ideas that come up mid-task go to the parking lot.
<!-- gd-skills:end -->
