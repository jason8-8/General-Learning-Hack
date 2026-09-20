> Publication update: the approved static wireframe and scroll refinement are included in this publishing change. Earlier statements about uncommitted or unpublished work below describe the audit checkpoint. The 3D-model task was cancelled.

# Audit verification

Checked locally on 20 September 2026. Application copied from tracked build commit `c0c8a76` into the main workspace, then repaired. Existing source worktree was not modified.

## Passed

- 37 Python tests, including the original 34 and new checks for pilot-count reconciliation, retrieved passage provenance/no-match behaviour, and the legacy price-fit boundary/non-finite inputs.
- JavaScript regression checks for unchanged/single/multiple-input comparisons, mismatched datasets, frozen baseline, selected concepts/audiences, monotonic scenario counts and invalid inputs.
- Browser flow in isolated headless Chrome with Playwright: readiness £10 baseline is 159/1000; frozen baseline survives a price change, concept change and family-audience selection; multiple changes trigger the warning.
- Export includes the selected basic concept, 200-profile family sample, original readiness baseline, note, timestamp and real recorded pilot metadata.
- Empty retrieval query result is shown without manufacturing a passage.
- Selected audience limits the buying-situation chart to that audience.
- Desktop 1440×1000 and mobile 390×844 screenshots inspected. No page-level horizontal overflow at 390px; zero JavaScript page errors in tested flow. Reduced-motion preference exercised.
- Python sources parsed; JavaScript syntax checked.

Browser evidence: `/private/tmp/hindsight-decision-desktop.png`, `/private/tmp/hindsight-decision-mobile.png`, `/private/tmp/hindsight-export.json`. These temporary files are not required to run the repository.

## Reproduce the local checks

```bash
python3 -m unittest discover -s product/prototype/tests -v
node product/prototype/tests/test_study_math.cjs
python3 product/prototype/server.py --port 8765
```

Open the local URL from README. Freeze a baseline beside the price control, change price, review the receipt, change concept and confirm the multiple-change warning, select an audience, export, inspect the file.

The agent-browser CLI was unavailable, so the browser-verification checklist was executed with bundled Playwright and installed Chrome. The filesystem sandbox blocked initial server/browser startup; approved isolated local execution succeeded.

## Not claimed

No new model runs, paid API calls, real interviews, independent predictive validation, finished video, deployment or push. The authored scenario and recorded model pilot use different offers and must not be interpreted as a controlled comparison. The legacy probability blend remains excluded from the demo. A full cross-browser/accessibility/security review and fresh-clone check on a second computer were not performed.
