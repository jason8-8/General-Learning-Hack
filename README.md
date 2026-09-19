# General Learning Hack

Public repo for the GL Hacks submission.

**Deadline:** Sunday 20 September 2026, 10:00 HKT. No extensions.

Judges do not read this repo. They see two artifacts only:

1. A **two-minute video** with a working prototype
2. A **90-second live pitch**

Everyone advances. No disqualifications. After 10:00 there may be no time to write the 90s — prep both now.

## What this is

One idea in. A cited audience frame. An assessment you can inspect. One assumption changed. A comparison out.

The number on screen is a deterministic scorecard, not “the market said yes.” Synthetic personas are hypotheses, not proof of demand.

```
S = Σ w_i · z_i
P_raw = σ(α + βS)
P(adopt) = clipped blend of P_raw and analog proxy rate
```

Same inputs → same `P(adopt)`. No LLM in the scoring path.

## Demo contrast (rescored 19 Sep)

| Product | Best-fit | P(adopt) | Poor-fit |
|---|---|---|---|
| Voice notes for students ($6/mo) | HK young professionals | 22.1% | firms ~3% |
| Corporate voice agent ($480/mo) | APAC consulting | 15.4% | students floored at 0.8% |

v1 qualitative frame is **two segments**: in-market buyer vs skeptic/blocker. Joint trait network and media-diet are stretch only.

## Folders

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

## Run

```bash
python -m pip install -r requirements.txt
python product/quant/score_engine.py
python product/quant/score_all.py
python product/scripts/build_workbook.py
```

Edit weights only in [`product/quant/weights.yaml`](product/quant/weights.yaml). Reasons: [`product/quant/WEIGHTS.md`](product/quant/WEIGHTS.md). Do not commit `.xlsx` or `.env`.

## What to show

- **Video (120s):** form → assessment → evidence → change price or audience → compare.
- **Live pitch (90s):** two named segments, distribution not an average, one `P(adopt)` labelled as a heuristic. No architecture tour.
