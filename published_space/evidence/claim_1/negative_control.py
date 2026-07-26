"""Six defect injections that must all be rejected for their intended reason."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from algorithms import (  # noqa: E402
    Trace,
    make_problem,
    rgo_inner,
    svgd_inner,
    wfr_inner,
    wgf_inner,
)


def main() -> int:
    problem = make_problem()
    theta = np.linspace(-0.12, 0.12, 8)
    x = problem.nominal[2]
    rejected: dict[str, str] = {}

    broken_algorithm_1 = Trace(algorithm=1)
    broken_algorithm_1.hit("nominal_sample")
    broken_algorithm_1.hit("worst_case_output")
    if broken_algorithm_1.counters.get("conditional_gradient_flow", 0) != 1:
        rejected["algorithm_1"] = "missing conditional gradient-flow call"

    y = x + 0.1
    lr = 0.04
    correct = problem.project(theta - lr * y)
    broken_ascent = problem.project(theta + lr * y)
    if not np.allclose(correct, broken_ascent):
        rejected["algorithm_2"] = "ascent sign differs from projected descent"

    _, broken_wgf = wgf_inner(
        problem,
        theta,
        x,
        np.random.default_rng(401),
        particles=64,
        inner_steps=2,
        inner_lr=0.015,
        noise_scale=0.0,
    )
    if broken_wgf.scalars["noise_sigma"] == 0.0:
        rejected["algorithm_3"] = "ULA Gaussian noise removed"

    _, _, broken_wfr = wfr_inner(
        problem,
        theta,
        x,
        np.random.default_rng(402),
        particles=64,
        inner_steps=8,
        inner_lr=0.015,
        weight_lr=0.3,
        weight_threshold=0.95 / 64,
        disable_reaction=True,
    )
    if (
        broken_wfr.counters.get("fisher_rao_mass_update", 0) == 0
        and broken_wfr.counters.get("birth_death_replacement", 0) == 0
    ):
        rejected["algorithm_4"] = "Fisher-Rao mass and birth-death removed"

    seed = 403
    correct_svg, _ = svgd_inner(
        problem,
        theta,
        x,
        np.random.default_rng(seed),
        particles=12,
        inner_steps=1,
        inner_lr=0.03,
        initial_deviation=0.4,
        bandwidth=3.0,
        repulsion_sign=1.0,
    )
    broken_svg, _ = svgd_inner(
        problem,
        theta,
        x,
        np.random.default_rng(seed),
        particles=12,
        inner_steps=1,
        inner_lr=0.03,
        initial_deviation=0.4,
        bandwidth=3.0,
        repulsion_sign=-1.0,
    )
    if float(np.max(np.abs(correct_svg - broken_svg))) > 1e-6:
        rejected["algorithm_5"] = "kernel repulsion sign reversed"

    _, broken_rgo = rgo_inner(
        problem,
        theta,
        x,
        np.random.default_rng(404),
        particles=512,
        accept_all=True,
    )
    if (
        broken_rgo.scalars["acceptance_rate"] == 1.0
        and broken_rgo.counters.get("rejection_reject", 0) == 0
    ):
        rejected["algorithm_6"] = "accept-all bypasses rejection test"

    expected = {f"algorithm_{index}" for index in range(1, 7)}
    if set(rejected) != expected:
        print(
            json.dumps(
                {
                    "status": "CONTROL_MALFUNCTION",
                    "rejected": rejected,
                },
                sort_keys=True,
            )
        )
        return 2

    print(
        json.dumps(
            {
                "status": "REJECTED_AS_EXPECTED",
                "defect_count": len(rejected),
                "rejected": rejected,
            },
            sort_keys=True,
        )
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
