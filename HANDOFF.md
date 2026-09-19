# GL Hack: handoff for Claude Code

Rewritten 19 Sep 2026, against `General-Learning-Hack-main1.zip`. Design switched to black and green the same evening. Read this whole file before touching code. It replaces the earlier handoff.

## 0. The one-minute version

- **Deadline.** Sunday 20 Sep 2026, 10:00 HKT. About 17 hours from now. No extensions.
- **What judges see.** A 120-second video with a working prototype and a 90-second live pitch. They never open the repo. Build only what those two need.
- **What the product is.** Enter an idea, an audience and a price. Get an assessment you can inspect: candidate buyers, alternatives, adoption factors, one finding with evidence. Change one assumption. Compare to the baseline.
- **How it is split.** Two systems.
  - **Fast path** (built): deterministic scorer. Instant. It owns the number.
  - **Slow path** (not built): a two-segment reaction split (in-market buyer vs skeptic) from persona calls, plus a kill objection. It streams into the same screen. Pre-cache it for both demos.
- **Where the project is.** The quant model works and is frozen. The repo says "do not deepen it." The evidence pack, the reaction layer and the app do not exist yet. That is the work.
- **The one new risk.** P is not monotonic in price for some segments. Cutting price can lower P (section 12, issue 1). Script the on-camera edit around it.
- **What you get here.** 10 bundle files, listed with their repo paths in section 17.
  - `HANDOFF.md`: this file.
  - `CLAUDE.md`: standing rules for Claude Code. Copy to the repo root.
  - `scorer.js`: the fast path, ported from Python, verified identical. Has `compareRows` and `suggestAudience`.
  - `check_parity.py`: proves `scorer.js` matches `product/quant/score_engine.py`. Works on the new and old repo layouts.
  - `mockup_standalone.html`: the clickable mockup as one file, black and green. Double-click to open in any browser. Use this one to look at the design.
  - `mockup_Main.dc.html`: the same mockup as editable source. It needs the Design canvas runtime (`support.js`) beside it, so it shows blank if opened directly.
  - `brand/colors.md`, `type.md`, `usage.md`, `logo.svg`: the new black and green brand. They replace the repo's navy and teal files.

## 1. What changed since the last handoff

| Topic | Before | Now |
|---|---|---|
| Input | Company profile (my late proposal, never in the repo) | Idea, audience, price, geography. This is what `product/BUILD.md` and `pitch/video.md` lock |
| Runtime | Assumed a server, hosted somewhere | Laptop only. No account, upload or infra. Demo must run cold |
| Results CSV | Stale | Regenerated. `score_all.py` matches the table in section 6 |
| README | Contradicted the numbers | Fixed. Best fit for voice notes is now "HK young professionals 22.1%" |
| Repo layout | `quant/`, `data/` at root | Everything under `product/`. Also `pitch/`, `research/`, `discussion/`, `brand/` |
| Deadline plan | 10:00 to 13:00 round window | Deadline is 10:00 HKT Sunday. After 10:00 there may be no time to write the 90 s |
| Brand | Mine (serif and terracotta), then the repo's navy and teal | **Black and green, digital.** JetBrains Mono, one typeface. Replaces the repo's `brand/` files (your call, 19 Sep evening) |
| Compare | Price and channel | One variable per rerun: **price or audience** |
| Evidence | Illustrative source chips | Cached pack. Each finding needs source, date, observation, inference, limit |

**Kept from before, now post-hack:** the company-profile intake, URL or PDF pre-fill, and the "next move" three-card screen. They are not in the video flow. Section 15 asks you to confirm.

## 2. What the two artifacts must show

**Video, 120 s** (`pitch/video.md`). 90 s product, 30 s wrapper.

| Time | On screen | Say |
|---|---|---|
| 0 to 10 | Slide 1, promise | Enter an idea. Assess its commercial potential. |
| 10 to 20 | Form: idea, audience, price, geography visible. Run. | This is all we assume. |
| 20 to 45 | Buyers, alternatives, adoption factors | One useful finding. Candidates, not customers. |
| 45 to 60 | Evidence panel for that finding | Source, date, observation, inference, limit. |
| 60 to 80 | Change **price or audience**. Compare to baseline. | What moved, what did not, what is still unknown. |
| 80 to 90 | Slide 2, learning | What changed. What to test next in the real world. |
| 90 to 105 | Context | Founders testing a pitch. VCs scanning an early idea. |
| 105 to 120 | Stack and limits | Actual tools used. Cached evidence labelled. No success probability. |

**Pitch, 90 s** (`pitch/slides.md`). Two slides, about 20 s. The rest is talking over the product. Point at: two named segments with sources, a split of reactions (not an average), one `P(adopt)` labelled as a heuristic. No architecture tour. Slide 2 needs "Observed change" from the recorded run and one real next test.

**Must be true on camera** (`product/BUILD.md`)

1. The form records idea, audience, price, geography.
2. The assessment shows buyers, alternatives, adoption factors.
3. One click opens source, date, observation, inference, limit.
4. Editing price **or** audience keeps the baseline and explains the delta.
5. Failures are visible. Cached evidence is labelled.

**Recording rules**

- Change one variable on the rerun.
- Cached evidence stays labelled "cached" with a date.
- If the assessment fails, do not pass a frozen screenshot off as a live compare.
- A score is a **heuristic**. Never "chance this startup works." No accuracy percentage at the close.
- Synthetic personas are hypotheses, not proof of demand.
- Use the student and corporate examples only if the recorded run really produces those numbers.

**Cut order if late** (`BUILD.md`): live retrieval, then extra segments, then the on-screen score, then anything outside the 80-second product block.

## 3. Product definition

**Predicts:** P(a unit in a segment adopts the product within 12 months). Unit = a person for B2C, a firm for B2B. It is not P(startup succeeds). Expected adopters = universe × P. That is a planning number, not a revenue forecast. Do not sum or compare expected adopters across B2C and B2B rows.

**Input:** four fields. Idea (text), audience (one of 5 segments), price per month, geography. Geography follows the audience in v1 (Hong Kong or APAC). The mockup's "This is all we assume" card shows exactly these four.

**Output, in the order the video shows it**

1. **Candidate buyers:** P per segment, yours vs best. Label "candidates, not customers."
2. **Alternatives buyers use:** nearest analogs from `analogs.csv` with price and proxy rate.
3. **Adoption factors:** the eight features ranked by points lost, tagged Lever or Fixed.
4. **One finding** plus a button to its evidence card.
5. **Reaction split:** buyer vs skeptic clusters and a kill objection (slow path).
6. **Compare:** baseline vs edit, what moved, what did not, what is still unknown.
7. **Learning:** observed change and one real-world next test.

## 4. Architecture: two systems, laptop edition

```
 Browser (fast path, no network, <100 ms)            Local Python process (slow path)
 ┌──────────────────────────────────────┐            ┌──────────────────────────────────┐
 │ form: idea, audience, price, geo     │            │ load frame: buyer + skeptic      │
 │ scorer.js -> P per segment           │  request   │ draw N personas from templates   │
 │ limiting factors + price/audience    │ ─────────► │ one Claude call per persona      │
 │ move, compare, evidence cards        │            │ cluster, pick kill objection     │
 │ reaction bars grow as events arrive  │ ◄───────── │ cache by profile hash            │
 └──────────────────────────────────────┘    SSE     └──────────────────────────────────┘
```

**Rules that keep them consistent**

- The number comes only from the fast path. The slow path never computes or changes P.
- One weights file feeds both sides: `product/quant/weights.yaml`. `scorer.js` holds a copy. `check_parity.py` catches drift.
- If the user edits price or audience after a run, the fast path updates instantly. Reactions get a "based on the earlier inputs" tag and a "Re-run reactions" button. Never auto re-run.
- If the slow path is down, the fast path still renders. Reactions show "unavailable." A visible failure is a rule, not a bug.
- **Pre-cache both demos.** Run each once for real, store the result as JSON, label it "cached run, date." The video and the pitch never wait on an API. The app replays the cache with the same streaming animation, and the label must stay visible.
- Cache by hash of (idea, audience, price, geography, weights version). LLM reactions are stable only through the cache. Do not call them deterministic.
- Text from any fetched page that flows into a persona prompt is untrusted data, never instructions.
- `.env` holds the API key and is gitignored. No key means cache-only mode. The app must start without one.

**Suggested stack (confirm in section 15):** one FastAPI app (add `fastapi`, `uvicorn`, `anthropic` to `requirements.txt`) that serves a static front end and the SSE endpoint. Front end is plain HTML and JS that loads `scorer.js`. No build step. `python product/app/server.py` starts it cold. The repo's Python is `pandas` and `openpyxl` only, so this is a small addition.

**Endpoints**

- `POST /api/jobs` with `{ idea, audienceId, price, geo, personas?: 40, seed? }` returns `202 { jobId, profileHash, cached }`.
- `GET /api/jobs/:id/events` (SSE): `progress { answered, total }`, `clusters { answered, clusters:[{ id, label, role, count }] }`, `objection { clusterId, text, count }`, `done { profileHash, weightsVersion, cached, ranAt }`, `error { code, message }`.
- `GET /api/jobs/:id`: latest snapshot (polling fallback).

## 5. Repo map (the new zip)

| Path | What it is | State |
|---|---|---|
| `README.md` | Deadline, pitch line, demo table, run commands | Current |
| `pitch/video.md`, `slides.md`, `README.md` | The 120 s and 90 s beats | Current. Source of the flow |
| `product/BUILD.md` | Locked choices, on-camera musts, cut order | Current |
| `product/PROJECT.md` | Original brief (6-step pipeline) | Context. Some scope is cut |
| `product/architecture.spec.json` | Earlier architecture diagram spec | "Not a build commitment." Its "Scope by 14:00" card has no date |
| `product/quant/score_engine.py` | `score(features)`, `price_fit()`, reads `weights.yaml` | Done |
| `product/quant/score_all.py` | Prints stored results and a self-check | Runs. Numbers match |
| `product/quant/weights.yaml` | Weights, calibration, `frame_mix` 0.60 / 0.40 | Source of truth |
| `product/quant/WEIGHTS.md` | Reason for each weight | Done |
| `product/data/products.csv` | 2 demo products | Done |
| `product/data/segments.csv` | 5 segments: universe, WTP, usage, maturity, channel | Done |
| `product/data/analogs.csv` | 15 shipped lookalikes with proxy rates | Done |
| `product/data/results_scored.csv` | 10 rows, features and outputs | Regenerated |
| `product/sheets/00..08_*.csv`, `scripts/build_workbook.py` | Workbook tabs and builder | Works. Do not commit `.xlsx` |
| `research/decisions.md`, `evidence.md`, `market.md`, `aaru.md` | v1 locks, evidence rules, market notes | Current |
| `research/assets/README.md` | Lists images | The images are **not** in the zip. `aaru.md` links to missing files |
| `brand/` | Colors, type, usage, `logo.svg` | Navy and teal in the zip. **Replace** with the bundle's black and green files |
| `discussion/` | Three short decision notes | Context |
| `requirements.txt` | `pandas>=2.0`, `openpyxl>=3.1` | Add web deps if you take section 4 |

**Not in the repo, and needed:** the app, the evidence pack, the persona frame, the reaction layer, the cached runs. Everything in `product/` that runs today is quant and sheets.

**Run today**

```bash
python -m pip install -r requirements.txt
python product/quant/score_engine.py
python product/quant/score_all.py
python product/scripts/build_workbook.py
```

## 6. The scoring model

```
S       = Σ w_i · z_i                      (8 features, each in [0,1])
raw     = sigmoid(alpha + beta·S)
prior_w = analog_coverage · icp_fit · max(price_fit, 0.10)
blended = (1 − prior_w)·raw + prior_w·analog_rate
P       = blended · (0.30 + 0.70·price_fit)
if icp_fit < 0.12:  P *= 0.25
P       = clamp(P, 0.008, 0.40)
expected adopters = universe · P
```

alpha −3.60, beta 4.20. Weights are placeholder priors, not fitted. Change them only in `product/quant/weights.yaml`. `score_engine.py` keeps a fallback copy, so keep the two in sync.

| Feature | Weight | Lever or Fixed |
|---|---:|---|
| icp_fit (right buyer) | 0.24 | Fixed |
| problem_intensity | 0.18 | Fixed |
| price_fit | 0.12 | Lever |
| readiness | 0.12 | Fixed |
| distribution_fit (channel) | 0.12 | Lever |
| switching_ease | 0.10 | Lever |
| analog_success | 0.08 | Fixed |
| competition_ease | 0.04 | Fixed |

`price_fit(price, wtp)`: ratio = price / WTP. At or under 0.6 gives 1.0. From 0.6 to 1.0 it falls linearly to 0.55. From 1.0 to 2.0 it is `0.55·(2 − ratio)`. Above 2.0 it is 0.02. Price ≤ 0 gives 1.0. WTP ≤ 0 gives 0.

**Worked example** (voice notes × HK students at $6): S 0.830, raw 47.1%, price_fit 0.831, prior_w 0.765, blended about 22%, multiplier 0.882, P 19.5%.

**Current results** (`score_all.py` and `scorer.js` agree)

| Product | Segment | P(adopt) | Expected adopters |
|---|---|---:|---:|
| Voice notes ($6) | HK students | 19.5% | 74,088 |
| Voice notes | HK young professionals | 22.1% | 203,458 |
| Voice notes | HK family SMEs | 3.0% | 8,484 |
| Voice notes | HK mid-market | 3.0% | 539 |
| Voice notes | APAC consulting | 3.4% | 143 |
| Corporate agent ($480) | HK students | 0.8% | 3,040 |
| Corporate agent | HK young professionals | 0.8% | 7,360 |
| Corporate agent | HK family SMEs | 2.7% | 7,457 |
| Corporate agent | HK mid-market | 7.0% | 1,266 |
| Corporate agent | APAC consulting | 15.4% | 645 |

**Why young professionals beat students** (the README now states it, so be ready to explain it): students have a higher raw score (S 0.83 vs 0.67) but a price ratio of 0.75 ($6 against an $8 ceiling), so price_fit is 0.83. Young professionals have a $15 ceiling, so price_fit is 1.0. The price multiplier and the analog blend then favour them.

**Limiting-factor view** (implemented in `scorer.js`)

- Points lost = weight × (1 − score). Sort descending. Tag Lever or Fixed.
- Corporate agent × HK mid-market at $480: price fit 0.115, right buyer 0.091, problem intensity 0.076, switching ease 0.065.
- Points lost is not effect on P. Raising switching ease from 0.35 to 0.70 moves P only from 7.0% to 7.8%. So the "biggest change to test" callout runs real changes through the scorer.
- `suggestMove` (price only when `channelMoves: false`): candidate price = `max(floor(0.6 × WTP), ceil(0.3 × price))`. That gives price_fit 1.0 and never a cut deeper than 70%. Suggest only if it adds at least 0.5 points of P.
- `suggestAudience`: best other audience, only if it beats this one by 2 points.
- Corporate × mid-market: $150 gives 19.4%, $240 gives 15.4%. Corporate × HK students: no price move helps, so the callout suggests the audience move to APAC consulting, 0.8% to 15.4%.
- `compareRows(a, b)`: per-factor from, to, delta, moved (more than 0.005), unmoved. Powers the compare screen.

## 7. Feature derivation: the gap that blocks a real product

`results_scored.csv` stores the eight feature scores for two demos. No code produces them. I checked which are recoverable, against all 10 stored rows.

| Feature | Recovered rule | Status |
|---|---|---|
| price_fit | `price_fit(product price, segment WTP)` | Verified |
| distribution_fit | Product channel × segment `buys_via`: app_store row 1.0 / 0.45 / 0.15 for app_store / owner_direct / sales_led. sales_led row 0.15 / 0.45 / 1.0 | Inferred from the two demos. The owner_direct product row is unknown |
| switching_ease | 1 − product `switching_cost` | Verified |
| readiness | B2C product: segment `category_usage`. B2B product: segment `digital_maturity` | Verified |
| icp_fit | 0.08 when product buyer type ≠ segment buyer type (all 5 mismatches; under the `< 0.12` collapse). Otherwise hand-set | Mismatch rule only |
| problem_intensity | Hand-set per product × segment | Unknown |
| competition_ease | 0.52 (notes), 0.76 (corporate), product level | Unknown |
| analog_success, analog_rate, analog_coverage | Similarity-weighted from `analogs.csv` | Unknown. Coverage is 1.0 on every row, which looks like a bug |

The three hand-set features carry 0.46 of the total weight.

| Product | Segment | icp_fit | problem_intensity |
|---|---|---:|---:|
| Voice notes | HK students | 0.92 | 0.86 |
| Voice notes | HK young professionals | 0.55 | 0.48 |
| Voice notes | HK family SMEs | 0.08 | 0.10 |
| Voice notes | HK mid-market | 0.08 | 0.12 |
| Voice notes | APAC consulting | 0.08 | 0.15 |
| Corporate agent | HK students | 0.08 | 0.05 |
| Corporate agent | HK young professionals | 0.08 | 0.18 |
| Corporate agent | HK family SMEs | 0.22 | 0.20 |
| Corporate agent | HK mid-market | 0.62 | 0.58 |
| Corporate agent | APAC consulting | 0.90 | 0.80 |

**For the hack:** do nothing here. The video runs the two demos, and the mockup and `scorer.js` hold their stored features. Say "right buyer and problem intensity are set by the team" wherever the evidence card touches them. The mockup already does.

**After the hack** (recommendation, not locked): keep "no LLM in P(adopt)." Build frozen prior tables (segment × job-to-be-done). An LLM may draft them once, offline. A human reviews. Commit them as CSVs so runtime stays deterministic. Any new idea then adjusts them through fixed rules.

## 8. Evidence pack spec

The repo allows cached reviews, filings and forums, labelled "cached" with the retrieve date. **Nothing is cached yet.** The mockup's evidence screen is built only from repo data and says so ("Cached pack · repo data only", source `product/data/*.csv`, date "Not recorded"). That is honest but thin.

**Finding schema**

```json
{
  "id": "ev_001",
  "factor": "price_fit",
  "source_type": "review | filing | forum | pricing_page | repo_data",
  "source_url": "",
  "published_at": null,
  "retrieved_at": "2026-09-19",
  "observation": "what the source says, quoted or closely paraphrased",
  "inference": "what we conclude from it",
  "limit": "why that conclusion might be wrong",
  "cached": true
}
```

**Rules** (`research/evidence.md`): a finding needs a source, a date if known, an observation, an inference and a limit. Never invent a source. If there is no source, use `repo_data` or label the item "assumed" or "illustrative."

**Do this, in order**

1. Keep the repo-data findings the mockup builds (price vs WTP, analogs, channel, switching, readiness, hand-set scores). They are true and already carry limits.
2. Add 6 to 10 real cached items per demo product. Good targets: app-store reviews and pricing pages for the analogs already in `analogs.csv` (GoodNotes, Notability, Notion; Intercom Fin, Aircall, Agentforce, Microsoft 365 Copilot), and one or two forum threads on the objection you will call "kill." Fetch once at build time, save as JSON under `research/evidence/`, stamp `retrieved_at`.
3. Show at most one finding per click. The top-limiter finding opens first.

Live retrieval is first in the cut order. Do not build it.

## 9. Slow path spec (reactions)

**Locked** (`research/decisions.md`, `discussion/2026-09-19-segments.md`)

- Two qualitative segments in v1: **in-market buyer** and **skeptic or blocker**. Fallback mix **0.60 / 0.40**, labelled **assumed**. `weights.yaml` holds it as `frame_mix`. It is not used inside P(adopt).
- Joint trait network and media-diet loop are stretch. Do not build them. Do not put them in S.
- Output is a distribution plus tail objections. **No average.**
- Persistence is cut. Cohort lives in memory.

**Frame template** (one per role)

```json
{
  "role": "buyer",
  "label": "In-market buyer",
  "weight": 0.60,
  "weight_status": "assumed",
  "attributes": ["3 to 5 grounded traits"],
  "source_ids": ["ev_003"]
}
```

Do not sample age × income × tenure as independent columns. Draw persona rows from these templates.

**Layer link (proposed, undecided):** the buyer role inherits the best-scoring market segment for the chosen product. The five segments are the market layer. The two roles are the reaction layer.

**Persona call.** Input: segment template plus the product card (idea, price, audience). Output: short JSON `{ "stance": "try|maybe|no", "reason": "<= 25 words", "dealBreaker": "..." }`. Then one clustering call over all reasons: at most 5 labelled clusters, each answer assigned. **Kill objection** = the deal-breaker text from the most decisive small skeptic cluster. Write that rule down before building.

**Defaults.** 40 personas as the default, up to 200 as a cap. Concurrency limit. Low temperature. Seed recorded in the cache.

**Show on screen:** status (Streaming or Complete), "n of N personas," the 60 / 40 bar with "assumed," the five cluster bars, the kill objection last. Streaming is driven by real events. In the mockup a timer simulates it (200 answers over about 5 s, early counts wobble). **Do not ship the wobble.**

**Illustrative content warning.** The cluster labels, shares and kill-objection quotes in the mockup are made-up samples. The real ones must come from a real run.

## 10. UX spec: mockup v3, black and green

Published, private until shared: **https://claude.ai/artifact/2AgXrJ1MQhwG6dX24C3hLE** ("GL Hack Idea Validator Mockup," version 8, two boards: the mockup and the file list). Offline copy: `mockup_standalone.html`. Source: `mockup_Main.dc.html`. The screens and numbers are unchanged from v2. Only the look changed.

**Design tokens** (full table and contrast ratios in `brand/colors.md`)

| Token | Value | Use |
|---|---|---|
| Black | `#050805` | Page and slide background. 32 px grid backdrop in the UI at `rgba(61,255,138,0.045)` |
| Panel | `#0A110B` | Cards, inputs |
| Raised / Tint | `#101C12` / `#0C2214` | Callouts, selected rows |
| Rule / Rule strong | `#1E3A24` / `#2F6B3C` | Hairlines / chip borders. Borders only, never text |
| Green | `#3DFF8A` | Action, emphasis, buyer, headings, key numbers |
| Text / Muted | `#D9F7DF` / `#8DB89A` | Body / captions |
| On green | `#03100A` | Type on a green fill |

Type: **JetBrains Mono**, one typeface (Consolas in PowerPoint if it is missing). Labels are 12 px uppercase with a `> ` prefix. Corners 2 px. Borders 1 px. The skeptic role is a **hatch** (`repeating-linear-gradient(135deg, #8DB89A 0 3px, #1E3A24 3px 6px)`), the buyer role solid green. No third hue, no warning colors. Glow (`text-shadow: 0 0 14px rgba(61,255,138,0.35)`) only on the one hero number per screen. Logo: `brand/logo.svg`, a prompt and cursor.

The repo's own brand says navy, teal and Calibri (`brand/*`, README row). This design replaces it. Update the slides and the video to match, or the deck and the app will look like two products.

**Screens** (top bar: Idea, Assessment, Evidence, Compare, Next test)

1. **Idea.** Idea text, two demo chips, audience chips (5), price stepper and presets, "This is all we assume" card, **Assess**.
2. **Assessment.** Lands with the fast-path number and factors already there. Candidate buyers table, alternatives, "Scorecard heuristic" card, adoption factors ranked by points lost with Lever or Fixed tags, a "Biggest change to test" callout (price first, then audience), the streaming two-segment panel and the kill objection.
3. **Evidence.** Six findings. The one for the top limiter opens first. Each shows Source, Date, Observation, Inference, Limit.
4. **Compare.** A Price or Audience toggle. Only one changes. The other stays locked to the baseline. Baseline vs edit cards, factor table with deltas, panels "What moved," "What did not move," "Still unknown."
5. **Next test.** Observed change and one real-world next test, from the compare.

Accessibility: real buttons, `aria-pressed` on toggles, `aria-label` on icon-only buttons, 44 px targets (the buyer rows are 34 px in the mockup; raise them in the real UI), 4.5:1 text contrast.

## 11. What is verified and what is not

- **Verified.** `scorer.js` matches `product/quant/score_engine.py` exactly (max difference 0) on 8 price and channel scenarios. Run `python product/scripts/check_parity.py` from the repo root. Exit 0 means parity. Also verified against the old layout.
- **Verified in Node, not in a browser.** Every screen state of the mockup renders with no missing template field. That covers both demos, all 5 segments, all 6 evidence cards and both compare variables. Scorer numbers in the mockup equal section 6. Streaming counts sum to the number answered.
- **Browser check.** The black and green mockup was loaded in headless Chromium with the real Design runtime and clicked through: Idea, Assess, Evidence, Compare, Next test, and the corporate demo. No console errors. Layout fits at 1280 × 880 on every screen. The standalone file opens from a local path. Persona clusters, quotes and shares are illustrative.
- **Not done.** Weights validation. The plan in `WEIGHTS.md` is to hold out 20% of analog rows and report MAE against `proxy_rate`. Not needed for the pitch.

## 12. Known issues (fix or disclose before recording)

1. **P is not monotonic in price.** The analog blend weight `prior_w = coverage · icp_fit · max(price_fit, 0.10)` grows as price fit rises. The analog rate (about 0.12 to 0.14) is lower than the model's raw P for strong-fit segments, so a lower price can pull P down.
   - Voice notes × HK students: $6 gives 19.5%. $3 to $4.80 gives 17.2%. P rises with price from $5 to $17.
   - Corporate × APAC consulting: P rises with price from $490 to about $1,600.
   - Small blips: notes × young professionals near $31, corporate × family SMEs near $90, corporate × mid-market near $510.
   - **Safe on-camera edits** (P moves the intuitive way): corporate × mid-market, price $480 to $150 (7.0% to 19.4%) or $240 (15.4%); corporate × mid-market to APAC consulting (7.0% to 15.4%); voice notes × students to young professionals (19.5% to 22.1%).
   - **Unsafe:** voice notes × students, any price cut. Corporate × consulting, any price rise.
   - Options: (a) script around it and disclose (recommended, zero engine change); (b) set `prior_w = coverage · icp_fit`. That fixes most of it but changes the demo numbers (students 15.0%, mid-market 5.2%), and the README table would move. The repo says do not deepen quant. Decide in section 15.
2. **Analog coverage is 1.0 on every row**, so confidence reads 0.82 to 0.95 even for absurd pairs like a notes app × consulting firms. It should depend on how close the analogs are. Do not show "confidence" on camera.
3. **Price cliff at 2× WTP.** price_fit drops to 0.02, so `sheets/08_Sensitivity.csv` looks flat above $99 for family SMEs. Do not show that sheet.
4. **Hand-set features carry 0.46 of the weight** (section 7). Label them "set by the team" wherever they appear. Every limiting-factor claim is an estimate.
5. **B2C rows count people, B2B rows count firms.** Never compare adopters across them.
6. **Evidence pack is empty.** The mockup shows repo data only (section 8).
7. **Missing images.** `research/assets/` lists diagrams that are not in the zip. `aaru.md` links to them. Harmless for the demo. Fix or remove the links.
8. **Naming and small data.** `analogs.csv` row `PLAID` is described as "Plaud / AI note gadgets." Its `penetration` column is dropped by `sheets/05_Analogs.csv`.
9. **`architecture.spec.json`** says "Scope by 14:00" with no date. It is an earlier plan, not a commitment.
10. **Only 2 demo products and 5 segments exist.** The form is free text on the idea, but the scorer scores only the demos. Say so on camera ("this build runs two demo ideas"), or the free-text box is a lie.

**Resolved since last handoff:** stale `results_scored.csv`, README contradicting the numbers.

## 13. Build plan

Order by what the recorded run needs. Stop deepening quant. Sleep somewhere in here.

**P0: needed to record the video**

1. **Repo hygiene.** Copy the 10 bundle files to the paths in section 17. Edit the brand row in `README.md` to say black and green. Run `python product/scripts/check_parity.py`. Acceptance: exit 0.
2. **App shell, fast path only.** Static page from the mockup (section 10), brand tokens, `scorer.js` inline. Idea, Assessment, Evidence, Compare, Next test. Acceptance: editing price or audience updates every number in under 100 ms with no network. Compare changes exactly one variable and keeps the baseline.
3. **Evidence pack v0.** Repo-data findings plus 6 to 10 real cached items per demo (section 8). Every card shows source, date, observation, inference, limit. Cached items show "cached" and the date.
4. **Reaction layer v0.** Frame templates, persona call, clustering call, kill-objection rule (section 9). Run it once per demo with the real API. Save the result as cached JSON. Replay it with SSE-style streaming. Acceptance: app works with no API key and the cached label is visible.
5. **Failure states.** Slow path down shows "unavailable." Compare shows a visible error, never a stale screen.
6. **Script the run.** Pick the on-camera edit from the safe list in issue 1. Record. Fill slide 2 from the recorded run ("Observed change," "Next test").
7. **Write the 90 s pitch** and the stack line for 105 to 120 s. List only tools you really used.

**P1: only if time remains**

8. Live persona run (not cached) behind the same endpoint, with a concurrency limit.
9. Fix issue 1(b) if the team prefers an engine change. Re-run `score_all.py`, update the README table, re-run parity.
10. A lever tornado: bars ranked by actual change in P when each lever moves.
11. Remove the missing-image links.

**P2: post-hack**

12. Feature derivation as frozen CSV priors (section 7), an "unmapped segment" state, real analog coverage.
13. Company-profile intake and URL or PDF pre-fill.
14. Holdout validation against `proxy_rate`.
15. Third segment, joint trait network, media-diet loop.

## 14. Working rules

- Same inputs, same output. No LLM in the scoring path. The LLM fills a schema and writes persona reactions, nothing else.
- Change weights only in `product/quant/weights.yaml`. Keep `score_engine.py` fallback and `scorer.js` in sync. Run parity after any scoring change.
- Label every rate a proxy and every hand-set score "set by the team."
- Cached evidence carries "cached" and a date. Never invent a source.
- Do not fit weights on the two demo products.
- Do not add a joint trait network to S. Do not average the reactions.
- Do not deepen quant unless the pitch needs one different number.
- Never say "chance this startup works." Never close on an accuracy percentage.
- Design is black and green (`brand/colors.md`). One typeface. Skeptic is a hatch, never a second color.
- Do not commit `.xlsx`, `.env` or keys.

**How the user likes to work** (stated preferences): lead with the answer, short sentences, conclusion first with supporting bullets. Ask 2 or 3 short clarifying questions before non-trivial work if the request is ambiguous. Avoid AI clichés and heavy em-dash use.

## 15. Open decisions (need the user)

1. **Input.** Confirm the repo's idea, audience, price, geography form for the pitch, with the company-profile intake parked as post-hack. (Recommended.)
2. **Price quirk.** Script around it (recommended) or change `prior_w`? (Issue 1.)
3. **Evidence.** Who collects the 6 to 10 cached sources per demo, and are app-store reviews, pricing pages and forum threads acceptable to the team?
4. **LLM access.** Which model and API key the team has, and the budget for persona calls. Default 40 personas, cap 200.
5. **Stack.** FastAPI plus a static page (recommended), or a pure static page that replays cached runs only?
6. **Layer link.** Does the buyer role inherit the best-scoring market segment?
7. **On-screen score.** Show `P(adopt)` in the video, labelled a heuristic, or cut it? (`BUILD.md` cut order puts it third.)
8. **Free-text idea box.** Keep it while only two demos are scoreable, with a visible "demo ideas only" note? (Mockup does.)
9. **Design.** Black and green replaces the repo's navy and teal. Confirm the slides and the video use it too.

## 16. Paste into Claude Code

`CLAUDE.md` is in the bundle as a file. Copy it to the repo root. Its contents:

```markdown
# GL Hack: working notes
Read HANDOFF.md before any change. It has the architecture, the model spec, known issues and the build plan.

Deadline: Sun 20 Sep 2026, 10:00 HKT. Judges see a 2-minute video and a 90-second pitch, not code. Build only what that story needs.

Rules
- Deterministic scorer (product/quant/score_engine.py, product/web/scorer.js). No LLM in P(adopt).
- Weights live only in product/quant/weights.yaml. Keep score_engine.py fallback and scorer.js in sync.
- Run `python product/scripts/check_parity.py` after any scoring change. It must exit 0.
- Runs on a laptop. No account, upload or infra. App must start with no API key (cached mode).
- Cached evidence is labelled "cached" with a date. Never invent a source. Personas are hypotheses.
- Compare changes one variable: price or audience.
- Design: black and green, digital. Tokens in brand/colors.md. One typeface, JetBrains Mono (Consolas in slides). Skeptic is a hatch, not a second color.
- Do not deepen quant. Do not commit .xlsx or .env.

Style
- Lead with the answer. Short sentences. Ask a few clarifying questions when a request is ambiguous.
- Avoid AI clichés and heavy em-dash use.
```

First prompt to give Claude Code:

```
Read HANDOFF.md fully. Then do P0 items 1 and 2 only:
1) Copy the bundle files to the paths in section 17. Edit the brand row in README.md to say black and green. Run python product/scripts/check_parity.py and report the result.
2) Build the static fast-path app from mockup_standalone.html and mockup_Main.dc.html (section 10): Idea, Assessment, Evidence, Compare, Next test. Same look: brand/colors.md tokens, JetBrains Mono. Use scorer.js. Use repo-data evidence for now. No slow path yet.
Before you start, ask me anything unclear in section 15 that blocks these two items. Do not start the evidence pack or the reaction layer yet.
```

## 17. File list

Also published as the second board of the artifact.

**In the bundle: copy these into the repo (10)**

| Bundle file | Goes to | Action | What it is |
|---|---|---|---|
| `HANDOFF.md` | `HANDOFF.md` | ADD | Full brief: architecture, model spec, known issues, build plan, open decisions. |
| `CLAUDE.md` | `CLAUDE.md` | ADD | Standing rules Claude Code reads every session. |
| `scorer.js` | `product/web/scorer.js` | ADD | Fast path. Port of the Python engine, verified identical. |
| `check_parity.py` | `product/scripts/check_parity.py` | ADD | Fails if scorer.js and score_engine.py disagree. |
| `mockup_standalone.html` | `product/web/reference/mockup_standalone.html` | ADD | The design. Double-click to open in a browser. |
| `mockup_Main.dc.html` | `product/web/reference/mockup_Main.dc.html` | ADD | Editable source of the same mockup. Needs the Design runtime. |
| `brand/colors.md` | `brand/colors.md` | REPLACE | Black and green tokens and contrast ratios. |
| `brand/type.md` | `brand/type.md` | REPLACE | JetBrains Mono, sizes and weights. |
| `brand/usage.md` | `brand/usage.md` | REPLACE | Do and do not. Skeptic is a hatch, not a color. |
| `brand/logo.svg` | `brand/logo.svg` | REPLACE | Prompt-and-cursor mark. |

**Already in the repo (44 files, by folder)**

| Folder | Files | Action | Note |
|---|---|---|---|
| `/` | README.md · requirements.txt · .gitignore | EDIT | 3 files. README: change the brand row to black and green. requirements: add web deps if you take the FastAPI stack. |
| `brand/` | README.md · colors.md · type.md · usage.md · logo.svg | REPLACE | 5 files. Four are replaced from the bundle. README stays. |
| `pitch/` | README.md · video.md · slides.md | READ FIRST | 3 files. The 120 s video and 90 s pitch beats. This is the flow. |
| `product/` | README.md · PROJECT.md · BUILD.md · architecture.spec.json | READ | 4 files. BUILD.md has the locks and the on-camera musts. |
| `product/quant/` | score_engine.py · score_all.py · weights.yaml · WEIGHTS.md | READ | 4 files. Change weights only in weights.yaml. |
| `product/data/` | analogs.csv · products.csv · segments.csv · results_scored.csv | READ | 4 files. Regenerated, matches the demo table. |
| `product/sheets/` | 00_Cover to 08_Sensitivity (9 CSVs) · README.md | READ | 10 files. Workbook tabs. Do not show 08. |
| `product/scripts/` | build_workbook.py | READ | 1 file. check_parity.py lands beside it. |
| `research/` | README.md · aaru.md · decisions.md · evidence.md · market.md · assets/README.md | READ | 6 files. Evidence rules live in evidence.md. assets/ images are missing. |
| `discussion/` | README.md · 2026-09-19-judging.md · -segments.md · -weights.md | READ | 4 files. Why the locks are what they are. |

**Claude Code creates (11)**

| File | Phase | What it is |
|---|---|---|
| `product/web/index.html` | P0-2 | App shell from the mockup. Five screens. |
| `product/web/app.js` | P0-2 | State, compare logic, streaming replay. Loads scorer.js. |
| `product/web/style.css` | P0-2 | Tokens from brand/colors.md. |
| `research/evidence/notes.json` | P0-3 | Cached evidence for voice notes. Source, date, observation, inference, limit. |
| `research/evidence/corp.json` | P0-3 | Cached evidence for the corporate agent. |
| `product/data/frame.json` | P0-4 | Buyer and skeptic templates. 60 / 40, marked assumed. |
| `product/scripts/run_personas.py` | P0-4 | One real run per demo. Writes the cache. |
| `product/app/server.py` | P0-4 | FastAPI. Serves product/web and the SSE stream. Starts with no key. |
| `product/cache/notes.json` | P0-4 | Cached reaction run, dated and labelled. |
| `product/cache/corp.json` | P0-4 | Cached reaction run, dated and labelled. |
| `.env` | P0-4 | Local only. API key. Gitignored. Never commit. |

**Order of work**

1. Copy the 10 bundle files to the paths above.
2. Edit one line in README.md: the brand row says black / green.
3. Run  python product/scripts/check_parity.py  and expect exit 0.
4. Paste the first prompt from HANDOFF.md section 16 into Claude Code.
# Design

Taken from [Impeccable](https://github.com/pbakaus/impeccable) where it helps. Not their gold/lacquer system. Not their command set.

Product truth stays in `product/PROJECT.md`. This file is look only.

## Direction

Dark mineral field. One phosphor hit. Technical geometry. Quiet chrome.

Void is tinted green-black, never `#000`. Phosphor is the only saturated color on a frame. Dim is a surface lift, not a second brand color.

Feel like a scorecard on a terminal that someone turned the brightness down on — not a neon poster, not a purple SaaS landing page.

## Tokens

Source: [colors.md](colors.md), [type.md](type.md). Do not invent a third green.

| Role | Token | Notes |
| --- | --- |
| Page ground | Void `#0B0F0C` | Tinted. Detector: no pure black |
| Raised surface | Dim `#163226` | One lift. Not a card inside a card |
| Accent | Phosphor `#3DFF8A` | Number, live mark, one CTA |
| Title | White `#F4FBF6` | Headlines on void |
| Body | Fog `#C8D5CC` | Body on void only |
| Meta | Mute `#7A9586` | Eyebrows, sources |
| Rule | Rule `#1F3A2E` | Hairline. No glow as atmosphere |

Phosphor text sits on Void or Dim. Never Fog text on Phosphor. Never gray on a colored fill.

## Type

Space Grotesk + Space Mono. That already clears Impeccable’s “overused font” rule (no Inter, no Arial-as-brand).

Ramp — pick a step, do not invent sizes:

| Step | Use |
| --- | --- |
| 12 | Caption, source, table chrome |
| 14 | UI body |
| 18–22 | Slide body |
| 20 | UI heading |
| 32–40 | Slide title |
| Mono 12–18 | `P(adopt)`, IDs, citations |

Eyebrows: Space Mono, tracked, Mute. Titles stay Grotesk. Do not title in Mono.

## Surface

- One raised plane per region. Split with hairlines, not nested Dim boxes.
- Radius 8px on the mark and controls. No 16px “friendly card.”
- Borders are Rule hairlines. No drop shadow, no dark outer glow, no purple-to-blue gradient.
- Group 2–3 facts as a row on Void, not a card of cards.

## Motion

If anything moves: short, linear or ease-out. No bounce. No elastic. No matrix rain.

## Do / don’t

Do: void field, phosphor on one number, Fog body, Mute meta, one mark, short lines.

Don’t (Impeccable detectors that apply here):

- Inter / Arial / system-sans as the brand face
- Pure `#000` or raw gray ramp
- Gray-on-color (Fog or Mute on Phosphor)
- Gradient text
- Nested cards
- Icon tiles above every heading
- Side-tab candy borders
- Dark glow as the background
- Bounce easing
- “Probability of success” as a badge
