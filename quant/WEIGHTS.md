# Weight rationale — 19 Sep 2026

Every number below is a **placeholder prior**, not a regression coefficient.

We do not have a labeled adopt/not-adopt panel for these products. So the weights are a published scoring rule: they encode what we believe causes 12-month adoption, they sum to 1.00, and they can be replaced later by a fit on held-out analog rows.

What “placeholder” means here:

- Chosen so mid-range scorecards land in the 5–20% band typical of consumer-app trial-to-paid and SMB-SaaS first-year attach.
- Chosen so the two demo products rank differently across segments (student notes vs $480 corporate agent).
- **Not** estimated from Census, App Store, or G2 conversion files.
- Mark every output as a proxy. Confidence falls when analog coverage is thin.

## Feature weights (must sum to 1.00)

| Feature | Old | New | Why this feature is in the algorithm | Why this placeholder |
| --- | ---: | ---: | --- | --- |
| `icp_fit` | 0.22 | **0.24** | Wrong buyer dominates every other signal. A student-priced notes app should not look adoptable to a mid-market IT buyer, and a $480 agent should not look adoptable to a 19-year-old. The engine also hard-collapses P when ICP < 0.12; the weight is the *soft* version of that gate. | Largest single weight because ICP is the first filter a judge will attack. 0.24 not 0.40 so the other seven features can still move the ranking inside a valid buyer. |
| `problem_intensity` | 0.16 | **0.18** | Adoption is a job-to-be-done, not a persona. If the pain is mild, WTP and channel do not matter. This is also the feature that should separate “in-market buyer” from “skeptic” once those two templates exist. | Raised one notch so acute pain can beat a mediocre analog. 0.18 keeps it second to ICP; we are not claiming JTBD is half the model without interview data. |
| `price_fit` | 0.16 | **0.12** | Price vs segment WTP ceiling is a real kill-switch (see `price_fit()` in the engine: ratio > 2× WTP ≈ 0.02). | Cut because the engine **already** multiplies final P by `(0.30 + 0.70 × price_fit)`. Leaving 0.16 *and* that multiplier double-punished price and flattened every other feature. 0.12 keeps it material without dominating. |
| `readiness` | 0.14 | **0.12** | Category usage (B2C) / digital maturity (B2B). This is how a family-owned shop and a Deloitte-like firm stay distinct when ICP is similar. | Trimmed slightly. Readiness is real but slow-moving; we already encode a lot of it in segment tables (`category_usage`, `digital_maturity`). 0.12 avoids counting the same maturity twice. |
| `analog_success` | 0.14 | **0.08** | What happened to shipped lookalikes, scaled to 0–1. The only feature that is an *outcome*, not a self-description. | Cut hard. The engine already blends `analog_rate` into P with weight `coverage × icp × price_fit`. Keeping 0.14 inside S *and* blending analog_rate double-counted the prior. 0.08 leaves a residue of “this category converts” without letting one Notion/Otter row run the model. |
| `distribution_fit` | 0.10 | **0.12** | Channel match. App-store products do not reach owner-direct SMEs. Sales-led products do not convert students. This is the most common silent miss in pitch decks. | Raised. For this hack, channel is observed and cheap to score, unlike true WTP. 0.12 is enough to flip a “good ICP, wrong storefront” row without pretending we modeled CAC. |
| `switching_ease` | 0.05 | **0.10** | Implementation days, habit, procurement. Family SMEs die here; students do not. The 19 Sep plan treats the skeptic/blocker as a first-class segment — switching *is* that person’s job. | Old 0.05 was a rounding error. Doubled so a 30-day SSO rollout can actually pull P down. Still 0.10 not 0.20 because we only have a coarse 0–1 friction flag, not measured time-to-value. |
| `competition_ease` | 0.03 | **0.04** | Crowded analog set (incumbent notes apps, incumbent contact-centre vendors) should cap upside. | Kept small on purpose. We do not have share data. 0.03 was noise (a 1.0 vs 0.0 swing moved S by 0.03). 0.04 is the smallest weight that can move reported P by about a point. Do not raise further until the analog table has an explicit incumbent flag. |

Sum: **1.00**.

## Calibration placeholders

| Param | Old | New | Why it exists | Why this placeholder |
| --- | --- | --- | --- | --- |
| `alpha` | −3.80 | **−3.60** | Logistic intercept. Sets the base rate when S is mid/low. | Slightly less punitive so a decent B2C fit (S ≈ 0.55) lands near ~12–15% raw, in line with the `consumer_app` / `productivity` category priors on the assumptions tab. Still negative: most eligible people do not adopt in 12 months. |
| `beta` | 4.40 | **4.20** | Slope on S. How fast good vs bad scorecards separate. | Eased a hair so we do not claim 30%+ raw P from a scorecard that is only “pretty good.” 4.2 still separates S=0.30 (~7% raw) from S=0.80 (~28% raw) before floors, blends, and price multiply. |
| `p_floor` | 0.008 | **0.008** | Never print 0%. Zero pretends certainty and breaks expected-adopter tables. | 0.8% of an eligible universe is “trace, not none.” Matches the old published floor. |
| `p_ceil` | 0.45 | **0.40** | Caps fantasy conversion. This model has no paid-acquisition or virality term. | Tightened. 45% of a Census-scale student universe in 12 months is not something our analog table can support. 40% is still generous and only reachable after ICP, price, and analog blend all fire. |

## Two-segment frame mix (qualitative only)

Not used inside `P(adopt)`. Used if the evidence cache has no cited mix.

| Segment | Weight | Why this placeholder |
| --- | ---: | --- |
| In-market buyer | 0.60 | First-pass idea tests should over-sample people who could care, or the cluster view is 80% “not for me.” |
| Skeptic / blocker | 0.40 | Large enough that kill objections survive clustering. Not 0.50: we are not claiming the addressable market is half blockers without evidence. |

Label **assumed** until a cited source replaces it.

## What we refused to do

- Fit weights on the two demo products. That would bake the demo ranking into the model.
- Add a joint trait network into S. That is a stretch item for the qualitative cohort, not a ninth scorecard feature.
- Give competition or switching 0.20+ without share or time-to-value data.

## How to replace these later

Hold out 20% of analog rows. Predict P. Report MAE against `proxy_rate`. Then either:

1. grid-search the eight weights on the train analogs, or
2. fit a logistic on the same z-vector.

Until that exists, change weights only in `quant/weights.yaml`.
