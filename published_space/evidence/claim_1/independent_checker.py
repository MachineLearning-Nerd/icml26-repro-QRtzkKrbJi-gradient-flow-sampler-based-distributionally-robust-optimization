"""Independent numerical and trace checker for the six algorithms."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from algorithms import (  # noqa: E402
    algorithm_1,
    algorithm_2,
    algorithm_3,
    algorithm_4,
    algorithm_5,
    algorithm_6,
    make_problem,
    rbf_kernel_and_repulsion,
    rgo_inner,
    svgd_inner,
    wfr_inner,
    wgf_inner,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def trace_contracts() -> dict[str, dict[str, int]]:
    problem = make_problem()
    theta = np.linspace(-0.12, 0.12, 8)

    def short_flow(theta_arg, x_arg, rng_arg):
        samples, _ = wgf_inner(
            problem,
            theta_arg,
            x_arg,
            rng_arg,
            particles=1,
            inner_steps=3,
            inner_lr=0.01,
        )
        return samples[0]

    outputs: dict[str, dict[str, int]] = {}
    _, trace1 = algorithm_1(
        problem, theta, np.random.default_rng(101), short_flow
    )
    require(
        trace1.counters
        == {
            "nominal_sample": 1,
            "conditional_gradient_flow": 1,
            "worst_case_output": 1,
        },
        "Algorithm 1 omitted a required sampling stage",
    )
    outputs["algorithm_1"] = trace1.counters

    _, trace2 = algorithm_2(
        problem,
        theta,
        np.random.default_rng(102),
        short_flow,
        outer_steps=4,
    )
    require(trace2.counters["algorithm_1_call"] == 4, "Algorithm 2 sampler count")
    require(trace2.counters["projected_dro_step"] == 4, "Algorithm 2 outer count")
    outputs["algorithm_2"] = trace2.counters

    theta3, trace3 = algorithm_3(
        problem, theta, np.random.default_rng(103)
    )
    require(trace3.counters["nominal_sample"] == 3, "Algorithm 3 nominal draws")
    require(trace3.counters["wgf_euler_update"] == 3 * 80 * 192, "Algorithm 3 ULA")
    require(trace3.counters["projected_dro_step"] == 3, "Algorithm 3 DRO update")
    require(np.all(np.isfinite(theta3)), "Algorithm 3 non-finite output")
    outputs["algorithm_3"] = trace3.counters

    theta4, trace4 = algorithm_4(
        problem, theta, np.random.default_rng(104)
    )
    require(trace4.counters["wfr_location_update"] == 3 * 45 * 192, "Algorithm 4 location")
    require(trace4.counters["fisher_rao_mass_update"] == 3 * 45 * 192, "Algorithm 4 mass")
    require(trace4.counters["weight_normalization"] == 3 * 45, "Algorithm 4 normalize")
    require(trace4.counters.get("birth_death_replacement", 0) > 0, "Algorithm 4 birth-death")
    require(abs(trace4.scalars["last_weight_sum"] - 1.0) < 1e-12, "Algorithm 4 mass sum")
    require(np.all(np.isfinite(theta4)), "Algorithm 4 non-finite output")
    outputs["algorithm_4"] = trace4.counters

    theta5, trace5 = algorithm_5(
        problem, theta, np.random.default_rng(105)
    )
    require(trace5.counters["score_force"] == 3 * 30 * 96, "Algorithm 5 score")
    require(trace5.counters["kernel_repulsion"] == 3 * 30 * 96, "Algorithm 5 repulsion")
    require(trace5.counters["kernel_pair_evaluation"] == 3 * 30 * 96 * 96, "Algorithm 5 kernel")
    require(np.all(np.isfinite(theta5)), "Algorithm 5 non-finite output")
    outputs["algorithm_5"] = trace5.counters

    theta6, trace6 = algorithm_6(
        problem, theta, np.random.default_rng(106)
    )
    require(trace6.counters["approximate_minimizer"] == 3, "Algorithm 6 minimizer")
    require(trace6.counters["rejection_accept"] == 3 * 192, "Algorithm 6 accepts")
    require(trace6.counters.get("rejection_reject", 0) > 0, "Algorithm 6 rejection")
    require(trace6.scalars["last_minimizer_gradient_inf"] < 1e-11, "Algorithm 6 optimizer")
    require(trace6.scalars["last_maximum_log_acceptance"] <= 1e-10, "Algorithm 6 envelope")
    require(np.all(np.isfinite(theta6)), "Algorithm 6 non-finite output")
    outputs["algorithm_6"] = trace6.counters
    return outputs


def transition_checks() -> dict[str, float]:
    problem = make_problem()
    theta = np.linspace(-0.12, 0.12, 8)
    x = problem.nominal[2]

    seed = 310
    rng_expected = np.random.default_rng(seed)
    xi = rng_expected.standard_normal((5, 8))
    eta = 0.013
    expected = (
        np.repeat(x[None, :], 5, axis=0)
        + eta
        * problem.grad_reward(
            theta, x, np.repeat(x[None, :], 5, axis=0)
        )
        + np.sqrt(eta * problem.epsilon / problem.tau) * xi
    )
    actual, _ = wgf_inner(
        problem,
        theta,
        x,
        np.random.default_rng(seed),
        particles=5,
        inner_steps=1,
        inner_lr=eta,
    )
    wgf_error = float(np.max(np.abs(actual - expected)))
    require(wgf_error < 1e-14, "WGF transition does not equal equation 12")

    y, weights, wfr_trace = wfr_inner(
        problem,
        theta,
        x,
        np.random.default_rng(311),
        particles=64,
        inner_steps=8,
        inner_lr=0.015,
        weight_lr=0.3,
        weight_threshold=0.95 / 64,
    )
    del y
    weight_sum_error = abs(float(weights.sum()) - 1.0)
    require(weight_sum_error < 1e-14, "WFR weights are not normalized")
    require(wfr_trace.counters.get("birth_death_replacement", 0) > 0, "WFR did not exercise birth-death")

    particles = x + np.random.default_rng(312).normal(0.0, 0.4, (7, 8))
    kernel, kernel_gradient = rbf_kernel_and_repulsion(particles, 3.0)
    score = (2.0 * problem.tau / problem.epsilon) * problem.grad_reward(
        theta, x, particles
    )
    expected_phi = (kernel.T @ score + kernel_gradient.sum(axis=0)) / 7
    seed_svg = 313
    init_rng = np.random.default_rng(seed_svg)
    initial = x + init_rng.normal(0.0, 0.4, (7, 8))
    kernel2, kernel_gradient2 = rbf_kernel_and_repulsion(initial, 3.0)
    score2 = (2.0 * problem.tau / problem.epsilon) * problem.grad_reward(
        theta, x, initial
    )
    expected_after = initial + 0.02 * (
        kernel2.T @ score2 + kernel_gradient2.sum(axis=0)
    ) / 7
    actual_after, _ = svgd_inner(
        problem,
        theta,
        x,
        np.random.default_rng(seed_svg),
        particles=7,
        inner_steps=1,
        inner_lr=0.02,
        initial_deviation=0.4,
        bandwidth=3.0,
    )
    svg_error = float(np.max(np.abs(expected_after - actual_after)))
    require(svg_error < 1e-14, "SVGD score/repulsion transition mismatch")
    require(float(np.linalg.norm(expected_phi)) > 0.0, "SVGD check is vacuous")

    _, rgo_trace = rgo_inner(
        problem,
        theta,
        x,
        np.random.default_rng(314),
        particles=1024,
    )
    acceptance = rgo_trace.scalars["acceptance_rate"]
    require(0.1 < acceptance < 0.999, "RGO rejection stage was vacuous")
    require(rgo_trace.scalars["maximum_log_acceptance"] <= 1e-10, "RGO envelope violation")

    return {
        "wgf_transition_max_error": wgf_error,
        "wfr_weight_sum_error": weight_sum_error,
        "wfr_birth_death_events": float(
            wfr_trace.counters["birth_death_replacement"]
        ),
        "svg_transition_max_error": svg_error,
        "rgo_acceptance_rate": acceptance,
        "rgo_rejections": float(rgo_trace.counters["rejection_reject"]),
        "rgo_maximum_log_acceptance": rgo_trace.scalars[
            "maximum_log_acceptance"
        ],
    }


def main() -> int:
    traces = trace_contracts()
    transitions = transition_checks()
    result = {
        "status": "PASS",
        "dimension": 8,
        "nominal_support_size": 6,
        "algorithms_checked": [1, 2, 3, 4, 5, 6],
        "trace_counters": traces,
        "transition_checks": transitions,
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
