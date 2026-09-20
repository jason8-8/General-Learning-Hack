# Demo video: 120 seconds

Updated 20 September 2026. Recordable script for the current build. The approved opening is preserved verbatim; the unverified target-state middle is archived in [the earlier script](archive/video-target-state-20260920.md). This replaces it for recording.

## Narration

```text
Learn from the future. Shape the present.

Throughout human evolution, we’ve learnt from experience.
From failure.
From what came before us.

But what if we could explore the outcomes before making a decision?

This is Hindsight. It helps founders find the assumption to test before they build.

Let’s assess an AI travel assistant.
Who would pay, and why leave their free tools?

We start with the competitive evidence.
Open a source and inspect what it actually supports.
Free itinerary tools make a generic planning offer difficult to distinguish.

Our proposed alternative is a trip-readiness check:
will the timing, transfers and constraints work together?

These charts are authored scenarios, not customer demand.
The assumptions are visible.

Freeze the baseline. Change one price.
The original stays visible, so we can inspect the difference.

Now look at the actual model pilot.
The same twenty synthetic travellers saw prices of ten and thirty pounds per trip.
All chose free tools in both runs.
That proves the pipeline ran. It doesn’t prove what customers will do.

So the next test is concrete.
Show real travellers a sample readiness check, the price, and their free alternatives.
Record their choice before changing the audience.

Save the evidence, the assumption, and what would change your decision.
Export it as one record.

Built with Python, JavaScript and a separate local simulation engine.
Recorded runs are labelled. Customer validation is still ahead.

Learn from the future. Shape the present.
```

## Recording sequence

| Time | Footage |
| --- | --- |
| 0–4s | Approved digital title |
| 4–14s | Approved evolution clip |
| 14–28s | Actual Hindsight interface, travel offer and question |
| 28–43s | Competitor evidence; open a source summary |
| 43–57s | Proposed readiness offer and visible authored-assumption disclosure |
| 57–72s | Freeze £10 baseline; change only price to £15; return to comparison |
| 72–91s | Actual recorded pilot cards: 20/20 chose free tools at both prices |
| 91–108s | Next-test note, predeclared decision rule, export |
| 108–120s | Actual stack and limits, then closing tagline |

This is a rehearsal target, not a measured narration duration. Record a scratch read first. If long, trim the middle; preserve the approved opening. Keep all provenance labels legible. Do not spend 20 seconds touring the RAG graph.

## Guardrails for the take

- The main page loads saved summaries and authored scenarios. Say “saved evidence” if asked; do not imply a live web-research run.
- The 1,000 rows are scenario construction, not 1,000 interviews.
- The pilot tested a different travel offer from the proposed readiness pack. Never call their difference a measured feature effect.
- Show the recorded model result as a limitation and reason for a real test, not a market verdict.
- No real customer interviews or independent validation have been supplied. The old real-feedback narration has been removed.
- Root `main.py` is billable media tooling, not the product. Start `product/prototype/server.py`.
- The existing CapCut text cues still contain the earlier target-state script. Replace/re-time them against this script before exporting. This audit has not edited CapCut or recorded narration.
