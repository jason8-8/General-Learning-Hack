> **Scope update, 19 September 2026:** Consumer SaaS launch assessment is the agreed direction. Read [BUILD.md](BUILD.md) for the current build plan, architecture and demo flow. The earlier brief below is historical wherever it conflicts. The old architecture.spec.json is also historical; use the layering diagram in the build plan.

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

## Design bets

| Bet | Why it matters |
| --- | --- |
| Evidence-grounded cohort | Personas must be derived from cited sources a judge can interrogate |
| Distribution over average | Disagreement is the signal; averaging hides the kill objections |
| Cold-start on stage | Time-to-first-insight measured in minutes, not a research sprint |
| Fan-out, then cluster | Scale comes from concurrent persona calls, not a longer prompt |
| Laptop-scoped | No persistence required for the demo; cohort can live in memory |

## Current scope

See `BUILD.md` for what to ship. See `../pitch/` for the video and live pitch.

**Build for real**

- Frame builder — two segments (in-market buyer, skeptic/blocker) + weights + citations
- Assessment + evidence inspection + one-assumption compare
- Existing quant scorecard

**Cut if late**

- Persistence, extra segments, joint trait network, media-diet updates

## Source of truth in this folder

- `../pitch/` — video and live pitch
- `BUILD.md` — what to ship
- `quant/weights.yaml` — published scorecard
- `architecture.spec.json` — earlier architecture, not a build commitment
- This file — original product brief
