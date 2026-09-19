# General Learning Hack

Public repo for the GL Hacks submission.

**Deadline:** Sunday 20 September 2026, 10:00 HKT. No extensions.

Judges do not read this repo. They see two artifacts only:

1. A **two-minute video** with a working prototype
2. A **90-second live pitch**

Everyone advances. No disqualifications. After 10:00 there may be no time to write the 90s — prep both now.

## One-line pitch

One idea in. A grounded audience. Concurrent reactions out. Clusters, not an average.

It exists so a founder or analyst can paste a pitch, see who would actually care, and inspect the split — enthusiasts, skeptics, and the objections in the tail — before talking to a real market.

## What this is

Enter an idea, an audience, and a price. Get an assessment you can inspect. Change one assumption. Compare to the baseline.

The number on screen is a deterministic scorecard, not “the market said yes.” Synthetic personas are hypotheses, not proof of demand.

```
S = Σ w_i · z_i
P_raw = σ(α + βS)
P(adopt) = clipped blend of P_raw and analog proxy rate
expected adopters = M_s × P
```

Same inputs → same `P(adopt)`. No LLM in the scoring path.

## What it is not

- Not a survey panel or a research firm
- Not a forecast of unit sales
- Not a single “the market thinks X” paragraph
- Not a cloud platform — demo is meant to run cold on a laptop

## Demo contrast (rescored 19 Sep)

| Product | Best-fit | P(adopt) | Poor-fit |
|---|---|---|---|
| Voice notes for students ($6/mo) | HK young professionals | 22.1% | firms ~3% |
| Corporate voice agent ($480/mo) | APAC consulting | 15.4% | students floored at 0.8% |

v1 qualitative frame is **two segments**: in-market buyer vs skeptic/blocker. Fallback mix if evidence has no weights: **0.60 / 0.40**, labelled assumed. Joint trait network and media-diet are stretch only.

## Folders

The short map is the index. The files inside still hold the full brief.

```
pitch/         what judges hear
product/       what runs
research/      what we can cite
discussion/    how we decided
brand/         how it looks
```

| Start here | Why |
| --- | --- |
| [`pitch/`](pitch/README.md) | 120s video + 90s pitch + judging rules |
| [`product/`](product/README.md) | Prototype + scorecard |
| [`research/decisions.md`](research/decisions.md) | Locks that survived argument |
| [`discussion/`](discussion/README.md) | Meeting threads |
| [`brand/`](brand/README.md) | Navy / teal tokens for slides and UI |

## What to show

- **Video (120s):** form → assessment → evidence → change price or audience → compare.
- **Live pitch (90s):** two named segments, distribution not an average, one `P(adopt)` labelled as a heuristic. No architecture tour.

Work backwards from those two artifacts. Quant is good enough — do not deepen it.

## Run

```bash
python -m pip install -r requirements.txt
python product/quant/score_engine.py
python product/quant/score_all.py
python product/scripts/build_workbook.py
```

Edit weights only in [`product/quant/weights.yaml`](product/quant/weights.yaml). Reasons: [`product/quant/WEIGHTS.md`](product/quant/WEIGHTS.md). Do not commit `.xlsx` or `.env`.
