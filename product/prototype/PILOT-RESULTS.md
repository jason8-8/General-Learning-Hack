# Priced pilot: 20 September 2026

Engine execution passed. Demand discrimination and predictive accuracy are not demonstrated. Do not extrapolate this result as customer demand.

| Condition | Responses | Hypothetical paid choice | Existing free tools | Neither | Time |
|---|---:|---:|---:|---:|---:|
| £10 per trip | 20/20 | 0 | 20 | 0 | 51.82s |
| £30 per trip | 20/20 | 0 | 20 | 0 | 50.40s |

Prices are test assumptions. Identical first 20 profiles from the stable shuffled graph population cover all five attitude cohorts, with nonrepresentative allocation. Prompts verified identical except price; fresh agents per condition. No outcome selection or forced distribution. Temperature 0.3; a single paired comparison cannot isolate stochastic variation.

Compared with the historical unpriced study, both the question and offer changed. Therefore its all-positive result versus this all-free result cannot be attributed to price alone. New wording stresses unproven benefits and may favour the status quo. No observed decision-category sensitivity to price. Feature sensitivity and repeated-run stability remain untested.

MiroFish-local IPCHandler → OASIS interviews → local Ollama qwen3-coder:30b. Forty model calls; zero paid API spend. Raw prompts, source lineage, profiles, outputs and calculations: travel/pilot-10.json and travel/pilot-30.json. Flat export: travel/pilot-responses.csv. Historical recordings preserved. Automated suite: 34 tests passed; JavaScript syntax check passed.

Next: collect real traveller choices on the identical offer, including their existing workflow and budget. Reserve independent feedback for evaluation. Predefine neutral wording and acceptance criteria before rerunning. Do not tune for a plausible-looking split.
