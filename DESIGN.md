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
