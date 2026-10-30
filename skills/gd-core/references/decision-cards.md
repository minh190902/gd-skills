# Decision cards — how to put a choice in front of the owner

A decision buried in a chat reply gets lost, answered half-way, or answered without the evidence. When the user has to settle something (a gate verdict, a direction, a style, a scope cut), write it as a **card**. Several cards waiting at once go in ROADMAP.md under "Pending decisions"; a chosen card moves to DECISIONS.md as an entry.

## Card format (text)

```markdown
### <n>. <the question, one line> (YYYY-MM-DD)
<context: 1–3 sentences, with links to the evidence (playtest log, sim table, doc)>
- (a) <option>: <what it means in practice>
- (b) <option>
- (c) <option>
- Recommendation [source]: **(x) <short reason>**   ← source = new analysis / D-xxx / playtest / reference
- Images: <file or chart id> | <caption>
- References: <title> | <url>
- If (x): <who does what next; how long>
- Chosen (YYYY-MM-DD, where): (x) <note>              ← filled in by the user's answer
```

Rules:
- **One question per card**, answerable by picking an option. "What do you think about X" is not a card.
- 2–4 options, mutually exclusive, each concrete enough to act on. Include "not now / park" when it is a real option.
- **Exactly one recommendation**, with its source and the main trade-off in one line. State uncomfortable signals plainly (a kill/pivot sign, a missed gate).
- Show, don't describe, when the choice is visual or numeric: a chart of the playtest numbers, the two art candidates side by side, a reference screenshot.
- The user's answer is recorded where the agent can read it later (the doc, or a page with shared storage), never only in a browser's local storage or a chat.

## Card page (optional)

For several cards or visual choices, render the cards as one page: each card with its options as clickable choices, the recommendation marked, a free-text note box, the images and reference links. Save the user's answers in a place the agent can read back, then copy them into ROADMAP.md / DECISIONS.md. The text format above stays the source; the page is a view of it.

## After the choice
1. Fill in "Chosen" on the card.
2. Add the DECISIONS.md entry (decision, why, rejected options, accepted risks), run `docs_check.py --fix` to refresh the index.
3. Remove the card from "Pending decisions" and put the follow-up step in STATE.md "Next".
