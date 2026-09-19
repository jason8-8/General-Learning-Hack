# Product

What runs. Pitch copy lives in `../pitch/`. Locks live in `../research/decisions.md`.

```
product/
  README.md BUILD.md PROJECT.md
  quant/     scorecard
  data/      products, segments, analogs, scored rows
  sheets/    workbook CSVs
  scripts/build_workbook.py
```

```bash
python product/quant/score_engine.py
python product/quant/score_all.py
python product/scripts/build_workbook.py
```

Two segments for the qualitative frame. Quant stays deterministic. Do not deepen weights this weekend.
