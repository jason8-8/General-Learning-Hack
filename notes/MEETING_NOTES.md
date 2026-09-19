# Meeting notes — 19 Sep 2026

Repo: `jason8-8/General-Learning-Hack`

## Attended decisions

Ship the original architecture. Do not start with an Aaru-style joint trait network.

| Decision | Locked choice |
| --- | --- |
| Sampling frame | Segments + weights + citations |
| Qualitative sim v1 | **Two segments only** |
| Segment roles | In-market buyer vs skeptic / blocker |
| Joint trait network | Stretch. After the view works |
| Media-diet loop | Stretch. Not v1 |
| Evidence | Cached reviews, filings, forums |
| Cohort | ~200 rows, in memory, seeded |
| Reactions | One Claude call per persona, then cluster |
| Output | Distribution + tail objections. No average |
| Persistence | Cut |
| Quant path | Separate deterministic scorecard. No LLM in P(adopt) |

## Two-segment sim (qualitative)

Names come from the category cache. Roles stay fixed:

1. **In-market buyer** — already shopping or using a substitute.
2. **Skeptic / blocker** — would have to approve, switch, or ignore it.

Each segment is a template (label, weight, 3–5 grounded attributes, `source_ids`). Do not sample age × income × tenure as independent columns.

Fallback mix if the cache has no weights: **0.60 buyer / 0.40 skeptic**, labeled **assumed**, not cited. Buyer-heavy because a first-pass idea test should over-sample people who could care; skeptic stays large enough that kill objections survive clustering.

## Quant model (this repo)

The workbook / `quant/` scorer is the other half of the demo. It answers `P(adopt | segment, product)` on a frozen universe. It does not interview synthetic users.

Weights were placeholders that summed to 1.00 but were not justified. Revamp is in:

- `quant/weights.yaml` — values + one-line why
- `quant/WEIGHTS.md` — full rationale and why each number is a placeholder
- `quant/score_engine.py` — same numbers, loaded from the yaml when present
- `sheets/02_Assumptions.csv` — published scorecard tab

Quant still uses the five HK / APAC universes in `data/segments.csv`. That is the *market* layer. The two-segment split above is the *reaction* layer. Do not collapse the quant universes to two until we have cited sizes for buyer vs blocker.

## Build order

1. Frame builder (two segments)
2. Cohort sample
3. Fan-out runner
4. Divergence + distribution view
5. Quant weights (this pass)
6. Stretch: third segment → joint network → media diet

## Done when

- Notes and weights are in this repo
- Every weight has a reason and a “why this placeholder” note
- Engine still sums to 1.00 and stays deterministic
