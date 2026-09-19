# Illustrative travel study

Open http://127.0.0.1:8765/ for the presentation. The real experiment UI remains at /lab. No model runs are required for this presentation.

## A 90-second walkthrough

1. Show the AI travel assistant and its five audience groups.
2. Select Family planners to narrow the study, or keep All travellers for the headline.
3. Search for `privacy` to retrieve a saved research passage. Explain that source context informs a grounded interview, but does not establish willingness to pay.
4. Move the price from £10 to £15: the full authored sample changes from 12/20 to 7/20 hypothetical paid choices. The median authored maximum price is £10.
5. Open a traveller's response to explain their benefit and objection.
6. Expand the method and assembled prompt. Export the example, including its disclosure and current selection.

## What actually executes

- Python serves the interface, fixture and `/api/showcase?q=privacy` endpoint.
- `showcase_service.py` splits saved research summaries into sentences, tokenises query and passage words, ranks by shared distinct keywords, and returns up to three matching passages with source links. This is lexical retrieval, not vector search or live web research.
- JavaScript applies the selected segment and price to 20 authored maximum-price values, computes counts, percentages and medians, and updates the chart and response panel.
- The assembled prompt includes offer, selected price, profile constraints and retrieved context. It is displayed, not submitted to a model.
- The generation step is replaced by authored fixtures. This is a RAG architecture demonstration with working retrieval, not a completed RAG-generated study.
- Separate real lab: MiroFish-local knowledge graph and profile seeds, OASIS interviews, local Ollama model, SQLite traces, Python orchestration. The real pilot remains unvalidated and is not the source of presentation figures.

## Data provenance

`travel/showcase-fixture.json` contains all 20 fictional profiles, invented opinions and maximum prices. Five workflow segments have four profiles each. Prices and quotes are manually authored for the walkthrough, not extracted from research or model runs. Paid choice means authored maximum >= displayed price. Everyone else keeps free tools. The allocation is not representative; there is no market extrapolation or accuracy claim.

Saved public research summaries in `travel/graph-sources.json` are displayed separately, with links and summary labels. Changing the retrieval query does not regenerate opinions or prices.

## Presentation

Black and green palette; local Space Grotesk and Space Mono. Sticky study context, scroll reveals, keyboard-operable audience and price controls, reduced-motion handling. Structural reference: https://getminds.ai/ (audience groups, study results, inspectable responses). No affiliation or borrowed validation claims.

## Verification

34 existing tests pass. New JavaScript passes syntax check. Fixture assertions verified 20 distinct profiles and 12 paid choices at £10; retrieval matching and no-match behaviour checked. Browser verified 12/20 at £10, 0/20 at £30, 7/20 at £15, family subset 3/4 at £15 and £17.50 median; privacy search returns one passage. At 390px the document has no horizontal overflow. Computed body font is Space Grotesk and background is #090d0b.

## Latest presentation revision: 1,000 profiles and RAG graph

Supersedes the earlier 20-profile presentation counts above. The fictional sample now contains 1,000 profiles, 200 in each of five groups. `scripts/build_showcase_population.py` deterministically expands the original authored seeds across destinations and durations, assigns authored price bands and multiselect friction answers, and ensures price wording matches each profile's maximum. These are not 1,000 independent interviews.

Full-sample paid choices: £5 → 820; £10 → 600; £15 → 360; £20 → 160; £25 → 60; £30 → 20. Fictional friction counts: coordination 498, cost comparison 620, reliability checks 608, replanning 630, booking organisation 550. Multiple selections allowed. Group organisers: 86% coordination. Budget travellers: 88% cost comparison. These percentages are computed from the fixture, not research estimates.

The RAG explorer displays connected source nodes, the currently retrieved passages, the query, selected fictional profile, assembled prompt and staged answer. Inspecting nodes reveals their actual contents and provenance. Searching updates passage nodes, edges and prompt context. Answers and willingness-to-pay values remain authored and do not change with retrieval. Chart and response filtering share one audience selection. The profile finder searches all matching profiles and renders up to 40 results for performance.

## Market-focused revision (supersedes prior illustrative counts)

See `research/travel-market-positioning.md`. Headline: **Learn from the future. Shape the present.** The commercial chart now compares a basic itinerary with a proposed trip-readiness pack across specific buying situations. Price outputs are labelled scenarios, with inspectable eligibility/price-response assumptions and low/high sensitivity bounds. The old generic friction percentages and 600/1000 example are obsolete. Competitor source cards and RAG retrieval now use `travel/market-sources.json`; exact annual USD pricing stays separate from hypothetical GBP per-trip tests. At £10: readiness 159/1000; basic 31/1000, both illustrative. Browser verified switching concepts updates results.
