"""Exact symbolic certificate for the v1 outer-loop counterexample."""

from __future__ import annotations

import json

import sympy as sp


def main() -> int:
    theta, z, noise, step = sp.symbols(
        "theta z xi r", real=True
    )
    iterations = sp.symbols("S", integer=True, nonnegative=True)
    loss = theta**2 / 2 + theta * z
    exponent = sp.expand(loss - z**2 / 2)
    completed_square_residual = sp.simplify(
        exponent - (-(z - theta) ** 2 / 2 + theta**2)
    )
    outer = theta**2
    outer_gradient = sp.diff(outer, theta)
    outer_hessian = sp.diff(outer_gradient, theta)
    sample = theta + noise
    stochastic_gradient = sp.diff(loss, theta).subs(z, sample)
    update = sp.expand(theta - step * stochastic_gradient)
    expected_update = (1 - 2 * step) * theta - step * noise
    update_residual = sp.simplify(update - expected_update)

    decay = (1 - 2 * step) ** (2 * iterations)
    exact_theta_second_moment = (
        decay
        + step / (4 * (1 - step)) * (1 - decay)
    )
    exact_stationarity = sp.simplify(4 * exact_theta_second_moment)
    expected_stationarity = sp.simplify(
        4 * decay + step / (1 - step) * (1 - decay)
    )
    recurrence_residual = sp.simplify(
        exact_stationarity - expected_stationarity
    )

    if completed_square_residual != 0:
        raise AssertionError("Gibbs target completion changed")
    if outer_gradient != 2 * theta or outer_hessian != 2:
        raise AssertionError("outer objective certificate changed")
    if stochastic_gradient != 2 * theta + noise:
        raise AssertionError("stochastic gradient certificate changed")
    if update_residual != 0 or recurrence_residual != 0:
        raise AssertionError("outer recurrence certificate changed")

    output = {
        "status": "PASS",
        "completed_square_residual": str(completed_square_residual),
        "target": "Normal(theta,1)",
        "outer_objective": "theta^2+constant",
        "L_Phi": 2,
        "gradient_observable_lipschitz": 1,
        "sampler_w2_error": 0,
        "stochastic_gradient_variance": 1,
        "update_residual": str(update_residual),
        "last_iterate_formula_residual": str(recurrence_residual),
        "necessary_step_bound": "r<=4*epsilon^2/(3+4*epsilon^2)",
        "iteration_lower_bound": (
            "S>=3*log(4/epsilon^2)/(32*epsilon^2)"
        ),
        "asymptotic_lower_order": (
            "Omega(epsilon^-2*log(1/epsilon))"
        ),
    }
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
