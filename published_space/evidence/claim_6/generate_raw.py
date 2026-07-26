"""Independent standard-library generator for committed numerical evidence."""

from __future__ import annotations

import json
import math


TAU = 0.7
EPSILON = 1.3
A_COEFF = EPSILON / (2.0 * TAU)
X_VALUES = (-2.0, -0.3, 0.9, 2.2)
ETAS = (-0.3, -0.1, 0.1, 0.3)
LOWER = -8.0
UPPER = 8.0
N_INTERVALS = 20000


def energy(x: float, y: float) -> float:
    potential = 0.08 * y**4 + 0.35 * y**2
    cost = (y - x) ** 2
    return potential + cost / (2.0 * TAU)


def gaussian_density(y: float, mean: float, sigma: float) -> float:
    z = (y - mean) / sigma
    return math.exp(-0.5 * z * z) / (sigma * math.sqrt(2.0 * math.pi))


def simpson(function) -> float:
    step = (UPPER - LOWER) / N_INTERVALS
    total = function(LOWER) + function(UPPER)
    total += 4.0 * sum(
        function(LOWER + step * index)
        for index in range(1, N_INTERVALS, 2)
    )
    total += 2.0 * sum(
        function(LOWER + step * index)
        for index in range(2, N_INTERVALS, 2)
    )
    return total * step / 3.0


def evaluate_case(x: float) -> dict[str, object]:
    normalizer = simpson(lambda y: math.exp(-energy(x, y) / A_COEFF))
    log_normalizer = math.log(normalizer)

    def target(y: float) -> float:
        return math.exp(-energy(x, y) / A_COEFF) / normalizer

    mean = 0.3 * x - 0.2
    sigma = 0.8 + 0.05 * abs(x)

    def proposal(y: float) -> float:
        return gaussian_density(y, mean, sigma)

    def log_proposal(y: float) -> float:
        z = (y - mean) / sigma
        return -0.5 * z * z - math.log(sigma * math.sqrt(2.0 * math.pi))

    proposal_mass = simpson(proposal)
    objective_q = simpson(
        lambda y: proposal(y)
        * (energy(x, y) + A_COEFF * log_proposal(y))
    )
    kl_q = simpson(
        lambda y: proposal(y)
        * (
            log_proposal(y)
            + energy(x, y) / A_COEFF
            + log_normalizer
        )
    )
    identity_residual = objective_q - (
        A_COEFF * kl_q - A_COEFF * log_normalizer
    )
    objective_p = -A_COEFF * log_normalizer

    perturbation_gaps: dict[str, float] = {}
    for eta in ETAS:
        perturbation_normalizer = simpson(
            lambda y: target(y) * (1.0 + eta * math.tanh(y))
        )

        def perturbed(y: float) -> float:
            return (
                target(y)
                * (1.0 + eta * math.tanh(y))
                / perturbation_normalizer
            )

        objective = simpson(
            lambda y: perturbed(y)
            * (
                energy(x, y)
                + A_COEFF * math.log(max(perturbed(y), 1e-300))
            )
        )
        perturbation_gaps[f"{eta:+.1f}"] = objective - objective_p

    stationarity_values = [
        energy(x, y)
        + A_COEFF
        * (
            1.0
            - energy(x, y) / A_COEFF
            - log_normalizer
        )
        for y in (-3.0, -1.0, 0.0, 1.0, 3.0)
    ]
    return {
        "x": x,
        "normalizer": normalizer,
        "target_mass": simpson(target),
        "proposal_mass": proposal_mass,
        "proposal_kl": kl_q,
        "identity_residual": identity_residual,
        "stationarity_span": max(stationarity_values)
        - min(stationarity_values),
        "perturbation_objective_gaps": perturbation_gaps,
    }


def main() -> int:
    output = {
        "schema_version": 1,
        "generator": "standard-library composite Simpson",
        "parameters": {
            "tau": TAU,
            "epsilon": EPSILON,
            "a": A_COEFF,
            "domain": [LOWER, UPPER],
            "intervals": N_INTERVALS,
            "x_values": list(X_VALUES),
            "perturbation_etas": list(ETAS),
        },
        "cases": [evaluate_case(x) for x in X_VALUES],
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
