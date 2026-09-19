# Current build architecture

Open `current-build.html` for the interactive Archify map. The source is `current-build.json`; this documents the local working tree, including the uncommitted scrolling interface. It is not a production deployment map.

## Read the diagram

1. The browser sends JSON requests to the loopback Python server. HTML, CSS, JavaScript and the bundled Space Grotesk / Space Mono fonts are served locally.
2. Confirmation gates precede research and assessment. The server validates the brief, audiences and factor records.
3. Evidence review uses recorded excerpts for the unchanged demonstration, or fetches a limited vendor catalogue for supported custom ideas. Three review workers label shared sources; these are not LLM agents.
4. The report builder calls the deterministic scorer and six authored stress tests. The current stress-test implementation also calls the scorer with the same inputs for each pass; the map omits that repeated call for readability. Threading does not create independent AI judgements.
5. Comparisons preserve the original baseline and reuse evidence. A revised numerical assumption changes the score; this does not establish that a revised product is better.
6. Reports remain in server memory until explicitly saved as local JSON files. Saved comparisons can be replayed. There is no shared database or hosted deployment in this map.
7. The disconnected MiroFish node is intentional: no adapter, model call, running customer simulation or paid provider integration exists in this prototype.

## Code evidence

- `product/prototype/static/app.js`: browser requests, confirmation flow, report rendering and comparison.
- `product/prototype/static/style.css`: local font faces and scrolling layout.
- `product/prototype/server.py`: dispatch, persistence, host checks and session token.
- `product/prototype/contracts.py`: validation and fingerprints.
- `product/prototype/research.py`: vendor catalogue, source retrieval and audience rules.
- `product/prototype/assessment.py`: report assembly, authored stress tests and baseline comparison.
- `product/prototype/quant_adapter.py`: validated factors, provenance and missing-input handling.
- `product/quant/score_engine.py`: existing weighted scoring implementation.
- `product/prototype/demo.json`: recorded demonstration inputs and excerpts.

## Archify delivery

Generated using the existing local Archify 2.17 package. The packaged renderer was not modified.

`delivery-receipt.json` contains the exact specification and artifact SHA-256 hashes, byte counts and the 9/9 showcase validation result. `current-build.visual-check.json` records the latest automated browser verification separately. The diagram is explanatory documentation; it does not add MiroFish to the app.
