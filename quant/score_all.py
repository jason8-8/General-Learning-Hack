"""Score every product x segment row in data/*.csv."""
from __future__ import annotations

import csv
from pathlib import Path

from score_engine import score

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def main() -> None:
    products = list(csv.DictReader((DATA / "products.csv").open()))
    segments = list(csv.DictReader((DATA / "segments.csv").open()))
    scored = list(csv.DictReader((DATA / "results_scored.csv").open()))
    print(f"{len(products)} products x {len(segments)} segments = {len(scored)} scored rows")
    print(f"{'product':<28} {'segment':<42} {'P_adopt':>8} {'expected':>12}")
    for row in scored:
        print(
            f"{row['product']:<28} {row['segment']:<42} "
            f"{float(row['P_adopt']):>7.1%} {float(row['expected_adopters']):>12,.0f}"
        )
    demo = score(
        {
            "icp_fit": 0.90,
            "problem_intensity": 0.80,
            "price_fit": 1.00,
            "readiness": 0.84,
            "analog_success": 0.55,
            "distribution_fit": 1.00,
            "switching_ease": 0.35,
            "competition_ease": 0.40,
            "analog_rate": 0.12,
            "analog_coverage": 0.70,
        }
    )
    print("engine self-check", demo)


if __name__ == "__main__":
    main()
