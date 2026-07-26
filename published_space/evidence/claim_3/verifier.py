"""Fail-closed verifier for the v1 outer-loop rate."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent


def run(name: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HERE / name)],
        cwd=HERE,
        capture_output=True,
        text=True,
    )


def output(completed: subprocess.CompletedProcess[str]) -> dict[str, object]:
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        raise AssertionError("sub-check emitted no JSON")
    return json.loads(lines[-1])


def main() -> int:
    certificate_process = run("certificate.py")
    if certificate_process.returncode != 0:
        raise AssertionError(certificate_process.stderr)
    certificate = output(certificate_process)
    if certificate["status"] != "PASS":
        raise AssertionError("symbolic counterexample did not pass")

    checker_process = run("independent_checker.py")
    if checker_process.returncode != 0:
        raise AssertionError(checker_process.stderr)
    checker = output(checker_process)
    if checker["status"] != "PASS":
        raise AssertionError("independent calibration did not pass")
    checker_summary = {
        "epsilon_count": checker["epsilon_count"],
        "exact_first_hit_match": checker["exact_first_hit_match"],
        "exit_code": checker_process.returncode,
        "largest_minimum_iterations": checker[
            "largest_minimum_iterations"
        ],
        "minimum_epsilon": checker["minimum_epsilon"],
        "normalized_ratio_range": checker["normalized_ratio_range"],
        "status": checker["status"],
    }
    recorded_checker = json.loads(
        (HERE / "independent_checker_output.json").read_text(encoding="utf-8")
    )
    if checker_summary != recorded_checker:
        raise AssertionError("recorded independent-checker output changed")

    control_process = run("negative_control.py")
    control = output(control_process)
    if control_process.returncode != 1:
        raise AssertionError("zero-variance control did not exit 1")
    if control["status"] != "COUNTEREXAMPLE_REJECTED_AS_EXPECTED":
        raise AssertionError("zero-variance control failed unexpectedly")
    recorded_control = json.loads(
        (HERE / "negative_control_output.json").read_text(encoding="utf-8")
    )
    if recorded_control != {"exit_code": 1, **control}:
        raise AssertionError("recorded control output changed")

    result = {
        "claim_id": 3,
        "verdict": "FALSIFIED",
        "certificate": {
            "exit_code": certificate_process.returncode,
            "L_Phi": certificate["L_Phi"],
            "gradient_observable_lipschitz": certificate[
                "gradient_observable_lipschitz"
            ],
            "sampler_w2_error": certificate["sampler_w2_error"],
            "stochastic_gradient_variance": certificate[
                "stochastic_gradient_variance"
            ],
            "asymptotic_lower_order": certificate[
                "asymptotic_lower_order"
            ],
        },
        "independent_checker": {
            key: checker_summary[key]
            for key in checker_summary
            if key != "status"
        },
        "negative_control": {
            "exit_code": control_process.returncode,
            "status": control["status"],
            "first_hit_iterations": control["first_hit_iterations"],
            "epsilon_inverse_squared_budget": control[
                "epsilon_inverse_squared_budget"
            ],
        },
        "current_v3_note": (
            "Theorem 5.2 changes the rate to epsilon^-4 with an "
            "S-dependent step; Theorem 5.5 changes total complexity "
            "to epsilon^-6."
        ),
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
