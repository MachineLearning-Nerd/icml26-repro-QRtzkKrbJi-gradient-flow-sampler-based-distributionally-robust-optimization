"""Antithetic exact-gradient control removes the variance obstruction."""

from __future__ import annotations

import json
import math


def main() -> int:
    epsilon = 0.01
    step = 0.25
    # z_plus=theta+xi and z_minus=theta-xi. Averaging theta+z over
    # the pair gives the exact gradient 2*theta.
    first_hit = math.ceil(math.log(2.0 / epsilon) / math.log(2.0))
    claimed_budget = math.ceil(epsilon**-2)
    final_stationarity = 4.0 * (0.5 ** (2 * first_hit))
    counterexample_rejected = (
        final_stationarity <= epsilon**2
        and first_hit <= claimed_budget
    )
    output = {
        "status": (
            "COUNTEREXAMPLE_REJECTED_AS_EXPECTED"
            if counterexample_rejected
            else "UNEXPECTED_COUNTEREXAMPLE"
        ),
        "mutation": "one Gaussian sample -> antithetic pair",
        "reason": "the stochastic-gradient variance cancels exactly",
        "epsilon": epsilon,
        "step": step,
        "first_hit_iterations": first_hit,
        "epsilon_inverse_squared_budget": claimed_budget,
        "final_stationarity": final_stationarity,
    }
    print(json.dumps(output, sort_keys=True))
    return 1 if counterexample_rejected else 0


if __name__ == "__main__":
    raise SystemExit(main())
