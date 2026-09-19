# Proposed demo: assess an AI travel assistant

> Build update, 20 September 2026: Jason has resumed implementation. The local six-person MiroFish interview demo and versioned feedback rerun now work, with bundled real-run replays. Sources/profiles remain curated, example feedback is illustrative, and separate validation is pending. Earlier references to a pause below describe the planning snapshot. See [current build](prototype/RUN-MIROFISH.md).

Updated 20 September 2026. Approved planning direction; implementation paused. No new API spending. The canonical approved narration and timings are in [pitch/video.md](../pitch/video.md); its opening is preserved verbatim. This worktree now contains that approved revision.

## Story and product

General Learning assesses an **AI travel assistant that helps people plan and navigate trips**. The question is who would pay, what they value, and why they would choose it over ChatGPT or free travel tools. We are not showing a functioning travel assistant or booking flow.

The main payoff is **prediction → real feedback → supported audience revision → separate evaluation**. Pricing-format comparison remains optional, not the required climax.

## Visual sequence

| Time | Scene | Evidence boundary |
|---|---|---|
| 0–24s | Approved opening: experience, failure and possible futures; line becomes idea field | Editable type/path animation, not fabricated product output |
| 24–38s | Travel product, paid-demand question and confirmed brief | Research begins after confirmation |
| 38–49s | Research sources lead into reviewed audience | Inspect one source and distinguish supported from modelled profile characteristics |
| 49–65s | Actual response count, one profile/answer and computed comparison | Show completed/failed/excluded counts and the engine that ran; synthetic answers and commercial assumptions stay separate |
| 65–80s | Frozen prediction beside compatible customer feedback | Use actual withheld feedback only; none has been supplied. Example data is labelled illustrative |
| 80–95s | One justified audience revision, new version and reassessment beside original | Highlight changed fields; never overwrite baseline or quietly alter scoring weights |
| 95–103s | Evaluate on separate untouched evidence | Otherwise show evaluation pending and the next real test |
| 103–120s | Actual recommendation and unresolved assumption; approved closing | No preselected winner, guaranteed outcome or unsupported accuracy claim |

Timing is a rehearsal target, not measured runtime. Use canonical narration from pitch/video.md without rewriting its approved opening. Recorded engine runs keep timestamp/model labels. Concept scenes remain visibly labelled. Never fabricate live progress.

## Visual direction and scale

Preserve Space Grotesk for headings/body, Space Mono for labels/figures, green-black and phosphor green. Keep the idea pinned as the viewer follows evidence into responses and feedback. No persona-chat requirement or full redesign is added.

Do not narrate three research agents or three audience groups. Internal specialisation can remain; audience composition follows the question and evidence. Aim for 1,000 independently evaluated respondents only after quality/cost/latency benchmarks. Suggested gates 50 → 250 → 1,000 are not approved spend or completed work. Six is an engineering smoke test. Never imply a larger achieved sample through decorative markers or duplicated records.

## Frozen baseline and feedback

Freeze the brief, offer/questions, audience/evidence versions, model configuration, responses and calculation inputs before revealing feedback. Feedback records collection date, recruitment limits, matching characteristics, exact offer and stated preference versus observed behaviour. Compare only compatible fields and report the sample size.

Use eligible feedback to revise needs, workflows, budgets, alternatives and objections, with a change log and new audience version. Small interview samples do not establish population proportions. Once feedback informs a revision, it cannot serve as untouched evaluation data. Separate evidence or a later real-world test is required for an improvement claim.

These are evidence/profile updates, not foundation-model fine-tuning or recursive self-improvement. Preserve deterministic quant Option A and the approved independent-branches fallback. Neither synthetic votes nor real feedback silently rewrite legacy weights.

## Recording gates

- Show working interactions only as product footage. Label non-working UI as concept.
- Identify actual engine/count/timing. No verified MiroFish travel run exists yet.
- No real interviews have been supplied. Illustrative feedback cannot be narrated as real customer findings.
- If feedback is not implemented, use the canonical script's future-facing replacement: the next step is to collect feedback, compare it with predictions and refine the audience. Do not fake an import or rerun.
- Pricing is optional. Existing price-fit defects still block those controls. Separate commercial scenarios require explicit currency, duration, frequency, cost and conversion assumptions.
- A different output is not evidence of greater accuracy; mark validation pending without untouched evaluation.

## Done means when resumed

Reviewed travel brief and traceable audience; real bounded engine run with completion/failure counts; frozen predictions compared with compatible withheld feedback; versioned revision preserving original; separate evaluation or explicit validation pending. A 1,000-person claim requires an actual measured run within agreed limits.

Current implementation remains the notes/productivity rule-based fallback. The local Ollama JSON probe was a connectivity check, not a travel simulation. This document does not resume implementation.

References: [approved amendment](LEARNING-LOOP-AMENDMENT.md), [travel research](../research/ai-travel-assistant.md), [build plan](BUILD.md).
