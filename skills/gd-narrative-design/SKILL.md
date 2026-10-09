---
name: gd-narrative-design
description: Narrative design for branching, consequence-driven games — choice & consequence tables, flag payoff audits, character arcs, chapter/quest structure, ludonarrative and agency checks. Use when writing or reviewing dialogue, adding choices, planning story or character arcs, checking "do our choices matter", designing quests/events, or before/after editing .dialogue files. Includes dialogue_audit.py for Godot Nathan Hoad Dialogue Manager (unused flags, unreachable branches, broken jumps, orphan titles).
---

# GD Narrative Design

Narrative design is *how* the story is delivered through systems: flags, consequences, gameplay, UI. Scriptwriting is *what* is told. This skill owns the former and quality-checks the latter. Read `PROJECT.md` for the pillars related to the story and the player fantasy.

## Tool: static audit (Godot + Dialogue Manager)
`<skill_dir>` is the directory containing this skill.
```bash
python -I <skill_dir>/scripts/dialogue_audit.py <game_root>                 # everything
python -I <skill_dir>/scripts/dialogue_audit.py <game_root> --stage stage_3 # choice table for files whose name contains "stage_3"
python -I <skill_dir>/scripts/dialogue_audit.py <game_root> --json          # for further processing
```
The report includes:
- Flags that are set but never read: consequences that are never paid off, possibly a *choice illusion*.
- Flags that are read but never set: unreachable branches, or a typo in the name.
- Jumps to titles that do not exist.
- Titles with no path leading to them.
- Choices with no consequence at all.
- The choice and consequence table.

The flag set/check function names come from `gd.config.json` (`flag_set_fns`, `flag_read_fns`). Flags built with format strings must be checked by hand. For other narrative tools (ink, Yarn…), build a similar table with grep.

**Run the audit before and after every dialogue edit.** Do not report "done" while there are broken jumps or newly introduced flags that are read but never set.

## Workflow A — Write or extend a chapter / stage

1. **Context:** read the previous chapter's content, the entry points the code calls into, and the audit results to know which earlier flags are *waiting for a payoff*.
2. **Beat sheet:** Setup → Tension → Twist → Resolution, tied to the phases of the core loop. Note the target emotion at the start, middle and end, plus **one low-emotion beat** as breathing room.
3. **Key choices.** Design them as a table *before writing dialogue*:

   | Moment | Option | Mechanical outcome (immediate) | Story outcome (immediate) | Later payoff (chapter, title) |
   |---|---|---|---|---|

   - Each option must differ in the *journey*, not just the wording. Each option needs at least one mechanical consequence, or a scheduled later payoff.
   - **Every new flag must have at least one planned read** (noted in the Payoff column). If not, drop the flag or turn it into an immediate consequence.
   - Conditional options (based on the player's history) reward what they have done. Use them generously, because they give past decisions weight.
   - Show the numeric change on the option label only when you want the player to choose by the numbers. For purely moral choices, consider hiding the numbers.
   - Avoid an "obviously right" option. A good dilemma is one where every choice costs something the player values.
4. **Pay off debts:** for each relevant old flag, write at least one reaction: a conditional line, a conditional option, a gameplay change, or an epilogue variant.
5. **Write dialogue** following the project's existing conventions, keeping each character's voice consistent with their arc.
6. **Audit and fix:** run the script, fix broken jumps and orphan flags, and paste the choice and consequence table into the chapter's design doc.
7. **System integration:** does a consequence need a hook outside dialogue? If a new system is needed, use `gd-design-review` then `gd-feature-spec`.

## Workflow B — Audit "do the player's choices matter?"

1. Run the full audit. Group flags that are set but never read by chapter and by character/arc.
2. Classify each flag:
   - **(a) needs payoff:** a major choice the player will remember.
   - **(b) log/stats only:** document it clearly; it can be used for the epilogue.
   - **(c) junk:** delete.
3. For group (a), propose a concrete payoff: which chapter, which title, what form. Prefer cheap payoffs such as a conditional line, a conditional option, or an epilogue variant.
4. Check Thomas Grip's 4 layers for each chapter (table in [references/narrative-checklists.md](references/narrative-checklists.md)).
5. Output: `<game_root>/docs/narrative/<YYYY-MM-DD>-consequence-audit.md`, with a flag → type → proposed payoff → ticket table.

## Workflow C — Character arc / quest

Use the Character Arc table and quest checklist in [references/narrative-checklists.md](references/narrative-checklists.md). If a character can die or be absent, always write **alternate branches** for every important beat of that character.

## Required checks before delivery
- [ ] Audit is clean: no broken jumps, no new flags that are read but never set
- [ ] Every new flag has a documented payoff
- [ ] No ludonarrative dissonance: mechanics reward what the story values, or the mismatch is intentional
- [ ] The player's goal matches the character's goal; if the player knows something the character doesn't, that gap is intentional
- [ ] There are low-emotion beats; not every moment is a climax
- [ ] Every piece of lore has in-world context and is skippable
- [ ] Cases where a character is absent or dead are handled
- [ ] Text is localization-ready (no string concatenation in code)
