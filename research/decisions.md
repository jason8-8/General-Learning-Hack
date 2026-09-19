# Current decisions

Updated 20 September 2026. Implementation remains paused by Jason. Source of truth: [build plan](../product/BUILD.md).

| Decision | Current direction |
| --- | --- |
| Product | Pre-launch consumer SaaS assessment |
| User | Founder deciding how to build and launch |
| Intake | Free-text idea, draft interpreted brief, founder confirms/edits; audience discovered by system |
| Pipeline | Intended: confirmed brief → shared research → reviewed audiences → simulation → structured scenarios → deterministic quant → report. Current code remains a rule-based fallback. |
| Quant | Reuse baseline with explicit provenance and missing-input handling; not a validated probability |
| Simulation | Primary experience; MiroFish selected but not integrated. Target 1,000 independent respondents subject to measured quality/cost/latency; six is a smoke test. No fixed audience-group count. Quant Option A primary; Option C remains fallback. |
| Report | Audience/value/barriers, frozen prediction versus real feedback, supported audience revision, untouched evaluation or validation pending |
| Learning loop | Evidence/profile updates with immutable baseline and change log; no silent weight retraining or foundation-model fine-tuning |
| Demo | AI travel assistant: who pays, for what, why not, and under which commercial assumptions. Travel abroad implicit; omit “international” in product name. Supersedes internship/voice-note ideas. |
| Evidence | Public sources, dated cache allowed; unsupported inputs unscored |
| Forecast benchmark | Proposed month-six paid subscribers/revenue plus retention; outcome dataset not established |
| Excluded from v1 | Auth, billing, database and fine-tuning |
| Delivery | Working 120-second video and 90-second pitch |

The old two-segment buyer/sceptic lock and fixed 60/40 population mix are superseded. Earlier corporate and preset-segment outputs remain historical fixtures. No application implementation or validated forecasting capability is claimed by this decision.

Competitor implications: [Minds and Aaru review](simulation-competitor-implications.md). Remaining technical decisions: [build plan](../product/BUILD.md#decisions-log). No chat UI/persona-chat requirement was introduced by the inter-task conversation. No answers are inferred from silence.

Latest demo research: [AI travel assistant](ai-travel-assistant.md). Proposed visual walkthrough: [demo storyboard](../product/DEMO-STORYBOARD.md). Research and video-task coordination are authorised; implementation remains paused.

Approved [learning-loop amendment](../product/LEARNING-LOOP-AMENDMENT.md) supersedes fixed counts and mandatory pricing comparison. No real interviews or full simulation run are supplied; concept scenes must be labelled.
