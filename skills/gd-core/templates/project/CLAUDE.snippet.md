<!-- gd-skills:begin -->
## Game design workflow (gd-* skills)

Design docs for this game: `{{DESIGN_DIR}}` (PROJECT, STATE, ROADMAP, DECISIONS, SYSTEMS, gd.config.json).

0. Know the pipeline stage (`{{DESIGN_DIR}}/ROADMAP.md`, skill `gd-pipeline`). When the user asks what to do next or is new to game development, give one step at a time (stage, next step, why, how, done when). Work that belongs to a later stage is flagged and, if the user still wants it, logged as stage debt.
1. Start of a design/gameplay session: read `{{DESIGN_DIR}}/STATE.md` (skill `gd-status`); report drift between git and STATE.
2. The user proposes an idea or a gameplay/story/system change → run `gd-design-review` before writing code. Challenge with evidence and never agree by default. The user decides; record the decision in DECISIONS.md.
3. The user is confused or overwhelmed → `gd-unstuck`.
4. Before changing code that writes shared state (see "Danger zones" in SYSTEMS.md) → run `system_map.py --impact` and check every reader.
5. After editing dialogue → run `dialogue_audit.py`; leave no broken jumps and no new read-but-never-set flags.
6. End of a session or task → update STATE.md, tick finished gate items in ROADMAP.md (and DECISIONS / SYSTEMS when they changed), then run `docs_check.py` (gd-core). New ideas that come up mid-task go to the parking lot.
7. Prototyping or asking "is it fun" → `gd-prototype`: one question, keep/kill criteria written and dated before building. Decisions the user must make → decision cards (gd-core references/decision-cards.md), recorded in ROADMAP "Pending decisions".
<!-- gd-skills:end -->
