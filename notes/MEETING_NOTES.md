# Meeting notes — 19 Sep 2026

Repo: `jason8-8/General-Learning-Hack`

---

## Pitch round 2 format and judging criteria

- **Title:** Pitch round 2 format and judging criteria
- **Date:** 19 Sep 2026
- **Noted by:** Jason Cheng
- **Source:** organizer briefing (transcript below)

### What judges will actually see

Judges will **not** look at code. They will **not** inspect technical details.

The only artifacts that count:

1. **2-minute video**
2. **1.5-minute in-person pitch**

That is the entire window to impress them. Work **backwards from the story**, not forwards from the stack.

### Format lock

| Item | Rule |
| --- | --- |
| Disqualifications | **None.** Every team is promoted to round 2 by default |
| Who pitches in person | Everyone. 90-second pitch is mandatory, not optional |
| Prep warning | After **10:00** there may be no time left to write the 90-second pitch. Prepare both artifacts **now** |
| Round 1 → round 2 window | **10:00–13:00** |
| What to prepare | Both the 2-minute video **and** the 1.5-minute live pitch |

### Team takeaway (this room)

Quant is good enough. Do not keep deepening the model.

Decide first: **what do we show in 2 minutes and in 90 seconds?** Then build only what that story needs.

Suggested split to design against:

- **Video (120s):** the story — one idea in, a split of reactions out, a kill objection in the tail. Why this is not “ask ChatGPT.”
- **Live pitch (90s):** the claim a judge can repeat — cited segments, distribution not an average, deterministic P(adopt) as the backup number. No architecture tour.

### Transcript (lightly cleaned)

> Ours, we believe you guys should be able to explain it to us in 90 seconds. So make sure you guys prepare for both of them because you may not have the time after 10 AM to prepare the 1.5 minutes.
>
> But one thing that I can tell you guys right now is between round 1 and round 2, which is between 10 AM and 1 PM, we just decided right now that we will not be doing any disqualifications. Which means all of you guys will be doing the in-person pitch.
>
> First we had kind of thought, okay, we'll maybe disqualify some teams, we'll let you guys know which teams make it to the second round, and only they will do the 1.5-minute pitch. But we talked to everyone and we think everyone's doing quite nice, so we kind of want everyone to do the 1.5-minute pitch also. So it's technically everyone gets promoted to round 2 by default.
>
> Based on the conversations with you guys and looking at your solutions: when we look at your solution, me and the other judges, we will not be looking at the code. We will be looking at the 2-minute video and the 1.5-minute pitch. That's all we know about your solution. We do not actually know any technical details about your solution. So that is the moment you get to impress us.
>
> Think about those 2 minutes and those 1.5 minutes and how you will impress us, and then work your way backwards. Don't think about the technical solution and then what the video will look like. Think about what the video will look like. Think about what the story will be. Work your way back.
>
> If you guys have any questions, let me know here or just WhatsApp me. Go back to your work.

Team side of the same conversation:

> Let's just focus on what we're gonna show. Work our way back. Quant is okay. This is the quant deterministic part. It's okay. I don't think it's that bad of a solution. I just think we need the perspective of what we are showing in those 2 minutes and 90 seconds. Once we have that, we can brainstorm what we actually need for the 2-minute.

---

## Product decisions (earlier the same day)

Ship the original architecture. Do not start with an Aaru-style joint trait network.

| Decision | Locked choice |
| --- | --- |
| Sampling frame | Segments + weights + citations |
| Qualitative sim v1 | **Two segments only** |
| Segment roles | In-market buyer vs skeptic / blocker |
| Joint trait network | Stretch. After the view works |
| Media-diet loop | Stretch. Not v1 |
| Evidence | Cached reviews, filings, forums |
| Cohort | ~200 rows, in memory, seeded |
| Reactions | One Claude call per persona, then cluster |
| Output | Distribution + tail objections. No average |
| Persistence | Cut |
| Quant path | Separate deterministic scorecard. No LLM in P(adopt) |

## Two-segment sim (qualitative)

Names come from the category cache. Roles stay fixed:

1. **In-market buyer** — already shopping or using a substitute.
2. **Skeptic / blocker** — would have to approve, switch, or ignore it.

Each segment is a template (label, weight, 3–5 grounded attributes, `source_ids`). Do not sample age × income × tenure as independent columns.

Fallback mix if the cache has no weights: **0.60 buyer / 0.40 skeptic**, labeled **assumed**, not cited.

## Quant model (this repo)

The workbook / `quant/` scorer answers `P(adopt | segment, product)` on a frozen universe. It does not interview synthetic users.

Judges will not open this. Treat it as a number the 90-second pitch can point at, not as the demo.

Weights + rationale:

- `quant/weights.yaml`
- `quant/WEIGHTS.md`
- `quant/score_engine.py`
- `sheets/02_Assumptions.csv`

Quant still uses the five HK / APAC universes in `data/segments.csv`. That is the market layer. The two-segment split is the reaction layer.

## Build order (rewritten against judging)

1. Lock the 120s story and the 90s spoken claim
2. Frame builder (two segments) — only if the story needs it on screen
3. Cohort + fan-out + clusters — only if the video shows the split
4. Distribution view — the thing in the video
5. Quant already exists. Do not deepen it unless the pitch needs one number
6. Stretch only after video + pitch copy exist: third segment, joint network, media diet

## Done when

- Both the 2-minute video script and the 90-second pitch can be said without opening a repo
- Screen shows two named segments, weights, sources, and a tail objection
- Quant stays deterministic and in the background
