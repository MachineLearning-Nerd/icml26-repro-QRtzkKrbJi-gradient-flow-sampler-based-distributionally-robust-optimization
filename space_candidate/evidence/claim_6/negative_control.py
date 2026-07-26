"""Wrong-temperature control; rejection is the expected outcome."""

from __future__ import annotations

import json


TAU = 0.7
EPSILON = 1.3
A_COEFF = EPSILON / (2.0 * TAU)


def energy(x: float, y: float) -> float:
    return 0.08 * y**4 + 0.35 * y**2 + (y - x) ** 2 / (2.0 * TAU)


def main() -> int:
    x = 0.9
    wrong_temperature = 2.0 * A_COEFF
    # An additive log-normalizer cancels from the span, so it need not be
    # estimated. The correct functional derivative must be constant in y.
    derivatives_without_constant = [
        energy(x, y)
        + A_COEFF
        * (1.0 - energy(x, y) / wrong_temperature)
        for y in (-3.0, -1.0, 0.0, 1.0, 3.0)
    ]
    stationarity_span = max(derivatives_without_constant) - min(
        derivatives_without_constant
    )
    rejected = stationarity_span > 0.1
    output = {
        "status": "REJECTED_AS_EXPECTED" if rejected else "UNEXPECTED_PASS",
        "mutation": "replace exp(-A/a) by exp(-A/(2a))",
        "reason": "Euler-Lagrange derivative is not constant in y",
        "stationarity_span": stationarity_span,
    }
    print(json.dumps(output, sort_keys=True))
    return 1 if rejected else 0


if __name__ == "__main__":
    raise SystemExit(main())
