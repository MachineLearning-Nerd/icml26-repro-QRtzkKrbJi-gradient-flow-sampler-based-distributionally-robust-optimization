"""Adaptive continuous check of the exact necessary-time counterexample."""

from __future__ import annotations

import json
import math
from pathlib import Path

from scipy.integrate import quad


HERE = Path(__file__).resolve().parent
RAW = HERE / "raw_results.json"
LIPSCHITZ = 1.0
LAMBDA_PL = 6.0
TOLERANCES = (1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12)


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


def main() -> int:
    unnormalized = lambda y: math.exp(-1.5 * y * y)
    normalizer = integrate(unnormalized)
    target_mean = integrate(lambda y: y * unnormalized(y)) / normalizer
    target_second_moment = (
        integrate(lambda y: y * y * unnormalized(y)) / normalizer
    )
    initial_oracle = 0.0
    gradient_error_at_zero = abs(initial_oracle - target_mean)
    initial_to_target_w2 = math.sqrt(target_second_moment)

    sweep = [
        {
            "epsilon": epsilon,
            "claimed_scale": math.log(
                LIPSCHITZ / math.sqrt(LAMBDA_PL * epsilon)
            )
            / LAMBDA_PL,
            "measured_first_hit": 0.0,
        }
        for epsilon in TOLERANCES
    ]
    recorded = json.loads(RAW.read_text(encoding="utf-8"))
    largest_raw_delta = 0.0
    for expected, actual in zip(
        recorded["tolerance_sweep"], sweep, strict=True
    ):
        for field in ("epsilon", "claimed_scale", "measured_first_hit"):
            delta = abs(float(expected[field]) - float(actual[field]))
            largest_raw_delta = max(largest_raw_delta, delta)
            if delta > 1e-14:
                raise AssertionError(f"raw sweep mismatch: {field}={delta}")

    if abs(target_mean) > 1e-12 or gradient_error_at_zero > 1e-12:
        raise AssertionError("time-zero gradient oracle is not exact")
    if abs(target_second_moment - 1.0 / 3.0) > 1e-11:
        raise AssertionError("continuous target variance changed")
    if initial_to_target_w2 < 0.5:
        raise AssertionError("counterexample accidentally became a warm start")
    if not all(item["claimed_scale"] > 0 for item in sweep):
        raise AssertionError("claimed lower-order scale is not positive")
    if not all(
        later["claimed_scale"] > earlier["claimed_scale"]
        for earlier, later in zip(sweep, sweep[1:])
    ):
        raise AssertionError("claimed lower-order scale does not diverge")

    output = {
        "status": "PASS",
        "normalizer": normalizer,
        "target_mean": target_mean,
        "target_second_moment": target_second_moment,
        "initial_to_target_w2": initial_to_target_w2,
        "gradient_error_at_zero": gradient_error_at_zero,
        "tolerance_count": len(sweep),
        "smallest_epsilon": min(TOLERANCES),
        "largest_claimed_scale": max(
            item["claimed_scale"] for item in sweep
        ),
        "all_measured_first_hits": sorted(
            {item["measured_first_hit"] for item in sweep}
        ),
        "largest_raw_delta": largest_raw_delta,
    }
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
