"""Route 4: dedicated exact-Algorithm-3 counterexample search."""

from __future__ import annotations

import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent


def stationarity(iterations: int, step: float) -> float:
    base = abs(1.0 - 2.0 * step)
    decay = (
        0.0
        if base == 0.0
        else math.exp(2.0 * iterations * math.log(base))
    )
    return 4.0 * decay + 2.0 * step / (1.0 - step) * (1.0 - decay)


def minimize_step(iterations: int) -> tuple[float, float]:
    lower = 1e-15
    upper = 0.499999999999
    ratio = (math.sqrt(5.0) - 1.0) / 2.0
    left = upper - ratio * (upper - lower)
    right = lower + ratio * (upper - lower)
    left_value = stationarity(iterations, left)
    right_value = stationarity(iterations, right)
    for _ in range(160):
        if left_value < right_value:
            upper, right, right_value = right, left, left_value
            left = upper - ratio * (upper - lower)
            left_value = stationarity(iterations, left)
        else:
            lower, left, left_value = left, right, right_value
            right = lower + ratio * (upper - lower)
            right_value = stationarity(iterations, right)
    step = (lower + upper) / 2.0
    return stationarity(iterations, step), step


def first_hit(epsilon: float) -> tuple[int, float, float]:
    lower = 0
    upper = 1
    while minimize_step(upper)[0] > epsilon**2:
        upper *= 2
    while lower + 1 < upper:
        middle = (lower + upper) // 2
        if minimize_step(middle)[0] <= epsilon**2:
            upper = middle
        else:
            lower = middle
    value, step = minimize_step(upper)
    return upper, step, value


def main() -> int:
    raw = json.loads((HERE / "raw_results.json").read_text(encoding="utf-8"))
    maximum_delta = 0.0
    ratios: list[float] = []
    for expected in raw["search"]:
        epsilon = float(expected["epsilon"])
        work, step, value = first_hit(epsilon)
        if work != int(expected["minimum_total_work"]):
            raise AssertionError("Gaussian first-hit work changed")
        maximum_delta = max(
            maximum_delta,
            abs(step - float(expected["optimizing_outer_step"])),
            abs(value - float(expected["stationarity_at_first_hit"])),
        )
        ratios.append(work / epsilon**-4)
    if maximum_delta > 1e-12:
        raise AssertionError("raw falsification-search regression changed")
    falsified = any(ratio > 1.0 for ratio in ratios)
    output = {
        "route": 4,
        "status": (
            "UNEXPECTED_FALSIFICATION"
            if falsified
            else "FALSIFICATION_NOT_ESTABLISHED"
        ),
        "assumptions_audited": [1, 2, 3, 4],
        "exact_algorithm": "Algorithm 3 Gaussian one-step ULA family",
        "epsilon_count": len(ratios),
        "minimum_work_to_epsilon_inverse_fourth_ratio": min(ratios),
        "maximum_work_to_epsilon_inverse_fourth_ratio": max(ratios),
        "reason": (
            "this faithful family remains within the claimed epsilon^-4 "
            "upper order and is not a counterexample"
        ),
        "missing_capability": (
            "a faithful direct-product entropy-DRO embedding that combines "
            "the stochastic outer lower bound with unavoidable inner work"
        ),
    }
    print(json.dumps(output, sort_keys=True))
    return 0 if falsified else 1


if __name__ == "__main__":
    raise SystemExit(main())
