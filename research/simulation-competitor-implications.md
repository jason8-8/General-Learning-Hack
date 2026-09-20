Approved later amendment: fixed six-agent scope and mandatory pricing comparison below are historical. See [learning-loop amendment](../product/LEARNING-LOOP-AMENDMENT.md) for benchmark-dependent scale and feedback-led payoff.

# Simulation competitors and build implications

Historical scope note: the internship example below was subsequently replaced by the AI travel assistant; see [current research](ai-travel-assistant.md) and [storyboard](../pitch/video.md). Methodological recommendations remain relevant.

Updated 20 September 2026. Research/plan update only; implementation remains paused. Incorporates the GL video-plan task's handoff and the latest decisions in this build task.

## Source verification

- **Minds:** [Audience guide](https://getminds.ai/guide/audiences), independently reopened in this task. It documents reviewable synthetic audiences, reusable studies, per-respondent answers, audience comparisons and deterministic server calculations over structured responses. It explicitly distinguishes synthetic results from population estimates. This supports separating collection, calculation and explanation; it does not establish our prototype's validity. The [study guide](https://getminds.ai/guide/studies) was inaccessible to this task's browser tool; its details in the handoff remain attributed to the video task rather than independently confirmed here.
- **Aaru:** [Simulation workflow](https://aaru.com/simulation), independently reopened. The published workflow starts with objectives, populations and questions, then organises simulation results around them. This is useful product framing, not proof of a particular internal quant implementation or our predictive performance.
- **Additional handoff sources:** [Minds PRISM](https://getminds.ai/research/minds-prism), [Aaru product innovation](https://aaru.com/use-cases/product-innovation), [Minds homepage](https://getminds.ai/). Profile conditioning, validation and visual observations from these pages were supplied by the video task, not independently re-audited here. No inspected evidence establishes a Minds-to-MiroFish dependency.

## Accepted implications

1. Lead with the founder's decision and research questions. The agreed example is a paid internship application assistant: who might pay, what they value, why they might reject it, and whether explicit economics could support a business.
2. Review candidate audiences before running. Ground them in workflows, alternatives, budgets and barriers. Do not infer age or other demographic composition from the product category alone. Show modelled and unknown profile fields as such.
3. Keep simulation primary and retain Q10 Option A: agents propose structured scenarios; deterministic Python tools calculate them. Q10 Option C remains the explicitly labelled fallback. The simulation does not create or validate the quantitative model.
4. Separate source evidence, synthetic response counts, assumed commercial scenarios and the unvalidated legacy index. A simulated payment intention is not measured conversion. With six agents, show counts and denominators, not market-share estimates or statistical certainty.
5. Make one conclusion traceable through its source, synthetic profile, question, generated answer and numerical inputs. End with an audience/offer hypothesis, barrier and real customer test.
6. Preserve the user-selected wording: “Learn from the future. Shape the present.” The video task reports that Aaru already uses the earlier alternative wording; do not revert it.

## Deferred

- Broad visual redesign, particle portraits, larger populations, persona chat and extensive research-method calculators. The requested chat interaction referred to communicating with another Codex task, not a new product feature.
- Pricing controls until the legacy price-fit defects are resolved and tested. Subscription, season pass and per-application offers belong in the research scope now; they are not permission to ship broken numerical controls.
- Real simulation integration until Jason resumes implementation. Local Ollama returned one structured response in about eight seconds; dependencies for a local MiroFish fork were installed, but no full MiroFish run or application adapter was verified. These are feasibility steps only.

## Conflicts resolved / remaining

- The old voice-note fixture is no longer the chosen demo. Preserve it in code until a deliberate implementation change; the plan now names the paid internship assistant.
- A high-volume-versus-high-fit feature comparison is not the primary question. It may become a follow-up scenario after investigating audience, value and willingness to pay.
- The old eight-hour estimate is historical. No current deadline or remaining time was inferred.
- Simulation plus a quant layer is not a defensible uniqueness claim by itself. Differentiation must be demonstrated in decision usefulness, traceability and real-world validation.
- Source-supported audience discovery is a target capability, not current behaviour. The current app has category rules and vendor excerpts. Generated customer research, generalisation and paid-business assessment are not implemented.
- Hong Kong/English remains the inherited team setting in BUILD.md; the new demo did not independently confirm geography. Verify before population-specific commercial claims.

## Priority when implementation resumes

Confirm study question and geography → gather applicant-workflow evidence → review up to three audience hypotheses → inspect one synthetic profile → run a bounded real simulation → validate structured outputs → calculate explicit scenarios → present a traceable report and next test. Do not restart implementation or incur external API spending from this document.
