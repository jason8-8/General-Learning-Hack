# AI travel assistant: demo research

> Build update, 20 September 2026: Jason has resumed implementation. The local six-person MiroFish interview demo and versioned feedback rerun now work, with bundled real-run replays. Sources/profiles remain curated, example feedback is illustrative, and separate validation is pending. Earlier references to a pause below describe the planning snapshot. See [current build](../product/prototype/RUN-MIROFISH.md).

Checked 20 September 2026. Research for a product assessed inside General Learning, not a travel assistant we are building. User-facing name: **AI travel assistant**. Travel abroad is implicit context; do not add “international” to the name.

## Confirmed brief

An AI travel assistant that helps people plan and navigate trips. Users discuss dates, budget and interests, compare options, revise itineraries and ask for help during the trip.

Research question: **Who would pay for an AI travel assistant, what would they value most, and why would they choose it over ChatGPT or free travel tools?**

This supersedes the internship-application and voice-note demo choices. Implementation remains paused; this is a research and storyboard update.

## Evidence register

### TR01 — Established feature overlap

- Source: [Mindtrip traveller FAQs](https://resources.mindtrip.ai/travelers/help/traveler-faqs)
- Publication date: not shown. Checked: 20 September 2026.
- Observation: Mindtrip describes conversational recommendations, editable itineraries, collaboration, booking organisation and in-trip maps. It says partner travel data and community knowledge supplement its conversational model.
- Supports: a competitor feature baseline and alternatives respondents should consider.
- Does not support: independent accuracy, retention, conversion or willingness to pay. Vendor self-description.
- Implication: a conversational itinerary alone is not a distinctive offer. Probe coordination, confidence and in-trip support.

### TR02 — Assistance and human support

- Source: [Layla homepage and FAQ](https://layla.ai/)
- Publication date: not shown. Checked: 20 September 2026.
- Observation: Layla advertises personalised trip planning and the option of human travel experts who plan, book and update trips.
- Supports: human support is part of a competitor's positioning, rather than an unexplored product category.
- Does not support: effectiveness or a verified price benchmark. No current consumer price was established in this review.
- Implication: ask when travellers would want human escalation, without quietly adding a labour-intensive service to our baseline offer.

### TR03 — Interest does not establish payment or trust

- Source: [Booking.com Global AI Sentiment Report announcement](https://news.booking.com/bookingcom-releases-the-global-ai-sentiment-report/)
- Published: 23 July 2025. Survey: April–May 2025, 37,325 respondents across 33 markets.
- Observation: the release reports 89% wanting AI in future travel planning, while 12% are comfortable with AI deciding independently. The second figure concerns general AI autonomy, not paid travel assistants specifically.
- Supports: investigating the distinction between interest, trust and delegated control.
- Does not support: a paid conversion rate, country-specific estimate, our proposed audience shares, or a success forecast. Industry-sponsored, self-reported research from 2025.
- Implication: retain “would use free”, “would consider paying” and “would not use” as distinct outcomes.

## Candidate audiences, not discovered customer segments

1. **Time-constrained trip organiser:** coordinates multiple people's preferences and currently uses messages, maps and booking sites. Hypothesis: reduced coordination effort could be valuable.
2. **Infrequent traveller seeking confidence:** wants help assessing unfamiliar options and avoiding mistakes. Hypothesis: explainable, current information may matter more than itinerary volume.
3. **Experienced independent planner:** already has an effective collection of tools and preferences. Hypothesis: the assistant must improve a specific task to justify switching.

These groupings are research hypotheses, not a fixed three-group architecture. Vary travel frequency, planning time and budget without prescribing outcomes. Six purposive synthetic profiles can smoke-test the pipeline; the approved ambition is 1,000 independently evaluated respondents if quality, cost and latency benchmarks support it. No synthetic sample establishes representative population weights. Do not assign preferred offers in the profiles. Evidence above motivates research questions but does not prove these segments or their size. Geography remains an inherited open check: BUILD.md previously specified Hong Kong/English; no new geographic selection was made.

## Study questions

- Describe the current planning process and the hardest unmet task, using the assigned profile rather than inventing external facts.
- Would this offer replace anything, supplement existing tools, or add no value?
- Would you use it free, consider paying, or decline? Explain the conditions.
- Which capability is worth paying for, if any? Which recommendation would you still verify elsewhere?
- At a stated price and duration, choose paid offer, current workaround or neither. No unstated pricing assumptions.
- What would change your decision, and what could make you stop using it?

Research does not establish a viable price. Confirm illustrative prices before priced simulation. Always record currency, included service, coverage period, trip frequency and active subscription months. A per-trip versus monthly comparison changes the pricing format; hold capabilities and profile constant and disclose total-cost differences.

## Numerical support

Separate (a) exact synthetic response counts and reasons, (b) explicit scenario arithmetic, (c) the existing unvalidated index. Neither six nor 1,000 synthetic cases by itself justifies calibrated market shares or real-world confidence intervals.

Proposed unit calculation: contribution per purchase = price minus model/data/payment/support costs; acquisition cost stays separate. Cost/revenue projections need explicit purchase counts and period. Do not turn “four of six would pay” into 67% real conversion. The old price-fit controls remain disabled until repaired; these calculations are a proposed separate commercial tool, not an existing feature.

## Remaining research before a substantive run

- Verify current consumer pricing/terms directly, without relying on search snippets or old articles.
- Collect real traveller interviews/reviews about planning effort, information verification and existing alternatives; vendor pages are insufficient audience evidence.
- Establish the intended initial market, plausible travel frequency and explicit price/cost scenarios.
- Investigate acquisition channels, seasonal use, repeat purchases and whether booking commissions are relevant. No commission revenue is assumed in the baseline.
- Capture a genuine bounded engine run with model, prompt version, inputs, timestamps and raw responses. There is no verified travel simulation result yet.

## Approved learning-loop amendment

The main demo payoff is now frozen predictions compared with compatible real feedback, a documented audience revision, and evaluation on separate untouched evidence. Monthly versus per-trip pricing is optional. Baseline run inputs/answers must be frozen before feedback is revealed. Feedback used to update profiles cannot then validate the update; small convenience samples can expose missing needs but do not estimate population proportions.

No real interviews were supplied. Authored feedback is illustrative, and unimplemented feedback screens are concept scenes. Do not claim fine-tuning, recursive self-improvement, automatic weight learning or improved accuracy without separate evidence.

The [approved amendment](../product/LEARNING-LOOP-AMENDMENT.md) records research precedent from Stanford interview-grounded agents, Minds, Aaru and OASIS. These references were supplied by the video task; they are not benchmarks of this implementation or evidence of travel-purchase accuracy.

## Graph build and scale experiment, 20 September 2026

The graph now uses two short, dated summaries in `product/prototype/travel/graph-sources.json`: Booking.com's 2025 AI sentiment research and Expedia Group's April 2026 AI Trust Gap release. Source links and collection details are preserved. The former supplies five general AI attitude cohorts; the latter supplies planning alternatives and transaction concerns. Neither supplies a paid-travel-assistant target-market distribution.

MiroFish-local extraction, SQLite storage, entity reading and graph-based profile generation have executed. Unsupported source anchors and out-of-ontology types are rejected. The resulting graph contains 14 nodes and 10 edges, including five self-relations representing attitudes. Some research entities remain isolated because proposed links were rejected; no links are invented to make the visual denser.

The 1,000 profiles cross five graph-derived attitude seeds with explicitly assumed travel party, frequency, current tools and planning effort. This is an experimental design, not 1,000 observed people. Each receives a separate OASIS interview. The full-size run is in progress; no claim of accurate demand inference follows from its scale.
