# Design

Taken from the [Impeccable skill](https://github.com/pbakaus/impeccable) where it helps. Not their gold/lacquer world. Not their 24 commands, live mode, or detector binary.

Product truth stays in `product/PROJECT.md`. This file is look only.

## What we actually pulled

The skill is a method, not a palette. Useful pieces:

1. **Split files.** `PRODUCT.md` = durable product truth. `DESIGN.md` = look. We already had that split.
2. **Mode before decoration.** Persuade / Operate / Read / Experience. Slides are Persuade. The laptop demo is Operate. Do not style the demo like a landing page.
3. **Craft floor.** Contrast, states, measure, copy, one inspect-and-fix pass. Then stop.
4. **Detector catalog.** The slop list is the useful part of the engine. The engine itself is not.
5. **Quieter / distill / typeset / layout.** Those four verbs are the refinement loop. The other twenty commands are for a design team with time.

Left on the table on purpose: `/live`, `/generate`, `/overdrive`, `/delight`, kinpaku tokens, hook wiring, native iOS/Android variants.

## Mode

| Surface | Mode | Consequence |
| --- | --- | --- |
| 90s slides | Persuade | Two slides. Short lines. One number. |
| Video | Persuade → Operate | Form, then the split. |
| Laptop demo | Operate | Density, tabular figures, states. Not a hero. |

Operate surfaces do not grow eyebrows, icon tiles, or a marketing kicker.

## Direction

Dark mineral field. One phosphor hit. Technical geometry. Quiet chrome.

Void is tinted green-black, never `#000`. Phosphor is the only saturated color on a frame (~10% of the pixels). Dim is a surface lift, not a second brand.

Scorecard with the brightness down. Not neon. Not purple SaaS.

## Tokens

Source: [colors.md](colors.md), [type.md](type.md). Do not invent a third green.

| Role | Token | Notes |
| --- | --- | --- |
| Page ground | Void `#0B0F0C` | Tinted |
| Raised surface | Dim `#163226` | One lift |
| Accent | Phosphor `#3DFF8A` | Number, live mark, one CTA |
| Title | White `#F4FBF6` | Headlines on void |
| Body | Fog `#C8D5CC` | Body on void only |
| Meta | Mute `#7A9586` | Sources, table chrome |
| Rule | Rule `#1F3A2E` | Hairline. No glow |

Phosphor text sits on Void or Dim. Never Fog or Mute on Phosphor.

## Type

**Space Grotesk** + **Space Mono**.

Honest note from the skill: their 2026 slop list now flags Space Grotesk next to Inter and Geist. We still keep it. The lock is already on camera, the pair with Space Mono is the identity, and swapping faces the night before the pitch is costume. Do not add a third family to “fix” that detector.

Ramp — pick a step:

| Step | Use |
| --- | --- |
| 12 | Caption, source, table chrome |
| 14 | UI body |
| 18–22 | Slide body |
| 20 | UI heading |
| 32–40 | Slide title |
| Mono 12–18 | `P(adopt)`, IDs, citations |

Rules from `typeset`:

- Body measure 45–75ch. Slides stay shorter.
- Light-on-dark gets a little more leading and tracking, not crushed letters. Tracking floor −0.04em.
- Size steps must be obvious. Adjacent roles cannot sit within 1.25×.
- Tabular figures on every number in the scorecard.
- Titles stay Grotesk. Mono is for measurement, not atmosphere.

## Surface

- One raised plane per region. Split with hairlines, not nested Dim boxes.
- Radius 8px on the mark and controls.
- Border *or* elevation, never both. We use hairlines. No shadow.
- Group 2–3 facts as a row on Void.
- Tight groups, generous gaps between groups. More space above a heading than below it.
- Theme selection, caret, focus ring, and scrollbar from this palette. Browser chrome is part of the kit.

## Craft floor (verify before ship)

- Contrast: body ≥ 4.5:1, large type ≥ 3:1.
- States that exist in the demo: default, loading, empty, error, disabled. Hover if there is a pointer.
- Copy uses the product’s words. Controls name the action. Errors name the problem and the next move.
- One authored motion moment, ease-out, already-visible default. No pulse-dot theater.
- Real content in the frame. No sparklines standing in for the split.

## Copy

From their slop list, applied to pitch language we already use:

- Name the job: idea in, cohort out, clusters not an average.
- Do not stack “Not X. A Y.” more than once.
- Do not badge `P(adopt)` as success.
- Do not number slide sections `01 / 02` as decoration. A page index is fine if it is navigation.

## Motion

Short. Ease-out. No bounce, elastic, matrix rain, pulsing live dots, or fake caret in a hero.

## Slop that still applies

- Nested cards
- Side-tab / thick accent borders
- Gradient text
- Radial phosphor halo behind the title
- Glow shadows
- Icon tile above a heading
- Decorative eyebrow / pill chip above a hero line
- Hero-metric template used as *page structure* (the live `P(adopt)` number is the product; do not repeat that shape on every panel)
- Inter / Roboto / Geist / Plus Jakarta as extras
- Cream/beige “tasteful AI” paper
- Purple-to-cyan palette
- Hairline plus wide soft shadow
- Grid-line wallpaper
- Auto marquee
- Marketing verbs: streamline, supercharge, next-generation

## Refinement loop

If a frame feels wrong, run one verb, not all of them:

| Verb | When |
| --- | --- |
| Distill | Too many boxes |
| Quieter | Too much phosphor or glow |
| Typeset | Hierarchy is flat |
| Layout | Rhythm is even and dead |
| Clarify | Labels do not say the action |
| Polish | Last pass, then stop |

Do not run Overdrive or Delight on this pitch.

## Still not extracted (and why)

| Skill piece | Why it stays out |
| --- | --- |
| `/live` + `/generate` | Needs their browser harness |
| 61-rule detector binary | We copied the names that fire on our kit |
| `/init` interview | `product/PROJECT.md` already holds audience and constraints |
| Native iOS/Android refs | Not the demo |
| Kinpaku component kit | Different product |
| Persona critique cast (Alex/Jordan/Sam) | We have buyer vs skeptic |
