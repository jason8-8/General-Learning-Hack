# Weight rationale

Placeholders. Sum to 1.00. Not fitted. Change only in `weights.yaml`.

| Feature | Weight |
| --- | ---: |
| icp_fit | 0.24 |
| problem_intensity | 0.18 |
| price_fit | 0.12 |
| readiness | 0.12 |
| analog_success | 0.08 |
| distribution_fit | 0.12 |
| switching_ease | 0.10 |
| competition_ease | 0.04 |

Calibration: α = −3.60, β = 4.20, floor 0.008, ceil 0.40.

Price and analog are smaller in S because the engine already applies them again on P. Full argument: `discussion/2026-09-19-weights.md`.
