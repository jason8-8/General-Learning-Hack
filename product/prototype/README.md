# Local launch-assessment prototype

A zero-dependency Python/browser implementation of the founder flow. This is a working **fallback prototype**, not the completed LLM/MiroFish research system.

Latest decisions take precedence over `product/BUILD.md`: note-taking and personal-productivity consumer SaaS; English; optional geography, unknown by default; founder confirmation before research; no paid API calls in this build session. The old fixed Hong Kong restriction and eight-hour statement do not apply to this implementation.

## Run

From the repository root (Python 3.9+; no pip install needed):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 product/prototype/server.py --port 8765
```

Open:

```text
http://127.0.0.1:8765
```

The server binds only to loopback. It serves its own assets and the existing brand logo; fonts fall back to the system stack as specified by the brand guide. No external frontend dependencies, database, auth service or billing.

## What works

1. Describe an idea. The manual drafting fallback preserves the original description. Edit the problem, core benefit, geography, alternatives and channel, then confirm.
2. Three concurrent **source-review workers** inspect a bounded vendor catalogue. Each URL is fetched once; duplicate references merge roles into one evidence record. This is not open-web search or three LLM research agents.
3. Inspect short source excerpts, URLs, retrieval timestamps, unknown publication dates and limitations. Failed pages stay unavailable. Offline mode creates no evidence.
4. Edit and confirm one to three need-based audience hypotheses. Suggestions use transparent category rules, not customer discovery.
5. Optionally supply quant inputs with reasons. Missing values stay null; the aggregate is suppressed until all eight inputs exist. User-entered values are labelled assumptions.
6. Run six independent **authored rule-based stress tests** over the confirmed audiences. Each invokes the deterministic quant adapter. Actual LLM-agent count is zero. No synthetic votes or demand estimates.
7. Inspect the report, assumptions, unvalidated rubric and next tests. Change the feature proposition and optionally one non-price factor. Baseline is immutable; evidence is visibly reused. Price comparison is rejected by both UI and server.
8. Save a baseline locally and replay it with cached-evidence and saved-run labels. Original retrieval dates and reactions are retained. Export JSON includes baseline plus the current comparison.

Local saves are under `product/prototype/.runs/`, excluded by the nested `.gitignore`. They contain the founder's brief and evidence, but no credentials. In-memory reports are capped at 100; the start page lists the 20 most recent saved runs. Export before ending a session if you want to retain a comparison: local save currently saves only its baseline.

## Evidence and numerical boundaries

Catalogue selection is a keyword heuristic: note-taking uses Voicenotes and Obsidian; task/planning/habit ideas use Todoist and TickTick. Unknown categories retrieve nothing. Vendor pages only establish what a vendor publishes, not actual capability, preferences, growth, willingness to pay or geographic demand. No source is fabricated or borrowed from a different cached idea.

Each evidence item has ID, URL, title, retrieval/publication dates, exact short observation, narrow supported claim, limitation, provenance, content hash and worker roles. A page shared by three workers remains one source.

The adapter imports `product/quant/score_engine.py` and its weight overrides. It uses only `S`, never exposes `raw_p` or `P_adopt`, and never renormalises weights. The legacy scorer is unchanged. Its price discontinuity and prior-blend issues are **not fixed**; price comparison remains disabled. The numeric index has no percent sign and no predictive-accuracy claim.

Rubric v1, explicitly unvalidated:

- Any missing factor: insufficient evidence; no aggregate.
- All factors present but fewer than four observed/inferred factors with valid source IDs: insufficient evidence; assumption index may be displayed.
- Otherwise: `S >= 0.70` promising; `0.40 <= S < 0.70` mixed; below `0.40` weak.
- Coverage counts evidence-backed factors separately from supplied inputs. Citation validation checks source existence, not whether a numeric judgement is justified. The current browser form only submits assumptions, so it cannot manufacture evidence coverage.

No historical outcome dataset exists. Commercial viability, demand trend, competitor stagnation and retention stay unknown without appropriate evidence. Synthetic outputs cannot mutate evidence or quant factors. Feature scenarios must explicitly supply the numerical assumption and reason.

## Integration seams and remaining work

- `contracts.py`: brief/audience validation, canonical URLs, fingerprints, deduplication.
- `research.py`: replace bounded-catalogue review with provider-backed market/competitor/customer research; preserve record contract and founder gate. Never let retrieved text become instructions.
- `quant_adapter.py`: deterministic, missing-aware mapping with source/provenance validation.
- `assessment.py`: replace `stress_tests` with the selected MiroFish adapter or explicitly labelled LLM fallback. Keep six independent calls, one round, measured usage and a spend cap. Suggested scenarios must remain separate from observed factors.
- `server.py`: localhost-only HTTP routes, session token and cross-origin checks, bounded input, memory state and explicit saves. No credential environment variables are read; no paid provider has been wired or called.
- `static/`: complete editable browser flow, responsive layout, keyboard tabs, loading/error/empty states and JSON export.

**Not implemented:** LLM brief extraction, open-web search, LLM research synthesis, evidence-derived factor mapping, real MiroFish or LLM agents, measured paid-model usage, 30-agent cohort, automatic customer discovery, automatic launch verdict generation from research. Broad report prose and stress-test prompts are authored templates. Do not present them as live AI analysis.

Provider/search credentials, an explicit external API budget and teammate code ownership remain unresolved. Codex weekly usage is separate from external app-provider charges. No paid calls were authorised or made. All new work is confined to this directory; the team scorer, brand and planning files are unchanged. The app has not been deployed; running it still requires the local server above.

## MiroFish feasibility check

Reviewed the official [repository and setup instructions](https://github.com/666ghj/MiroFish), [backend dependencies](https://github.com/666ghj/MiroFish/blob/main/backend/requirements.txt) and [maintainer FAQ](https://github.com/666ghj/MiroFish/issues/726) on 20 September 2026 local time.

Mainline requires Python 3.11–3.12, Node 18+, `uv`, an LLM API key and a separate Zep Cloud key. Backend dependencies include Flask, OpenAI SDK, Zep, CAMEL/OASIS and PyMuPDF. The system Python here is 3.9.6; a newer bundled runtime exists, but switching Python does not supply credentials or spending approval. The repo declares AGPL-3.0; no source code was copied or installed.

Gate result: **blocked before execution**, not a demonstrated failure of MiroFish. No real run, runtime/cost measurement or quant-tool bridge has been validated. Keep MiroFish as the selected next integration; do not call this fallback MiroFish. No 30-agent run has occurred.

## Verification

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s product/prototype/tests -v
```

Tests cover null versus zero, finite/range validation, rubric boundaries, deterministic weighted effects, source IDs/provenance, founder gates, immutable comparison, price rejection, source deduplication and failure behaviour, unknown geography, unseen/unsupported ideas, simulation separation and saved-run replay.

Browser checks cover two distinct ideas, source inspection, report tabs, feature comparison, JSON export, saved replay, desktop and 390px mobile layout. See `VERIFICATION.md` for observed results and limitations.
