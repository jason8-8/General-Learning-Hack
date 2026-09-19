# Audience learning loop: build-plan amendment

> Build update, 20 September 2026: Jason has resumed implementation. The local six-person MiroFish interview demo and versioned feedback rerun now work, with bundled real-run replays. Sources/profiles remain curated, example feedback is illustrative, and separate validation is pending. Earlier references to a pause below describe the planning snapshot. See [current build](prototype/RUN-MIROFISH.md).

Updated: 20 September 2026.
Status: planning direction approved by Jason. Implementation remains paused; no new API spending authorised.

This approved amendment has been reconciled with this worktree's BUILD.md, research decisions and demo storyboard. It supersedes earlier fixed three-audience counts and the mandatory pricing-format comparison. Implementation remains unchanged and paused. The main checkout's BUILD.md was not overwritten.

## Experience

General Learning assesses **an AI travel assistant that helps people plan and navigate trips**. We are not demonstrating a functioning travel assistant.

Describe and confirm idea → research → evidence-grounded audience → simulated responses and recommendations → real customer feedback → compare with saved predictions → revise audience → test again.

Do not enumerate three research agents or three audience groups in narration. Internal specialisation can remain; audience composition follows evidence and the study question. No persona-chat requirement is added.

## Scale

Target 1,000 independently evaluated synthetic respondents if measured quality, cost and latency permit. Six remains an engineering smoke test, not the product ambition. Suggested scale gates: 50, 250, then 1,000; these are not completed runs or spending approval.

Record requested, completed, failed and excluded counts. One offer with one response per person implies roughly 1,000 generation calls before research, profile creation, retries and analysis; another offer adds work. Measure tokens, limits and elapsed time before recording. Social interactions and multiple rounds need separate design and benchmarking.

Show actual completed responses. More synthetic respondents do not create independent real-world evidence or calibrated market shares. Never inflate counts with repeated records or decorative markers.

## Real feedback and model revisions

Save the baseline brief, questions/offer, audience version, evidence version, model configuration, answers and calculation inputs before revealing real feedback.

Feedback records identify collection date, recruitment/sample limits, offer tested, available respondent characteristics, and whether the observation is stated preference or actual behaviour. Avoid unnecessary identifying details.

1. Evaluate frozen predictions against compatible real answers the run did not see. Show mismatches and sample size.
2. Use eligible feedback to revise needs, workflows, alternatives, budgets and objections. Change population proportions only when supported; convenience interviews do not establish demographic distributions.
3. Create a new audience version and change log; preserve the original run.
4. Test improvement on separate untouched evidence or a later real-world test. Reproducing supplied feedback is adaptation, not predictive validation. Do not repeatedly tune on a test set and still call it held out.

Start with evidence/profile updates and explicit parameter adjustments. This does not imply foundation-model fine-tuning or recursive self-improvement. Fitted response calibration requires enough relevant labelled outcomes. Sparse feedback can support qualitative corrections while validation remains insufficient.

## Quantitative and simulation contracts

Preserve Q10 Option A: agents propose structured scenarios; deterministic Python tools calculate them. Independent quant and simulation branches meeting in the report remain the approved fallback.

Separate source-backed observations, synthetic responses and assumption-based calculations. Audience updates must not silently rewrite legacy scoring weights. Explain each changed input and its provenance.

MiroFish travel adaptation and a full run remain unverified. Its social-simulation origin does not provide validated purchasing predictions or an automatic calibration loop. Identify the engine that actually ran.

## Demo and acceptance

The main payoff becomes saved prediction versus real feedback versus revised assessment. A pricing-format comparison is optional rather than mandatory.

Done means when implementation resumes:
- Reviewed travel brief and traceable audience, with actual simulation completion/failure counts.
- Frozen predictions compared with compatible real feedback withheld from the baseline.
- A versioned audience revision showing exactly what changed, without overwriting baseline results.
- Any claim of improved predictions supported by separate evaluation; otherwise validation pending.
- The 1,000-person claim used only after a measured run meets agreed resource limits.
- Recommendations trace to evidence, synthetic responses or assumptions and identify a real next test.

Real interviews have not been supplied here. Illustrative feedback must be labelled illustrative. A non-working feedback UI must be shown as a concept, not product footage. Current known build state: paused, rule-based fallback, no verified full MiroFish travel run.

## Research basis

- [Stanford interview-grounded agents](https://hai.stanford.edu/policy/simulating-human-behavior-with-ai-agents): precedent for 1,052 interview-grounded individuals, not our travel-purchase accuracy.
- [Minds audience methodology](https://getminds.ai/guide/audiences): separates profile characteristics from withheld outcomes; synthetic quant remains directional.
- [Aaru methodology](https://aaru.com/simulation): company description of training, held-out evaluation and later observed outcomes, not evidence our implementation has those capabilities.
- [MiroFish runner](https://github.com/666ghj/MiroFish/blob/main/backend/app/services/simulation_runner.py): social-platform, round-based execution requires adaptation.
- [OASIS paper](https://arxiv.org/abs/2411.11581): scaling precedent, not a runtime benchmark for our hardware.

Script and storyboard: [pitch/video.md](../pitch/video.md).
