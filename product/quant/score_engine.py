"""Deterministic P(adopt | segment, product) engine.

Same inputs → same output. No LLM in the scoring path.
Weights live in weights.yaml.
"""
from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent

WEIGHTS = {
    "icp_fit": 0.24,
    "problem_intensity": 0.18,
    "price_fit": 0.12,
    "readiness": 0.12,
    "analog_success": 0.08,
    "distribution_fit": 0.12,
    "switching_ease": 0.10,
    "competition_ease": 0.04,
}
CALIB_A = -3.60
CALIB_B = 4.20
P_FLOOR = 0.008
P_CEIL = 0.40


def _load_yaml_overrides() -> None:
    path = ROOT / "weights.yaml"
    if not path.exists():
        return
    section = None
    weights: dict[str, float] = {}
    calib: dict[str, float] = {}
    for raw in path.read_text().splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.startswith("weights:"):
            section = "weights"
            continue
        if line.startswith("calibration:"):
            section = "calibration"
            continue
        if line.startswith("frame_mix:") or line.startswith("notes:"):
            section = None
            continue
        if section and ":" in line and line.startswith("  "):
            key, val = line.strip().split(":", 1)
            try:
                num = float(val.strip())
            except ValueError:
                continue
            if section == "weights":
                weights[key] = num
            elif section == "calibration":
                calib[key] = num
    global WEIGHTS, CALIB_A, CALIB_B, P_FLOOR, P_CEIL
    if weights:
        WEIGHTS = weights
    if "alpha" in calib:
        CALIB_A = calib["alpha"]
    if "beta" in calib:
        CALIB_B = calib["beta"]
    if "p_floor" in calib:
        P_FLOOR = calib["p_floor"]
    if "p_ceil" in calib:
        P_CEIL = calib["p_ceil"]


_load_yaml_overrides()


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
    print("weights", WEIGHTS)
    print("weights sum", round(sum(WEIGHTS.values()), 6))
    print("calib", {"alpha": CALIB_A, "beta": CALIB_B, "floor": P_FLOOR, "ceil": P_CEIL})
