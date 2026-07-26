"""Independent quadrature and SciPy calibration of the exact instance."""

from __future__ import annotations

import json
import math
from pathlib import Path

from scipy.integrate import quad
from scipy.optimize import minimize_scalar


HERE = Path(__file__).resolve().parent
RAW = HERE / "raw_results.json"


def integrate(function) -> float:
    value, error = quad(
        function,
        -math.inf,
        math.inf,
        epsabs=1e-12,
        epsrel=1e-12,
        limit=200,
    )
    if error > 1e-10:
        raise AssertionError(f"quadrature error too large: {error}")
    return value


def stationarity(iterations: int, step: float) -> float:
    base = abs(1.0 - 2.0 * step)
    decay = (
        0.0
        if base == 0.0
        else math.exp(2.0 * iterations * math.log(base))
    )
    return 4.0 * decay + step / (1.0 - step) * (1.0 - decay)


def best_at(iterations: int) -> tuple[float, float]:
    result = minimize_scalar(
        lambda step: stationarity(iterations, step),
        bounds=(1e-14, 0.499999999),
        method="bounded",
        options={"xatol": 1e-14, "maxiter": 500},
    )
    if not result.success:
        raise AssertionError(result.message)
    return float(result.fun), float(result.x)


def first_hit(epsilon: float) -> tuple[int, float, float]:
    lower = 0
    upper = 1
    while best_at(upper)[0] > epsilon**2:
        upper *= 2
    while lower + 1 < upper:
        middle = (lower + upper) // 2
        if best_at(middle)[0] <= epsilon**2:
            upper = middle
        else:
            lower = middle
    value, step = best_at(upper)
    return upper, step, value


def check_targets() -> tuple[float, float]:
    max_mean_error = 0.0
    max_variance_error = 0.0
    for theta in (-1.0, 0.0, 1.0):
        density = lambda z: math.exp(-0.5 * (z - theta) ** 2)
        normalizer = integrate(density)
        mean = integrate(lambda z: z * density(z)) / normalizer
        variance = (
            integrate(lambda z: (z - mean) ** 2 * density(z))
            / normalizer
        )
        max_mean_error = max(max_mean_error, abs(mean - theta))
        max_variance_error = max(max_variance_error, abs(variance - 1.0))
    return max_mean_error, max_variance_error


def main() -> int:
    recorded = json.loads(RAW.read_text(encoding="utf-8"))
    max_mean_error, max_variance_error = check_targets()
    max_step_delta = 0.0
    max_value_delta = 0.0
    exact_first_hit_match = True
    normalized_ratios: list[float] = []
    for expected in recorded["calibrated_first_hits"]:
        epsilon = float(expected["epsilon"])
        iterations, step, value = first_hit(epsilon)
        exact_first_hit_match &= iterations == int(
            expected["minimum_iterations"]
        )
        max_step_delta = max(
            max_step_delta, abs(step - float(expected["optimizing_step"]))
        )
        max_value_delta = max(
            max_value_delta,
            abs(value - float(expected["stationarity_at_first_hit"])),
        )
        if iterations < float(expected["analytic_iteration_lower_bound"]):
            raise AssertionError("calibrated first hit violates lower bound")
        normalized_ratios.append(
            iterations * epsilon**2 / math.log(1.0 / epsilon)
        )

    if max_mean_error > 1e-11 or max_variance_error > 1e-11:
        raise AssertionError("continuous Gibbs target reconstruction failed")
    if not exact_first_hit_match:
        raise AssertionError("independent first-hit iteration changed")
    if max_step_delta > 2e-7 or max_value_delta > 2e-9:
        raise AssertionError("independent optimum does not match raw data")
    if not all(0.5 < ratio < 1.5 for ratio in normalized_ratios):
        raise AssertionError("calibration is inconsistent with log/epsilon^2")

    output = {
        "status": "PASS",
        "target_count": 3,
        "max_target_mean_error": max_mean_error,
        "max_target_variance_error": max_variance_error,
        "epsilon_count": len(recorded["calibrated_first_hits"]),
        "minimum_epsilon": min(
            row["epsilon"] for row in recorded["calibrated_first_hits"]
        ),
        "largest_minimum_iterations": max(
            row["minimum_iterations"]
            for row in recorded["calibrated_first_hits"]
        ),
        "exact_first_hit_match": exact_first_hit_match,
        "max_optimizing_step_delta": max_step_delta,
        "max_stationarity_delta": max_value_delta,
        "normalized_ratio_range": [
            min(normalized_ratios),
            max(normalized_ratios),
        ],
    }
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
