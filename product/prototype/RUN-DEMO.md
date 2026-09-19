# Run the guided demo on your computer

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

## Walk through the example

1. Click **Start guided demo**. Review the prewritten voice-note brief and click **Confirm brief & inspect sources**.
2. Open **Inspect sources and research gaps**. These are real recorded vendor excerpts, not fresh research. Review the three audience hypotheses.
3. Open **Add explicit quant inputs**, then click **Use illustrative demo assumptions**. This explicitly fills eight sample inputs with 0.50. Click **Confirm audiences & run assessment**.
4. The real deterministic calculation returns **0.500**. Evidence coverage stays **0/8**, and the commercial outlook stays **insufficient evidence**: these sample inputs do not establish demand.
5. Open **Compare**, click **Load the demo comparison**, then **Compare with baseline**. Switching ease changes from 0.50 to 0.90; the index becomes **0.540**, a **+0.040** change. This is model sensitivity, not a success-probability increase.
6. Click **Save comparison** to retain both runs locally. Reload and choose the saved assessment to replay them. **Export JSON** downloads a portable copy.

The six stress tests are authored rules, not LLM or MiroFish agents. Custom ideas currently support note-taking and personal productivity only. Their live mode fetches a limited catalogue of vendor pages; it needs an internet connection. Unsupported categories show an explanation instead of a generic empty report.

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
