---
name: gd-unstuck
description: Help the user when they feel confused, overwhelmed or stuck on game design or project direction — untangle a messy set of questions into facts to look up, decisions to make and worries to park, find the one blocking decision, recommend, and give the next small step. Use when the user says they are "confused", "lost", "don't know where to start", "it's all a mess", "I don't get why" (in any language), asks many tangled questions at once, contradicts earlier ideas, or seems lost about how systems fit together.
---

# GD Unstuck — untangling

When confused, the user does not need more information; they need to **hold fewer things in their head**. The end goal is one settled decision or one small next step, with everything else written down.

## Process

1. **Don't lecture right away.** Treat the user's message as their brain dump. If the message is too short to understand, ask just one question: "What's bothering you most right now?"
2. **Reflect back:** split the message into a numbered list, one short line per item, using the user's own words. Ask again if any item was misunderstood.
3. **Classify** each item:

   | Type | Handling |
   |---|---|
   | ❓ **Fact to look up** | Look it up right away (code, `system_map.py`, docs) and answer with evidence |
   | ⚖ **Decision to make** | Group them, then find the decision blocking the others (step 4) |
   | ✅ **Already decided** | Quote the matching entry in DECISIONS.md, restate it, no need to rethink |
   | 🅿 **Worry about the future** | Put it in the parking lot in STATE.md |
   | 🚫 **Not a problem** | Briefly explain why |

4. **Find the blocking decision**: the one the other decisions depend on. Draw a short dependency chain if it helps (`A → B → C`). It usually sits at the earliest broken layer of the Game Map (Player → Structure → Cognition → Dynamics → Perception), or in the pillars in PROJECT.md.
5. **For that decision:** give 2–3 options, a short trade-off table (pillar served · systems affected · cost), and **one recommendation with reasons**. If there is genuinely not enough data to choose, propose the cheapest way to get it: a prototype of a few hours, a simulation run, or reading the code.
6. **Smallest next step**: about 1–2 hours, with an observable result.
7. **Record:** the settled decision in DECISIONS.md, worries in the parking lot, the next step in the "Next" section of STATE.md (via `gd-status`). Tell the user explicitly that everything has been written down, so they no longer need to remember it.

## When confused about how systems relate
Draw a simple ASCII diagram: the core loop from PROJECT.md, each system placed in its phase, and arrows for the state variables they share (from `system_map.py` or SYSTEMS.md). One correct picture replaces ten paragraphs of explanation.

## How to talk
- Short, clear, step by step. Don't list 10 options.
- Use concrete examples from the user's own game (character names, levels, screens), not generic theory.
- End with: the settled decision (if any), the next step, and where things were recorded.
