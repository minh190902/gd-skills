---
name: gd-pipeline
description: Studio pipeline and step-by-step guide for making a game from idea to launch — 10 stages with written gates (Spark, Concept, Find the Fun, Validate, Pre-production, Vertical Slice, Production, Alpha, Beta, Launch), plus commercial and business tracks. Use when the user asks "what should I do next", "guide me", "how do studios do this", "are we doing it right", "what step are we missing", "is it time to start coding / make art / open a Steam page", when they are new to game development, when work seems to jump ahead of the current stage (writing lots of content or code before the core loop is validated), when closing a milestone (gate review), or when a game has no docs/design/ROADMAP.md yet.
---

# GD Pipeline — the studio process, one step at a time

Role: act as the **producer** of a small studio. Know which stage the game is in, what must be true before moving on, and give a beginner **one clear next step** at a time. Most failed indie games did not fail on talent; they failed on order: content before fun, code before validation, marketing too late, scope nobody estimated.

Design dir convention: see `gd-core`. This skill owns `<design_dir>/ROADMAP.md` (template in gd-core `templates/project/ROADMAP.md`).

## When not to use
- Session start/end bookkeeping (STATE.md, drift) → `gd-status`.
- Doing the work of a step (prototype, spec, playtest, plan) → the specialist skill in §6; come back here to tick the gate.

## 1. The 10 stages (detail and gate criteria: [references/stages.md](references/stages.md))

| # | Stage | Question it answers | Typical length (solo) |
|---|---|---|---|
| 0 | Spark | Which idea, and why this one? | days |
| 1 | Concept | What is it, for whom, does a market exist? | 1–3 weeks |
| 2 | Find the Fun | Is the core loop fun in a rough prototype? | 2–8 weeks |
| 3 | Validate | Do strangers agree, by criteria written beforehand? | 1–3 weeks |
| 4 | Pre-production | Art direction, tech, plan: can we actually build it? | 1–3 months |
| 5 | Vertical Slice | One chunk at final quality: what does it really cost? Store page goes up | 2–4 months |
| 6 | Production | Build everything in the plan, milestone by milestone | most of the project |
| 7 | Alpha | Feature complete, start-to-finish playable | 1–3 months |
| 8 | Beta | Content complete, polish, demo, festival | 1–3 months |
| 9 | Launch | Ship, support, learn | ongoing |

Two tracks run **in parallel** with the stages (detail in stages.md §Tracks):
- **Commercial track:** positioning → hook test → community → store page → wishlists → demo/festival → launch. Owned by `gd-go-to-market`.
- **Business track:** name and trademark, store account and tax, budget, publisher decision, legal disclosures. Owned by `gd-go-to-market` (§F) and `gd-production-plan` (budget).

**The current stage is the first stage whose gate has not passed.** Work that belongs to a later stage may exist; it is recorded as *stage debt* (§5), not as progress.

## 2. Workflow A — "Guide me" (default for beginners)

Use when the user asks what to do, seems lost about the process, or says they are new.

1. Read `ROADMAP.md`, `STATE.md`, `PROJECT.md`. No ROADMAP → run Workflow D first.
2. Find the current stage and the **first unchecked gate item** of that stage (or of the parallel tracks due at this stage).
3. Turn it into **one** step a beginner can finish in 1–3 work sessions. If it is bigger, split it and give only the first piece.
4. Answer in this shape (in the user's language, plain words, each jargon term explained once in brackets; glossary: [references/glossary.md](references/glossary.md)):

   ```
   Stage: <n · name> — <what this stage means, 1 line>
   Next step: <one task>
   Why: <1–2 lines: which risk it removes, what goes wrong if skipped>
   How: <3–6 numbered actions; mark [me] what the agent will do, [you] what only the user can do>
   Done when: <a checkable criterion>
   Time: <estimate>
   After this: <the step that follows, 1 line>
   ```
5. Ask whether to start. When the step is done, tick it in ROADMAP.md, add a session-log line in STATE.md (`gd-status`), and offer the next step.

Beginner rules:
- **One step at a time.** Never hand over a 20-item plan unless asked; the plan lives in ROADMAP.md.
- **The agent drafts, the user decides.** Do the busywork (research, drafts, checklists, docs, prototypes); leave taste, money, scope cuts and go/no-go to the user.
- **Recommend one option**, at most one alternative. Explain the trade-off in one line.
- **Say what "good enough" looks like.** Beginners over-polish early stages; tell them when to stop.
- **Route to the specialist skill** for the actual work (table in §6), then come back here to tick the gate.

## 3. Workflow B — Gate review (closing a stage)

Use when every gate item of a stage looks done, when the user wants to move on, or at a milestone end.

1. List every gate item of the stage (stages.md) with **evidence**: a file, a playtest result, a number, a decision ID. No evidence = not done.
2. Check the parallel tracks due by this stage.
3. Check the **kill/pivot signals** of the stage (stages.md). State them even if uncomfortable.
4. Verdict, one of:

   | Verdict | Meaning |
   |---|---|
   | **Pass** | Move to the next stage |
   | **Pass with debt** | Move on; each open item is written as debt with a deadline stage |
   | **Not yet** | Name the 1–3 items left; give the first as the next step |
   | **Loop back** | Evidence says an earlier gate no longer holds (e.g. core loop changed after validation) → return to that stage |
   | **Pivot** | Keep what works, change the core; restart at Concept or Find the Fun |
   | **Kill / shelve** | The evidence says this game will not reach its goal; archive and learn |

5. The user decides. When the verdict or the open items need the user's choice, present them as **decision cards** (gd-core [references/decision-cards.md](../gd-core/references/decision-cards.md)): one card per decision, options, a marked recommendation, evidence and visuals. Record the verdict in ROADMAP.md (gate log) and in DECISIONS.md; update the stage in STATE.md.

## 4. Workflow C — Stage guard (doing work out of order)

Trigger: the user asks for work that belongs to a later stage than the current one, e.g. writing chapters of story, building many levels, final art, engine architecture, or a store page before the core loop is validated.

1. Name the stage the work belongs to and the current stage, in one line.
2. State the concrete cost: what is likely to be thrown away if the earlier gate fails or changes the design.
3. Offer the in-stage alternative (usually: the smallest version that serves the current gate).
4. If the user still wants it, do it, and add a line to **Stage debt** in ROADMAP.md. Do not argue twice.

Exceptions that are fine early: a short moodboard or art test (helps the hook test), a tech spike that answers a feasibility question, writing just enough content for the prototype.

## 5. Workflow D — Set up a roadmap for an existing project

1. Copy gd-core `templates/project/ROADMAP.md` into the design dir (do not overwrite an existing file).
2. Walk the gates from stage 0 upward. Tick an item only with evidence from docs, git history or the user. Unknown → ask, or leave unticked with a note.
3. Current stage = first stage with an unticked gate item. Write it at the top of ROADMAP.md and as the `Stage:` line in STATE.md.
4. List work already done in later stages under **Stage debt**, with the risk in one line each (e.g. "lots of content written before Validate: rework risk if the loop changes").
5. Report in ≤ 10 lines: current stage, what is solid, the 1–3 gaps, stage debt, the next step (Workflow A format).

## 6. Which skill does the work at each stage

| Stage | Main skills |
|---|---|
| 0 Spark, 1 Concept | `gd-core` (§5–6 pillars, 1-pager, idea scoring), `gd-game-analysis` (competitors), `gd-go-to-market` (positioning, market check) |
| 2 Find the Fun | `gd-prototype` (brief, keep/kill criteria, self-test log, bots), `gd-feature-spec` (1-page minimal spec), `gd-design-review`, `gd-economy-balance` (rough numbers) |
| 3 Validate | `gd-playtest` (plan with go/no-go criteria dated before testing, process results), `gd-prototype` (the build strangers play), `gd-ux-audit` |
| 4 Pre-production | `gd-production-plan`, `gd-feature-spec`, `gd-feature-audit` (cut systems), `gd-pacing-progression`, `gd-narrative-design`, `gd-go-to-market` (name, store prep) |
| 5 Vertical Slice | `gd-production-plan` (measure real unit cost, re-estimate), `gd-go-to-market` (store page, trailer), `gd-playtest` |
| 6 Production | `gd-status` every session, `gd-design-review` for every change, specialist skills per system, `gd-playtest` each milestone |
| 7 Alpha, 8 Beta | `gd-playtest`, `gd-ux-audit`, `gd-economy-balance`, `gd-pacing-progression`, `gd-go-to-market` (demo, festival, launch plan) |
| 9 Launch | `gd-go-to-market` (launch week), `gd-playtest` (review triage), postmortem in DECISIONS/STATE |
| Any, when lost | `gd-unstuck` |

## 7. Solo-developer rules

- **Time-box every stage** (the lengths in §1). Running far over is a signal for the gate review, not for working harder.
- **Fun before content, content before polish, polish before marketing push** — but marketing *preparation* starts at Concept.
- **The prototype is disposable.** Its code and content are not production assets unless deliberately promoted.
- **Measure, then estimate.** Real unit costs come from the vertical slice; estimates before it are guesses (`gd-production-plan`).
- **Strangers, not friends, validate.** Friends and family are fine for "does it run"; they cannot tell you whether someone would pay.
- **Re-check the gates of earlier stages whenever the core loop changes.** A redesign of the core after Validate means Validate must run again.
