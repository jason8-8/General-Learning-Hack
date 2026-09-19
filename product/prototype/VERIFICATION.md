# Verification record

Checked on 20 September 2026, Asia/Hong_Kong. UTC retrieval timestamps correctly fall on 19 September.

## Passed

- 16 Python tests: deterministic quant, missing values, invalid numbers, provenance/citation validation, rubric boundaries, expected single-factor weight effect, confirmation gates, unknown geography, second unseen idea, unsupported-category behaviour, source deduplication/failure handling, immutable baseline, price-comparison rejection, reaction/evidence separation, metadata extraction and saved replay.
- JavaScript syntax checks for the browser application and browser-test script.
- Real browser flow in isolated headless Chrome through bundled Playwright: voice-note idea and a separately typed habit-restart idea; no preset ID required.
- Live vendor-page retrieval from the local application. Voice-note run returned Voicenotes and Obsidian; exact short metadata descriptions, source IDs and timestamps appeared in the evidence pack. First successful retrieval took 2.804 seconds; timings are recorded per run, not promised.
- Source inspection, audience confirmation, report navigation, six labelled rule-based passes, proposition comparison, baseline preservation, JSON download, local save and saved-run replay.
- Numerical browser scenario: eight explicit assumptions of 0.5 produce index 0.500. Changing switching ease to 0.9 produces +0.040, matching its 0.10 weight. Evidence coverage stays 0/8 and outlook stays insufficient evidence.
- Price factor absent from comparison options; server rejection covered by Python tests.
- Desktop 1440×1000 and mobile 390×844 screenshots inspected. No page-level horizontal overflow at 390px. Quant table scrolls within its own container. Zero browser JavaScript errors. Reduced-motion browser setting exercised.
- Existing scorer and brand assets unchanged. Changes confined to `product/prototype/`. Local saved runs excluded from Git.

Browser summary:

```json
{"passed":true,"flows":2,"liveSources":true,"savedReplay":true,"quantDelta":0.04,"priceDisabled":true,"export":true,"mobileOverflow":false,"consoleErrors":[]}
```

## Not verified / not implemented

- No live LLM or search provider, no real MiroFish run, no LLM cohort, no 30-agent run, no paid-model usage. All external API spend: $0.
- The three concurrent workers review a bounded catalogue. Their code is not an LLM research-agent implementation.
- No evidence-derived numerical judgement. Browser inputs are explicit founder assumptions. Broad report copy and stress-test questions are authored templates.
- The existing price-fit boundary and nonmonotonic probability-blend behaviour remain unfixed. Adoption probabilities are not exposed; price comparison is disabled.
- No independent demand study, validated customer segments, historical outcome dataset, or predictive accuracy measurement.
- No broad accessibility audit or production security review. The app is a local prototype, not a deployment-ready service.

## Browser runner

`tests/browser.cjs` requires a running localhost server and Playwright/Chrome. It accepts `PLAYWRIGHT_MODULE`, `CHROME_PATH` and `PROTOTYPE_URL` for an existing runtime. It makes no paid calls, fetches the fixed official vendor pages, and creates a demo saved baseline. Screenshots and JSON export go to `/private/tmp/launch-*` on this macOS workspace.

The first browser attempt found no bundled Chromium executable. The installed Chrome worked when launched outside the filesystem sandbox. An ambiguous test selector was corrected; application functionality did not fail at that step.

## Demo repair follow-up

- Reproduced the actual user-facing problem in the in-app browser: a sports-coaching idea was accepted outside the source catalogue and produced a generic unscored report. Preserved that input as a local saved run.
- Added a four-step guided voice-note demonstration with a prewritten editable brief, real recorded vendor excerpts, opt-in illustrative factors and a prepared comparison. The unchanged demo makes no network calls.
- Fixed category substring matches (for example, “already”, “invoice” and “planet”) and reject unsupported ideas before research.
- Local saves now retain the selected comparison and restore it across loss of server memory. Existing baseline-only saves remain readable.
- 20 Python tests passed, including demo network isolation, unsupported-category rejection, classification regression and full comparison persistence.
- Verified the guided flow in the actual in-app browser: 0.500 baseline, 0.540 alternative, +0.040 delta, 0/8 evidence coverage, explicit authored-fallback labels and save confirmation.
- LLM and MiroFish integration remain unimplemented. The guided demo demonstrates workflow and deterministic sensitivity, not real market prediction.
