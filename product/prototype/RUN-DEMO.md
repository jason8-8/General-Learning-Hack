# Run the guided demo on your computer

> **Superseded — this is the legacy note-taking fallback**, now served at `/legacy`. The current demo product is the AI travel assistant: use [RUN-MIROFISH.md](RUN-MIROFISH.md) for the real engine at `/lab`, and [SHOWCASE-DEMO.md](SHOWCASE-DEMO.md) for the illustrative presentation at `/`. The instructions below still work, but they start the earlier voice-notes flow — do not record it as the current product.

You need Git, Python 3.9 or newer, and a web browser. No API key, Node.js, pip install or paid account is required. The guided example works offline after cloning because its source excerpts are bundled and visibly dated.

## Fresh checkout

macOS / Linux:

```bash
git clone --branch main https://github.com/jason8-8/General-Learning-Hack.git
cd General-Learning-Hack
python3 product/prototype/server.py --port 8765
```

Windows PowerShell:

```powershell
git clone --branch main https://github.com/jason8-8/General-Learning-Hack.git
cd General-Learning-Hack
py -3 product/prototype/server.py --port 8765
```

Keep that terminal running. Open this address on the **same computer**:

```text
http://127.0.0.1:8765/
```

`127.0.0.1` points to your own computer. Jason's local server is not a public deployment; each teammate runs their own copy.

## Walk through Hindsight

1. Open the root page to see **Learn from the future. Shape the present.**
2. Review the five travel buying situations and the cited competitor context.
3. Compare the basic itinerary with the proposed trip-readiness pack. Change price and audience to inspect the commercial scenarios.
4. Open the RAG explorer: search saved research and select a source, passage, profile, prompt or staged-answer node.
5. Inspect assumptions and export the illustrative dataset. The 1,000 profiles and price-response assumptions are fictional, not measured customer demand.

The presentation needs no model. Retrieval over bundled summaries and chart calculations run locally. Generation is staged. Real recorded MiroFish pilots are at `/lab`; install the optional engine using [RUN-MIROFISH.md](RUN-MIROFISH.md) only to run new interviews. The earlier guided scorecard remains at `/legacy`.

See [SHOWCASE-DEMO.md](SHOWCASE-DEMO.md) for the presentation method and latest revisions.

## If you already cloned the repository

First check for your own edits:

```bash
git status
```

If the working tree is clean, switch to main and update:

```bash
git switch main
git pull --ff-only origin main
```

Then start the server with the command for your operating system above. If Git reports local changes or diverged history, stop and preserve that work before integrating; these instructions do not reset or overwrite it.

## Run the verification checks

From the repository root, macOS / Linux:

```bash
python3 -m unittest discover -s product/prototype/tests -v
```

Windows PowerShell:

```powershell
py -3 -m unittest discover -s product/prototype/tests -v
```

Expected: 20 tests pass. They cover missing inputs, citations, numerical behaviour, confirmation gates, recorded-demo network isolation, category matching and saved comparison replay. These tests do not need a server, API key or network.

## Common problems

- **Python command missing:** install Python 3.9+ from the official Python website, then reopen your terminal. On Windows, the documented command uses the Python launcher (`py`).
- **Address already in use:** stop an older demo with Ctrl+C, or choose another port.

macOS / Linux alternative port:

```bash
python3 product/prototype/server.py --port 8766
```

Windows alternative port:

```powershell
py -3 product/prototype/server.py --port 8766
```

Open the matching address:

```text
http://127.0.0.1:8766/
```

- **Invalid local session after restarting the server:** reload the page. Unsaved server memory is cleared on restart; explicitly saved assessments remain available.
- **A live source is unavailable:** try the guided example. It uses bundled recorded evidence and never fabricates a replacement source.

Stop the server with **Ctrl+C**. Saved reports stay in `product/prototype/.runs/` on your own computer and are ignored by Git. They may contain your product ideas; they are not shared with teammates by a push.
