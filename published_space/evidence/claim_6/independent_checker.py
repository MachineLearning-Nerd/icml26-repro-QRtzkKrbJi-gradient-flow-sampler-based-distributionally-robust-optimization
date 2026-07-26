"""Adaptive-quadrature check independent of the raw-result generator."""

from __future__ import annotations

import json
import math
from pathlib import Path

from scipy.integrate import quad


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw_results.json"
TAU = 0.7
EPSILON = 1.3
A_COEFF = EPSILON / (2.0 * TAU)
X_VALUES = (-2.0, -0.3, 0.9, 2.2)
ETAS = (-0.3, -0.1, 0.1, 0.3)


def energy(x: float, y: float) -> float:
    return 0.08 * y**4 + 0.35 * y**2 + (y - x) ** 2 / (2.0 * TAU)


def integrate(function) -> float:
    value, error = quad(
        function,
        -math.inf,
        math.inf,
        epsabs=2e-11,
        epsrel=2e-11,
        limit=300,
    )
    if error > 2e-9:
        raise AssertionError(f"quadrature error estimate too large: {error}")
    return value


def gaussian_density(y: float, mean: float, sigma: float) -> float:
    z = (y - mean) / sigma
    return math.exp(-0.5 * z * z) / (sigma * math.sqrt(2.0 * math.pi))


def evaluate_case(x: float) -> dict[str, object]:
    normalizer = integrate(lambda y: math.exp(-energy(x, y) / A_COEFF))
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

    proposal_mass = integrate(proposal)
    objective_q = integrate(
        lambda y: proposal(y)
        * (energy(x, y) + A_COEFF * log_proposal(y))
    )
    kl_q = integrate(
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

    gaps: dict[str, float] = {}
    for eta in ETAS:
        perturbation_normalizer = integrate(
            lambda y: target(y) * (1.0 + eta * math.tanh(y))
        )

        def perturbed(y: float) -> float:
            return (
                target(y)
                * (1.0 + eta * math.tanh(y))
                / perturbation_normalizer
            )

        objective = integrate(
            lambda y: perturbed(y)
            * (
                energy(x, y)
                + A_COEFF * math.log(max(perturbed(y), 1e-300))
            )
        )
        gaps[f"{eta:+.1f}"] = objective - objective_p

    stationarity = [
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
        "target_mass": integrate(target),
        "proposal_mass": proposal_mass,
        "proposal_kl": kl_q,
        "identity_residual": identity_residual,
        "stationarity_span": max(stationarity) - min(stationarity),
        "perturbation_objective_gaps": gaps,
    }


def compare_to_raw(actual: list[dict[str, object]]) -> float:
    recorded = json.loads(RAW.read_text(encoding="utf-8"))
    if len(recorded["cases"]) != len(actual):
        raise AssertionError("raw case count changed")
    largest_delta = 0.0
    numeric_fields = (
        "normalizer",
        "target_mass",
        "proposal_mass",
        "proposal_kl",
        "identity_residual",
        "stationarity_span",
    )
    for expected_case, actual_case in zip(recorded["cases"], actual, strict=True):
        if expected_case["x"] != actual_case["x"]:
            raise AssertionError("raw x ordering changed")
        for field in numeric_fields:
            delta = abs(float(expected_case[field]) - float(actual_case[field]))
            largest_delta = max(largest_delta, delta)
            if delta > 2e-8:
                raise AssertionError(
                    f"raw regression mismatch at x={actual_case['x']}, "
                    f"{field}: {delta}"
                )
        for eta in expected_case["perturbation_objective_gaps"]:
            delta = abs(
                float(expected_case["perturbation_objective_gaps"][eta])
                - float(actual_case["perturbation_objective_gaps"][eta])
            )
            largest_delta = max(largest_delta, delta)
            if delta > 2e-8:
                raise AssertionError(
                    f"raw perturbation mismatch at x={actual_case['x']}, "
                    f"eta={eta}: {delta}"
                )
    return largest_delta


def main() -> int:
    cases = [evaluate_case(x) for x in X_VALUES]
    max_identity_residual = max(
        abs(float(case["identity_residual"])) for case in cases
    )
    max_mass_error = max(
        max(
            abs(float(case["target_mass"]) - 1.0),
            abs(float(case["proposal_mass"]) - 1.0),
        )
        for case in cases
    )
    max_stationarity_span = max(
        abs(float(case["stationarity_span"])) for case in cases
    )
    min_kl = min(float(case["proposal_kl"]) for case in cases)
    min_perturbation_gap = min(
        float(gap)
        for case in cases
        for gap in case["perturbation_objective_gaps"].values()
    )
    max_raw_delta = compare_to_raw(cases)

    if max_identity_residual > 2e-9:
        raise AssertionError("conditional variational identity failed")
    if max_mass_error > 2e-9:
        raise AssertionError("continuous density normalization failed")
    if max_stationarity_span > 2e-10:
        raise AssertionError("Euler-Lagrange stationarity failed")
    if min_kl <= 1e-4:
        raise AssertionError("unrelated proposal did not produce positive KL")
    if min_perturbation_gap <= 1e-5:
        raise AssertionError("nonzero feasible perturbation did not increase J")

    output = {
        "status": "PASS",
        "case_count": len(cases),
        "max_identity_residual": max_identity_residual,
        "max_mass_error": max_mass_error,
        "max_stationarity_span": max_stationarity_span,
        "minimum_proposal_kl": min_kl,
        "minimum_perturbation_objective_gap": min_perturbation_gap,
        "max_raw_generator_delta": max_raw_delta,
        "cases": cases,
    }
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
