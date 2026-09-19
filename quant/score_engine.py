"""Deterministic P(adopt | segment, product) engine.

Same inputs → same output. No LLM in the scoring path.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent

WEIGHTS = {
    "icp_fit": 0.22,
    "problem_intensity": 0.16,
    "price_fit": 0.16,
    "readiness": 0.14,
    "analog_success": 0.14,
    "distribution_fit": 0.10,
    "switching_ease": 0.05,
    "competition_ease": 0.03,
}
CALIB_A = -3.80
CALIB_B = 4.40
P_FLOOR = 0.008
P_CEIL = 0.45


def sigmoid(z: float) -> float:
    z = max(min(z, 20.0), -20.0)
    return 1.0 / (1.0 + math.exp(-z))


def price_fit(price: float, wtp: float) -> float:
    if wtp <= 0:
        return 0.0
    if price <= 0:
        return 1.0
    ratio = price / wtp
    if ratio <= 0.6:
        return 1.0
    if ratio <= 1.0:
        return 1.0 - 0.45 * (ratio - 0.6) / 0.4
    if ratio <= 2.0:
        return 0.55 * (2.0 - ratio)
    return 0.02


def score(features: dict) -> dict:
    missing = [k for k in WEIGHTS if k not in features]
    if missing:
        raise KeyError(f"missing features: {missing}")
    S = sum(WEIGHTS[k] * float(features[k]) for k in WEIGHTS)
    raw = sigmoid(CALIB_A + CALIB_B * S)
    analog_r = float(features.get("analog_rate", raw))
    cov = float(features.get("analog_coverage", 0.0))
    icp = float(features["icp_fit"])
    pf = float(features["price_fit"])
    prior_w = cov * icp * max(pf, 0.10)
    blended = (1.0 - prior_w) * raw + prior_w * analog_r
    P = blended * (0.30 + 0.70 * pf)
    if icp < 0.12:
        P *= 0.25
    P = max(P_FLOOR, min(P_CEIL, P))
    return {"S": S, "raw_p": raw, "P_adopt": P}


if __name__ == "__main__":
    print("weights sum", sum(WEIGHTS.values()))
    demo = {
        "icp_fit": 0.90,
        "problem_intensity": 0.80,
        "price_fit": 0.85,
        "readiness": 0.84,
        "analog_success": 0.50,
        "distribution_fit": 1.00,
        "switching_ease": 0.35,
        "competition_ease": 0.40,
        "analog_rate": 0.10,
        "analog_coverage": 0.70,
    }
    print(score(demo))
