"""Symbolic certificate for the Proposition 1 counterexample."""

from __future__ import annotations

import json

import sympy as sp


def main() -> int:
    theta, y = sp.symbols("theta y", real=True)
    tau = sp.Rational(1, 4)
    loss = theta * y + y**2 / 2
    energy = -loss + y**2 / (2 * tau)
    theta_zero_energy = sp.simplify(energy.subs(theta, 0))
    hessian = sp.diff(theta_zero_energy, y, 2)
    gradient = sp.diff(theta_zero_energy, y)
    pl_residual = sp.simplify(gradient**2 - 6 * theta_zero_energy)
    loss_hessian = sp.diff(loss, y, 2)
    mixed_hessian = sp.diff(loss, theta, y)
    completed_square = sp.simplify(
        energy
        - (
            sp.Rational(3, 2) * (y - theta / 3) ** 2
            - theta**2 / 6
        )
    )
    target_mean = theta / 3
    initial_oracle = sp.diff(loss, theta).subs(y, 0)
    target_oracle_at_zero = target_mean.subs(theta, 0)

    exact_checks = {
        "loss_y_hessian": loss_hessian,
        "mixed_hessian": mixed_hessian,
        "energy_y_hessian": hessian,
        "pl_residual_at_lambda_6": pl_residual,
        "completed_square_residual": completed_square,
        "initial_oracle_at_theta_0": initial_oracle,
        "target_oracle_at_theta_0": target_oracle_at_zero,
    }
    expected = {
        "loss_y_hessian": sp.Integer(1),
        "mixed_hessian": sp.Integer(1),
        "energy_y_hessian": sp.Integer(3),
        "pl_residual_at_lambda_6": sp.Integer(0),
        "completed_square_residual": sp.Integer(0),
        "initial_oracle_at_theta_0": sp.Integer(0),
        "target_oracle_at_theta_0": sp.Integer(0),
    }
    if exact_checks != expected:
        raise AssertionError(f"symbolic counterexample changed: {exact_checks}")

    output = {
        "status": "PASS",
        "exact_checks": {key: str(value) for key, value in exact_checks.items()},
        "lambda_pl": 6,
        "strong_convexity": 3,
        "loss_smoothness": 1,
        "gradient_observable_lipschitz": 1,
        "entropy_regularization": (
            "2*tau=1/2, hence target proportional to exp(-U)"
        ),
        "target_mean": "theta/3",
        "target_variance_at_theta_0": "1/3",
        "initial_to_target_w2": "sqrt(1/3)",
        "required_time_for_every_positive_epsilon": 0,
    }
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
