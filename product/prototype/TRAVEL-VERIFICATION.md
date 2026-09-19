# Travel demo verification — 20 September 2026

## Verified story

Browser review → local job API → MiroFish-local IPCHandler → OASIS interview → Ollama → SQLite → validated response → Python calculation → browser display → frozen baseline → supplied feedback → revised audience → separate saved run.

| Check | Result |
|---|---|
| Browser-triggered baseline | `8d81e6ff29bc4301`, 6/6 valid, 0 failed, 0 excluded, 16.74 seconds, 6 calls, 4,905 tokens |
| Browser-triggered revision | `fe2bf7744f814540`, 6/6 valid, 0 failed, 0 excluded, 16.13 seconds, 6 calls, 4,937 tokens |
| Local model | `qwen3-coder:30b`, Ollama localhost, temperature 0.3, maximum 700 output tokens/call |
| Paid API spend | $0 |
| Baseline preservation | Separate input/results directories; only T01 profile changed in v2; other five profiles identical |
| Feedback provenance | One authored illustrative observation, never labelled a real interview |
| Recorded baseline and revision | Both replayed in the browser after server restart; no new inference required |
| Calculation checks | Every recorded time-value result matches its explicit scenario inputs |
| Automated tests | 27 Python tests passed, including legacy tests and invalid feedback/shape/path/failure handling |
| JavaScript | `node --check` passed |
| Desktop | Inspected at 1440 × 900; sticky idea and chapter navigation visible; no horizontal overflow |
| Mobile | Inspected at 390 × 844; initial grid overflow fixed; viewport and document width both 390, including recorded revision |
| Typography | Computed Space Grotesk body / Space Mono labels; both font files served locally |
| Browser logs | No captured warning/error logs during replay checks |
| Motion | CSS reduced-motion override and JS media-query-aware scroll are implemented; OS preference was not changed for testing |

## Scientific result, separate from technical result

All six respondents chose `consider_paying` in both recorded runs. The example feedback said `free_only`; the revised T01 response still said `consider_paying`. The UI explicitly shows the remaining mismatch and warns about uniform outputs. No improvement claim is supported.

Some responses assume additional capabilities (for example work/personal separation or calendar integration). The broad, unpriced offer and this local coding model are inadequate for credible paid-demand inference. The demo proves the execution and inspection path. It does not prove realistic purchasing behaviour, generalisation, source-grounded persona discovery, social diffusion or 1,000-respondent scalability.

Two earlier technical runs are retained locally: the initial social-role run (29.76 seconds) and the first custom-role check (20.59 seconds). They are not the bundled recording. Four six-person runs total were executed during this build, all local. The bundled recordings are the baseline and revision initiated through the browser; they were not selected to show an improved decision.

## Files and execution

- `travel_runner.py`: engine adapter; raw prompt/output and SQLite evidence retained.
- `travel_service.py`: bounded background job, local storage and versioned revisions.
- `static/travel.*`: root UI; previous app remains `/legacy`.
- `travel/recorded-run.json`, `travel/recorded-revision.json`: actual synthetic recordings, portable across machines.
- `RUN-MIROFISH.md`, `setup-mirofish.sh`: teammate setup and dependency pinning.

Latest parsing and failure-accounting safeguards were unit-tested after the recorded runs; the recordings retain the runner hashes from their actual execution. A clean installation on a second computer has not been tested. No real feedback or separate validation dataset exists in the demo. Current changes are local and have not been pushed in this build session.
