# Stages, gates and tracks — detailed reference

Each stage lists: **Goal**, **Deliverables** (with default file locations under `<game_root>/docs/`), **Gate** (all must be true, each with evidence), **Out of stage** (work to avoid now), **Kill/pivot signals**, **Common mistakes**.

The stage sequence is the usual industry order (concept → prototype → vertical slice → production → alpha → beta → launch), with an explicit **Validate** stage inserted because solo and first-time developers most often skip it. Lengths are rough ranges for one person working part- or full-time; adjust in ROADMAP.md.

---

## 0 · Spark
- **Goal:** pick one idea on purpose instead of the first one.
- **Deliverables:** 3–5 idea cards and their scores (`gd-core` → references/pillars-and-concept.md, "Idea generation") in `analysis/ideas.md`.
- **Gate:**
  - [ ] At least 3 ideas compared on Feasibility, Innovation and Audience fit (1–5)
  - [ ] The chosen idea passes the 5 market filters (Desire, Contrast, Feasibility, Scalability, Meaning) with one line of evidence each
  - [ ] "Why me": one line on why this developer can build this game (skills, time, interest)
- **Out of stage:** any code, art or lore beyond a one-page sketch.
- **Kill/pivot signals:** no comparable game has ever sold; the idea needs skills or money the developer cannot get.
- **Common mistakes:** picking the dream project as a first commercial game; picking by theme instead of by loop.

## 1 · Concept
- **Goal:** state the game clearly enough that a stranger gets the genre in 5 seconds, and confirm the market exists.
- **Deliverables:** `design/PROJECT.md` filled (identity, fantasy, 3–5 pillars, core loop, business targets); a 1-pager; a short market check (`analysis/<date>-market.md` via `gd-game-analysis` / `gd-go-to-market` §A).
- **Gate:**
  - [ ] Pillars (3–5, verb + qualifier) and the player fantasy are written
  - [ ] Core loop drawn at 3 scales (seconds, a session, the whole game)
  - [ ] 3+ comparable games in the niche, with price, review count and rough sales, at least 2 of them commercially healthy for a team of similar size
  - [ ] Hook: one genre-first sentence; 5 strangers can say what genre it is and what they would do in it
  - [ ] Business targets written: platform, price range, intended length, time budget (hours/week × months), money budget
- **Out of stage:** world bibles, full story, many characters, final art, engine architecture.
- **Kill/pivot signals:** the niche's successful games were all made by much larger teams; strangers cannot tell what the game is after two rewrites of the hook.
- **Common mistakes:** a "X meets Y" pitch that names two genres the game is not; skipping the price/length target (it decides scope later).

## 2 · Find the Fun
- **Goal:** prove the core loop is fun in the cheapest possible form (paper, HTML, greybox in an engine).
- **Deliverables:** a playable prototype of the core loop only; a 1-page minimal spec per risky mechanic (`gd-feature-spec`); a self-play log (`playtest/<date>-selftest.md`): what was fun, what was boring, what changed.
- **Gate:**
  - [ ] The core loop is playable end to end in one sitting (one full cycle at least)
  - [ ] The developer has played it 10+ times and logged what is fun and what is not
  - [ ] The riskiest design question (written at the start) has an answer
  - [ ] The loop has been stable (no redesign of the core) for the last 1–2 iterations
- **Out of stage:** content beyond what one cycle needs, final art, polish, production code architecture, save systems, localization.
- **Kill/pivot signals:** after several iterations the developer is bored of their own loop; the fun only appears with content that does not exist yet ("it will be fun once the story is in").
- **Common mistakes:** building the prototype in production quality; testing with bots/simulations only (good for balance, blind to fun); adding systems to fix a loop instead of fixing the loop.

## 3 · Validate
- **Goal:** strangers confirm the fun, judged by criteria written **before** the test.
- **Deliverables:** a playtest plan with go/no-go thresholds (`gd-playtest` Workflow A) and a results report with a decision (`gd-playtest` Workflow B); 5–10 blind testers from the target audience (online communities, itch.io, Discord, local game dev meetups).
- **Gate:**
  - [ ] Go/no-go criteria written and dated before the first tester played (e.g. "≥ 60% would play another session", "≥ 4 of 6 can explain the goal after 5 minutes", "no S1 confusion in the first 5 minutes")
  - [ ] 5+ blind testers who are not friends or family played the current loop
  - [ ] Results compared with the criteria; a decision recorded in DECISIONS.md: Go / Iterate (back to 2) / Pivot / Kill
- **Out of stage:** same as stage 2; scaling content up "while waiting for testers".
- **Kill/pivot signals:** testers stop early and nobody asks to play again; they enjoy a different part of the game than the pillars claim (→ pivot toward that part).
- **Common mistakes:** writing criteria after seeing results; explaining the game during the test; treating "it's nice" as a pass.

## 4 · Pre-production
- **Goal:** answer "can we build it, at what cost, looking like what?" before committing years.
- **Deliverables:**
  - Art direction test: one target screenshot/mock at intended final quality, plus the production method (self-made, contracted, purchased, generated) and its cost per asset
  - Audio direction: references and method
  - Tech spike in the real engine: skeleton project, the riskiest technical feature, save/load, one build exported for the target platform
  - Feature specs for the systems kept after validation (`gd-feature-spec`); systems cut or merged (`gd-feature-audit`)
  - Production plan v1 (`gd-production-plan`): scope inventory, estimate, milestones, cut list, risk register, budget
  - Vertical slice definition: which part of the game, what "final quality" means
- **Gate:**
  - [ ] Art target image approved by the developer, method and cost per asset known
  - [ ] Engine skeleton runs a build on the target platform; riskiest tech question answered
  - [ ] Specs exist for every system in the vertical slice
  - [ ] Production plan v1: estimate fits the time budget, or scope was cut until it does
  - [ ] Vertical slice scope written and small (one level/chapter/area)
  - [ ] Business track items due at this stage (§Tracks) are done
- **Out of stage:** producing content for the whole game; final balancing.
- **Kill/pivot signals:** honest estimate is 2× or more over the time budget even after cutting to "must have"; art method is unaffordable.
- **Common mistakes:** skipping the art test because "art comes later" (art drives the store page); planning without measured unit costs and treating the plan as fixed.

## 5 · Vertical Slice
- **Goal:** one chunk of the game at final quality; measure real production cost; open the store page.
- **Deliverables:** the slice build (15–30 minutes of play); measured hours per content unit; production plan v2; store page "Coming Soon" with capsule art, screenshots, short trailer (`gd-go-to-market` §C).
- **Gate:**
  - [ ] Slice plays 15–30 minutes without crashes at intended quality
  - [ ] Stranger playtest on the slice meets the stage-3 criteria again (or better)
  - [ ] Real unit costs measured; production plan v2 still fits the time budget (or scope cut)
  - [ ] Store page live; capsule and trailer show the core verb in the first 5 seconds
  - [ ] Publisher decision made (self-publish or pitch with the slice)
- **Out of stage:** second and third chapters; polish of non-slice areas.
- **Kill/pivot signals:** real unit cost makes the full game impossible even at minimum scope; wishlists stay near zero after the page has been promoted (check the hook and art first).
- **Common mistakes:** a slice that is too big (a whole act); calling a horizontal prototype a vertical slice.

## 6 · Production
- **Goal:** build the rest of the game per plan, in milestones of 2–6 weeks, each ending with a playable build and a playtest.
- **Deliverables:** milestone builds; updated STATE/ROADMAP every session; specs before each new system; regular devlogs/community posts.
- **Gate → Alpha:**
  - [ ] Every planned feature is implemented (feature lock)
  - [ ] The game is playable start to finish, placeholder content allowed
  - [ ] Plan re-estimated at every milestone; scope cuts recorded in DECISIONS
- **Out of stage:** new systems not in the plan (→ `gd-design-review`, usually Park); polish passes on areas not yet content-complete.
- **Kill/pivot signals:** two consecutive milestones slip by more than 50%: run `gd-production-plan` cut workflow.
- **Common mistakes:** feature creep; no playtests "until it is ready"; silence on social channels for months.

## 7 · Alpha
- **Goal:** feature complete; balance and pacing over the whole game.
- **Deliverables:** full-run playtests (`gd-playtest`), balance pass (`gd-economy-balance`), pacing map (`gd-pacing-progression`), UX audit of every screen (`gd-ux-audit`), demo build planned.
- **Gate → Beta:**
  - [ ] All content in (content lock), no placeholders in the critical path
  - [ ] No known crash or progression blocker
  - [ ] At least one external tester finished the whole game
  - [ ] Demo build chosen and tested if a festival is planned
- **Out of stage:** new features.
- **Common mistakes:** adding content instead of fixing what exists.

## 8 · Beta
- **Goal:** polish, fix, localize, optimize; peak marketing before launch.
- **Deliverables:** bug list triaged to zero blockers; performance on minimum spec; localization; final store assets and trailer; demo/festival; launch plan (`gd-go-to-market` §E).
- **Gate → Launch:**
  - [ ] Release candidate: no S1/S2 bugs, runs on minimum spec, save compatibility tested
  - [ ] Store page complete, release date announced, price set
  - [ ] Wishlist or audience target from the plan reached, or the launch date moved deliberately
  - [ ] Launch checklist (`gd-go-to-market` references/launch-checklist.md) done
- **Common mistakes:** launching on a fixed date with too few wishlists; launching without a demo period.

## 9 · Launch and after
- **Goal:** ship, respond, stabilize, learn.
- **Deliverables:** launch-week plan; hotfixes; review replies; sales and refund tracking; postmortem (what worked, what to repeat, what to avoid) recorded in DECISIONS.md.
- **Gate (close project or move to updates/DLC):**
  - [ ] Critical post-launch bugs fixed
  - [ ] Postmortem written
  - [ ] Decision: support/updates, port, sequel, or move on

---

## Tracks (run in parallel with the stages)

### Commercial track (`gd-go-to-market`)
| Due by stage | Item |
|---|---|
| 1 Concept | Positioning: genre-first hook, comparable games, price/length target |
| 3 Validate | Hook test with strangers; a place to collect interested people (Discord, mailing list, social account) |
| 4 Pre-production | Final name chosen; capsule art concept; store page drafted |
| 5 Vertical Slice | Store page live (Coming Soon); short trailer; first announcement |
| 6 Production | Regular devlog/social cadence; press and creator list; festivals list with deadlines |
| 7 Alpha | Public demo plan; festival registration (deadlines are weeks before the event) |
| 8 Beta | Demo live, festival, release date, launch discount, press kit |
| 9 Launch | Launch-week plan, creator keys, review replies |

### Business track
| Due by stage | Item |
|---|---|
| 1 Concept | Money and time budget written (`gd-production-plan` §F) |
| 4 Pre-production | Name checked for trademark and search conflicts; store developer account opened; how revenue will be received and taxed in the developer's country; asset/tool licenses checked |
| 5 Vertical Slice | Publisher decision; store content disclosures (e.g. AI-generated content) prepared |
| 8 Beta | Age-rating / content questionnaires; EULA/privacy if data is collected; final credits and licenses |

## Stage debt

Work done ahead of its stage. Not forbidden, but every line carries rework risk. Format in ROADMAP.md:

`- <work> · belongs to stage <n> · done during stage <m> · risk: <one line> · revisit at: <gate>`

Review stage debt at every gate review. Debt that keeps growing faster than gates pass means the project is producing material, not progress.
