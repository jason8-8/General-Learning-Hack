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

## Demo contrast (from the working session)

| Product | Best-fit segment | P(adopt) | Poor-fit |
|---|---|---|---|
| Voice notes for students ($6/mo) | HK students / young professionals | ~19–22% | firms ~3% |
| Corporate voice agent ($480/mo) | APAC consulting | ~15% | family SME ~2%, students floored |

That is the Deloitte-vs-family-business example as numbers: price, readiness, and channel kill the SME row.

## Repo layout

```
README.md
requirements.txt
quant/score_engine.py       # scoring function only
quant/build_quant_model.py  # rebuilds CSVs + Excel workbook
data/products.csv
data/segments.csv
data/analogs.csv
data/results_scored.csv
```

## Run

```bash
python -m pip install -r requirements.txt
python quant/score_engine.py
python quant/build_quant_model.py
```

`build_quant_model.py` writes the inspectable workbook `GL_Hack_Adoption_Quant_Model.xlsx` (cover, method, assumptions, products, segments, analogs, results, waterfall, sensitivity).

## What the LLM is allowed to do

Fill a product schema (category, price, channel, buyer type). After the JSON is valid, it is out of the scoring path.

## Out of scope

Unit sales, LTV, “will the company succeed,” and novel categories with zero analogs. Proxy rates in `data/analogs.csv` are planning priors, not vendor-reported conversion.
