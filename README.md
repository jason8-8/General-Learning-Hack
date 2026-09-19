# General Learning Hack

Public repo for the GL Hacks submission.

**Deadline:** Sunday 20 September 2026, 10:00 HKT. No extensions.

Judges do not read code. They see a **two-minute video** (working prototype) plus the written explanation. Prep the story first.

## Start here

1. [docs/demo-video.md](docs/demo-video.md) — what to record
2. [docs/pitch-deck.md](docs/pitch-deck.md) — two slides around the product
3. [docs/build-plan.md](docs/build-plan.md) — what the prototype must do
4. [notes/MEETING_NOTES.md](notes/MEETING_NOTES.md) — judging + product lock
5. [quant/WEIGHTS.md](quant/WEIGHTS.md) — why the scorecard numbers exist

## What this repo contains

**Story / demo**

Input an idea → assessment (buyers, alternatives, adoption) → inspect evidence → change one assumption → compare.

**Quant (already built)**

Deterministic `P(adopt | segment, product)`. Same inputs → same output. No LLM in the scoring path.

```
S = Σ w_i · z_i
P_raw = σ(α + βS)
P(adopt) = clipped blend of P_raw and analog proxy rate
```

| Product | Best-fit | P(adopt) | Poor-fit |
|---|---|---|---|
| Voice notes for students ($6/mo) | HK young professionals | 22.1% | firms ~3% |
| Corporate voice agent ($480/mo) | APAC consulting | 15.4% | students floored at 0.8% |

Edit weights only in [quant/weights.yaml](quant/weights.yaml).

```bash
python -m pip install -r requirements.txt
python quant/score_engine.py
python quant/score_all.py
python scripts/build_workbook.py
```

Workbook tabs live as CSVs in [sheets/](sheets/). Do not commit `.xlsx` or `.env`.

## Layout

```
README.md
PROJECT.md
notes/MEETING_NOTES.md
docs/demo-video.md
docs/pitch-deck.md
docs/build-plan.md
docs/architecture.spec.json
quant/                  scorecard
data/                   products, segments, analogs, scored rows
sheets/                 workbook CSVs
scripts/build_workbook.py
```
