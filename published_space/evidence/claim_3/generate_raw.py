"""Standard-library calibration of the best constant-step last iterate."""

from __future__ import annotations

import json
import math


EPSILONS = (0.2, 0.1, 0.05, 0.02, 0.01)


def stationarity(iterations: int, step: float) -> float:
    decay_base = abs(1.0 - 2.0 * step)
    decay = (
        0.0
        if decay_base == 0.0
        else math.exp(2.0 * iterations * math.log(decay_base))
    )
    return 4.0 * decay + step / (1.0 - step) * (1.0 - decay)


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


def first_hit(epsilon: float) -> dict[str, float | int]:
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
    minimum, step = minimize_step(upper)
    analytic_lower_bound = (
        3.0
        / (32.0 * epsilon**2)
        * math.log(4.0 / epsilon**2)
    )
    return {
        "epsilon": epsilon,
        "minimum_iterations": upper,
        "optimizing_step": step,
        "stationarity_at_first_hit": minimum,
        "analytic_iteration_lower_bound": analytic_lower_bound,
        "S_times_epsilon_squared": upper * epsilon**2,
        "normalized_by_log": (
            upper * epsilon**2 / math.log(1.0 / epsilon)
        ),
    }


def main() -> int:
    output = {
        "schema_version": 1,
        "generator": (
            "exact recurrence, golden-section step search, "
            "doubling and binary first-hit search"
        ),
        "instance": {
            "theta_0": 1.0,
            "L_Phi": 2.0,
            "gradient_variance": 1.0,
            "delta_sample": 0.0,
        },
        "calibrated_first_hits": [first_hit(eps) for eps in EPSILONS],
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
