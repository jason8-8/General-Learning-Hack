# Hindsight

**Test the assumption before you build the idea.**

Learn from the future. Shape the present.

Hindsight helps a founder inspect the evidence behind a product decision, compare explicit scenarios, and save the next test with real customers. The demo assesses a proposed AI travel assistant. It does not plan or book trips.

## Run the demo

Python 3.9+ and a browser. No installation, API key or model required for the recorded demonstration.

```bash
python3 product/prototype/server.py --port 8765
```

Open:

```text
http://127.0.0.1:8765/
```

## What works

- Search bundled competitor summaries and inspect their sources.
- Change offer, audience or price in an explicitly authored scenario.
- Freeze a baseline, inspect the change, and flag comparisons that change several inputs.
- View actual recorded model-pilot counts separately from fictional scenarios.
- Write what would change your decision, then export the baseline, selection and next-test note.
- Inspect recorded model experiments and the illustrative feedback/revision workflow at `/lab`.

## What the results mean

The presentation has **1,000 deterministic scenario rows**, not 1,000 independent model interviews. Its price thresholds, eligibility and concept effects are authored assumptions. The readiness concept beats the basic concept by construction; this is not evidence of preference.

Two actual local-model pilots used the same 20 synthetic profiles at £10 and £30 per trip. Both completed 20/20 and all selected free tools. They prove execution, not customer demand, predictive accuracy or useful price sensitivity. The pilot offer differs from the presentation's readiness concept.

No real customer feedback or independent validation set has been supplied. The feedback example in the lab is illustrative. The legacy adoption-probability model is excluded from the current demo.

## Judge-facing materials

| File | Purpose |
| --- | --- |
| [120-second video](pitch/video.md) | Recordable script aligned with working functionality |
| [90-second live pitch](pitch/slides.md) | Two slides and complete spoken script |
| [Judge questions](pitch/JUDGE-QA.md) | Defensible answers and concrete next test |
| [Audit](HACKATHON-AUDIT.md) | Red flags, fixes, limitations and priorities |
| [Current product contract](product/CURRENT.md) | Canonical state, superseding older plans |
| [Verification](product/prototype/AUDIT-VERIFICATION.md) | Current test and browser evidence |

The repo brief records GL Hacks submission at **10:00 HKT on 20 September 2026**, a two-minute prototype video and a 90-second live pitch. These event details were not reconfirmed with organisers in this audit.

## Verify

```bash
python3 -m unittest discover -s product/prototype/tests -v
node product/prototype/tests/test_study_math.cjs
```

Node is only needed for the JavaScript regression check. The app itself uses the Python standard library. Start the application with `product/prototype/server.py`. Local media-generation helpers are separate from the published app.

Local credentials, generated workbooks and saved private runs stay Git-ignored. No paid calls were made in this audit. Existing work was preserved; the prototype was copied from tracked build commit `c0c8a76`, then repaired in this checkout.
