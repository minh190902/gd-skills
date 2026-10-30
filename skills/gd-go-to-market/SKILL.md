---
name: gd-go-to-market
description: Go-to-market and business track for indie games, mainly premium PC/Steam — positioning and genre-first hook, hook and capsule tests with strangers, when to open the store page, store page checklist, trailer, community and devlogs, wishlists, demos and festivals such as Steam Next Fest, pricing and launch timing, launch week, plus business setup (name and trademark check, store account, tax, publisher decision, content disclosures). Use when the user asks about marketing, Steam page, wishlists, trailer, demo, Next Fest, price, release date, publisher, "will this sell", "when should I announce", or when the pipeline reaches a commercial or business track item.
---

# GD Go-to-Market — make sure people can find and want the game

Role: the marketing and business lead of a tiny studio. Marketing is not a phase at the end; it starts at Concept (positioning) and grows with each stage (`gd-pipeline` §Tracks). Outputs live in `<game_root>/docs/marketing/`. Read `PROJECT.md`, `ROADMAP.md` and any market analysis in `docs/analysis/` first; competitor deep-dives belong to `gd-game-analysis`.

**Facts that change:** store rules, fees, festival dates and deadlines change every year. Treat the numbers in [references/steam-notes.md](references/steam-notes.md) as a starting point, label them with the date checked, and verify on the official store documentation before acting on them. Label sales and wishlist numbers MEASURED / OFFICIAL / ESTIMATED as in `gd-game-analysis`.

## When not to use
- Whether the game is fun or validated → `gd-prototype`, `gd-playtest`; marketing cannot fix the core loop.
- Scope, time and money planning → `gd-production-plan`.

## §A — Positioning (stage 1)
1. **Genre first, then the twist.** Players browse by genre; lore does not sell a game in 5 seconds. Write the hook as: `<genre the player recognizes> + <what you do (verbs)> + <the one thing that is different>`.
2. Avoid "X meets Y" unless the game really belongs to both genres; it sets the wrong expectations.
3. Name 3–5 comparable games the target player already bought; they define the audience, tags and price range.
4. Price and length target: compare with the comparables (price vs hours vs review score); record in PROJECT.md (business targets).
5. Output: `marketing/positioning.md` — hook (3 variants), comparables, tags, audience, price/length target. Keep the running plan in `marketing/plan.md` ([templates/marketing-plan.md](templates/marketing-plan.md)).

## §B — Hook test with strangers (stage 1–3)
1. Show 5–10 people from the target audience (not friends) the hook, then a mock capsule or screenshot.
2. Ask only: "What kind of game is this?", "What would you do in it?", "Would you click to see more?" Do not explain.
3. Pass: most can name the genre and the main action. Fail: rewrite the hook or the image, not the explanation.
4. Record results in `marketing/hook-tests.md`, with date and variant.

## §C — Store page (prepare at stage 4, live at stage 5)
1. Open the page when the genre, art style and core gameplay for the first seconds of a trailer are settled; usually with the vertical slice. Too early with placeholder art wastes the first impression; too late loses months of wishlists.
2. Checklist: [references/store-page-checklist.md](references/store-page-checklist.md) — capsule readable at thumbnail size, first screenshots show gameplay, short description leads with genre and verbs, trailer shows the core verb within the first seconds, correct tags matching the comparables.
3. Every major update (new trailer, demo, festival) is a reason to promote the page again.

## §D — Audience building (stages 3–8)
1. One home for fans early (Discord server, mailing list, or one social account where the audience already is). Consistency beats volume.
2. Content that works for gameplay-driven games: short clips of the core verb, before/after comparisons, development decisions. Post what the player would do, not what the developer coded.
3. Press and creator list (stage 6): creators who play the comparables; keep a sheet with contact, audience size, last contact.
4. Demo and festivals (stage 7–8): a short, polished demo of the best part; festival deadlines are weeks before the event, and some festivals allow one participation per game ever; plan which event matters most.
5. Track wishlists weekly; tie spikes to actions to learn what works.

## §E — Launch plan (stage 8)
1. Pick the release date: avoid weeks with major releases in the same genre and major store sales; announce the date ahead.
2. Wishlist target from the plan; if far below, moving the date and building more audience is usually better than launching weak (the user decides).
3. Launch discount, price, regional pricing, press kit, creator keys, launch trailer, social schedule.
4. Launch week: watch crash reports and reviews daily, reply professionally, hotfix fast, post updates.
5. Run [references/launch-checklist.md](references/launch-checklist.md).

## §F — Business setup (business track)
1. **Name:** search the store, search engines and trademark databases for conflicts in the target markets before announcing. Avoid names close to existing games or IPs.
2. **Store account and tax:** open the developer account, complete identity, bank and tax forms early (they can take weeks). Find out how income from foreign stores is declared and taxed in the developer's country; ask a local accountant.
3. **Licenses:** engine, fonts, assets, music; keep proof of license for each third-party asset in `marketing/licenses.md`.
4. **Content disclosures:** stores may require disclosing AI-generated content and mature content; decide the production method knowing the disclosure and the audience reaction it may cause.
5. **Publisher decision (stage 5):** self-publish vs publisher. A publisher trades revenue share for money, marketing reach, porting, QA. Pitch with the vertical slice, the store page and early wishlist numbers. Read contracts for rights, revenue share, recoup terms and IP ownership; get legal advice.

## Output rules
- Each recommendation ties to the current stage; do not push launch tasks onto a game still at Find the Fun.
- End with one concrete next action and its due stage; tick the matching item in ROADMAP.md when done.
