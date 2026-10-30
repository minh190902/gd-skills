# Sources & attribution

The `gd-*` skill set was built (October 2026) on research from **Game Design Guide** — https://gamedesign.guide (v1.01, 02/09/2025, by Evgenia Gapeeva), licensed **CC BY 4.0**. The content has been paraphrased, condensed and adapted for the project; it is not quoted verbatim.

Main pages used:
- Theory (5-layer Game Map): https://gamedesign.guide/theory
- Analysis (feature breakdown, UX failures, player behavior, actionable analysis): https://gamedesign.guide/analysis
- Practice (templates GDD / Feature Concept / Balance / Narrative Design Doc / Pitch, iteration, documentation): https://gamedesign.guide/practice
- Specialties (system, balance, narrative, content, encounter, UX design): https://gamedesign.guide/specialties
- Terminology (choice illusion, ludonarrative dissonance, agency, friction, FTUE, funnel, retention…): https://gamedesign.guide/terminology

Additions NOT on the site (our own):
- The UX severity scale (S1–S4) and UX report template in `gd-ux-audit`.
- Balance formulas (diminishing returns, soft cap, sink/faucet ratio) in `gd-economy-balance/references/balance-math.md` — standard industry knowledge (Schreiber & Romero, *Game Balance*).
- The `dialogue_audit.py` and `economy_sim.py` scripts.
- The design dir convention (PROJECT / STATE / DECISIONS / SYSTEMS / ROADMAP) and the gd-status, gd-design-review, gd-unstuck skills.
- `gd-pipeline`, `gd-production-plan`, `gd-go-to-market` (added 2026-10-12): the common industry stage sequence (concept → prototype → vertical slice → production → alpha → beta → launch) with an explicit Validate stage and stage gates; production estimating practice; indie marketing practice as commonly taught (e.g. Chris Zukowski, howtomarketagame.com) and the Steamworks documentation (partner.steamgames.com/doc). Store facts are dated and must be re-verified.

- v0.3 additions (2026-10-30): `gd-prototype`, decision cards, `docs_check.py`, the TypeScript profile of `system_map.py`, flags-in-code for `dialogue_audit.py`, `economy_sim.py growth`, and the genre levers reference. Several rules of thumb (prototype brief and kill criteria, genre balance levers, accessibility floors, Steam and itch timing notes, the check-script contract) were adapted from **awesome-gamedev-agent-skills** — https://github.com/gamedev-skills/awesome-gamedev-agent-skills (Apache-2.0); rewritten, not copied. The process lessons (targeted self-test sessions, AI vs blind human scoring, decision pages, one doc per topic, no-budget production) come from using these skills on a real project.

Further reading (from the site's bibliography): *The Art of Game Design* (Schell), *Game Feel* (Swink), *The Gamer's Brain* (Hodent), *Game Balance* (Schreiber & Romero), *Advanced Game Design: A Systems Approach* (Sellers), *Game Design Workshop* (Fullerton), *Thinking in Systems* (Meadows), *Writing for Games* (Nicklin).
