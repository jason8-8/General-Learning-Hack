# Build plan traced to the demo

Proposed implementation scope only. This task creates documentation; it does not authorise an application build, deployment, commit or push. Read the [demo video](demo-video.md) and [two-slide pitch plan](pitch-deck.md) together with this plan.

## Borrow first, build the comparison flow

Borrow existing research and model capabilities. [Societies](https://societies.ai/solutions) is prior art for grounded audience simulation, as checked in the originating task; it is not an agreed dependency. Don't claim the category is novel. Check access, cost and data coverage before selecting any service.

Build the distinctive flow: input → assessment → inspect evidence → edit one assumption → compare. A checked evidence pack and a small assessment routine are enough to test that interaction. No stack, provider, scoring weights, product name, category or geography has been selected. EdTech remains an option.

Done means:

- A real input produces an assessment whose findings distinguish evidence, inference and unknowns.
- Editing price OR audience produces a traceable comparison while preserving the original run.
- The team can record the flow and prepare all required submission assets before the deadline.

## Minimum components and proof points

| Demo proof point | Minimum component | Acceptance check |
| --- | --- | --- |
| 10–20s: enter an idea | Form with idea, audience and price; visible category/geography context | Validate required fields and price unit/currency. The run records exactly what was entered. |
| 20–45s: assess | Assessment routine and view for buyer candidates, competitors/alternatives and adoption factors | All three sections appear. Unsupported findings say evidence is missing rather than inventing facts. |
| 45–60s: inspect | Evidence records and a finding detail panel | One click shows the supporting source, date, observation, reasoning and limitation. |
| 60–80s: change and compare | Editable assumption, saved baseline and comparison view | Change one field; preserve the baseline; explain changed findings. An unchanged result is acceptable if justified. |
| Record reliably | Loading/error states and explicit cached-evidence mode | Source failure is visible. Cached evidence stays labelled; errors never display a stale result as a new run. |

These are responsibilities, not separate services. Keep them in the smallest structure the chosen tools support. Accounts, payments and persistent databases are not needed to prove this flow.

## Minimal data contract

This is a proposed contract between input, assessment and display. Field names may change; their meaning must survive.

| Record | Required contents | Why it exists |
| --- | --- | --- |
| Scenario | `id`, `idea`, `audience`, `category`, `geography`, `price.amount`, `price.currency`, `price.unit` | Makes the tested assumptions explicit. |
| Evidence | `id`, `url`, `title`, `published_at` (nullable), `retrieved_at`, `observation`, `limitations` | Lets the viewer check what supports a finding. Missing dates remain null. |
| Finding | `id`, `kind` (buyer/competitor/adoption), `statement`, `evidence_ids`, `reasoning`, `unknowns`, `claim_type` (observation/inference/assumption/simulation) | Separates a cited observation from the model's inference. Empty evidence means unsupported, not established. |
| Assessment | `id`, `scenario_id`, `created_at`, `evidence_mode`, `evidence_pack_version`, `method_version`, `findings` | Records which inputs, evidence and method produced a result. |
| Comparison | `baseline_id`, `revised_id`, `changed_field`, `before`, `after`, `finding_changes`, `explanations` | Makes a one-variable change reviewable. |

When comparing, hold the evidence pack and method version fixed where possible. If changing audience requires different evidence, disclose that difference and don't attribute the whole result to the audience edit alone. Control model variation through structured outputs and stable settings where available; do not promise identical outputs from an uncontrolled model call.

Start without a headline score. If a score helps the chosen example, add its formula, factor values, weights and version to the contract and label it “heuristic”. A transparent formula is inspectable, not automatically empirically valid. No probabilities of startup success, investment-return promises, invented confidence intervals or asserted accuracy. Synthetic personas can generate hypotheses but cannot supply evidence of real demand.

## Scope and exclusions

Include one researched example, one baseline, one revised scenario, source inspection and a next-test recommendation. Prefer readable findings to a large synthetic cohort.

Exclude broad market coverage, autonomous monitoring, portfolio returns, elaborate persona fan-out, historical validation and production infrastructure from the minimum demo. If historical testing is later attempted, fix the prediction date, use only information available before that date, define outcomes and evaluation rules in advance, and hold out cases. Later-outcome leakage would invalidate the exercise. A present-day language model may already know the historical outcome, even when prompted to use only old information; address that contamination before calling the exercise a predictive back-test.

## Ordered milestones

The verified deadline is **Sunday 20 September 2026, 10:00 HKT, no extensions**. Build began Saturday 19 September at 10:00; offsite work is allowed after 18:00. Return Sunday at 13:00; showcase 14:00–15:30; results 16:00. These replace the same-day schedule in [CONTEXT.md](../CONTEXT.md).

The following cut-offs are proposed protection for recording and submission, not a claim about team capacity. If time is short, cut features before cutting this buffer.

1. **Select the demonstration.** Team chooses the idea, audience, geography and meaningful price-or-audience edit. Confirm a relevant studies, job/internship or life track and the personal reason for building it. Gate: enough accessible evidence to explain one useful finding.
2. **Prepare evidence and contract.** AI can gather candidate sources and structure records; the team checks relevance and accepts the inference boundaries. Gate: source links resolve and observations support the selected finding.
3. **Complete one vertical path.** Build form → assessment → evidence inspection before adding breadth. Gate: all inputs and displayed findings are traceable.
4. **Add edit and comparison.** Preserve baseline, change one field and explain the difference. Gate: the comparison reflects the actual revised input, including a defensible no-change outcome.
5. **Rehearse and freeze scope by Sunday 07:00 HKT.** Verify the complete path, failure handling and claim labels. Cut optional scoring or live retrieval if they threaten reliability.
6. **07:00–08:30: record and export.** Capture the 90-second core and produce the official two-minute video with context. Watch the full export and retain a backup.
7. **08:30–09:30: package and submit.** Prepare the public GitHub repo, two-minute prototype video and written explanation of problem, operation and actual technologies. Check the public repo contains no secrets or credentials, verify links and complete submission. These are future delivery steps, not actions authorised by this documentation task.
8. **09:30–10:00: contingency.** Verify receipt and repair upload or access issues before the hard deadline. Don't plan new features here.

## Decisions, dependencies and ownership

| Open decision or risk | Proposed response | Who does it |
| --- | --- | --- |
| Example/category/geography | Select for evidence availability and a clear comparison, not assumed host preference | Jason/team decides; AI researches candidates |
| Stack/provider/access/cost | Reuse available tools; verify access and latency before depending on them | AI checks and proposes; team supplies account access and spending decisions |
| Thin or contradictory evidence | Show the limitation, narrow the claim or change example | AI flags and structures; team accepts scope |
| Price or audience edit | Choose one that tests a commercially meaningful assumption | Team chooses; AI prepares and checks the comparison |
| Scores and weights | Omit unless explainable; disclose any chosen heuristic | AI drafts formula options; team approves interpretation |
| Submission and claims | Verify actual technology list, track fit, source claims and asset access | AI drafts/checks; team owns final judgement, recording and submission |

AI can take research, evidence extraction, contract drafting, implementation once separately authorised, checks, narration drafts and packaging preparation. Only Jason/team can supply their personal motivation, choose what they stand behind, grant account access, approve spending and complete relationship-dependent work. No staffing level or budget is assumed.

## Source precedence

The originating task verified the full [official PDF](/Users/jasoncheng/Desktop/GL%20Hacks.pdf), pages 5–6 and 9, and [intro transcript](https://notes.granola.ai/t/066040e4-1cc0-45bd-95ce-7cd87acd65c3-008umkv4). Required assets are a public GitHub repo, two-minute video including a working prototype, and written explanation of the problem, how the solution works and technologies. No separate deck or live-pitch duration is specified.

The intro does not require EdTech or a product for General Learning. The old brief's example adoption percentages, success probabilities and confidence intervals are unvalidated proposals and must not become product claims. The existing [architecture diagram](architecture.html) and [specification](architecture.spec.json) predate the later quantitative-scoring refinement; their cohort size, provider and fan-out design are not implementation commitments. Existing files remain unchanged.

Assuming: one evidence-supported example is sufficient for the demo, the team can access a suitable research/model capability, and the proposed recording buffer remains feasible.
