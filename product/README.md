> **Scope update, 20 September 2026:** The assessed demo product is an **AI travel assistant**, superseding the voice-notes / note-taking example that still appears below. Read [BUILD.md](BUILD.md) for the current build plan and [LEARNING-LOOP-AMENDMENT.md](LEARNING-LOOP-AMENDMENT.md) for the approved learning loop. Everything below is historical wherever it conflicts. The old architecture.spec.json is also historical; use the layering diagram in the build plan.

# Product

The prototype behind the pitch.

One idea in. A cited audience frame. An assessment you can inspect. One assumption changed. A comparison out.

The live demo flow is in [`../pitch/video.md`](../pitch/video.md). Locks: [`../research/decisions.md`](../research/decisions.md). This folder is the thing on screen.

## Two layers

| Layer | What it answers | Where |
| --- | --- | --- |
| Qualitative | Who reacts, and how they split | two-segment frame + evidence + clusters (to build) |
| Quantitative | `P(adopt | segment, product)` | `quant/` (already runs) |

~~v1 qualitative frame is **two segments**: in-market buyer vs skeptic/blocker.~~ **Superseded:** the travel study uses evidence-led audience groups (five in the current presentation), not a fixed two-segment frame. See [`BUILD.md`](BUILD.md) Q6 and [`LEARNING-LOOP-AMENDMENT.md`](LEARNING-LOOP-AMENDMENT.md).

## Quant

Deterministic. Same inputs → same output. No LLM in the scoring path.

```
S = Σ w_i · z_i
P_raw = σ(α + βS)
P(adopt) = clipped blend of P_raw and analog proxy rate
expected adopters = M_s × P
```

Weights are published placeholders that sum to 1.00. Not fitted. Change only in [`quant/weights.yaml`](quant/weights.yaml). Why each number: [`quant/WEIGHTS.md`](quant/WEIGHTS.md).

**Historical examples — superseded by the AI travel assistant.** Kept only to show the engine's output shape; do not quote these in the pitch or video.

| Product | Best-fit | P(adopt) | Poor-fit |
|---|---|---|---|
| Voice notes for students ($6/mo) | HK young professionals | 22.1% | firms ~3% |
| Corporate voice agent ($480/mo) | APAC consulting | 15.4% | students floored at 0.8% |

```bash
python -m pip install -r requirements.txt
python product/quant/score_engine.py
python product/quant/score_all.py
python product/scripts/build_workbook.py
```

Workbook tabs are the CSVs in [`sheets/`](sheets/). Do not commit `.xlsx`.

## Layout

```
product/
  README.md
  PROJECT.md                 original brief
  BUILD.md                   what must work on camera
  quant/                     scorecard
  data/                      products, segments, analogs, scored rows
  sheets/                    workbook CSVs
  scripts/build_workbook.py
```

Do not spend Saturday afternoon retuning weights unless the 90-second pitch needs one different number.
