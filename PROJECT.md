# Synthetic Market Simulation

Working name: **general-learning-hack**

This project is a laptop-scale demo that turns one product idea into a **distribution of simulated buyer reactions**, not a single averaged opinion.

It exists so a founder or analyst can paste a pitch, see who would actually care, and inspect the split — enthusiasts, skeptics, and the objections in the tail — before talking to a real market.

## One-line pitch

One idea in. A grounded persona cohort. Concurrent reactions out. Clusters, not an average.

## Who it is for

- Founders testing a pitch before customer interviews
- Analysts who need a first-pass demand shape, not a memo
- Judges / reviewers who will ask “where did these people come from?”

## What it does

1. **Pitch intake** — founder submits one idea plus a category.
2. **Sampling frame** — segments and weights derived from *cited* market evidence (reviews, filings, forums), not invented demographics.
3. **Persona cohort** — a seeded cohort (target: ~200 rows) derived from that frame.
4. **Simulation runner** — async fan-out; one model call per persona (Claude API).
5. **Divergence engine** — clusters the raw reactions. It reports the split and refuses to collapse it into one paragraph.
6. **Distribution view** — spread, clusters, and objections. The tail is the product.

## What it is not

- Not a survey panel or a real research firm
- Not a forecast of unit sales
- Not a single “the market thinks X” summary
- Not a cloud platform — the demo is meant to run cold on a laptop, with no account, upload, or infra to stand up

## Design bets (useful when doing market research)

These are the claims the product is making against adjacent tools (LLM chat, synthetic users, survey software, concept-test platforms):

| Bet | Why it matters |
| --- | --- |
| Evidence-grounded cohort | Personas must be derived from cited sources a judge can interrogate |
| Distribution over average | Disagreement is the signal; averaging hides the kill objections |
| Cold-start on stage | Time-to-first-insight measured in minutes, not a research sprint |
| Fan-out, then cluster | Scale comes from concurrent persona calls, not a longer prompt |
| Laptop-scoped | No persistence required for the demo; cohort can live in memory |

## Competitive neighborhood (for research)

When researching the market, compare against these *jobs*, not only companies:

- “Talk to an LLM about my idea” (ChatGPT / Claude chat)
- Synthetic user / persona products (e.g. synthetic interview tools)
- Concept testing and demand surveys (SurveyMonkey, Qualtrics, Wynter, PickFu)
- Community and review mining (Reddit, G2, app-store reviews)
- Early-stage research agencies and freelance user researchers

The wedge is: **cited sampling frame + many reactions + clustered split**, delivered as a cold demo rather than a research engagement.

## Current scope (from architecture)

See `docs/build-plan.md` for the demo flow. `notes/MEETING_NOTES.md` holds judging + product lock.

**Build for real**

- Frame builder — **two segments** (in-market buyer, skeptic/blocker) + weights + citations
- Cohort sampled from those two segments only (~200 rows, in memory)
- Fan-out runner
- Clustering / divergence
- Distribution view

**Stub if needed**

- One cached evidence pull per category (instead of live retrieval)

**Cut if late**

- Persistence — keep the cohort in memory
- Extra segments, joint trait network, media-diet updates (stretch only)

## Source of truth in this folder

- `docs/build-plan.md` — demo flow to record
- `docs/demo-video.md` / `docs/pitch-deck.md` — submission story
- `notes/MEETING_NOTES.md` — judging rules
- `quant/weights.yaml` — published scorecard
- `docs/architecture.spec.json` — earlier architecture, not a build commitment
- This file — original product brief
