# General Learning Hack — idea validation quant model

Deterministic adoption scorer for the GL Hack idea-validation product.

The model does **not** interview synthetic users. It maps a structured product and a structured segment to:

```
S = Σ w_i · z_i
P_raw = σ(α + βS)
P(adopt | s, x) = clipped blend of P_raw and analog proxy rate
expected adopters = M_s × P
```

Same inputs always produce the same output.

## Demo contrast

| Product | Best-fit segment | P(adopt) | Poor-fit |
|---|---|---|---|
| Voice notes for students ($6/mo) | HK students / young professionals | ~19–22% | firms ~3% |
| Corporate voice agent ($480/mo) | APAC consulting | ~15% | family SME ~2%, students floored |

## Workbook (the 00–08 sheets)

Sheet tabs live in [`sheets/`](sheets/). Rebuild the Excel file locally:

```bash
python -m pip install -r requirements.txt
python scripts/build_workbook.py
```

That writes `GL_Hack_Adoption_Quant_Model.xlsx` at the repo root with tabs:

`00_Cover` `01_Method` `02_Assumptions` `03_Product` `04_Segments` `05_Analogs` `06_Results` `07_Waterfall` `08_Sensitivity`

GitHub cannot store the binary `.xlsx` through this push path. The CSVs + builder *are* the workbook on GitHub.

## Repo layout

```
README.md
requirements.txt
scripts/build_workbook.py   # sheets/*.csv -> .xlsx
quant/score_engine.py
quant/score_all.py
quant/weights.yaml
data/
sheets/                     # the nine model tabs
```

## Run the scorer

```bash
python quant/score_engine.py
python quant/score_all.py
```

## LLM role

Fill a product schema only. After JSON is valid, it is out of the scoring path.
