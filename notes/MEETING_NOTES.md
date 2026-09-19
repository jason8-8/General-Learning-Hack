# Meeting notes — 19 Sep 2026

## Judging (round 2 briefing)

Judges do **not** read code. They only see:

1. A **2-minute video**
2. A **90-second in-person pitch**

| Rule | Detail |
| --- | --- |
| Disqualifications | None. Everyone advances |
| Live pitch | Mandatory for every team |
| Clock | After 10:00 there may be no time to write the 90s. Prep both now |
| Round 1 → 2 window | 10:00–13:00 |

Work backwards from the story. Quant is good enough — do not deepen it.

- **Video (120s):** one idea in, a split of reactions out, a kill objection in the tail. Why this is not “ask ChatGPT.”
- **Pitch (90s):** cited segments, distribution not an average, one P(adopt) number as backup. No architecture tour.

## Product lock

| Decision | Choice |
| --- | --- |
| Qualitative v1 | Two segments: in-market buyer vs skeptic/blocker |
| Frame | Segments + weights + citations |
| Joint trait network | Stretch only |
| Media-diet loop | Stretch only |
| Cohort | ~200 rows, in memory, seeded |
| Output | Clusters + tail objections. No average |
| Quant | Deterministic scorecard. No LLM in P(adopt) |

Fallback frame mix if evidence has no weights: **0.60 buyer / 0.40 skeptic**, labeled assumed.

Quant universes stay the five HK / APAC rows in `data/segments.csv`. Do not collapse those to two.
