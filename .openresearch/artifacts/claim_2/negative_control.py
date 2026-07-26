"""Same model at theta=1; t=0 must fail the gradient tolerance."""

from __future__ import annotations

import json
import math


def main() -> int:
    theta = 1.0
    target_mean = theta / 3.0
    initial_mean = 0.0
    epsilon = 0.1
    initial_error = abs(target_mean - initial_mean)
    first_hit = math.log(initial_error / epsilon) / 3.0
    rejected = initial_error > epsilon and first_hit > 0.0
    output = {
        "status": "REJECTED_AS_EXPECTED" if rejected else "UNEXPECTED_PASS",
        "mutation": "theta=0 -> theta=1 (break target symmetry)",
        "reason": "time-zero gradient error exceeds epsilon",
        "theta": theta,
        "epsilon": epsilon,
        "initial_gradient_error": initial_error,
        "positive_first_hit_time": first_hit,
    }
    print(json.dumps(output, sort_keys=True))
    return 1 if rejected else 0


if __name__ == "__main__":
    raise SystemExit(main())
