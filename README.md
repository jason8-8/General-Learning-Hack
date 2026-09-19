# General Learning Hack

Deterministic idea-validation scorer. Same inputs → same `P(adopt)`.

Judges will not read this repo. They see a **2-minute video** and a **90-second pitch** only. Notes: [`notes/MEETING_NOTES.md`](notes/MEETING_NOTES.md).

```
S = Σ w_i · z_i
P_raw = σ(α + βS)
P(adopt | s, x) = clipped blend of P_raw and analog proxy rate
expected adopters = M_s × P
```

Weights are published placeholders. Edit [`quant/weights.yaml`](quant/weights.yaml). Why each number: [`quant/WEIGHTS.md`](quant/WEIGHTS.md).

## Demo contrast (rescored 19 Sep)

| Product | Best-fit | P(adopt) | Poor-fit |
|---|---|---|---|
| Voice notes for students ($6/mo) | HK young professionals | 22.1% | firms ~3% |
| Corporate voice agent ($480/mo) | APAC consulting | 15.4% | students floored at 0.8% |

## Run

```bash
python -m pip install -r requirements.txt
python quant/score_engine.py
python quant/score_all.py
python scripts/build_workbook.py
```

Workbook tabs are the CSVs in [`sheets/`](sheets/). The `.xlsx` is built locally; it is not committed.

## Layout

```
notes/MEETING_NOTES.md   judging + product lock
quant/weights.yaml       edit weights here
quant/WEIGHTS.md         rationale
quant/score_engine.py
data/                    products, segments, analogs, scored rows
sheets/                  workbook tabs
scripts/build_workbook.py
```

LLM may fill a product schema. After JSON is valid it is out of the scoring path.
